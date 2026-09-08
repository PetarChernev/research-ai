# O014: Reduction-field polarization bridge

Canonical machine-checkable obligation. `spec.yaml` is the declaration,
`run.py` (or the declared entrypoint) is the implementation, and `result.json`
is written **only** by the deterministic runner.

## Targets

Claims: C027

Derivations: D024

## Question tested

Under the exact C027/D024 fixed-interface, ordered-pair, ordinary-circle assumptions, does the unit spacelike reduction field V determine Omega_V^{AB}=omega^{AB}+V^A(D_omega V)^B-(D_omega V)^A V^B under the two minimality conditions; does the dependent primitive B_V=-integral_Y(omega-Omega_V)^{AB} wedge P_AB have the complete omega/E/V variation and graded Noether identity stated in D024; does D004 plus B_V cancel exactly the coset connection momentum while retaining the stabilizer projection; and on the basic rank-three polar trace does it cancel the 43 row but leave the free-coframe residual that forces c=0, with transverse V residual and polar corner pullback zero?

## What this does not test

It does not establish tangent admissibility, global or large-gauge holonomy, a
total mixed moment map, an observable algebra, action-class completeness,
functional preservation, Hamiltonian closure, hyperbolicity, C002/C003, or
independent verification. Moving interfaces, nonbasic fields, sources, and
alternative `V,K,R` terms are also omitted.

## Assumptions encoded in the implementation

The executable uses `eta=diag(-,+,+,+,+)`, `epsilon01234=+1`, a spacelike unit
`V`, ordered antisymmetric-pair sums, positive D004 core incidence,
`oY=oSigma wedge dtheta`, fiber forms right, and formal ordinary period
`tau=2pi`. `E`, `omega`, `V`, and the unit multiplier are independent before
variation. Both defining conditions on `Omega_V` are imposed. Polar data are
those stated in the specification. Frozen D005 chain-rule terms are assumed
zero only on the complete imported D005 shell.

## Representation and trust-surface assessment

1. **Mathematical domain:** finite tensors in `R^(1,4)`, ordered antisymmetric
   bivectors, finite spacetime exterior forms, and one field-space variation of
   the polynomial boundary primitive. Coefficients are exact
   `fractions.Fraction` values.
2. **Operations needed:** epsilon momentum construction, wedge multiplication,
   graph-based Leibniz variation, `delta K=D(delta V)+delta omega V`, graded
   covariant differentiation, one explicit integration by parts, coefficient
   extraction, projector contraction, and rational matrix rank.
3. **Exact/canonical representation:** internal indices have order
   `0<1<2<3<4`; graded atoms are sorted with Koszul signs and equal monomials
   are collected. The concrete polar basis is `x0<x1<x2<dtheta`. No numerical
   approximation is present.
4. **Equality:** equality is decidable by exact equality of canonical sparse
   coefficient tuples. Projector and uniqueness statements use deterministic
   rational row reduction.
5. **Assumptions/conventions:** `eta=diag(-,+,+,+,+)`,
   `epsilon01234=+1`, both antisymmetric orders, `V^2=1`, positive core
   incidence, fiber forms right, and ordinary circle period are explicit.
   Frozen D005 chain-rule rows are set aside only after its complete shell.
6. **CAS trust:** no CAS is used. A CAS would add simplifier, assumption, and
   canonicalization behavior to the trusted surface without helping this small
   decidable algebra.
7. **Kernel choice:** the claim-local `Expr`/`Poly` kernel is intentionally
   small and auditable. It materially exposes the expression graph, graded
   signs, and IBP rule that a target-value script could hide.
8. **Existing substrate:** Python integer arithmetic and `Fraction` are
   adequate. No dependency, Engineer work, reusable kernel, or environment
   change is needed.
9. **Custom-infrastructure risk:** no reusable infrastructure is introduced.
   Extending O013 would instead import the scientifically wrong independent-
   reference variation semantics.
10. **Validation paths:** D024 target rows are encoded separately from the
    graph differentiator; D004 and `hhP` matrices are assembled independently;
    `h^A{}_B` is exposed and `h_A{}^B=eta_AC h^C{}_D eta^{DB}` is constructed
    explicitly before projecting lower-index momentum; a concrete exact `c=2`
    polar support derives `P43/P34`, action, coframe and `V` rows; and six
    fresh-process upstream mutations must fail. These paths share conventions
    and producer provenance, so they are correlated controls, not independent
    verification.

