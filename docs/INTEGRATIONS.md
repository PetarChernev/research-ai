# Optional Literature Integrations

The baseline repository defines no project MCP server and works with OpenCode's normal web tools and local artifacts. Global configuration varies by user; inspect it with `opencode debug config`. No credential is stored or required by this repository.

Any integration is a discovery or retrieval aid. Its output becomes claim evidence only after the literature agent checks the actual source, records an exact locator and regime in `research/literature/notes/`, and adds verified metadata to `bibliography.bib`.

## Semantic Scholar

Use the official [Academic Graph API](https://api.semanticscholar.org/api-docs/graph) for paper discovery, metadata, references, citations, and related works. Small public requests may work without credentials; an API key improves rate limits. Keep any key in the environment or OpenCode credential storage, never in this repository.

OpenCode's `websearch` availability depends on the configured provider or an explicitly enabled search integration. When unavailable, use `webfetch` with the official Semantic Scholar, arXiv, or Crossref endpoints and observe their rate limits; this remains provider-neutral but still sends URLs and queries to those services.

An MCP server can be added later under `mcp` in `opencode.json` after checking its maintenance status, source, requested permissions, and current command syntax. Do not select a package by name alone. The literature agent should use Semantic Scholar to find candidate and citing papers, then inspect primary text before asserting support.

## Zotero

Zotero's official Web API v3 exposes public libraries without authentication and private libraries with a user-controlled key. The desktop client provides a read API at `http://localhost:23119/api/` when enabled; read access needs no web API key. See the official [Zotero API documentation](https://www.zotero.org/support/dev/web_api/v3/basics).

If a Zotero MCP is intentionally installed later, scope it to read/search and attachment retrieval unless write access is genuinely needed. Keep local-library paths and keys out of committed config. Useful outputs are checked BibTeX entries, annotations with page locators, and local/full-text candidates. Zotero metadata alone does not establish a scientific claim.

## PaperQA2 or Local-Paper Retrieval

[PaperQA2](https://github.com/Future-House/paper-qa) can index a curated PDF/text corpus and expose the `pqa` CLI. It is deliberately not installed here because it is a substantial optional dependency and its model/embedding configuration may require credentials or local model services.

If adopted, prefer a separate locked environment and a thin OpenCode tool that invokes a fixed `pqa` command. Record the PaperQA version, settings, corpus manifest, document checksums, index identity, query, and returned page-level evidence. Store the corpus under an ignored location such as `data/papers/`; do not commit copyrighted PDFs or generated indexes. Treat retrieved passages as leads requiring source inspection.

## arXiv and DOI Metadata

The official arXiv Atom API supports fielded search and ID lookup at `https://export.arxiv.org/api/query`; follow its rate guidance and preserve versioned arXiv IDs. For DOI metadata, use the public Crossref REST endpoint `https://api.crossref.org/works/{doi}` or the relevant registration agency. Resolve the DOI and check corrections, versions, and retractions rather than trusting a single metadata record.

For papers, record at minimum title, authors, year, DOI or versioned arXiv ID, stable URL, access date, and exact evidence location. Respect licenses and access controls when retrieving full text.

## Adding an Integration Safely

1. Verify current upstream documentation and maintenance.
2. Use project-local configuration only when the integration is project-specific.
3. Reference secrets through supported environment or credential mechanisms; never write their values to files.
4. Start read-only and least-privileged.
5. Test loading with `opencode debug config` and inspect the exposed tool names.
6. Update the literature agent's permissions only for the exact tools needed.
7. Keep a manual web/API path so integration failure does not block research.
