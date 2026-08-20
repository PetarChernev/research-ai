# Research Decisions

Record consequential choices, not routine edits. Examples include abandoning a hypothesis, changing conventions, narrowing scope, selecting a numerical method, or accepting a contested source interpretation.

## Entry format

### YYYY-MM-DD: Short decision title

- **Decision:** What changed.
- **Reason:** Why this choice has the highest expected research value.
- **Evidence:** Stable claim, derivation, experiment, literature-note, or verification links.
- **Alternatives considered:** Serious alternatives and why they were not selected.
- **Reversibility:** What new evidence would trigger reconsideration.

### 2026-08-19: Make classical `4 \leftrightarrow 5` consistency the first gate

- **Decision:** Start the broader dynamical-dimensionality program with the minimal Lorentz-covariant classical `d\in\{4,5\}` state space, variational principle, and linearized consistency problem. Treat the supplied Hopf-fermion note as a hypothesis inventory and downstream benchmark, not as established theory or a manuscript ready for polishing.
- **Reason:** Every defect, spin-statistics, quantum-gravity, gauge, and phenomenology claim depends on having a well-defined state space and evolution law. Constraint closure, hyperbolicity, and resolution independence are relatively cheap and potentially decisive failure tests.
- **Evidence:** Program dependency analysis in `research/QUESTION.md`; no evidentiary claim has yet been established.
- **Alternatives considered:** (i) immediately solve the compacton/radius toy model—deferred because it cannot test covariance or interface consistency; (ii) begin with exact Hopf/FR topology—retained as a bounded audit but it cannot establish topology of an undefined full geometric configuration space; (iii) build a discrete quantum sum first—deferred because allowed histories and continuum observables are not yet defined.
- **Reversibility:** Reorder the program if literature establishes a no-go theorem for the chosen classical route, supplies an already complete alternative framework, or shows that a discrete definition can specify state space and causal amplitudes without a continuum precursor.

### 2026-08-19: Keep intrinsic and resolution descriptions as competitors

- **Decision:** Do not assume that a quotient/differential-space description and a rank-varying coframe on a smooth five-dimensional resolution are physically equivalent. Test that equivalence, including observables and gauge redundancies.
- **Reason:** A degenerate fifth direction on a fixed manifold may retain physical data that an exact quotient removes; silently equating them would beg the central dimensional-ontology question.
- **Evidence:** Distinction and required observable `resolution independence` recorded in `research/QUESTION.md`.
- **Alternatives considered:** Declare the resolution fundamental (too close to fixed-dimensional Kaluza–Klein ontology) or declare only the quotient fundamental (currently lacks a ready variational calculus).
- **Reversibility:** Merge the descriptions only after an explicit equivalence theorem or a controlled effective equivalence in the relevant regime; select one if a discriminating calculation proves the other inconsistent.

### 2026-08-19: Use the final quotient diffeology provisionally

- **Decision:** For the next foundation calculation, use the final diffeology of the explicit quotient as the provisional intrinsic smooth structure. Do not treat either ambient-horn smooth structure as resolution-independent, and keep independent `U(1)`/`SO(1,4)` connection data explicit rather than assuming collapse gauges them away.
- **Reason:** The two flat-profile horn resolutions are homeomorphic but not diffeomorphic under their canonical comparison, while the final quotient smooth algebra and form equalizer depend only on the common quotient map. Independently retained nonzero exterior curvature survives ordinary gauge, so silently dropping it would change the state space.
- **Evidence:** C007–C009 and `research/derivations/D002.md`; procedurally separated reports `research/results/verification/C007-2026-08-19.md` through `C009-2026-08-19.md` support the restricted derivations but do not independently verify them.
- **Alternatives considered:** Use an ambient-horn differential structure (rejected provisionally because it depends on the flat profile); identify all resolutions by topology alone (too coarse if circumference/coframe data are physical); omit connections at the outset (retained as a possible coframe-only theory, but not assumed for first-order gravity).
- **Reversibility:** Reconsider if the final diffeology lacks a usable integration/Stokes or causal structure, if a physically motivated action selects one embedding profile, or if a canonical reduction proves the exterior connection sector to be regular zero-charge gauge.

### 2026-08-19: Void two wrong-branch verification reports and require branch checks before delegation