### Boosted metric-lowering regression

The generic projector test uses the exact unit-spacelike representative
`V=(3/4,0,0,0,5/4)` and compatible `K=(5,1,2,3,3)`, for which `V.K=0`.
For lower-index `P_ab` paired with upper `delta omega^{ij}`, the independently
assembled target is
`P_parallel_ij=h_i{}^a h_j{}^b P_ab`. Its ordered `01` row is exactly
`(25/8) P01-(15/8) P14`. The historical unlowered assembly instead gives the
wrong plus sign and is required to differ. The former purely spatial
representative is retained as a masking control: both assemblies coincide
there, documenting why it could not detect this Lorentzian index error.

## Method

A claim-local exact rational exterior/index calculation with a generic projector path, an independently assembled adapted-polar coefficient path, explicit graded field-space variation, and fresh-process semantic mutations; no floating point, sampling, heuristic simplification, or general-purpose CAS.

Rationale: The decisive bridge is finite polynomial tensor algebra, wedge ordering, ordered-pair multiplicity, a small linear uniqueness statement, and one exact polar specialization. Canonical sparse forms and rational matrices make equality decidable while keeping the trust surface smaller than a general CAS or functional/PDE stack. Generic and adapted-gauge paths attack different errors.

## Acceptance criterion

The exact criterion is frozen in `spec.yaml`. Six fresh-process mutations must
each exit `1`. They act upstream: omit the `delta omega V` part of `delta K`;
delete the `K P` term generated by the IBP product rule; reverse the IBP
boundary convention; replace the dependent primitive graph by a genuinely
independent `Omega` graph (which cancels every connection row); remove one
ordered polar momentum before contraction; or use the all-plus graded ordering
when the Euler rows are inserted into the Noether polynomial. Downstream D024
expectations are unchanged.

Declare thresholds, tolerances, precision, sample sizes, or rigor level before
running. Do not adjust the criterion after seeing output; supersede the
obligation instead and say why.

## Infrastructure used

No reusable scientific kernel is imported. The wrapper fingerprints
`pyproject.toml`, `uv.lock`, `scripts/run_check.py`, and
`scripts/_research.py`. Producer and infrastructure provenance:
`openai/gpt-5.6-sol`.

## How to run

```bash
uv run --locked python scripts/run_check.py O014
```

The runner determines the canonical outcome from actual process execution:

```text
exit 0 -> passed
exit 1 -> failed
exit 2 -> inconclusive
anything else, timeout, or a non-executable entrypoint -> error
```

Never write or edit `result.json` by hand.

## Result

The deterministic wrapper recorded the second repaired implementation as
`passed` with `46/46` exact assertions and all six fresh-process semantic
mutations detected with exit `1`. The result fingerprints implementation
SHA-256 `02a6bb68996337f1eda08e980d2c2686729e14730885c09bd2b30ac6c9a94f53`
and unchanged spec SHA-256
`2569a7fb59e700dc116c007a6055a49e372d0c41174f8005c547416b0f80d59f`.

### Direct development smoke (noncanonical)

Before the canonical run, direct stdlib execution of `run.py` exited `0` with all
`46/46` exact assertions satisfied, including the boosted `01` witness and the
negative old-unlowered law. The parent process launched each semantic
mutation in a fresh child process; all six exited `1`: `omit-delta-omega-V`,
`delete-second-F`, `reverse-corner`, `independent-Omega`,
`omit-polar-order`, and `all-plus-noether`. This did not invoke the canonical
wrapper and did not update `result.json`.

The durable repair history is preserved in
`research/critiques/C027-2026-08-23-openai-01.md` through `-03.md`: the first
report rejected target-shaped/self-comparing variation rows, the second exposed
Lorentzian index lowering hidden by a purely spatial test vector, and the third
found no blocking issue after the expression-graph and boosted-frame repairs.

## Interpretation and limitations

A pass is correlated exact machine evidence only for the finite C027/D024
algebra under encoded assumptions. It is not independent verification and does
not cross the interpretation boundaries above.
