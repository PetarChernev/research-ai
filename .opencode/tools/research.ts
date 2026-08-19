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

export const status = tool({
  description:
    "Read durable research artifacts and return a compact machine-readable status. Use for status reports instead of relying on chat history.",
  args: {},
  async execute(_args, context) {
    return runHelper("research_status.py", ["--json"], context)
  },
})

export const validate_state = tool({
  description:
    "Validate claim IDs, statuses, artifact references, experiment result JSON, verification guardrails, and required research fields. Use after material artifact changes.",
  args: {
    strict: tool.schema.boolean().optional().describe("Treat validation warnings as failures"),
  },
  async execute(args, context) {
    const command = ["--json"]
    if (args.strict) command.push("--strict")
    return runHelper("validate_research_state.py", command, context)
  },
})