- **Decision:** Treat `research/results/verification/C008-2026-08-19-anthropic.md` and `research/results/verification/C009-2026-08-19-anthropic.md` as **void, non-evidentiary artifacts**. They are excluded from the claim ledger and must not be cited. They are superseded by `C008-2026-08-19-anthropic-r2.md` and `C009-2026-08-19-anthropic-r2.md`. Every future delegation must confirm the working branch before a subagent reads or writes research artifacts.
- **Reason:** Those two reports were produced while the worktree was checked out at the `main` baseline, where the research artifacts did not exist. As a result they assert as findings that `research/derivations/D002.md` is absent and that the claim ledger is empty, and they verified claim text supplied by the task prompt rather than by a durable artifact. Both statements are false on the research branch `reseach/hopf-solitons`. Keeping them citable would inject fabricated provenance into the record.
- **Evidence:** `git status` and the branch history show the artifacts were present and committed at `03cbb8f` on the research branch; the r2 reports confirm `D002.md` is readable and the ledger populated. The void reports' own "Findings" sections state the missing-artifact claims explicitly.
- **Alternatives considered:** (i) delete them outright, initially deferred to preserve the audit trail; (ii) silently re-run and ignore them, which would hide a provenance failure; (iii) edit their frontmatter to mark them void, which would mutate an existing report, contrary to the verification protocol.
- **Resolution (2026-08-20):** After discussion, the user confirmed the reports should be deleted rather than retained: the audit trail is already preserved in this entry and in `STATE.md`, and keeping factually false files on disk (asserting the ledger and `D002.md` were missing, when they were not) risked being mistaken for evidence despite not being ledger-linked. Both files were removed via `bash rm` (the `edit` tool denies `research/results/verification/**`; `bash` requires explicit user confirmation per command, so this executed only with direct authorization, not as a permission workaround). The genuine cross-provider verifications, `C007/C008/C009-2026-08-19-anthropic-r2.md`, produced after the branch was corrected against the real `D002.md` and ledger, remain the evidentiary record for C007–C009.
- **Reversibility:** None expected; this entry is the durable record of the incident and its resolution.

### 2026-08-20: Patch legacy verification reports for the new model-provenance schema

- **Decision:** Add the required `verifier_model` and `originating_models` frontmatter fields to the four pre-schema same-model reports (`C004-`, `C007-`, `C008-`, `C009-2026-08-19.md`), without altering any other content, outcome, or finding. Both fields were set to `openai/gpt-5.6-sol` for all four, matching their existing prose disclosure of a same-model session.
- **Reason:** `research_validate_state --strict` failed with 16 structural errors because these four reports predate the `verifier_model`/`originating_models` schema requirement introduced alongside the model-bound verifier agents. The fix is a metadata migration, not a scientific change: the reports already stated in prose that they were same-model checks.
- **Evidence:** `scripts/validate_research_state.py` now returns `valid: true` with 0 errors. The 8 remaining `--strict` warnings on these same four files (`verifier model also materially produced the claim`, `verifier shares a provider with at least one originating model`) are correct and expected, matching their `"supported but not independently verified"`/`"inconclusive"` outcomes.
- **Alternatives considered:** Rewriting these reports as fresh cross-provider verifications was rejected; that would require new independent reasoning, not a metadata patch, and the genuine cross-provider checks already exist as separate `-anthropic-r2` reports for C007–C009.
- **Reversibility:** None expected; this is a permanent schema-compliance fix executed with explicit user authorization via `bash` (the `edit` tool denies this directory).

### 2026-08-19: Shift the F0 program from bare-quotient dynamics to the enriched-interface question

- **Decision:** Stop trying to derive an action from the bare final quotient calculus. Reformulate the live F0 question as: *what is the minimal enrichment beyond the bare quotient that yields a covariant, field-space-integrable interface action, and is that enrichment physical or gauge?* The next decisive calculation is the canonical/presymplectic analysis of the `D005` edge sector, not another integration-calculus attempt.
- **Reason:** `D003` (C010–C011) shows the bare final diffeology supplies no canonical measure, no stratum weights, and no nonzero collapsed-fiber trace. `D004` (C012–C013) shows the resulting five-dimensional Palatini boundary potential pushes to zero while the four-dimensional one does not, leaving an uncancelled mismatch that no pure matching multiplier can repair without forcing `P^-_{ab}=0`. `D005` (C014–C015) shows the natural covariant repair is field-space integrable only with companion coframe/reference/`eta` variations, and that the reference-free version degenerates the induced triad. The obstruction is therefore located precisely at the enrichment data, and further bare-calculus work has low information value.
- **Evidence:** `research/derivations/D003.md`, `D004.md`, `D005.md`; claims C010–C015; `research/literature/INTEGRATION_MAP.md`, which finds no established `5 -> 3` incidence operator or collapsed-fiber pushforward theorem.
- **Alternatives considered:** (i) continue searching for an intrinsic integration functional, deprioritized because both the derivation and the literature map isolate the same missing object; (ii) accept the enriched action immediately and proceed to defects, rejected because the edge sector's charge status is exactly what decides H002 versus H003; (iii) abandon the continuum route for a discrete model, premature while a nondegenerate enriched branch exists.
- **Reversibility:** Return to the intrinsic route if a stratified-integration theorem supplying collapsed incidence is found, or if the edge sector turns out to be regular zero-charge first-class, which would make the enrichment pure gauge and revive H002.
