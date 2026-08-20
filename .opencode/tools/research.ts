import { tool } from "@opencode-ai/plugin"
import path from "node:path"

async function runHelper(
  script: string,
  args: string[],
  context: { worktree: string; directory: string; abort: AbortSignal },
) {
  const root = context.worktree || context.directory
  const uv = Bun.which("uv")
  if (!uv) {
    throw new Error("The research tools require uv. Install uv, then run `uv sync --locked` in the project root.")
  }
  const child = Bun.spawn([uv, "run", "--locked", "python", path.join(root, "scripts", script), ...args], {
    cwd: root,
    stdout: "pipe",
    stderr: "pipe",
    signal: context.abort,
  })
  const [stdout, stderr, exitCode] = await Promise.all([
    new Response(child.stdout).text(),
    new Response(child.stderr).text(),
    child.exited,
  ])
  if (exitCode !== 0) {
    const detail = (stderr || stdout || `exit code ${exitCode}`).trim().slice(0, 8000)
    throw new Error(`${script} failed: ${detail}`)
  }
  return stdout.trim()
}

export const new_hypothesis = tool({
  description:
    "Allocate the next HNNN ID and scaffold a hypothesis from the project template. Use instead of manually choosing hypothesis IDs.",
  args: {
    title: tool.schema.string().min(1).describe("Concise hypothesis title"),
    statement: tool.schema.string().optional().describe("Initial falsifiable statement"),
    question: tool.schema.string().optional().describe("Question addressed; defaults to research/QUESTION.md"),
  },
  async execute(args, context) {
    const command = ["--title", args.title, "--json"]
    if (args.statement) command.push("--statement", args.statement)
    if (args.question) command.push("--question", args.question)
    return runHelper("new_hypothesis.py", command, context)
  },
})

export const new_experiment = tool({
  description:
    "Allocate the next ENNN ID and scaffold a reproducible experiment directory. Use before implementing a new computational test.",
  args: {
    title: tool.schema.string().min(1).describe("Concise experiment title"),
    claims: tool.schema
      .array(tool.schema.string().regex(/^C\d{3}$/))
      .optional()
      .describe("Existing CNNN claim IDs under test"),
    method: tool.schema.string().optional().describe("Planned numerical or computational method"),
    question: tool.schema.string().optional().describe("Question addressed; defaults to research/QUESTION.md"),
  },
  async execute(args, context) {
    const command = ["--title", args.title, "--json"]
    for (const claim of args.claims || []) command.push("--claim", claim)
    if (args.method) command.push("--method", args.method)
    if (args.question) command.push("--question", args.question)
    return runHelper("new_experiment.py", command, context)
  },
})

export const init_computation_plan = tool({
  description:
    "Create research/COMPUTATION.md from the global method-neutral template when a research question is initialized. It records the question and leaves every methodological choice to the research director.",
  args: {
    question: tool.schema.string().optional().describe("Question addressed; defaults to research/QUESTION.md"),
    phase: tool.schema.string().optional().describe("Short description of the current methodological regime"),
    force: tool.schema
      .boolean()
      .optional()
      .describe("Replace an already-initialized plan instead of refusing (discards the recorded strategy)"),
  },
  async execute(args, context) {
    const command = ["--json"]
    if (args.question) command.push("--question", args.question)
    if (args.phase) command.push("--phase", args.phase)
    if (args.force) command.push("--force")
    return runHelper("init_computation_plan.py", command, context)
  },
})

export const new_check = tool({
  description:
    "Allocate the next ONNN ID and scaffold a claim-linked machine-check obligation (spec.yaml, run.py, README.md). Never creates result.json: an obligation with no result has not run.",
  args: {
    title: tool.schema.string().min(1).describe("Concise obligation title"),
    question: tool.schema.string().min(1).describe("Exact mathematical question the check tests"),
    acceptance_criterion: tool.schema
      .string()
      .min(1)
      .describe("Predeclared pass/fail criterion, decided before implementation"),
    claims: tool.schema
      .array(tool.schema.string().regex(/^C\d{3}$/))
      .optional()
      .describe("Existing CNNN claim IDs under test"),
    derivations: tool.schema
      .array(tool.schema.string().regex(/^D\d{3}$/))
      .optional()
      .describe("Existing DNNN derivation IDs under test"),
    check_class: tool.schema
      .enum([
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
      ])
      .optional()
      .describe("Kind of assertion under test; it does not select a library, language, or tool"),
    method: tool.schema.string().optional().describe("Method the research selected for this obligation"),
    method_rationale: tool.schema.string().optional().describe("Why that method suits this assertion"),
    independence: tool.schema
      .enum(["not-required", "recommended", "required"])
      .optional()
      .describe("Whether an independent implementation or alternate method is warranted"),
    independence_rationale: tool.schema.string().optional().describe("Why that independence level applies"),
    optional: tool.schema
      .boolean()
      .optional()
      .describe("Record the obligation as not part of the currently required verification strategy"),
  },
  async execute(args, context) {
    const command = [
      "--title",
      args.title,
      "--question",
      args.question,
      "--acceptance-criterion",
      args.acceptance_criterion,
      "--json",
    ]
    for (const claim of args.claims || []) command.push("--claim", claim)
    for (const derivation of args.derivations || []) command.push("--derivation", derivation)
    if (args.check_class) command.push("--check-class", args.check_class)
    if (args.method) command.push("--method", args.method)
    if (args.method_rationale) command.push("--method-rationale", args.method_rationale)
    if (args.independence) command.push("--independence", args.independence)
    if (args.independence_rationale) command.push("--independence-rationale", args.independence_rationale)
    if (args.optional) command.push("--optional")
    return runHelper("new_check.py", command, context)
  },
})

export const run_check = tool({
  description:
    "Execute a machine-check obligation through the deterministic wrapper. The wrapper alone derives the canonical outcome from the actual process exit status and writes research/checks/ONNN/result.json. Never write that file by hand.",
  args: {
    obligation: tool.schema.string().regex(/^O\d{3}$/).describe("Obligation ID, for example O001"),
    timeout: tool.schema.number().positive().optional().describe("Wall-clock limit in seconds"),
  },
  async execute(args, context) {
    const command = [args.obligation, "--json"]
    if (args.timeout) command.push("--timeout", String(args.timeout))
    return runHelper("run_check.py", command, context)
  },
})

export const status = tool({
  description:
    "Read durable research artifacts and return a compact machine-readable status, including computational verification obligations and blockers. Use for status reports instead of relying on chat history.",
  args: {},
  async execute(_args, context) {
    return runHelper("research_status.py", ["--json"], context)
  },
})

export const validate_state = tool({
  description:
    "Validate claim IDs, statuses, artifact references, experiment result JSON, machine-check obligation specs and results, computational-verification gates, verification guardrails, and required research fields. Use after material artifact changes.",
  args: {
    strict: tool.schema.boolean().optional().describe("Treat validation warnings as failures"),
  },
  async execute(args, context) {
    const command = ["--json"]
    if (args.strict) command.push("--strict")
    return runHelper("validate_research_state.py", command, context)
  },
})
