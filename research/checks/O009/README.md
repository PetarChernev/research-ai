# O009: Static collapse background equations

Canonical machine-checkable obligation. `spec.yaml` is the declaration,
`run.py` (or the declared entrypoint) is the implementation, and `result.json`
is written **only** by the deterministic runner.

## Targets

Claims: C021

Derivations: D018

## Question tested

Under the exact C021/D018 static unwarped coframe E=(dt,dx,dy,ds,rho(s)dtheta), D004 ordered-pair Palatini conventions, source-free constant cosmological terms, the D002 smooth-flat endpoint data, flat 4D exterior, and the stated D005 fixed-seed shell substitutions, do the Cartan and coframe equations reduce uniquely to omega^43=rho' dtheta, R^34=-rho'' ds wedge dtheta, G_a=(k-Lambda_5)Xi_a/kappa_5 for a=0,1,2, G_3=G_4=-Lambda_5 Xi/kappa_5, Lambda_4=0, and hence Lambda_5=0, rho''=0 and rho identically zero when rho(0)=rho'(0)=0, while retaining rho=cs as the one-endpoint polar control and satisfying the shell table?

## What this does not test

This finite check does not test whether the D002 category is physically
admissible, any other action or background, functional trace preservation, the
broad existential claims C002/C003, hyperbolicity or stability, or independent
verification. It tests only the exact restricted C021/D018 bridge.

## Assumptions encoded in the implementation

- The Cartan equations are solved only on the invertible open core `s>0`, with
  `eta=diag(-,+,+,+,+)`, `epsilon_01234=+1`, and D004's curvature sign.
- D004's Euler forms include both orders of every antisymmetric pair and their
  exact prefactors. Both bulks are source free and cosmological terms constant.
- The exterior is flat. D002 smooth-flat extension supplies both endpoint data;
  the polar control omits `rho'(0)=0`.
- The D005 shell uses planar traces, `a0=0`, `g=u=1`, `K=0`,
  `b=kappa_4^-1`, constant coframes, and proper outer corners.
- Equality is exact canonical equality, with no floats, samples, tolerances,
  random choices, or heuristic simplification.

## Representation and trust-surface assessment

**Objects, domain, and bases.** O009 represents every antisymmetric
spin-connection one-form on `(E0,...,E4)`, torsion and curvature two-forms,
D004 coframe Euler four-forms, exterior residual three-forms, the affine profile
`rho=cs+d`, and planar shell two-forms. Coefficients are `Fraction` values and
free sparse polynomials. Coordinate and coframe bases are kept distinct.

**Primitives and equality.** The only operations are wedge canonicalization,
Levi-Civita parity, explicit finite ordered-index enumeration, exact RREF,
polynomial substitution, and differentiation of the declared connection jet.
Equality is exact sparse-map or RREF equality and is decidable in this domain.

**Cartan semantics.** The runner builds and solves the complete 50-by-50 linear
torsion system for all `omega^{AB}_C`, proves full rank, and checks all 50
residuals. The source factors `q=rho'/rho` only where `rho>0`; afterward
`q E4=rho' dtheta`, so no division enters curvature or endpoint work.

**CAS and infrastructure.** No CAS is used: a heuristic simplifier would enlarge
the trust surface for a finite canonical problem. The existing fingerprinted
`research/computation/exact_graded/` kernel is adequate; no Engineer or new
environment is needed.

**Shared risks and alternate assembly.** O009 shares D004 epsilon,
ordered-pair, orientation, and Palatini conventions and `exact_graded` with
O002/O008, so agreement is correlated. A separate component path constructs the
warped-plane Riemann component and contracts it to Ricci/scalar/Einstein
components without the Euler enumeration helper. Shell `P^-` uses separate
local permutation parity from `Q`. These cross-checks share assumptions,
arithmetic, and producer model `openai/gpt-5.6-sol`; they are not independent.

## Method

Finite exact exterior-form/Cartan assembly and exact linear-polynomial elimination, with a separately assembled direct component or warped-product cross-check and semantic mutations.

Rationale: The load-bearing bridge consists only of exact wedge signs, ordered epsilon multiplicities, a small linear torsion solve, and affine endpoint elimination. Exact canonical arithmetic is cheaper and more discriminating than numerical sampling or a general PDE solver, while an alternate component assembly attacks the main shared transcription risk.

## Acceptance criterion

Pass iff an exact canonical implementation (1) solves the open-core torsion equations and obtains the unique nonzero connection pair omega^43=+rho' dtheta, omega^34=-rho' dtheta with every torsion residual zero; (2) obtains only R^43=+rho'' ds wedge dtheta and R^34=-rho'' ds wedge dtheta; (3) independently enumerates the D004 ordered-pair Euler forms and obtains coefficients k-Lambda_5 for A=0,1,2 and -Lambda_5 for A=3,4, with the flat exterior residual forcing Lambda_4=0; (4) eliminates these exact equations to Lambda_5=0, rho''=0 and, for rho=cs+d, c=d=0 under rho(0)=rho'(0)=0, while a control imposing only rho(0)=0 retains nonzero c; (5) obtains exact zero/equality for every declared D005 shell/orbit substitution; and (6) detects predeclared mutations of the spin-connection sign, ordered-pair multiplicity or cosmological coefficient, omission of a normal/circle equation, and deletion of the rho'(0)=0 endpoint condition. Fail on any exact mismatch or ineffective mutation. Inconclusive only if a predeclared exact-domain operation is unsupported before scientific comparison; implementation exceptions are errors.

## Infrastructure used

- `research/computation/exact_graded/`
- `pyproject.toml`, `uv.lock`, `scripts/_research.py`, `scripts/run_check.py`

Infrastructure and check producer model: `openai/gpt-5.6-sol`. No new reusable
substrate was created.

## How to run

```bash
uv run --locked python scripts/run_check.py O009
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

No result recorded. The absence of `result.json` means this obligation has not
run.

## Interpretation and limitations

When canonically executed, the outcome applies only to the encoded finite exact
assertions. It cannot establish category admissibility, completeness of the
action/background search, functional trace preservation, broad C002/C003, or
independent verification. Mutation controls establish discriminating power for
the targeted defects but do not make this an independent implementation.
