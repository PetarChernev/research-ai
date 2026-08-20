#!/usr/bin/env python3
"""Validate research IDs, references, schemas, and epistemic guardrails."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from _research import (
    PROJECT_ROOT,
    append_provenance,
    current_question,
    git_state,
    load_frontmatter,
    markdown_sections,
    sha256_file,
)


CLAIM_STATUSES = {
    "conjecture",
    "derived",
    "numerically-supported",
    "literature-supported",
    "reproduced",
    "verified",
    "inconclusive",
    "contradicted",
    "rejected",
}
IMPORTANCE_LEVELS = {"low", "medium", "high", "critical"}
CHECK_STATUSES = {"pending", "passed", "failed", "inconclusive", "not-applicable"}
HYPOTHESIS_STATUSES = {
    "proposed",
    "active",
    "testing",
    "supported",
    "disfavored",
    "falsified",
    "retired",
}
DERIVATION_STATUSES = {"draft", "complete", "checked", "superseded"}
EXPERIMENT_STATUSES = {"planned", "ready", "running", "complete", "failed", "archived"}
# Generic, method-neutral vocabulary. A class names the kind of assertion under
# test; it never implies a library, language, or tool.
OBLIGATION_CLASSES = {
    "exact-symbolic",
    "formal",
    "numerical",
    "convergence",
    "independent-implementation",
    "limiting-case",
    "symmetry",
    "dimensional",
    "counterexample",
    "other",
}
OBLIGATION_STATUSES = {"active", "superseded"}
OBLIGATION_INDEPENDENCE = {"not-required", "recommended", "required"}
OBLIGATION_OUTCOMES = {"passed", "failed", "inconclusive", "error"}
COMPUTATION_SECTIONS = [
    "Current research phase",
    "Checkability map",
    "Current machine-check obligations",
    "Computational representations and methods",
    "Research-specific computational infrastructure",
    "Numerical and formal evidence standards",
    "Independence strategy",
    "Phase-transition triggers",
    "Deferred or non-machine-checkable issues",
    "Known limitations and risks",
    "Related decisions",
]
COMPUTATION_UNINITIALIZED_MARKER = "Status: not-started"
VERIFICATION_OUTCOMES = {
    "verified",
    "supported but not independently verified",
    "inconclusive",
    "failed verification",
    "contradicted",
}
EXPLICIT_CHECK_OUTCOMES = {"passed", "failed", "inconclusive", "not-applicable"}
VERIFICATION_SECTIONS = [
    "Claim tested",
    "Independence statement",
    "Reconstruction",
    "Falsification attempts",
    "Checks",
    "Computational evidence reviewed",
    "Sufficiency of computational obligations",
    "Missing or adversarial checks",
    "Computational independence",
    "Findings",
    "Outcome",
    "Required follow-up",
]
REPORT_PLACEHOLDER_PREFIXES = (
    "quote the exact",
    "state which",
    "re-derive or reproduce",
    "record attempted",
    "list failures",
    "list the relevant",
    "explain whether",
    "identify checks",
    "use exactly one",
    "state what would",
)
LITERATURE_SECTIONS = [
    "Question investigated",
    "Search strategy",
    "Source identity",
    "Claims supported",
    "Claims contradicted",
    "Exact evidence location",
    "Assumptions / regime",
    "Confidence",
    "Unresolved issues",
]
CLAIM_ID = re.compile(r"^C\d{3}$")
HYPOTHESIS_ID = re.compile(r"^H\d{3}$")
DERIVATION_ID = re.compile(r"^D\d{3}$")
EXPERIMENT_ID = re.compile(r"^E\d{3}$")
OBLIGATION_ID = re.compile(r"^O\d{3}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
MODEL_ID = re.compile(r"^[a-z0-9][a-z0-9._-]*/[A-Za-z0-9][A-Za-z0-9._-]*$")


@dataclass
class Obligation:
    """Structural view of one machine-check obligation under research/checks/."""

    id: str
    path: Path
    spec: dict[str, Any] | None = None
    result: dict[str, Any] | None = None

    @property
    def status(self) -> str | None:
        return self.spec.get("status") if isinstance(self.spec, dict) else None

    @property
    def is_active(self) -> bool:
        return self.status == "active"

    @property
    def is_required(self) -> bool:
        return bool(self.spec.get("required")) if isinstance(self.spec, dict) else False

    @property
    def outcome(self) -> str | None:
        if not isinstance(self.result, dict):
            return None
        value = self.result.get("outcome")
        return value if isinstance(value, str) else None

    @property
    def targets(self) -> list[Any]:
        if not isinstance(self.spec, dict):
            return []
        claims = self.spec.get("claims")
        return claims if isinstance(claims, list) else []

    def satisfied(self) -> bool:
        return self.outcome == "passed"


@dataclass
class Report:
    errors: list[dict[str, str]] = field(default_factory=list)
    warnings: list[dict[str, str]] = field(default_factory=list)

    def error(self, location: str, message: str) -> None:
        self.errors.append({"location": location, "message": message})

    def warning(self, location: str, message: str) -> None:
        self.warnings.append({"location": location, "message": message})


def relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def artifact_ids(directory: Path, prefix: str, *, directories: bool = False) -> dict[str, Path]:
    suffix = "" if directories else r"\.md"
    pattern = re.compile(rf"^({prefix}\d{{3}}){suffix}$")
    found: dict[str, Path] = {}
    if not directory.exists():
        return found
    for path in directory.iterdir():
        if directories != path.is_dir():
            continue
        match = pattern.fullmatch(path.name)
        if match:
            found[match.group(1)] = path
    return found


def require_fields(
    data: dict[str, Any], fields: set[str], location: str, report: Report
) -> None:
    for name in sorted(fields - data.keys()):
        report.error(location, f"missing required field '{name}'")


def require_sections(
    body: str, names: list[str], location: str, report: Report
) -> None:
    sections = markdown_sections(body)
    for name in names:
        if name not in sections:
            report.error(location, f"missing required section '## {name}'")


def valid_choice(value: Any, choices: set[str]) -> bool:
    return isinstance(value, str) and value in choices


def valid_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def valid_model_id(value: Any) -> bool:
    return isinstance(value, str) and bool(MODEL_ID.fullmatch(value))


def verification_has_model_separation(metadata: dict[str, Any]) -> bool:
    verifier_model = metadata.get("verifier_model")
    originating_models = metadata.get("originating_models")
    return (
        valid_model_id(verifier_model)
        and isinstance(originating_models, list)
        and bool(originating_models)
        and all(valid_model_id(model) for model in originating_models)
        and verifier_model not in originating_models
    )


def explicit_check_outcome(value: Any) -> str | None:
    if isinstance(value, str) and value in EXPLICIT_CHECK_OUTCOMES:
        return value
    if isinstance(value, dict) and isinstance(value.get("status"), str):
        status = value["status"]
        return status if status in EXPLICIT_CHECK_OUTCOMES else None
    return None


def reject_json_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON number '{value}'")


def load_json_object(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_json_constant)
    if not isinstance(data, dict):
        raise ValueError("root must be a JSON object")
    return data


def confined_artifact(root: Path, value: str, directory: Path) -> Path | None:
    if Path(value).is_absolute():
        return None
    candidate = (root / value).resolve()
    boundary = directory.resolve()
    try:
        candidate.relative_to(boundary)
    except ValueError:
        return None
    return candidate if candidate.is_file() else None


def verification_report_is_substantive(body: str) -> bool:
    sections = markdown_sections(body)
    for name in VERIFICATION_SECTIONS:
        content = sections.get(name, "").strip()
        if len(content) < 20 or content.lower().startswith(REPORT_PLACEHOLDER_PREFIXES):
            return False
    check_lines = [line.strip() for line in sections["Checks"].splitlines() if line.strip().startswith("-")]
    if not check_lines or any(line.endswith(":") for line in check_lines):
        return False
    return True


def literature_note_is_substantive(body: str) -> bool:
    sections = markdown_sections(body)
    supported = sections.get("Claims supported", "").strip().lower()
    location = sections.get("Exact evidence location", "").strip().lower()
    return (
        len(supported) >= 20
        and not supported.startswith("list only claims")
        and len(location) >= 10
        and not location.startswith("give page")
    )


def validate_id_reference(
    value: Any,
    pattern: re.Pattern[str],
    known: set[str] | dict[str, Path],
    kind: str,
    location: str,
    report: Report,
) -> None:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        report.error(location, f"invalid {kind} reference '{value}'")
    elif value not in known:
        report.error(location, f"references unknown {kind} '{value}'")


def validate_markdown_artifacts(
    root: Path,
    report: Report,
    claims: set[str],
    hypotheses: dict[str, Path],
    derivations: dict[str, Path],
) -> None:
    hypothesis_sections = [
        "Question addressed",
        "Statement",
        "Motivation",
        "Assumptions",
        "Predictions",
        "What would support it",
        "What would falsify it",
        "Discriminating experiments/derivations",
        "Related claims",
        "Related literature",
        "Current evidence",
        "Open problems",
    ]
    for artifact_id, path in hypotheses.items():
        location = relative(root, path)
        try:
            metadata, body = load_frontmatter(path)
        except (OSError, ValueError, yaml.YAMLError) as exc:
            report.error(location, str(exc))
            continue
        require_fields(metadata, {"id", "title", "status", "created_at", "updated_at"}, location, report)
        if metadata.get("id") != artifact_id:
            report.error(location, f"frontmatter id must be '{artifact_id}'")
        if not valid_choice(metadata.get("status"), HYPOTHESIS_STATUSES):
            report.error(location, f"invalid hypothesis status '{metadata.get('status')}'")
        for timestamp in ("created_at", "updated_at"):
            if not valid_timestamp(metadata.get(timestamp)):
                report.error(location, f"{timestamp} must be a timezone-aware ISO-8601 timestamp")
        require_sections(body, hypothesis_sections, location, report)

    derivation_sections = [
        "Target claim",
        "Assumptions",
        "Notation",
        "Known inputs",
        "Derivation",
        "Approximations",
        "Validity regime",
        "Dimensional check",
        "Limiting-case checks",
        "Candidate machine-checkable obligations",
        "Relationship to literature",
        "Unresolved concerns",
        "Conclusion",
    ]
    for artifact_id, path in derivations.items():
        location = relative(root, path)
        try:
            metadata, body = load_frontmatter(path)
        except (OSError, ValueError, yaml.YAMLError) as exc:
            report.error(location, str(exc))
            continue
        require_fields(
            metadata,
            {"id", "title", "status", "target_claims", "created_at", "updated_at"},
            location,
            report,
        )
        if metadata.get("id") != artifact_id:
            report.error(location, f"frontmatter id must be '{artifact_id}'")
        if not valid_choice(metadata.get("status"), DERIVATION_STATUSES):
            report.error(location, f"invalid derivation status '{metadata.get('status')}'")
        for timestamp in ("created_at", "updated_at"):
            if not valid_timestamp(metadata.get(timestamp)):
                report.error(location, f"{timestamp} must be a timezone-aware ISO-8601 timestamp")
        targets = metadata.get("target_claims")
        if not isinstance(targets, list):
            report.error(location, "target_claims must be a list")
        else:
            for claim_id in targets:
                validate_id_reference(claim_id, CLAIM_ID, claims, "claim", location, report)
        require_sections(body, derivation_sections, location, report)


def validate_obligation_spec(
    root: Path,
    report: Report,
    obligation: Obligation,
    derivations: dict[str, Path],
) -> Path | None:
    """Validate spec.yaml structurally and return the resolved entrypoint."""
    location = relative(root, obligation.path) + "/spec.yaml"
    spec = obligation.spec
    if spec is None:
        return None
    require_fields(
        spec,
        {
            "schema_version",
            "id",
            "title",
            "claims",
            "derivations",
            "class",
            "required",
            "status",
            "question",
            "assumptions",
            "acceptance_criterion",
            "method",
            "implementation",
            "independence",
            "created_at",
            "updated_at",
        },
        location,
        report,
    )
    if spec.get("schema_version") != 1:
        report.error(location, "schema_version must be 1")
    if spec.get("id") != obligation.id:
        report.error(location, f"id must be '{obligation.id}'")
    if not isinstance(spec.get("title"), str) or not spec.get("title", "").strip():
        report.error(location, "title must be a nonempty string")
    for list_field in ("claims", "derivations", "assumptions"):
        if not isinstance(spec.get(list_field), list):
            report.error(location, f"{list_field} must be a list")
    if not valid_choice(spec.get("class"), OBLIGATION_CLASSES):
        report.error(location, f"invalid check class '{spec.get('class')}'")
    if not isinstance(spec.get("required"), bool):
        report.error(location, "required must be a boolean")
    if not valid_choice(spec.get("status"), OBLIGATION_STATUSES):
        report.error(location, f"invalid obligation status '{spec.get('status')}'")
    for text_field in ("question", "acceptance_criterion"):
        value = spec.get(text_field)
        if not isinstance(value, str) or not value.strip():
            report.error(location, f"{text_field} must be a nonempty string")
    for timestamp in ("created_at", "updated_at"):
        if not valid_timestamp(spec.get(timestamp)):
            report.error(location, f"{timestamp} must be a timezone-aware ISO-8601 timestamp")

    method = spec.get("method")
    if not isinstance(method, dict):
        report.error(location, "method must be a mapping")
    else:
        if not isinstance(method.get("description"), str) or not method.get("description", "").strip():
            report.error(location, "method.description must be a nonempty string")
        if not isinstance(method.get("rationale"), str):
            report.error(location, "method.rationale must be a string")

    independence = spec.get("independence")
    if not isinstance(independence, dict):
        report.error(location, "independence must be a mapping")
    else:
        if not valid_choice(independence.get("requirement"), OBLIGATION_INDEPENDENCE):
            report.error(
                location, f"invalid independence.requirement '{independence.get('requirement')}'"
            )
        if not isinstance(independence.get("rationale"), str):
            report.error(location, "independence.rationale must be a string")

    for derivation_id in spec.get("derivations", []) if isinstance(spec.get("derivations"), list) else []:
        validate_id_reference(
            derivation_id, DERIVATION_ID, derivations, "derivation", location, report
        )

    implementation = spec.get("implementation")
    if not isinstance(implementation, dict):
        report.error(location, "implementation must be a mapping")
        return None
    infrastructure = implementation.get("infrastructure")
    if not isinstance(infrastructure, list):
        report.error(location, "implementation.infrastructure must be a list")
    else:
        for item in infrastructure:
            if not isinstance(item, str) or not item.strip() or Path(item).is_absolute():
                report.error(location, f"invalid infrastructure path '{item}'")
                continue
            candidate = (root / item).resolve()
            try:
                candidate.relative_to(root.resolve())
            except ValueError:
                report.error(location, f"infrastructure path escapes repository: '{item}'")
            else:
                if not candidate.exists():
                    report.error(location, f"infrastructure path does not exist: '{item}'")

    entrypoint = implementation.get("entrypoint")
    if not isinstance(entrypoint, str) or not entrypoint.strip() or Path(entrypoint).is_absolute():
        report.error(location, "implementation.entrypoint must be a repository-relative path")
        return None
    resolved = (root / entrypoint).resolve()
    try:
        resolved.relative_to(obligation.path.resolve())
    except ValueError:
        report.error(location, "implementation.entrypoint must resolve inside the obligation directory")
        return None
    if not resolved.is_file():
        report.error(location, f"implementation.entrypoint does not exist: '{entrypoint}'")
        return None
    return resolved


def validate_obligation_result(
    root: Path,
    report: Report,
    obligation: Obligation,
    entrypoint: Path | None,
) -> None:
    """Validate a recorded machine result without judging its science."""
    location = relative(root, obligation.path) + "/result.json"
    result = obligation.result
    spec = obligation.spec if isinstance(obligation.spec, dict) else {}
    if result is None:
        return
    require_fields(
        result,
        {
            "schema_version",
            "obligation_id",
            "claims",
            "derivations",
            "outcome",
            "exit_code",
            "started_at",
            "completed_at",
            "command",
            "runner_command",
            "implementation",
            "git_commit",
            "dirty_worktree",
            "spec_sha256",
            "implementation_sha256",
            "environment",
            "observations",
            "artifacts",
            "logs",
            "notes",
        },
        location,
        report,
    )
    if result.get("schema_version") != 1:
        report.error(location, "schema_version must be 1")
    if result.get("obligation_id") != obligation.id:
        report.error(location, f"obligation_id must be '{obligation.id}'")
    if not valid_choice(result.get("outcome"), OBLIGATION_OUTCOMES):
        report.error(location, f"invalid outcome '{result.get('outcome')}'")
    if result.get("exit_code") is not None and not isinstance(result.get("exit_code"), int):
        report.error(location, "exit_code must be null or an integer")
    for timestamp in ("started_at", "completed_at"):
        if not valid_timestamp(result.get(timestamp)):
            report.error(location, f"{timestamp} must be a timezone-aware ISO-8601 timestamp")
    for text_field in ("command", "runner_command"):
        if not isinstance(result.get(text_field), str) or not result.get(text_field, "").strip():
            report.error(location, f"{text_field} must be a nonempty string")
    if not isinstance(result.get("notes"), str):
        report.error(location, "notes must be a string")
    if result.get("git_commit") is not None and not isinstance(result.get("git_commit"), str):
        report.error(location, "git_commit must be null or a string")
    if result.get("dirty_worktree") is not None and not isinstance(result.get("dirty_worktree"), bool):
        report.error(location, "dirty_worktree must be null or boolean")
    if not isinstance(result.get("environment"), dict) or not result.get("environment"):
        report.error(location, "environment must be a nonempty mapping")
    if not isinstance(result.get("observations"), dict):
        report.error(location, "observations must be a mapping")
    if result.get("git_commit") is None:
        report.warning(location, "machine result recorded without a Git commit")

    for id_field, pattern in (("claims", CLAIM_ID), ("derivations", DERIVATION_ID)):
        values = result.get(id_field)
        if not isinstance(values, list):
            report.error(location, f"{id_field} must be a list")
            continue
        if any(not isinstance(value, str) or not pattern.fullmatch(value) for value in values):
            report.error(location, f"invalid {id_field} entry in the recorded result")
        expected = spec.get(id_field)
        if isinstance(expected, list) and values != expected:
            report.error(location, f"result {id_field} disagree with spec.yaml")

    implementation = spec.get("implementation") if isinstance(spec.get("implementation"), dict) else {}
    declared_entrypoint = implementation.get("entrypoint")
    if isinstance(declared_entrypoint, str) and result.get("implementation") != declared_entrypoint:
        report.error(location, "result implementation path disagrees with spec.yaml")

    for hash_field, target in (
        ("spec_sha256", obligation.path / "spec.yaml"),
        ("implementation_sha256", entrypoint),
    ):
        value = result.get(hash_field)
        if not isinstance(value, str) or not SHA256.fullmatch(value):
            report.error(location, f"{hash_field} must be a lowercase SHA-256 digest")
            continue
        if target is None or not target.is_file():
            continue
        try:
            actual = sha256_file(target)
        except OSError as exc:
            report.error(location, f"cannot hash {relative(root, target)}: {exc}")
            continue
        if value != actual:
            report.error(
                location,
                f"{hash_field} does not match the current file; rerun scripts/run_check.py "
                f"{obligation.id} because the recorded result is stale",
            )

    for path_field in ("artifacts", "logs"):
        values = result.get(path_field)
        if not isinstance(values, list):
            report.error(location, f"{path_field} must be a list")
            continue
        for value in values:
            if not isinstance(value, str) or not value.strip() or Path(value).is_absolute():
                report.error(location, f"invalid {path_field} path '{value}'")
                continue
            candidate = (root / value).resolve()
            try:
                candidate.relative_to(root.resolve())
            except ValueError:
                report.error(location, f"{path_field} path escapes repository: '{value}'")
            else:
                if not candidate.is_file():
                    report.error(location, f"{path_field} path does not exist: '{value}'")


def validate_obligations(
    root: Path,
    report: Report,
    derivations: dict[str, Path],
) -> dict[str, Obligation]:
    """Load and structurally validate every machine-check obligation."""
    directory = root / "research" / "checks"
    obligations: dict[str, Obligation] = {}
    if not directory.is_dir():
        return obligations
    for entry in sorted(directory.iterdir()):
        if entry.is_file():
            if entry.name != "README.md":
                report.error(
                    relative(root, entry), "unexpected file in research/checks/; obligations are directories"
                )
            continue
        if not OBLIGATION_ID.fullmatch(entry.name):
            report.error(
                relative(root, entry),
                "obligation directories must be named ONNN; allocate IDs with scripts/new_check.py",
            )
            continue
        obligations[entry.name] = Obligation(id=entry.name, path=entry)

    for obligation_id, obligation in obligations.items():
        location = relative(root, obligation.path)
        if not (obligation.path / "README.md").is_file():
            report.error(location, "missing required file 'README.md'")
        spec_path = obligation.path / "spec.yaml"
        if not spec_path.is_file():
            report.error(location, "missing required file 'spec.yaml'")
        else:
            try:
                spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, yaml.YAMLError) as exc:
                report.error(location + "/spec.yaml", str(exc))
                spec = None
            if spec is not None and not isinstance(spec, dict):
                report.error(location + "/spec.yaml", "must contain a mapping")
                spec = None
            obligation.spec = spec
        entrypoint = validate_obligation_spec(root, report, obligation, derivations)

        result_path = obligation.path / "result.json"
        if result_path.is_file():
            try:
                obligation.result = load_json_object(result_path)
            except (OSError, UnicodeError, ValueError) as exc:
                report.error(location + "/result.json", str(exc))
                obligation.result = None
            validate_obligation_result(root, report, obligation, entrypoint)
        elif obligation.is_active and obligation.is_required:
            report.warning(
                location,
                "active required obligation has no result.json; it has not run",
            )
    return obligations


def validate_obligation_claim_links(
    root: Path,
    report: Report,
    claims: set[str],
    claims_by_id: dict[str, dict[str, Any]],
    obligations: dict[str, Obligation],
) -> None:
    """Require obligation -> claim references to exist and be reciprocal."""
    for obligation_id, obligation in obligations.items():
        if not isinstance(obligation.spec, dict):
            continue
        location = relative(root, obligation.path) + "/spec.yaml"
        targets = obligation.spec.get("claims")
        if not isinstance(targets, list):
            continue
        for claim_id in targets:
            validate_id_reference(claim_id, CLAIM_ID, claims, "claim", location, report)
            if not isinstance(claim_id, str) or claim_id not in claims_by_id:
                continue
            if obligation.status != "active":
                continue
            evidence = claims_by_id[claim_id].get("evidence")
            listed = evidence.get("computational_checks") if isinstance(evidence, dict) else None
            if not isinstance(listed, list) or obligation_id not in listed:
                report.error(
                    location,
                    f"active obligation targets {claim_id} but the claim does not list "
                    f"'{obligation_id}' under evidence.computational_checks",
                )


def validate_ledger(
    root: Path,
    report: Report,
    hypotheses: dict[str, Path],
    derivations: dict[str, Path],
    experiments: dict[str, Path],
    obligations: dict[str, Obligation],
) -> tuple[dict[str, dict[str, Any]], dict[str, Any] | None]:
    path = root / "research" / "claims" / "ledger.yaml"
    location = relative(root, path)
    try:
        ledger = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        report.error(location, str(exc))
        return {}, None
    if not isinstance(ledger, dict):
        report.error(location, "ledger root must be a mapping")
        return {}, None
    require_fields(ledger, {"schema_version", "claims"}, location, report)
    if ledger.get("schema_version") != 2:
        report.error(location, "schema_version must be 2")
    entries = ledger.get("claims")
    if not isinstance(entries, list):
        report.error(location, "claims must be a list")
        return {}, ledger

    by_id: dict[str, dict[str, Any]] = {}
    required = {
        "id",
        "claim",
        "status",
        "importance",
        "hypotheses",
        "assumptions",
        "evidence",
        "checks",
        "dependencies",
        "conflicts",
        "created_at",
        "updated_at",
    }
    for index, entry in enumerate(entries):
        entry_location = f"{location}:claims[{index}]"
        if not isinstance(entry, dict):
            report.error(entry_location, "claim entry must be a mapping")
            continue
        require_fields(entry, required, entry_location, report)
        claim_id = entry.get("id")
        if not isinstance(claim_id, str) or not CLAIM_ID.fullmatch(claim_id):
            report.error(entry_location, f"invalid claim id '{claim_id}'")
            continue
        if claim_id in by_id:
            report.error(entry_location, f"duplicate claim id '{claim_id}'")
            continue
        by_id[claim_id] = entry
        if not isinstance(entry.get("claim"), str) or not entry.get("claim", "").strip():
            report.error(entry_location, "claim must be a non-empty string")
        for timestamp in ("created_at", "updated_at"):
            if not valid_timestamp(entry.get(timestamp)):
                report.error(entry_location, f"{timestamp} must be a timezone-aware ISO-8601 timestamp")
        if not valid_choice(entry.get("status"), CLAIM_STATUSES):
            report.error(entry_location, f"invalid claim status '{entry.get('status')}'")
        if not valid_choice(entry.get("importance"), IMPORTANCE_LEVELS):
            report.error(entry_location, f"invalid importance '{entry.get('importance')}'")
        for list_field in ("hypotheses", "assumptions", "dependencies", "conflicts"):
            if not isinstance(entry.get(list_field), list):
                report.error(entry_location, f"{list_field} must be a list")

        evidence = entry.get("evidence")
        if not isinstance(evidence, dict):
            report.error(entry_location, "evidence must be a mapping")
            evidence = {}
        evidence_fields = {
            "derivations",
            "experiments",
            "literature",
            "computational_checks",
            "verification",
        }
        require_fields(evidence, evidence_fields, entry_location + ":evidence", report)
        for field_name in evidence_fields:
            if not isinstance(evidence.get(field_name), list):
                report.error(entry_location, f"evidence.{field_name} must be a list")

        checks = entry.get("checks")
        if not isinstance(checks, dict):
            report.error(entry_location, "checks must be a mapping")
            checks = {}
        check_fields = {
            "dimensional_analysis",
            "limiting_cases",
            "computational_verification",
            "independent_verification",
        }
        require_fields(checks, check_fields, entry_location + ":checks", report)
        for name in check_fields:
            if not valid_choice(checks.get(name), CHECK_STATUSES):
                report.error(entry_location, f"invalid checks.{name} value '{checks.get(name)}'")

        for hypothesis_id in entry.get("hypotheses", []) if isinstance(entry.get("hypotheses"), list) else []:
            validate_id_reference(
                hypothesis_id, HYPOTHESIS_ID, hypotheses, "hypothesis", entry_location, report
            )
        qualifying_derivations = 0
        for derivation_id in evidence.get("derivations", []) if isinstance(evidence.get("derivations"), list) else []:
            validate_id_reference(
                derivation_id, DERIVATION_ID, derivations, "derivation", entry_location, report
            )
            if isinstance(derivation_id, str) and derivation_id in derivations:
                try:
                    derivation_metadata, _ = load_frontmatter(derivations[derivation_id])
                except (OSError, ValueError, yaml.YAMLError):
                    continue
                targets = derivation_metadata.get("target_claims")
                if isinstance(targets, list) and claim_id not in targets:
                    report.error(entry_location, f"derivation '{derivation_id}' does not target {claim_id}")
                if (
                    derivation_metadata.get("status") in {"complete", "checked"}
                    and isinstance(targets, list)
                    and claim_id in targets
                ):
                    qualifying_derivations += 1

        qualifying_experiments = 0
        for experiment_id in evidence.get("experiments", []) if isinstance(evidence.get("experiments"), list) else []:
            validate_id_reference(
                experiment_id, EXPERIMENT_ID, experiments, "experiment", entry_location, report
            )
            if not isinstance(experiment_id, str) or experiment_id not in experiments:
                continue
            try:
                experiment_metadata, _ = load_frontmatter(experiments[experiment_id] / "README.md")
                experiment_result = load_json_object(experiments[experiment_id] / "result.json")
            except (OSError, ValueError, yaml.YAMLError):
                continue
            experiment_claims = experiment_metadata.get("claims")
            result_claims = experiment_result.get("claims")
            if isinstance(experiment_claims, list) and claim_id not in experiment_claims:
                report.error(entry_location, f"experiment '{experiment_id}' does not target {claim_id}")
            experiment_checks = experiment_result.get("checks")
            check_names = ("convergence", "independent_seed", "known_limit", "precision")
            checks_pass = isinstance(experiment_checks, dict) and all(
                explicit_check_outcome(experiment_checks.get(name)) in {"passed", "not-applicable"}
                for name in check_names
            )
            if (
                experiment_metadata.get("status") == "complete"
                and isinstance(experiment_claims, list)
                and claim_id in experiment_claims
                and isinstance(result_claims, list)
                and claim_id in result_claims
                and isinstance(experiment_result.get("results"), dict)
                and bool(experiment_result["results"])
                and isinstance(experiment_checks, dict)
                and experiment_checks.get("completed") is True
                and checks_pass
            ):
                qualifying_experiments += 1

        listed_obligations = (
            evidence.get("computational_checks")
            if isinstance(evidence.get("computational_checks"), list)
            else []
        )
        qualifying_checks = 0
        for obligation_id in listed_obligations:
            validate_id_reference(
                obligation_id, OBLIGATION_ID, obligations, "obligation", entry_location, report
            )
            obligation = obligations.get(obligation_id) if isinstance(obligation_id, str) else None
            if obligation is None or not isinstance(obligation.spec, dict):
                continue
            if claim_id not in obligation.targets:
                report.error(entry_location, f"obligation '{obligation_id}' does not target {claim_id}")
                continue
            if obligation.is_active and obligation.satisfied():
                qualifying_checks += 1

        # Structural gate over the project's own declared verification strategy.
        # It says nothing about whether those obligations are scientifically
        # sufficient; that judgment belongs to the independent verifier.
        unsatisfied_required = sorted(
            obligation_id
            for obligation_id, obligation in obligations.items()
            if obligation.is_active
            and obligation.is_required
            and claim_id in obligation.targets
            and not obligation.satisfied()
        )
        if unsatisfied_required and checks.get("computational_verification") == "passed":
            report.error(
                entry_location,
                "checks.computational_verification cannot be passed while active required "
                f"obligation(s) lack a passing result: {', '.join(unsatisfied_required)}",
            )

        qualifying_literature_notes = 0
        for source in evidence.get("literature", []) if isinstance(evidence.get("literature"), list) else []:
            if not isinstance(source, str) or not source.strip():
                report.error(entry_location, f"invalid literature evidence reference '{source}'")
            elif source.startswith("research/"):
                note = confined_artifact(root, source, root / "research" / "literature" / "notes")
                if note is None or note.name == "README.md" or note.suffix != ".md":
                    report.error(entry_location, f"invalid or missing literature-note path: '{source}'")
                else:
                    try:
                        _, note_body = load_frontmatter(note)
                    except (OSError, ValueError, yaml.YAMLError):
                        continue
                    if literature_note_is_substantive(note_body):
                        qualifying_literature_notes += 1

        verification_outcomes = []
        qualifying_verified_reports = 0
        for source in evidence.get("verification", []) if isinstance(evidence.get("verification"), list) else []:
            if not isinstance(source, str):
                report.error(entry_location, "verification evidence must be a path under research/results/verification/")
            else:
                report_path = confined_artifact(
                    root, source, root / "research" / "results" / "verification"
                )
                if report_path is None or report_path.name == "README.md" or report_path.suffix != ".md":
                    report.error(entry_location, f"invalid or missing verification report: '{source}'")
                    continue
                try:
                    report_metadata, report_body = load_frontmatter(report_path)
                except (OSError, ValueError, yaml.YAMLError) as exc:
                    report.error(entry_location, f"cannot read verification report '{source}': {exc}")
                    continue
                if report_metadata.get("claim_id") != claim_id:
                    report.error(entry_location, f"verification report '{source}' targets another claim")
                outcome = report_metadata.get("outcome")
                verification_outcomes.append(outcome)
                if (
                    outcome == "verified"
                    and isinstance(report_metadata.get("source_artifacts"), list)
                    and bool(report_metadata["source_artifacts"])
                    and verification_has_model_separation(report_metadata)
                    and verification_report_is_substantive(report_body)
                ):
                    qualifying_verified_reports += 1

        status = entry.get("status")
        if status == "derived" and not qualifying_derivations:
            report.error(entry_location, "derived status requires a complete reciprocal derivation")
        if status == "numerically-supported" and not qualifying_experiments:
            report.error(entry_location, "numerically-supported status requires a complete checked experiment")
        if status == "literature-supported" and not qualifying_literature_notes:
            report.error(entry_location, "literature-supported status requires a linked literature note")
        if status == "reproduced":
            if checks.get("computational_verification") != "passed":
                report.error(
                    entry_location, "reproduced status requires checks.computational_verification: passed"
                )
            if not qualifying_experiments and not qualifying_checks:
                report.error(
                    entry_location,
                    "reproduced status requires a complete checked experiment or a passing "
                    "active machine-check obligation",
                )
        if status == "verified":
            if checks.get("independent_verification") != "passed":
                report.error(entry_location, "verified status requires checks.independent_verification: passed")
            for check_name in ("dimensional_analysis", "limiting_cases", "computational_verification"):
                if checks.get(check_name) not in {"passed", "not-applicable"}:
                    report.error(entry_location, f"verified status requires an explicit passing {check_name} check")
            if unsatisfied_required:
                report.error(
                    entry_location,
                    "verified status requires every active required obligation to have a passing "
                    f"result; unsatisfied: {', '.join(unsatisfied_required)}",
                )
            if not qualifying_verified_reports:
                report.error(
                    entry_location,
                    "verified status requires a substantive linked report with known model separation",
                )
            if any(outcome in {"failed verification", "contradicted"} for outcome in verification_outcomes):
                report.error(entry_location, "verified status conflicts with a linked failed or contradicted report")

    known_ids = set(by_id)
    for claim_id, entry in by_id.items():
        entry_location = f"{location}:{claim_id}"
        for field_name in ("dependencies", "conflicts"):
            values = entry.get(field_name, [])
            if not isinstance(values, list):
                continue
            for reference in values:
                if not isinstance(reference, str) or not CLAIM_ID.fullmatch(reference):
                    report.error(entry_location, f"invalid {field_name} claim reference '{reference}'")
                elif reference == claim_id:
                    report.error(entry_location, f"{field_name} cannot reference the claim itself")
                elif reference not in known_ids:
                    report.error(entry_location, f"{field_name} references unknown claim '{reference}'")
    return by_id, ledger


def validate_experiments(
    root: Path,
    report: Report,
    claims: set[str],
    experiments: dict[str, Path],
) -> None:
    readme_sections = [
        "Question",
        "Hypothesis/claim tested",
        "Method",
        "Expected discriminating result",
        "Parameters",
        "Environment",
        "How to run",
        "Convergence plan",
        "Validation checks",
        "Result",
        "Interpretation",
        "Known limitations",
    ]
    required_files = ("README.md", "config.yaml", "run.py", "analysis.py", "result.json")
    required_result = {
        "schema_version",
        "experiment_id",
        "title",
        "claims",
        "git_commit",
        "dirty_worktree",
        "command",
        "config_sha256",
        "started_at",
        "completed_at",
        "environment",
        "parameters",
        "random_seeds",
        "results",
        "checks",
        "artifacts",
        "notes",
    }
    for experiment_id, directory in experiments.items():
        location = relative(root, directory)
        for name in required_files:
            if not (directory / name).is_file():
                report.error(location, f"missing required file '{name}'")
        for name in ("raw", "figures"):
            if not (directory / name).is_dir():
                report.error(location, f"missing required directory '{name}/'")

        readme_claims: list[Any] | None = None
        readme_status: str | None = None
        config: dict[str, Any] | None = None
        config_hash_actual: str | None = None
        result: dict[str, Any] | None = None
        readme = directory / "README.md"
        if readme.exists():
            try:
                metadata, body = load_frontmatter(readme)
                require_fields(
                    metadata,
                    {"id", "title", "status", "claims", "created_at", "updated_at"},
                    location + "/README.md",
                    report,
                )
                if metadata.get("id") != experiment_id:
                    report.error(location + "/README.md", f"frontmatter id must be '{experiment_id}'")
                readme_status = metadata.get("status")
                if not valid_choice(readme_status, EXPERIMENT_STATUSES):
                    report.error(location + "/README.md", f"invalid experiment status '{readme_status}'")
                for timestamp in ("created_at", "updated_at"):
                    if not valid_timestamp(metadata.get(timestamp)):
                        report.error(
                            location + "/README.md",
                            f"{timestamp} must be a timezone-aware ISO-8601 timestamp",
                        )
                readme_claims = metadata.get("claims")
                if not isinstance(readme_claims, list):
                    report.error(location + "/README.md", "claims must be a list")
                    readme_claims = None
                require_sections(body, readme_sections, location + "/README.md", report)
            except (OSError, ValueError, yaml.YAMLError) as exc:
                report.error(location + "/README.md", str(exc))

        config_claims: list[Any] | None = None
        config_path = directory / "config.yaml"
        if config_path.exists():
            try:
                config_bytes = config_path.read_bytes()
                config_hash_actual = hashlib.sha256(config_bytes).hexdigest()
                config = yaml.safe_load(config_bytes)
                if not isinstance(config, dict):
                    report.error(location + "/config.yaml", "must contain a mapping")
                    config = None
                else:
                    require_fields(
                        config,
                        {
                            "schema_version",
                            "experiment_id",
                            "claims",
                            "title",
                            "method",
                            "parameters",
                            "random_seeds",
                            "inputs",
                            "solver",
                            "convergence",
                        },
                        location + "/config.yaml",
                        report,
                    )
                    if config.get("schema_version") != 1:
                        report.error(location + "/config.yaml", "schema_version must be 1")
                    if config.get("experiment_id") != experiment_id:
                        report.error(location + "/config.yaml", f"experiment_id must be '{experiment_id}'")
                    if not isinstance(config.get("title"), str) or not config.get("title", "").strip():
                        report.error(location + "/config.yaml", "title must be a nonempty string")
                    if not isinstance(config.get("method"), str) or not config.get("method", "").strip():
                        report.error(location + "/config.yaml", "method must be a nonempty string")
                    config_claims = config.get("claims")
                    if not isinstance(config_claims, list):
                        report.error(location + "/config.yaml", "claims must be a list")
                        config_claims = None
                    if not isinstance(config.get("parameters"), dict):
                        report.error(location + "/config.yaml", "parameters must be a mapping")
                    if not isinstance(config.get("random_seeds"), list):
                        report.error(location + "/config.yaml", "random_seeds must be a list")
                    inputs = config.get("inputs")
                    if not isinstance(inputs, list):
                        report.error(location + "/config.yaml", "inputs must be a list")
                    else:
                        for index, item in enumerate(inputs):
                            if not isinstance(item, dict) or not isinstance(item.get("source"), str):
                                report.error(
                                    location + "/config.yaml",
                                    f"inputs[{index}] must identify a source",
                                )
                            elif not any(item.get(key) for key in ("sha256", "version", "generated_by")):
                                report.error(
                                    location + "/config.yaml",
                                    f"inputs[{index}] needs sha256, version, or generated_by provenance",
                                )
            except (OSError, UnicodeError, yaml.YAMLError) as exc:
                report.error(location + "/config.yaml", str(exc))

        result_claims: list[Any] | None = None
        result_path = directory / "result.json"
        if result_path.exists():
            try:
                result = load_json_object(result_path)
            except (OSError, UnicodeError, ValueError) as exc:
                report.error(location + "/result.json", str(exc))
                result = None
            if result is not None:
                require_fields(result, required_result, location + "/result.json", report)
                if result.get("schema_version") != 1:
                    report.error(location + "/result.json", "schema_version must be 1")
                if result.get("experiment_id") != experiment_id:
                    report.error(location + "/result.json", f"experiment_id must be '{experiment_id}'")
                result_claims = result.get("claims")
                if not isinstance(result_claims, list):
                    report.error(location + "/result.json", "claims must be a list")
                    result_claims = None
                checks = result.get("checks")
                if not isinstance(checks, dict):
                    report.error(location + "/result.json", "checks must be a mapping")
                    checks = {}
                else:
                    require_fields(
                        checks,
                        {"completed", "convergence", "independent_seed", "known_limit", "precision"},
                        location + "/result.json:checks",
                        report,
                    )
                    if not isinstance(checks.get("completed"), bool):
                        report.error(location + "/result.json", "checks.completed must be boolean")
                    if checks.get("completed"):
                        for name in ("convergence", "independent_seed", "known_limit", "precision"):
                            if explicit_check_outcome(checks.get(name)) is None:
                                report.error(
                                    location + "/result.json",
                                    f"completed checks require an explicit {name} outcome",
                                )
                if not isinstance(result.get("parameters"), dict):
                    report.error(location + "/result.json", "parameters must be a mapping")
                if not isinstance(result.get("title"), str) or not result.get("title", "").strip():
                    report.error(location + "/result.json", "title must be a nonempty string")
                if not isinstance(result.get("environment"), dict):
                    report.error(location + "/result.json", "environment must be a mapping")
                if not isinstance(result.get("random_seeds"), list):
                    report.error(location + "/result.json", "random_seeds must be a list")
                if not isinstance(result.get("results"), dict):
                    report.error(location + "/result.json", "results must be a mapping")
                if not isinstance(result.get("artifacts"), list):
                    report.error(location + "/result.json", "artifacts must be a list")
                else:
                    for artifact in result.get("artifacts", []):
                        if not isinstance(artifact, str) or not artifact.strip():
                            report.error(location + "/result.json", f"invalid artifact path '{artifact}'")
                            continue
                        candidate = (
                            (root / artifact).resolve()
                            if artifact.startswith("research/")
                            else (directory / artifact).resolve()
                        )
                        try:
                            candidate.relative_to(root.resolve())
                        except ValueError:
                            report.error(location + "/result.json", f"artifact escapes repository: '{artifact}'")
                        else:
                            if not candidate.exists():
                                report.error(location + "/result.json", f"artifact does not exist: '{artifact}'")
                if result.get("git_commit") is not None and not isinstance(result.get("git_commit"), str):
                    report.error(location + "/result.json", "git_commit must be null or a string")
                if result.get("dirty_worktree") is not None and not isinstance(
                    result.get("dirty_worktree"), bool
                ):
                    report.error(location + "/result.json", "dirty_worktree must be null or boolean")
                if result.get("command") is not None and not isinstance(result.get("command"), str):
                    report.error(location + "/result.json", "command must be null or a string")
                if result.get("config_sha256") is not None and not re.fullmatch(
                    r"[0-9a-f]{64}", str(result.get("config_sha256"))
                ):
                    report.error(location + "/result.json", "config_sha256 must be null or lowercase SHA-256")
                if result.get("results") and result.get("git_commit") is None:
                    report.warning(location + "/result.json", "results exist without a Git commit")
                if config is not None:
                    if result.get("parameters") != config.get("parameters"):
                        report.error(location, "result parameters do not match config.yaml")
                    if result.get("random_seeds") != config.get("random_seeds"):
                        report.error(location, "result random_seeds do not match config.yaml")

                if readme_status == "complete":
                    if not isinstance(result.get("results"), dict) or not result.get("results"):
                        report.error(location + "/README.md", "status complete requires nonempty results")
                    if not isinstance(result.get("command"), str) or not result["command"].strip():
                        report.error(location + "/result.json", "complete experiment requires a command")
                    if not isinstance(result.get("environment"), dict) or not result["environment"]:
                        report.error(location + "/result.json", "complete experiment requires environment metadata")
                    if not valid_timestamp(result.get("started_at")) or not valid_timestamp(
                        result.get("completed_at")
                    ):
                        report.error(location + "/result.json", "complete experiment requires run timestamps")
                    if not isinstance(result.get("dirty_worktree"), bool):
                        report.error(location + "/result.json", "complete experiment requires dirty-worktree state")
                    if not checks.get("completed", False):
                        report.error(location + "/README.md", "status complete requires completed result checks")
                    for name in ("convergence", "independent_seed", "known_limit", "precision"):
                        if explicit_check_outcome(checks.get(name)) not in {"passed", "not-applicable"}:
                            report.error(
                                location + "/README.md",
                                f"status complete requires passing or not-applicable {name} check",
                            )
                    if config_hash_actual is not None:
                        if result.get("config_sha256") != config_hash_actual:
                            report.error(location + "/result.json", "config_sha256 does not match config.yaml")

        if readme_status == "complete" and result is None:
            report.error(location + "/README.md", "status complete requires a valid result.json")

        claim_lists = [values for values in (readme_claims, config_claims, result_claims) if values is not None]
        if claim_lists and any(values != claim_lists[0] for values in claim_lists[1:]):
            report.error(location, "claim links disagree among README.md, config.yaml, and result.json")
        for claim_id in claim_lists[0] if claim_lists else []:
            validate_id_reference(claim_id, CLAIM_ID, claims, "claim", location, report)


def validate_literature_notes(root: Path, report: Report) -> None:
    directory = root / "research" / "literature" / "notes"
    if not directory.exists():
        return
    for path in directory.rglob("*.md"):
        if path.name == "README.md":
            continue
        location = relative(root, path)
        try:
            path.resolve().relative_to(directory.resolve())
            metadata, body = load_frontmatter(path)
        except ValueError as exc:
            report.error(location, str(exc))
            continue
        except (OSError, yaml.YAMLError) as exc:
            report.error(location, str(exc))
            continue
        require_fields(
            metadata,
            {"citation_key", "title", "authors", "year", "doi", "arxiv", "url", "date_accessed"},
            location,
            report,
        )
        for field_name in ("citation_key", "title"):
            value = metadata.get(field_name)
            if not isinstance(value, str) or not value.strip() or "{{" in value:
                report.error(location, f"{field_name} must be a resolved nonempty string")
        if not isinstance(metadata.get("authors"), list) or not metadata.get("authors"):
            report.error(location, "authors must be a nonempty list")
        if not any(metadata.get(name) for name in ("doi", "arxiv", "url")):
            report.error(location, "record at least one stable DOI, arXiv ID, or URL")
        try:
            datetime.fromisoformat(str(metadata.get("date_accessed")))
        except ValueError:
            report.error(location, "date_accessed must be ISO-8601")
        require_sections(body, LITERATURE_SECTIONS, location, report)


def validate_verification_reports(root: Path, report: Report, claims: set[str]) -> None:
    directory = root / "research" / "results" / "verification"
    if not directory.exists():
        return
    for path in directory.rglob("*.md"):
        if path.name == "README.md":
            continue
        location = relative(root, path)
        try:
            path.resolve().relative_to(directory.resolve())
        except ValueError:
            report.error(location, "verification report resolves outside its designated directory")
            continue
        if not re.fullmatch(r"C\d{3}-\d{4}-\d{2}-\d{2}(?:-[a-z0-9-]+)?\.md", path.name):
            report.error(location, "verification filename must be CNNN-YYYY-MM-DD[-attempt].md")
        try:
            metadata, body = load_frontmatter(path)
        except (OSError, ValueError, yaml.YAMLError) as exc:
            report.error(location, str(exc))
            continue
        require_fields(
            metadata,
            {
                "claim_id",
                "outcome",
                "date",
                "verifier",
                "verifier_model",
                "originating_models",
                "source_artifacts",
            },
            location,
            report,
        )
        validate_id_reference(metadata.get("claim_id"), CLAIM_ID, claims, "claim", location, report)
        if isinstance(metadata.get("claim_id"), str) and not path.name.startswith(metadata["claim_id"] + "-"):
            report.error(location, "filename claim ID does not match frontmatter")
        if not valid_choice(metadata.get("outcome"), VERIFICATION_OUTCOMES):
            report.error(location, f"invalid verification outcome '{metadata.get('outcome')}'")
        try:
            datetime.fromisoformat(str(metadata.get("date")))
        except ValueError:
            report.error(location, "date must be ISO-8601")
        verifier = metadata.get("verifier")
        if (
            not isinstance(verifier, str)
            or not verifier.strip()
            or verifier == "independent-verifier"
            or "{{" in verifier
        ):
            report.error(location, "verifier must identify the actual verification agent or method")
        verifier_model = metadata.get("verifier_model")
        if not valid_model_id(verifier_model):
            report.error(location, "verifier_model must be a full provider/model ID")
        originating_models = metadata.get("originating_models")
        if not isinstance(originating_models, list) or not originating_models:
            report.error(location, "originating_models must be a nonempty list")
        else:
            for model in originating_models:
                if model == "unknown":
                    report.warning(location, "originating model is unknown; model separation is unproven")
                elif not valid_model_id(model):
                    report.error(location, f"invalid originating model ID '{model}'")
            if valid_model_id(verifier_model):
                known_models = [model for model in originating_models if valid_model_id(model)]
                if verifier_model in known_models:
                    report.warning(location, "verifier model also materially produced the claim or its evidence")
                verifier_provider = verifier_model.split("/", 1)[0]
                if any(model.split("/", 1)[0] == verifier_provider for model in known_models):
                    report.warning(location, "verifier shares a provider with at least one originating model")
        if metadata.get("outcome") == "verified" and not verification_has_model_separation(metadata):
            report.error(location, "verified outcome requires known originating models distinct from verifier_model")
        source_artifacts = metadata.get("source_artifacts")
        if not isinstance(source_artifacts, list) or not source_artifacts:
            report.error(location, "source_artifacts must be a nonempty list")
        else:
            for source in source_artifacts:
                if not isinstance(source, str) or not source.strip():
                    report.error(location, f"invalid source artifact '{source}'")
                elif source.startswith("research/"):
                    candidate = (root / source).resolve()
                    try:
                        candidate.relative_to(root.resolve())
                    except ValueError:
                        report.error(location, f"source artifact escapes repository: '{source}'")
                    else:
                        if not candidate.is_file():
                            report.error(location, f"source artifact does not exist: '{source}'")
        require_sections(body, VERIFICATION_SECTIONS, location, report)
        if not verification_report_is_substantive(body):
            report.error(location, "verification report still contains empty or instructional sections")
        outcome_section = markdown_sections(body).get("Outcome", "").lower()
        if isinstance(metadata.get("outcome"), str) and metadata["outcome"] not in outcome_section:
            report.error(location, "Outcome section must state the frontmatter outcome")


def validate_supporting_state(root: Path, report: Report) -> None:
    expected = [
        "research/QUESTION.md",
        "research/STATE.md",
        "research/COMPUTATION.md",
        "research/DECISIONS.md",
        "research/provenance.jsonl",
        "research/claims/ledger.yaml",
        "research/literature/bibliography.bib",
    ]
    for name in expected:
        if not (root / name).is_file():
            report.error(name, "required artifact is missing")

    section_requirements = {
        "research/QUESTION.md": ["Question", "Scope", "Conventions", "Success criteria"],
        "research/COMPUTATION.md": COMPUTATION_SECTIONS,
        "research/STATE.md": [
            "Current question",
            "Current working picture",
            "Active hypotheses",
            "Highest-value claims",
            "Strongest evidence",
            "Known contradictions",
            "Open verification tasks",
            "Running/next experiments",
            "Literature gaps",
            "Next recommended actions",
        ],
    }
    for name, sections in section_requirements.items():
        path = root / name
        if path.exists():
            try:
                require_sections(path.read_text(encoding="utf-8"), sections, name, report)
            except (OSError, UnicodeError) as exc:
                report.error(name, str(exc))

    # A computation plan is required once a research question actually exists.
    # The validator checks that the plan is initialized and structurally
    # complete; it never judges the scientific method the research chose.
    plan = root / "research" / "COMPUTATION.md"
    if plan.is_file() and current_question(root):
        try:
            plan_text = plan.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            report.error("research/COMPUTATION.md", str(exc))
            plan_text = ""
        if COMPUTATION_UNINITIALIZED_MARKER in plan_text:
            report.error(
                "research/COMPUTATION.md",
                "a research question is initialized but the computational verification strategy "
                "is still the uninitialized scaffold; run scripts/init_computation_plan.py and "
                "populate it",
            )
        phase = markdown_sections(plan_text).get("Current research phase", "").strip()
        if phase.lower().startswith(("not set", "none", "tbd")):
            report.error(
                "research/COMPUTATION.md",
                "'## Current research phase' must describe the current methodological regime",
            )

    provenance = root / "research" / "provenance.jsonl"
    if provenance.exists():
        allowed_fields = {
            "timestamp",
            "agent",
            "provider_id",
            "model_id",
            "session_id",
            "tool",
            "operation",
            "experiment_id",
            "obligation_id",
            "claim_id",
            "command",
            "relevant_paths",
            "git_commit",
            "dirty_worktree",
            "success",
        }
        try:
            provenance_lines = provenance.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            report.error("research/provenance.jsonl", str(exc))
            provenance_lines = []
        for line_number, line in enumerate(provenance_lines, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line, parse_constant=reject_json_constant)
            except (json.JSONDecodeError, ValueError) as exc:
                report.error(f"research/provenance.jsonl:{line_number}", str(exc))
                continue
            if not isinstance(record, dict):
                report.error(f"research/provenance.jsonl:{line_number}", "record must be an object")
                continue
            unknown = set(record) - allowed_fields
            if unknown:
                report.error(
                    f"research/provenance.jsonl:{line_number}",
                    f"unsupported field(s): {', '.join(sorted(unknown))}",
                )
            if not valid_timestamp(record.get("timestamp")):
                report.error(f"research/provenance.jsonl:{line_number}", "invalid timestamp")
            if not isinstance(record.get("operation"), str) or not record.get("operation", "").strip():
                report.error(f"research/provenance.jsonl:{line_number}", "operation must be a string")
            if "success" in record and not isinstance(record["success"], bool):
                report.error(f"research/provenance.jsonl:{line_number}", "success must be boolean")
            provider_id = record.get("provider_id")
            model_id = record.get("model_id")
            if (provider_id is None) != (model_id is None):
                report.error(
                    f"research/provenance.jsonl:{line_number}",
                    "provider_id and model_id must be recorded together",
                )
            for field_name, value in (("provider_id", provider_id), ("model_id", model_id)):
                if value is not None and (not isinstance(value, str) or not value.strip()):
                    report.error(
                        f"research/provenance.jsonl:{line_number}",
                        f"{field_name} must be a nonempty string",
                    )
            paths = record.get("relevant_paths", [])
            if not isinstance(paths, list):
                report.error(f"research/provenance.jsonl:{line_number}", "relevant_paths must be a list")
            else:
                for value in paths:
                    if not isinstance(value, str) or Path(value).is_absolute():
                        report.error(
                            f"research/provenance.jsonl:{line_number}",
                            f"invalid relevant path '{value}'",
                        )
                        continue
                    try:
                        (root / value).resolve().relative_to(root.resolve())
                    except ValueError:
                        report.error(
                            f"research/provenance.jsonl:{line_number}",
                            f"relevant path escapes repository: '{value}'",
                        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    report = Report()
    hypotheses = artifact_ids(root / "research" / "hypotheses", "H")
    derivations = artifact_ids(root / "research" / "derivations", "D")
    experiments = artifact_ids(root / "research" / "experiments", "E", directories=True)
    obligations = validate_obligations(root, report, derivations)
    claims_by_id, _ = validate_ledger(
        root, report, hypotheses, derivations, experiments, obligations
    )
    claim_ids = set(claims_by_id)
    validate_obligation_claim_links(root, report, claim_ids, claims_by_id, obligations)
    validate_markdown_artifacts(root, report, claim_ids, hypotheses, derivations)
    validate_experiments(root, report, claim_ids, experiments)
    validate_literature_notes(root, report)
    validate_verification_reports(root, report, claim_ids)
    validate_supporting_state(root, report)

    payload = {
        "valid": not report.errors and not (args.strict and report.warnings),
        "errors": report.errors,
        "warnings": report.warnings,
        "counts": {
            "claims": len(claim_ids),
            "hypotheses": len(hypotheses),
            "derivations": len(derivations),
            "experiments": len(experiments),
            "obligations": len(obligations),
            "active_obligations": sum(1 for item in obligations.values() if item.is_active),
        },
    }
    commit, dirty = git_state(root)
    append_provenance(
        root,
        tool="validate_research_state",
        operation="research-validation",
        command=(
            "uv run --locked python scripts/validate_research_state.py"
            + (" --strict" if args.strict else "")
        ),
        relevant_paths=[
            "research/claims/ledger.yaml",
            "research/STATE.md",
            "research/COMPUTATION.md",
        ],
        git_commit=commit,
        dirty_worktree=dirty,
        success=payload["valid"],
    )
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for issue in report.errors:
            print(f"ERROR {issue['location']}: {issue['message']}")
        for issue in report.warnings:
            print(f"WARNING {issue['location']}: {issue['message']}")
        print(
            f"Validation {'passed' if payload['valid'] else 'failed'}: "
            f"{len(report.errors)} error(s), {len(report.warnings)} warning(s); "
            f"{len(claim_ids)} claim(s), {len(hypotheses)} hypothesis artifact(s), "
            f"{len(derivations)} derivation(s), {len(experiments)} experiment(s), "
            f"{len(obligations)} machine-check obligation(s)."
        )
    return 0 if payload["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
