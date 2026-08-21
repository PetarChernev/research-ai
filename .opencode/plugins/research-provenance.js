import { appendFile, mkdir } from "node:fs/promises"
import { execFileSync } from "node:child_process"
import path from "node:path"

const RESEARCH_COMMANDS = new Set([
  "research-start",
  "research-explore",
  "research-cycle",
  "new-hypothesis",
  "new-experiment",
  "new-check",
  "run-check",
  "verify-claim",
  "research-status",
])

export const ResearchProvenance = async ({ worktree }) => {
  const root = path.resolve(worktree)
  const logPath = path.join(root, "research", "provenance.jsonl")
  const sessions = new Map()

  const rememberSession = (input) => {
    if (!input?.sessionID) return
    const current = sessions.get(input.sessionID) || {}
    const modelID = input.model?.modelID || input.model?.id
    sessions.set(input.sessionID, {
      agent: input.agent || current.agent,
      providerID: input.model?.providerID || current.providerID,
      modelID: modelID || current.modelID,
    })
  }

  const gitCommit = () => {
    try {
      return execFileSync("git", ["-C", root, "rev-parse", "HEAD"], {
        encoding: "utf8",
        stdio: ["ignore", "pipe", "ignore"],
        timeout: 1000,
        maxBuffer: 4096,
      }).trim()
    } catch {
      return null
    }
  }

  const normalizeResearchPath = (candidate) => {
    if (typeof candidate !== "string" || !candidate.trim()) return null
    const absolute = path.isAbsolute(candidate) ? candidate : path.resolve(root, candidate)
    const relative = path.relative(root, absolute).split(path.sep).join("/")
    if (relative === "research" || relative.startsWith("research/")) return relative
    return null
  }

  const patchPaths = (patchText) => {
    if (typeof patchText !== "string") return []
    const paths = []
    for (const line of patchText.split("\n")) {
      const match = line.match(/^\*\*\* (?:Add|Update|Delete) File: (.+)$/)
      const moved = line.match(/^\*\*\* Move to: (.+)$/)
      const candidate = normalizeResearchPath((match || moved)?.[1])
      if (candidate) paths.push(candidate)
    }
    return [...new Set(paths)]
  }

  const append = async (record) => {
    try {
      const clean = Object.fromEntries(
        Object.entries({
          timestamp: new Date().toISOString(),
          ...record,
          git_commit: gitCommit(),
        }).filter(([, value]) => value !== undefined && value !== null),
      )
      await mkdir(path.dirname(logPath), { recursive: true })
      await appendFile(logPath, `${JSON.stringify(clean)}\n`, "utf8")
    } catch {
      // Provenance is best effort and must never block ordinary research work.
    }
  }

  return {
    "chat.message": async (input) => {
      try {
        rememberSession(input)
      } catch {
        // Ignore malformed optional metadata.
      }
    },
    "chat.params": async (input) => {
      try {
        rememberSession(input)
      } catch {
        // Ignore malformed optional metadata.
      }
    },
    "command.execute.before": async (input) => {
      try {
        if (!RESEARCH_COMMANDS.has(input.command)) return
        const session = sessions.get(input.sessionID)
        await append({
          agent: session?.agent || "research-director",
          provider_id: session?.providerID,
          model_id: session?.modelID,
          operation: "research-command",
          command: `/${input.command}`,
        })
      } catch {
        // Hooks are deliberately fail-open.
      }
    },
    "tool.execute.after": async (input, output) => {
      try {
        let relevantPaths = []
        if (["write", "edit"].includes(input.tool)) {
          const candidate = normalizeResearchPath(input.args?.filePath)
          if (candidate) relevantPaths = [candidate]
        } else if (input.tool === "apply_patch") {
          relevantPaths = patchPaths(input.args?.patchText)
        }

        let operation = relevantPaths.length ? "research-artifact-write" : null
        if (relevantPaths.some((item) => item.startsWith("research/critiques/"))) {
          operation = "internal-critique-write"
        } else if (relevantPaths.some((item) => item.startsWith("research/environment/"))) {
          operation = "research-environment-write"
        } else if (relevantPaths.some((item) => item.startsWith("research/computation/"))) {
          operation = "research-infrastructure-write"
        }
        const command = input.tool === "bash" ? input.args?.command : null
        const experimentMatch =
          typeof command === "string"
            ? command.match(
                /(?:uv\s+run(?:\s+--locked)?\s+python|(?:\S*\/)?python(?:3(?:\.\d+)*)?)\s+(?:\S*\/)?research\/experiments\/(E\d{3})\/run\.py(?:\s|$)/,
              )
            : null
        if (experimentMatch) {
          operation = "experiment-command"
          relevantPaths = [`research/experiments/${experimentMatch[1]}`]
        }
        const checkMatch =
          typeof command === "string"
            ? command.match(
                /(?:uv\s+run(?:\s+--locked)?\s+python|(?:\S*\/)?python(?:3(?:\.\d+)*)?)\s+(?:\S*\/)?scripts\/run_check\.py\s+(O\d{3})\b/,
              )
            : null
        if (checkMatch) {
          operation = "check-command"
          relevantPaths = [`research/checks/${checkMatch[1]}`]
        }
        const delegatedTask = input.tool === "task" ? input.args : null
        const delegatedAgent = delegatedTask?.subagent_type
        if (delegatedAgent === "engineer") {
          operation = "engineer-provisioned"
        } else if (delegatedAgent === "theorist") {
          operation = "theory-branch-delegated"
          const match = delegatedTask.prompt?.match(/research\/derivations\/(D\d{3})\.md/)
          if (match) relevantPaths = [`research/derivations/${match[1]}.md`]
        } else if (delegatedAgent === "internal-critic-openai") {
          operation = "internal-critique-delegated"
          const match = delegatedTask.prompt?.match(/research\/critiques\/[A-Za-z0-9._/-]+\.md/)
          if (match) relevantPaths = [match[0]]
        }
        if (!operation) return

        const experimentID = relevantPaths
          .map((item) => item.match(/(?:^|\/)(E\d{3})(?:\/|$)/)?.[1])
          .find(Boolean)
        const obligationID = relevantPaths
          .map((item) => item.match(/(?:^|\/)(O\d{3})(?:\/|$)/)?.[1])
          .find(Boolean)
        const claimID = relevantPaths
          .map((item) => item.match(/(?:^|\/)(C\d{3})(?:[-/.]|$)/)?.[1])
          .find(Boolean)
        const delegatedObligationID =
          typeof delegatedTask?.prompt === "string" && delegatedAgent === "engineer"
            ? delegatedTask.prompt.match(/\b(O\d{3})\b/)?.[1]
            : undefined
        const session = sessions.get(input.sessionID)
        await append({
          agent: session?.agent,
          provider_id: session?.providerID,
          model_id: session?.modelID,
          tool: input.tool,
          operation,
          delegated_agent: delegatedAgent,
          task:
            typeof delegatedTask?.description === "string"
              ? delegatedTask.description.slice(0, 240)
              : undefined,
          experiment_id: experimentID,
          obligation_id: obligationID || delegatedObligationID,
          claim_id: claimID,
          relevant_paths: relevantPaths,
          success:
            input.tool === "bash" && typeof output?.metadata?.exit === "number"
              ? output.metadata.exit === 0
              : true,
        })
      } catch {
        // Never expose arguments or outputs while handling a logging failure.
      }
    },
  }
}
