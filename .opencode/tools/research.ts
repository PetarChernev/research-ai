import { tool } from "@opencode-ai/plugin"
import path from "node:path"
import { readFile, readdir, realpath, stat } from "node:fs/promises"

const SKIPPED_DIRECTORIES = new Set([".git", ".venv", "node_modules", "__pycache__"])

function isSensitive(relative: string) {
  const components = relative.split(/[\\/]/)
  const basename = components.at(-1) || ""
  return (
    components.some(
      (item) => item === ".env" || (item.startsWith(".env.") && item !== ".env.example"),
    ) ||
    /\.(?:pem|key|p12|pfx)$/i.test(basename) ||
    /^credentials.*\.json$/i.test(basename)
  )
}

function globPattern(value: string) {
  let expression = ""
  for (let index = 0; index < value.length; index += 1) {
    const character = value[index]
    if (character === "*" && value[index + 1] === "*" && value[index + 2] === "/") {
      expression += "(?:.*/)?"
      index += 2
    } else if (character === "*" && value[index + 1] === "*") {
      expression += ".*"
      index += 1
    } else if (character === "*") {
      expression += "[^/]*"
    } else if (character === "?") {
      expression += "[^/]"
    } else {
      expression += character.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
    }
  }
  return new RegExp(`^${expression}$`)
}

function boundedOutput(stdout: string, stderr: string) {
  const output = [stdout.trim(), stderr.trim()].filter(Boolean).join("\n")
  return output.slice(0, 50000) || "No output."
}

async function runFixed(
  argv: string[],
  context: { worktree: string; directory: string; abort: AbortSignal },
  accepted = new Set([0]),
) {
  const root = context.worktree || context.directory
  const child = Bun.spawn(argv, {
    cwd: root,
    stdout: "pipe",
    stderr: "pipe",
    stdin: "ignore",
    signal: context.abort,
  })
  const [stdout, stderr, exitCode] = await Promise.all([
    new Response(child.stdout).text(),
    new Response(child.stderr).text(),
    child.exited,
  ])
  if (!accepted.has(exitCode)) {
    throw new Error(`${path.basename(argv[0])} failed: ${boundedOutput(stdout, stderr)}`)
  }
  return boundedOutput(stdout, stderr)
}

