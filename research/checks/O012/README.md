# O012: Finite-slope mixed interface variation

Canonical machine-checkable obligation for C025/D022. `result.json` is written
only by the deterministic runner.

## Question and boundary

O012 tests whether the D004 ordered five-index Palatini potential on the D022
planar finite-slope trace has zero collapsed-`E4` channel and exact free mixed
coefficient

`p_! Theta_(5,chi43) = tau kappa5_inv delta_chi43 oSigma`, `tau=2pi`,

while the unchanged D005 basic persistent action has no `chi43` incidence and
all displayed fixed-seed shell substitutions remain exact.

It does **not** test whether the finite-regularity class is physically preferred,
define a nonlinear BV action, establish quotient descent of the mixed
connection, classify possible mixed counterterms, test moving interfaces, or
decide C002/C003, constraints, hyperbolicity, or global gauge questions.

## Representation and trust-surface assessment

1. **Domain:** a finite free exterior algebra on
   `du0<du1<du2<dtheta`, its three-dimensional base algebra, finite internal
   indices `0,...,4`, and a free polynomial ring over exact rationals.
2. **Operations:** exact arithmetic, wedge canonicalization, antisymmetric
   component lookup, permutation parity, complete ordered-index enumeration,
   fiber-leg extraction, and finite D005 substitutions.
3. **Canonical equality:** polynomial monomials and wedge words are sorted and
   collected into sparse tuples. Equality and zero are decidable tuple equality.
   `tau` is formal and interpreted exactly as `2pi`.
4. **Conventions:** `epsilon01234=epsilon0123=+1`, both antisymmetric pair
   orders, `omega43=-omega34`, `oSigma=du0 du1 du2`, fiber forms right,
   core-minus-exterior incidence, positive ordinary circle, `E4|Sigma=0`, the
   free finite `delta omega43=delta_chi43 dtheta`, and frozen D005 incidence.
5. **CAS trust:** no CAS, simplifier, numerical library, sampling, or tolerance
   is used. Such machinery would add trust without helping this finite algebra.
6. **Infrastructure:** `exact_graded` could represent these forms, but O012
   needs only a few claim-local primitives. A short self-contained exact path is
   smaller; new reusable infrastructure or Engineer work would add risk.
7. **Alternate checks:** the primary coefficient comes from all ordered
   five-index terms. A separate hand path combines two connection orders, six
   coframe permutations, `epsilon3012=-1`, and moving `dtheta` past three
   coframes. Exact planar `Q=Pminus` components and four fresh-process mutations
   are correlated checks, not independent verification.

## Frozen D005 incidence and shell

The candidate has `e=(du0,du1,du2,0)`, `g=u=1`, `a0=0`,
`a=bar_a=barvarpi=omega_plus=varpi=0`, `Delta e=Delta omega=K=0`,
`b=kappa4_inv`, `lambda=-Q`, `mu=0`, and constant coframes (`dQ=0`).
The explicitly represented D005 fields are `e_plus`, `omega_plus_ab`,
`e_minus`, `varpi_ab`, `g`, `lambda_ab`, `mu_a`, and seed-orbit `u` data.
Their variation incidence includes both connections, both coframes, both
multipliers, `g`, and the seed-orbit tangent; it contains neither `omega43` nor
`chi43`. Proper outer-corner support is assumed.

The reproduced rows are `Delta e=Delta omega=0`, `Q+lambda=0`,
`Pminus+lambda=0`, `Q=Pminus`, `H(K)+mu=0`, `mu=0`,
`D_bar_a Q+D_barvarpi lambda+mu diamond e=dQ-dQ=0`, and fixed-seed
`D_bar_a Q=dQ=0`.

## Acceptance and mutations

The exact criterion is frozen in `spec.yaml`. The baseline executes four fresh
child processes. Reversing the core sign, omitting one antisymmetric order,
replacing the finite tangent by the smooth-flat zero trace, or inserting a
fictitious D005 mixed cancellation must each return exit code `1`.

## Infrastructure and execution

No reusable research kernel is imported. The wrapper fingerprints
`pyproject.toml`, `uv.lock`, `scripts/run_check.py`, and `scripts/_research.py`.

```bash
uv run --locked python scripts/run_check.py O012
```

Exit protocol: `0` passed, `1` failed, `2` inconclusive; any other exit is an
error. Never write or edit `result.json` manually.

## Interpretation

A pass is exact machine evidence for the encoded coefficient, frozen D005
incidence, and shell substitutions. It remains correlated with D004/D005/D022
and the same producer model; it is not independent verification.

Producer: `openai/gpt-5.6-sol`.
