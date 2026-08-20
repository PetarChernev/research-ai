import { appendFile, mkdir } from "node:fs/promises"
import { execFileSync } from "node:child_process"
import path from "node:path"

const RESEARCH_COMMANDS = new Set([
  "research-start",
  "research-cycle",
  "new-hypothesis",
  "new-experiment",
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
        const command = input.tool === "bash" ? input.args?.command : null
        const experimentMatch =
          typeof command === "string"
            ? command.match(/research\/experiments\/(E\d{3})(?:\/|\b)/)
            : null
        if (experimentMatch) {
          operation = "experiment-command"
          relevantPaths = [`research/experiments/${experimentMatch[1]}`]
        }
        if (!operation) return

        const experimentID = relevantPaths
          .map((item) => item.match(/(?:^|\/)(E\d{3})(?:\/|$)/)?.[1])
          .find(Boolean)
        const claimID = relevantPaths
          .map((item) => item.match(/(?:^|\/)(C\d{3})(?:[-/.]|$)/)?.[1])
          .find(Boolean)
        const session = sessions.get(input.sessionID)
        await append({
          agent: session?.agent,
          provider_id: session?.providerID,
          model_id: session?.modelID,
          tool: input.tool,
          operation,
          experiment_id: experimentID,
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