async function confinedTarget(root: string, candidate: string) {
  if (!candidate || path.isAbsolute(candidate) || candidate.includes("\0")) {
    throw new Error("Search paths must be nonempty repository-relative paths.")
  }
  const rootReal = await realpath(root)
  const target = path.resolve(root, candidate)
  const targetReal = await realpath(target)
  const relative = path.relative(rootReal, targetReal)
  if (relative === ".." || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) {
    throw new Error("Search path escapes the repository.")
  }
  if (isSensitive(relative)) {
    throw new Error("Search path is excluded by the sensitive-file policy.")
  }
  return targetReal
}

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
  const child = Bun.spawn([uv, "run", "--locked", "--no-sync", "python", path.join(root, "scripts", script), ...args], {
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

export const new_derivations = tool({
  description:
    "Preallocate a batch of distinct DNNN derivation artifacts before launching parallel theorists.",
  args: {
    wave: tool.schema.string().min(1).describe("Short exploration-wave label"),
    branches: tool.schema
      .array(
        tool.schema.object({
          title: tool.schema.string().min(1).describe("Branch title"),
          charter: tool.schema.string().min(1).describe("Distinct bounded branch charter"),
          target_claims: tool.schema
            .array(tool.schema.string().regex(/^C\d{3}$/))
            .optional()
            .describe("Existing claim IDs addressed by this branch"),
        }),
      )
      .min(1)
      .max(16),
    question: tool.schema.string().optional().describe("Question addressed; defaults to QUESTION.md"),
  },
  async execute(args, context) {
    const branches = args.branches.map((branch) => ({
      title: branch.title,
      charter: branch.charter,
      target_claims: branch.target_claims || [],
    }))
    const command = [
      "--wave",
      args.wave,
      "--branches-json",
      JSON.stringify(branches),
      "--json",
    ]
    if (args.question) command.push("--question", args.question)
    return runHelper("new_derivations.py", command, context)
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

export const safe_search = tool({
  description:
    "Search repository text without shell redirection or access to secret-like files. Use instead of shell grep or rg.",
  args: {
    pattern: tool.schema.string().min(1).max(1000).describe("Regular expression to search for"),
    path: tool.schema.string().min(1).optional().describe("Repository-relative file or directory; defaults to ."),
    include: tool.schema
      .string()
      .min(1)
      .max(200)
      .optional()
      .describe("Optional ripgrep include glob, for example *.md"),
  },
  async execute(args, context) {
    const root = context.worktree || context.directory
    const target = await confinedTarget(root, args.path || ".")
    if (args.include?.startsWith("!")) throw new Error("Include globs may not begin with !.")
    let expression: RegExp
    try {
      expression = new RegExp(args.pattern)
    } catch (error) {
      throw new Error(`Invalid search regular expression: ${error}`)
    }
    const include = args.include ? globPattern(args.include) : null
    const rootReal = await realpath(root)
    const files: string[] = []
    const targetStat = await stat(target)
    if (targetStat.isFile()) {
      files.push(target)
    } else {
      const pending = [target]
      while (pending.length && files.length < 5000) {
        const directory = pending.pop()!
        for (const entry of await readdir(directory, { withFileTypes: true })) {
          if (entry.isSymbolicLink() || SKIPPED_DIRECTORIES.has(entry.name)) continue
          const candidate = path.join(directory, entry.name)
          if (entry.isDirectory()) pending.push(candidate)
          else if (entry.isFile()) files.push(candidate)
          if (files.length >= 5000) break
        }
      }
    }

    const matches: string[] = []
    for (const file of files.sort()) {
      const relative = path.relative(rootReal, file).split(path.sep).join("/")
      if (isSensitive(relative)) continue
      if (include && !include.test(relative) && !include.test(path.basename(relative))) continue
      const info = await stat(file)
      if (info.size > 2_000_000) continue
      const content = await readFile(file, "utf8")
      if (content.includes("\0")) continue
      for (const [index, line] of content.split(/\r?\n/).entries()) {
        expression.lastIndex = 0
        if (expression.test(line)) {
          matches.push(`${relative}:${index + 1}: ${line.slice(0, 2000)}`)
          if (matches.length >= 200) break
        }
      }
      if (matches.length >= 200) break
    }
    return matches.join("\n") || "No matches."
  },
})

export const git_inspect = tool({
  description:
    "Run one fixed read-only Git inspection without arbitrary flags, pathspecs, hooks, helpers, or output redirection.",
  args: {
    operation: tool.schema
      .enum(["status", "diff", "diff-stat", "log", "head"])
      .describe("Inspection to perform"),
  },
  async execute(args, context) {
    const git = Bun.which("git")
    if (!git) throw new Error("research_git_inspect requires git.")
    const commands = {
      status: [git, "--no-pager", "status", "--short"],
      diff: [git, "--no-pager", "-c", "diff.external=", "diff", "--no-ext-diff", "--no-textconv"],
      "diff-stat": [
        git,
        "--no-pager",
        "-c",
        "diff.external=",
        "diff",
        "--no-ext-diff",
        "--no-textconv",
        "--stat",
      ],
      log: [git, "--no-pager", "log", "--oneline", "-10"],
      head: [git, "rev-parse", "HEAD"],
    }
    return runFixed(commands[args.operation], context)
  },
})

export const run_tests = tool({
  description:
    "Run a fixed repository test suite through the locked, pre-synchronized uv environment. No arbitrary Python arguments are accepted.",
  args: {
    suite: tool.schema
      .enum(["all", "configuration", "research-state", "checks"])
      .optional()
      .describe("Fixed test group; defaults to all"),
  },
  async execute(args, context) {
    const uv = Bun.which("uv")
    if (!uv) throw new Error("research_run_tests requires uv and a prior `uv sync --locked`.")
    const suites = {
      all: ["discover", "-s", "tests", "-t", "."],
      configuration: ["tests.test_repository_config"],
      "research-state": [
        "tests.test_baseline",
        "tests.test_research_status",
        "tests.test_claim_integration",
      ],
      checks: ["tests.test_new_check", "tests.test_run_check", "tests.test_computation_plan"],
    }
    return runFixed(
      [
        uv,
        "run",
        "--locked",
        "--no-sync",
        "python",
        "-B",
        "-m",
        "unittest",
        ...suites[args.suite || "all"],
      ],
      context,
    )
  },
})

export const run_experiment = tool({
  description:
    "Run the fixed run.py or analysis.py entrypoint for one ENNN experiment through the pre-synchronized root environment.",
  args: {
    experiment: tool.schema.string().regex(/^E\d{3}$/).describe("Experiment ID"),
    stage: tool.schema.enum(["run", "analysis"]).describe("Fixed experiment entrypoint"),
  },
  async execute(args, context) {
    const root = context.worktree || context.directory
    const relative = path.join(
      "research",
      "experiments",
      args.experiment,
      args.stage === "run" ? "run.py" : "analysis.py",
    )
    const entrypoint = await confinedTarget(root, relative)
    const uv = Bun.which("uv")
    if (!uv) throw new Error("research_run_experiment requires uv and a prior `uv sync --locked`.")
    return runFixed(
      [uv, "run", "--locked", "--no-sync", "python", "-B", entrypoint],
      context,
    )
  },
})

export const run_infrastructure_tests = tool({
  description:
    "Run fixed Python unittest discovery for one direct child of research/computation. No command or Python arguments are accepted.",
  args: {
    component: tool.schema
      .string()
      .regex(/^[A-Za-z0-9][A-Za-z0-9_.-]*$/)
      .describe("Directory name under research/computation"),
  },
  async execute(args, context) {
    const root = context.worktree || context.directory
    const component = path.join("research", "computation", args.component)
    await confinedTarget(root, component)
    const tests = path.join(component, "tests")
    await confinedTarget(root, tests)
    const uv = Bun.which("uv")
    if (!uv) {
      throw new Error("research_run_infrastructure_tests requires uv and a prior `uv sync --locked`.")
    }
    return runFixed(
      [
        uv,
        "run",
        "--locked",
        "--no-sync",
        "python",
        "-B",
        "-m",
        "unittest",
        "discover",
        "-s",
        tests,
        "-t",
        ".",
      ],
      context,
    )
  },
})
