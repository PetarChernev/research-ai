"""Configuration, permission scope, and documentation consistency checks."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml

from tests.support import PROJECT_ROOT


AGENTS = PROJECT_ROOT / ".opencode" / "agents"
COMMANDS = PROJECT_ROOT / ".opencode" / "commands"
SKILLS = PROJECT_ROOT / ".opencode" / "skills"
CONFIG_GLOBS = (
    ".opencode/agents/*.md",
    ".opencode/commands/*.md",
    ".opencode/skills/*/SKILL.md",
    ".opencode/tools/*.ts",
    ".opencode/plugins/*.js",
    "opencode.json",
)


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    assert lines[0] == "---", f"{path} has no frontmatter"
    end = next(index for index, line in enumerate(lines[1:], 1) if line == "---")
    return yaml.safe_load("\n".join(lines[1:end]))


class AgentCompatibilityTests(unittest.TestCase):
    def test_agents_do_not_set_step_caps(self) -> None:
        # OpenCode 1.18.19 sends its final-step instruction as an assistant
        # prefill, which Claude 4.6+ rejects before it can return a summary.
        capped = [path.name for path in AGENTS.glob("*.md") if "steps" in frontmatter(path)]
        self.assertEqual(capped, [], "explicit agent step caps trigger OpenCode issue #40455")


class AgentRenameTests(unittest.TestCase):
    def test_scientific_computation_replaced_numerics(self) -> None:
        self.assertTrue((AGENTS / "scientific-computation.md").is_file())
        self.assertFalse((AGENTS / "numerics.md").exists())

    def test_no_active_configuration_references_the_old_agent(self) -> None:
        # Matches agent references such as `numerics`, numerics:, agents/numerics.md.
        reference = re.compile(r"(?:`numerics`|(?:^|[\s\"'/])numerics(?:\.md|:))")
        stale = []
        for pattern in CONFIG_GLOBS:
            for path in PROJECT_ROOT.glob(pattern):
                for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                    if reference.search(line):
                        stale.append(f"{path.relative_to(PROJECT_ROOT)}:{number}: {line.strip()}")
        self.assertEqual(stale, [], "stale numerics agent references remain")

    def test_no_stale_agent_reference_in_documentation(self) -> None:
        reference = re.compile(r"`numerics`")
        stale = []
        for path in list(PROJECT_ROOT.glob("docs/*.md")) + [
            PROJECT_ROOT / "README.md",
            PROJECT_ROOT / "AGENTS.md",
        ]:
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if reference.search(line):
                    stale.append(f"{path.relative_to(PROJECT_ROOT)}:{number}")
        self.assertEqual(stale, [], "documentation still names the removed numerics agent")

    def test_director_delegates_to_scientific_computation(self) -> None:
        permission = frontmatter(AGENTS / "research-director.md")["permission"]
        self.assertIn("scientific-computation", permission["task"])
        self.assertNotIn("engineer", permission["task"])
        self.assertNotIn("numerics", permission["task"])
        self.assertEqual(permission["task"]["internal-critic-openai"], "allow")
        self.assertEqual(permission["task"]["verifier-anthropic"], "allow")
        self.assertNotIn("verifier-openai", permission["task"])
        for tool in ("research_new_check", "research_run_check", "research_init_computation_plan"):
            self.assertEqual(permission[tool], "allow")
        self.assertEqual(permission["skill"]["computational-verification"], "allow")


class ScientificComputationScopeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.permission = frontmatter(AGENTS / "scientific-computation.md")["permission"]

    def test_write_scope(self) -> None:
        edit = self.permission["edit"]
        self.assertEqual(edit["*"], "deny")
        for allowed in ("research/experiments/**", "research/checks/**"):
            self.assertEqual(edit[allowed], "allow")
        self.assertNotIn("research/computation/**", edit)
        self.assertNotIn("research/environment/**", edit)
        self.assertEqual(edit["research/checks/**/result.json"], "deny")
        keys = list(edit)
        self.assertGreater(
            keys.index("research/checks/**/result.json"),
            keys.index("research/checks/**"),
            "the result.json denial must follow the broader allow rule",
        )

    def test_tool_scope(self) -> None:
        for tool in (
            "research_new_experiment",
            "research_new_check",
            "research_run_check",
            "research_run_experiment",
            "research_run_infrastructure_tests",
        ):
            self.assertEqual(self.permission[tool], "allow")

    def test_skill_scope(self) -> None:
        skills = self.permission["skill"]
        self.assertEqual(skills["*"], "deny")
        for skill in ("computational-verification", "numerical-experiment"):
            self.assertEqual(skills[skill], "allow")

    def test_it_can_delegate_only_to_engineer_and_cannot_touch_the_ledger(self) -> None:
        self.assertEqual(self.permission["task"], {"*": "deny", "engineer": "allow"})
        self.assertNotIn("research/claims/**", self.permission["edit"])
        self.assertNotIn("research/results/verification/**", self.permission["edit"])

    def test_verifiers_cannot_run_checks(self) -> None:
        for name in ("verifier-anthropic.md", "internal-critic-openai.md"):
            permission = frontmatter(AGENTS / name)["permission"]
            self.assertNotIn("research_run_check", permission)
            self.assertNotIn("research_new_check", permission)

    def test_verifiers_are_bounded_read_only_auditors(self) -> None:
        path = AGENTS / "verifier-anthropic.md"
        permission = frontmatter(path)["permission"]
        self.assertEqual(permission["bash"], "deny")
        self.assertEqual(permission["webfetch"], "deny")
        self.assertEqual(permission["websearch"], "deny")
        self.assertNotIn("reproduce-result", permission["skill"])
        text = " ".join(path.read_text(encoding="utf-8").split())
        for marker in (
            "no more than twelve investigative tool calls",
            "at most three serious falsification attacks",
            "Do not write code",
            "at most 2,500 words",
            "user approved",
        ):
            self.assertIn(marker, text)

    def test_internal_critic_is_non_independent_and_separately_scoped(self) -> None:
        path = AGENTS / "internal-critic-openai.md"
        metadata = frontmatter(path)
        self.assertEqual(metadata["model"], "openai/gpt-5.6-sol")
        permission = metadata["permission"]
        self.assertEqual(
            permission["edit"], {"*": "deny", "research/critiques/**": "allow"}
        )
        self.assertNotIn("research/results/verification/**", permission["edit"])
        text = " ".join(path.read_text(encoding="utf-8").split())
        self.assertIn("not model-independent", text)
        self.assertIn("Never use `verified`", text)

    def test_opus_is_reserved_for_the_sole_verifier(self) -> None:
        opus_agents = []
        for path in AGENTS.glob("*.md"):
            if frontmatter(path).get("model") == "anthropic/claude-opus-5":
                opus_agents.append(path.name)
        self.assertEqual(opus_agents, ["verifier-anthropic.md"])
        for name in (
            "research-director.md",
            "theorist.md",
            "literature.md",
            "scientific-computation.md",
            "engineer.md",
        ):
            self.assertEqual(frontmatter(AGENTS / name)["model"], "openai/gpt-5.6-sol")


class EngineerScopeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.path = AGENTS / "engineer.md"
        self.metadata = frontmatter(self.path)
        self.permission = self.metadata["permission"]

    def test_engineer_agent_exists_as_a_subagent(self) -> None:
        self.assertTrue(self.path.is_file())
        self.assertEqual(self.metadata["mode"], "subagent")

    def test_engineer_write_scope_is_infrastructure_only(self) -> None:
        self.assertEqual(
            self.permission["edit"],
            {
                "*": "deny",
                "research/computation/**": "allow",
                "research/environment/**": "allow",
            },
        )
        for forbidden in (
            "research/checks/**",
            "research/claims/**",
            "research/STATE.md",
            "research/DECISIONS.md",
            "research/results/verification/**",
        ):
            self.assertNotIn(forbidden, self.permission["edit"])

    def test_engineer_cannot_delegate_or_run_scientific_tools(self) -> None:
        self.assertEqual(self.permission["task"], "deny")
        for tool in ("research_new_check", "research_run_check", "research_validate_state"):
            self.assertNotIn(tool, self.permission)
        self.assertEqual(
            self.permission["skill"], {"*": "deny", "research-engineering": "allow"}
        )
        self.assertEqual(self.permission["research_run_infrastructure_tests"], "allow")

    def test_engineer_is_not_a_verifier(self) -> None:
        text = " ".join(self.path.read_text(encoding="utf-8").split())
        self.assertIn("not a peer scientific role", text)
        self.assertIn("never an independent verifier", text)
        self.assertIn("Do not write `research/checks/ONNN/run.py`", text)


class DelegationDepthTests(unittest.TestCase):
    def test_exactly_one_nested_engineering_edge_is_enabled(self) -> None:
        import json

        config = json.loads((PROJECT_ROOT / "opencode.json").read_text(encoding="utf-8"))
        self.assertEqual(config["subagent_depth"], 2)
        scientific = frontmatter(AGENTS / "scientific-computation.md")["permission"]
        engineer = frontmatter(AGENTS / "engineer.md")["permission"]
        self.assertEqual(scientific["task"], {"*": "deny", "engineer": "allow"})
        self.assertEqual(engineer["task"], "deny")


class ArtifactSurfaceTests(unittest.TestCase):
    def test_commands_exist(self) -> None:
        for name in ("new-check.md", "run-check.md", "research-explore.md"):
            path = COMMANDS / name
            self.assertTrue(path.is_file(), f"missing command {name}")
            self.assertEqual(frontmatter(path)["agent"], "research-director")

    def test_computational_verification_skill_exists(self) -> None:
        path = SKILLS / "computational-verification" / "SKILL.md"
        self.assertTrue(path.is_file())
        self.assertEqual(frontmatter(path)["name"], "computational-verification")

    def test_research_engineering_skill_exists(self) -> None:
        path = SKILLS / "research-engineering" / "SKILL.md"
        self.assertTrue(path.is_file())
        self.assertEqual(frontmatter(path)["name"], "research-engineering")

    def test_numerical_experiment_skill_remains_about_experiments(self) -> None:
        text = (SKILLS / "numerical-experiment" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("research/experiments/ENNN/", text)
        self.assertIn("computational-verification", text)
        self.assertIn("not the generic machine", text)
        self.assertIn("verification mechanism", text)

    def test_tools_export_the_new_helpers(self) -> None:
        text = (PROJECT_ROOT / ".opencode" / "tools" / "research.ts").read_text(encoding="utf-8")
        for export in (
            "export const new_check",
            "export const run_check",
            "export const init_computation_plan",
            "export const new_derivations",
            "export const safe_search",
            "export const git_inspect",
            "export const run_tests",
            "export const run_experiment",
            "export const run_infrastructure_tests",
        ):
            self.assertIn(export, text)
        self.assertIn('runHelper("run_check.py"', text)
        self.assertIn('runHelper("new_check.py"', text)
        for marker in (
            "isSensitive",
            "confinedTarget",
            "SKIPPED_DIRECTORIES",
            '["status", "diff", "diff-stat", "log", "head"]',
            '["all", "configuration", "research-state", "checks"]',
            '"--no-sync"',
            'tool.schema.enum(["run", "analysis"])',
        ):
            self.assertIn(marker, text)

    def test_provenance_plugin_records_engineering_handoffs(self) -> None:
        text = (PROJECT_ROOT / ".opencode" / "plugins" / "research-provenance.js").read_text(
            encoding="utf-8"
        )
        for marker in (
            'delegatedAgent === "engineer"',
            'operation = "engineer-provisioned"',
            "delegated_agent: delegatedAgent",
            "delegatedTask.description.slice(0, 240)",
            'operation = "research-environment-write"',
            'operation = "research-infrastructure-write"',
            'operation = "theory-branch-delegated"',
            'operation = "internal-critique-delegated"',
            'operation = "internal-critique-write"',
        ):
            self.assertIn(marker, text)

    def test_derivation_template_exposes_candidate_obligations(self) -> None:
        text = (PROJECT_ROOT / "templates" / "derivation.md").read_text(encoding="utf-8")
        self.assertIn("## Candidate machine-checkable obligations", text)
        self.assertNotIn("## Symbolic/numerical checks", text)

    def test_verification_template_covers_computational_evidence(self) -> None:
        text = (PROJECT_ROOT / "templates" / "verification-report.md").read_text(encoding="utf-8")
        for section in (
            "## Computational evidence reviewed",
            "## Sufficiency of computational obligations",
            "## Missing or adversarial checks",
            "## Computational independence",
            "## Scope and decisive bridge",
            "## Reconstruction",
            "## Falsification attempts",
        ):
            self.assertIn(section, text)
        self.assertIn("user_approved: true", text)

    def test_internal_critique_template_is_explicitly_non_independent(self) -> None:
        text = (PROJECT_ROOT / "templates" / "internal-critique.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("review_kind: internal-critique", text)
        self.assertIn("independent: false", text)
        self.assertNotIn("failed verification", text)

    def test_agents_document_the_directory_boundary(self) -> None:
        text = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for path in (
            "research/COMPUTATION.md",
            "research/computation/",
            "research/environment/",
            "research/checks/",
        ):
            self.assertIn(path, text)

    def test_architecture_diagram_lists_scientific_computation(self) -> None:
        text = (PROJECT_ROOT / "docs" / "AGENT_ARCHITECTURE.md").read_text(encoding="utf-8")
        self.assertIn("|-- Scientific Computation", text)
        self.assertIn("|   `-- Engineer", text)
        self.assertIn("bounded breadth", text.lower())
        self.assertIn("provisioned implementation subagent", text)

    def test_shell_permissions_do_not_broadly_allow_interpreters_or_read_commands(self) -> None:
        forbidden = ("uv *", "python *", "python3 *", "cat *", "grep *", "rg *")
        for path in AGENTS.glob("*.md"):
            permission = frontmatter(path)["permission"]
            self.assertEqual(permission.get("grep"), "deny")
            self.assertEqual(permission.get("research_safe_search"), "allow")
            bash = permission.get("bash")
            if not isinstance(bash, dict):
                continue
            for pattern in forbidden:
                self.assertNotEqual(
                    bash.get(pattern), "allow", f"{path.name} broadly allows {pattern}"
                )

    def test_exploration_never_routes_to_opus(self) -> None:
        explore = (COMMANDS / "research-explore.md").read_text(encoding="utf-8")
        cycle = (COMMANDS / "research-cycle.md").read_text(encoding="utf-8")
        self.assertIn("Do not route any task to Opus", explore)
        self.assertIn("Never invoke Opus", cycle)

    def test_scientific_computation_retains_claim_check_ownership(self) -> None:
        text = " ".join(
            (AGENTS / "scientific-computation.md").read_text(encoding="utf-8").split()
        )
        self.assertIn("required author of the actual research-specific `research/checks/ONNN/run.py`", text)
        self.assertIn("Do not provision Engineer merely because claim-specific code", text)

    def test_no_active_research_environment_is_required_on_main(self) -> None:
        directory = PROJECT_ROOT / "research" / "environment"
        self.assertEqual(sorted(path.name for path in directory.iterdir()), ["README.md"])

    def test_no_obsolete_architectural_statements(self) -> None:
        obsolete = (
            "numerics is the only computational role",
            "all computation is an experiment",
            "symbolic software is only an ad hoc cross-check",
            "Use symbolic software only as a documented cross-check.",
            "Workers cannot launch subagents.",
            "`subagent_depth` is one",
            "one-level task delegation",
            "scientific-computation` writes experiment directories, machine-check obligations, and reusable computational infrastructure",
        )
        for path in PROJECT_ROOT.rglob("*.md"):
            if "node_modules" in path.parts or ".venv" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            for phrase in obsolete:
                self.assertNotIn(phrase, text, f"{path.relative_to(PROJECT_ROOT)} keeps: {phrase}")


if __name__ == "__main__":
    unittest.main()
