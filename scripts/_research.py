"""Shared, dependency-light helpers for research workspace scripts."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
_TEMPLATE_TOKEN = re.compile(r"\{\{[A-Z0-9_]+\}\}")
_SENSITIVE_COMMAND = re.compile(
    r"(?:api[_-]?key|authorization|password|secret|token)", re.IGNORECASE
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def clean_inline(value: str, *, fallback: str, limit: int = 240) -> str:
    cleaned = " ".join(value.split())
    return (cleaned or fallback)[:limit]


def next_artifact_id(directory: Path, prefix: str) -> str:
    """Return the next stable ID after inspecting files and directories."""
    directory.mkdir(parents=True, exist_ok=True)
    pattern = re.compile(rf"^{re.escape(prefix)}(\d{{3}})(?:\D|$)")
    used = []
    for entry in directory.iterdir():
        match = pattern.match(entry.name)
        if match:
            used.append(int(match.group(1)))
    number = max(used, default=0) + 1
    if number > 999:
        raise RuntimeError(f"No {prefix}NNN identifiers remain; extend the ID schema deliberately.")
    return f"{prefix}{number:03d}"


def sha256_file(path: Path) -> str:
    """Return the lowercase SHA-256 of a file's bytes."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_path(path: Path) -> tuple[str, str]:
    """Hash a file or directory deterministically, excluding filesystem metadata.

    Directory hashes include sorted relative entry names, entry kinds, and file
    content hashes. Timestamps, ownership, permissions, and traversal order do
    not affect the result. Symlinks and special files are rejected because their
    external or platform-dependent targets are not a reproducible dependency.
    """
    if path.is_symlink():
        raise ValueError(f"symbolic links cannot be fingerprinted reproducibly: {path}")
    if path.is_file():
        return "file", sha256_file(path)
    if not path.is_dir():
        raise ValueError(f"infrastructure path must be a file or directory: {path}")

    digest = hashlib.sha256()
    digest.update(b"research-directory-sha256-v1\0")
    entries = sorted(path.rglob("*"), key=lambda item: item.relative_to(path).as_posix())
    for entry in entries:
        relative = entry.relative_to(path).as_posix().encode("utf-8")
        if entry.is_symlink():
            raise ValueError(f"symbolic links cannot be fingerprinted reproducibly: {entry}")
        if entry.is_dir():
            digest.update(b"directory\0" + relative + b"\0")
        elif entry.is_file():
            digest.update(
                b"file\0"
                + relative
                + b"\0"
                + sha256_file(entry).encode("ascii")
                + b"\0"
            )
        else:
            raise ValueError(f"special files cannot be fingerprinted reproducibly: {entry}")
    return "directory", digest.hexdigest()


def fingerprint_paths(root: Path, values: list[str]) -> tuple[list[dict[str, str]], str]:
    """Fingerprint declared repository-relative dependencies and their aggregate."""
    normalized: list[str] = []
    for value in values:
        if not isinstance(value, str) or not value.strip() or Path(value).is_absolute():
            raise ValueError(f"invalid infrastructure path '{value}'")
        path_value = Path(value).as_posix()
        if path_value in normalized:
            raise ValueError(f"duplicate infrastructure path '{path_value}'")
        normalized.append(path_value)

    records: list[dict[str, str]] = []
    for value in sorted(normalized):
        unresolved = root / value
        if unresolved.is_symlink():
            raise ValueError(f"symbolic links cannot be declared as infrastructure: '{value}'")
        candidate = unresolved.resolve()
        try:
            candidate.relative_to(root.resolve())
        except ValueError as exc:
            raise ValueError(f"infrastructure path escapes repository: '{value}'") from exc
        if not candidate.exists():
            raise ValueError(f"infrastructure path does not exist: '{value}'")
        kind, digest = sha256_path(candidate)
        records.append({"path": value, "type": kind, "sha256": digest})

    encoded = json.dumps(records, sort_keys=True, separators=(",", ":"), allow_nan=False)
    aggregate = hashlib.sha256(encoded.encode("utf-8")).hexdigest()
    return records, aggregate


def render_template(template: Path, replacements: dict[str, str]) -> str:
    content = template.read_text(encoding="utf-8")
    required = set(_TEMPLATE_TOKEN.findall(content))
    available = {"{{" + key + "}}" for key in replacements}
    unresolved = sorted(required - available)
    if unresolved:
        raise ValueError(f"Unresolved template tokens in {template}: {', '.join(unresolved)}")
    for key, value in replacements.items():
        content = content.replace("{{" + key + "}}", value)
    return content


def write_new(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        handle.write(content)


def write_from_template(
    template: Path, destination: Path, replacements: dict[str, str]
) -> None:
    write_new(destination, render_template(template, replacements))


def load_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return {}, text
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line == "---")
    except StopIteration as exc:
        raise ValueError(f"Unclosed YAML frontmatter in {path}") from exc
    frontmatter = yaml.safe_load("\n".join(lines[1:end])) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError(f"Frontmatter in {path} must be a mapping")
    return frontmatter, "\n".join(lines[end + 1 :])


def markdown_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def current_question(root: Path) -> str:
    path = root / "research" / "QUESTION.md"
    if not path.exists():
        return ""
    sections = markdown_sections(path.read_text(encoding="utf-8"))
    question = sections.get("Question", "").strip()
    if not question or question.lower().startswith("not set"):
        return ""
    return " ".join(question.split())


def git_state(root: Path) -> tuple[str | None, bool | None]:
    try:
        status = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain", "--untracked-files=normal"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None, None
    if status.returncode != 0:
        return None, None
    dirty = bool(status.stdout.strip())
    try:
        commit = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None, dirty
    return (commit.stdout.strip() if commit.returncode == 0 else None), dirty


def relative_to_root(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def append_provenance(root: Path, **event: Any) -> None:
    """Append a small, secret-averse metadata record; never block research work."""
    allowed = {
        "agent",
        "session_id",
        "tool",
        "operation",
        "delegated_agent",
        "task",
        "experiment_id",
        "obligation_id",
        "claim_id",
        "command",
        "relevant_paths",
        "git_commit",
        "dirty_worktree",
        "success",
    }
    record = {key: value for key, value in event.items() if key in allowed and value is not None}
    command = record.get("command")
    if isinstance(command, str):
        if len(command) > 500 or "\n" in command or _SENSITIVE_COMMAND.search(command):
            record.pop("command", None)
    record["timestamp"] = utc_now()
    path = root / "research" / "provenance.jsonl"
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(record, sort_keys=True, separators=(",", ":"), allow_nan=False) + os.linesep
        with path.open("a", encoding="utf-8") as handle:
            handle.write(line)
    except Exception:
        pass


def write_json(path: Path, data: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(data, indent=2, sort_keys=False, allow_nan=False) + "\n", encoding="utf-8"
    )
    temporary.replace(path)
