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
  const agents = new Map()

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
        if (input.agent) agents.set(input.sessionID, input.agent)
      } catch {
        // Ignore malformed optional metadata.
      }
    },
    "command.execute.before": async (input) => {
      try {
        if (!RESEARCH_COMMANDS.has(input.command)) return
        await append({
          agent: agents.get(input.sessionID) || "research-director",
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
        await append({
          agent: agents.get(input.sessionID),
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
