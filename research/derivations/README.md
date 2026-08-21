# Derivations

Substantial derivations use stable IDs `D001`, `D002`, and so on. The research director preallocates paths with `research_new_derivations` before launching parallel theorists, preventing workers from racing for the same ID. Keep the branch charter, notation, assumptions, exact steps, approximations, validity conditions, dimensional checks, and limiting cases in the artifact.

Sequential derivations created before this lifecycle use
`exploration_wave: null`; do not retroactively group them into a wave.

Allowed statuses are `draft`, `complete`, `checked`, and `superseded`. `checked` means the recorded checks were performed; it does not independently verify the target claim. Link derivation IDs from `research/claims/ledger.yaml`.
