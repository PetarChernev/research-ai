# O006: Honest C016 shell pullback

Canonical machine-checkable obligation. `spec.yaml` is the declaration,
`run.py` (or the declared entrypoint) is the implementation, and `result.json`
is written **only** by the deterministic runner.

## Targets

Claims: C016

Derivations: D006

## Question tested

On the D006 planar rank-three branch, if the Stueckelberg shell is imposed by substituting lambda=-Q(e) before field-space differentiation, does the explicitly assembled 20-dimensional presymplectic matrix on independent tangent coordinates (chi_v, xi, delta e) include the required xi-delta e cross block yet have exact rank 10 and nullity 10, while the fixed-reference pullback at Pi=0, delta Pi=0 is zero and direct contraction gives the shell minus-frame moment map +Ad_(g^-1)Q with a nonzero +b/2 planar witness?

## What this does not test

This obligation does not include the bulk symplectic form, total Lorentz Gauss
generators, secondary constraints, global/topological modes, or a corner
polarization.  It therefore does not decide whether the rank-ten finite shell
block is physical, second class, or removed by first-class gauge.  It also does
not rederive D005's action or D006's imported algebraic shell.  A pass supports
only the stated pointwise planar finite representation.

## Assumptions encoded in the implementation

The implementation encodes `epsilon_0123=+1`, `eta=diag(-,+,+,+)`, Lorentz
pairs `(01,02,03,12,13,23)`, `dx1<dx2`, the cut coframe
`e^0=e^3=0`, `e^1=dx1`, `e^2=dx2`, and `Omega=delta Theta` with right
Maurer--Cartan variables.  The nonzero scale is represented by `b=1`; ranks are
scale independent and the witness restores `b/2`.

The Lorentz pairing is `G=diag(eta_aa eta_bb)`.  For one potential term
`<p(e),delta h h^-1>`, field-space differentiation is represented by
`[[A_p,-G dp],[(G dp)^T,0]]`, with
`(A_p)_IJ=<p,[T_I,T_J]>`.  The B shell is imposed first:
`lambda=-Q(e)`, hence `Theta_B|shell=<Q(e),chi_v-xi>` on independent
coordinates `(chi_v[6],xi[6],delta e[8])`.  In particular, `delta lambda` is
not independent.  For A, `Pi=0` and `delta Pi=dQ+delta lambda=0` are imposed by
`delta lambda=-dQ`, not by declaring the answer to be a zero matrix.

The shell minus-frame vector has `chi_v=0` and
`xi=-Ad_g(alpha_-)`.  All coefficients are `Fraction` values.  No float,
tolerance, random sample, CAS, or heuristic simplifier occurs.

## Method

Exact rational assembly of the pulled-back field-space two-form directly from the shell potential, with explicit cross blocks, null-vector certificates, gauge-vector contraction, and mutation controls.

Rationale: The verifier identified a finite representation defect in O005. The corrected assertion is a small decidable matrix problem; direct construction from the pulled-back potential is cheaper and more discriminating than new infrastructure or a general CAS.

## Representation and trust-surface assessment

1. **Domain.**  The represented objects are the rational Lorentz algebra and
   pairing, the two-generator cut exterior algebra, `dQ: Q^8 -> Q^6`, and an
   alternating form on `Q^20`.
2. **Operations.**  Only epsilon parity, wedge/coefficient extraction, Lorentz
   brackets and pairing, exact block insertion, transpose, entrywise equality,
   rank/nullspace, matvec, and one rational adjoint calculation are needed.
3. **Exactness.**  Every coefficient lies in `Q`; exterior and coordinate bases
   are finite and ordered.  No approximation or branch choice occurs.
4. **Equality.**  Sparse exterior maps and rational matrices have canonical
   entries, so equality is decidable entrywise.  Deterministic RREF decides rank
   and independence.
5. **Conventions.**  Orientation, signature, bracket, pairing, basis orders,
   Maurer--Cartan/Omega signs, shell-before-differentiation, and gauge-vector
   signs are explicit in the spec and runner.
6. **CAS surface.**  A CAS would add parsing, assumptions, simplification, and
   matrix algorithms to the trusted surface.  None is used or needed.
7. **Small kernel.**  A new reusable presymplectic kernel is not justified.  A
   short claim-specific implementation of the universal first-order term is
   smaller and more auditable.
8. **Existing substrate.**  `Fraction` and the frozen `exact_graded` exterior,
   epsilon, and rational-matrix primitives exactly cover the required domain.
9. **Infrastructure risk.**  New custom infrastructure or Engineer work would
   add risk and producer provenance without supplying a missing operation.
10. **Cross-checks.**  The implementation checks explicit `Q,dQ` entries,
    antisymmetry, ten named null certificates independently of the RREF
    nullspace, equal-rank entrywise disagreement with O005's shortcut, direct
    gauge contraction against a separately built adjoint inverse, and four
    process-local semantic mutations.

The trusted reusable surface is Python `Fraction`, `ExteriorAlgebra`,
`levi_civita_sign`, `RationalMatrix`, and the deterministic wrapper.  The
claim-specific trusted surface is the declared Lorentz bracket/pairing,
potential-term insertion, rational adjoint, and exact assertions.  This remains
correlated with O005 and is not an independent scientific verification.

## Acceptance criterion

Pass iff all exact requirements in `spec.yaml` hold: explicit `Q,dQ`; honest
20x20 shell differentiation with nonzero `xi-delta e`; rank/nullity 10/10 and
ten independent null certificates; entrywise inequality from the equal-rank
O005 shortcut; derived fixed-reference zero pullback; direct
`+Ad_(g^-1)Q` contraction and `+b/2` witness; and rejection of the four named
process-local mutations.  Any mismatch fails.  Only a non-rank-three declared
triad or degenerate represented pairing is inconclusive; exceptions are errors.

## Infrastructure used

The declared paths are `research/computation/exact_graded`, `pyproject.toml`,
`uv.lock`, `scripts/_research.py`, and `scripts/run_check.py`.  The relevant
frozen contract is `research/COMPUTATION.md` Domain E and the exact-kernel
contract.  O006 uses only the public exterior/epsilon/rational-matrix API and
adds no reusable code or dependency.  No Engineer was provisioned.

Producer model: `openai/gpt-5.6-sol`.  The existing infrastructure producer
model recorded for this use is also `openai/gpt-5.6-sol`.

## How to run

```bash
uv run --locked python scripts/run_check.py O006
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

Canonical outcome: `passed` (exit `0`), recorded once at
`research/checks/O006/result.json` on 2026-08-21.  All 36 exact assertions
passed.  The runner also recorded the implementation/spec hashes, environment,
declared infrastructure fingerprints, and stdout/stderr logs.

## Interpretation and limitations

The canonical result records whether the finite exact assertion passed.  Even a
pass does not prove smooth/global statements, rederive the upstream shell, or
classify the rank-ten block as gauge or physical.  Exact RREF is decisive for
the encoded rational matrix but remains only as faithful as the declared basis,
pairing, signs, and shell map.  The model-separated verifier's hand
reconstruction is an alternate scientific path; this implementation is a
machine-check repair, not new independence.
