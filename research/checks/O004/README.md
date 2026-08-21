# O004: D005 reference branches and rank table

Exact claim-linked obligation for the finite algebraic assertions in the
reference branches of `D004`--`D005`. `spec.yaml` preserves the predeclared
criterion, `run.py` decides it, and only the deterministic wrapper may create
`result.json`.

## Targets

Claims: C013, C015

Derivations: D004, D005

## Question tested

After dressing exterior quantities into the core frame and exactly differentiating the D005 basic planar connection-sector action, do the reference-free, distinct-fixed-reference, and distinct-freely-varied-reference treatments respectively imply Pminus=0, Q=Pminus with b=kappa4_inv on a rank-three triad, and Q=0; and does the companion map K to H(K) have exact rank 12, nullity 6, with a nonzero-curvature element in its kernel?

## What this does not test

O004 does not classify boundary actions beyond the three displayed completion
families, establish the existence or global covariance of the bundle
isomorphism `g`, decide whether a fixed reference is gauge or physical, analyze
the Stueckelberg orbit equation or corner charge, or prove compatibility with a
bulk solution. It does not test moving interfaces, nonbasic circle modes, mixed
`SO(1,4)` components, constraint closure, hyperbolicity, positivity, quantum
effects, or the future `D006` canonical problem. It also does not independently
verify C013 or C015; a passing finite computation is evidence only for the
encoded equations and rank statements.

## Assumptions encoded in the implementation

- The interface is fixed and fields are in the basic horizontal persistent
  sector. Exterior quantities have already been dressed into the core frame;
  local existence of `g` is assumed.
- The boundary sign from `D004` is core minus exterior. For one independent
  Lorentz/form component the connection-sector action is represented exactly by

  ```text
  L = Q*(omega-a) + lambda*(omega-varpi) - Pminus*varpi.
  ```

- **Reference-free** means substitute `a=varpi` in `L` before taking a field
  derivative, so `delta a=delta varpi`. **Fixed reference** means `a` is a
  distinct geometrically transforming datum with `delta a=0`. **Freely varied
  reference** means the distinct `delta a` is independent. Differentiating the
  independent action first and identifying the symbols afterward is not the
  reference-free variational problem.
- `epsilon_0123=+1`; Lorentz pairs are canonicalized with `a<b`, while the
  action sums both ordered pair values. The planar frame is
  `(e0,e1,e2,e3)=(du0,du1,du2,0)` on the ordered basis
  `du0<du1<du2`, with internal normal `n=3`.
- Ordinary positively oriented circle integration is used. `tau` is the exact
  formal period `+2pi`; `b=tau*gamma` and
  `gamma=ell_star*kappa5_inv` are explicit sequential substitutions.
- The coefficient ring is a polynomial integral domain over the rationals.
  `kappa4_inv`, `kappa5_inv`, and the desired-branch `b` are nonzero. Pointwise
  coframe rank is interpreted over the fraction field.
- For the curvature witness the reference is flat, the planar coframe is
  closed, and `K` has constant coefficients. Thus the represented curvature is
  exactly `K^a_c wedge K^cb` with internal metric `diag(-,+,+,+)`.
- There are no floats, tolerances, random samples, inverse coframes, implicit
  metric operations, or CAS transformations.

## Method

The primary path uses the existing `exact_graded` public API for canonical
polynomial differentiation, exact exterior products and epsilon signs, and
rational matrix rank/nullspace. It constructs all index sums rather than
assuming a hidden Einstein convention.

Two alternate conclusion-critical paths are included as required by Domain D:

1. a direct exact coefficient-balance table reconstructs each branch gradient
   from the `B_a`, multiplier, and exterior Palatini contributions without
   calling the shared polynomial differentiation routine;
2. an adapted signed `M/S` decomposition reconstructs every entry of `H` and
   proves the kernel count without using the shared row-reduction result.

For the latter, the 18 domain coordinates are ordered by

```text
(01,02,03,12,13,23) tensor (du0,du1,du2),
```

and the 12 codomain coordinates by

```text
c=(0,1,2,3) tensor (du0^du1,du0^du2,du1^du2).
```

Writing `K^(3i)=M^i_j e^j` and
`(K12,-K02,K01)^i=S^i_j e^j`, the exact signed output obeys

```text
(H_i[12], -H_i[02], H_i[01])^m
    = M^m_i - tr(M)*delta^m_i,
H_3 = (S10-S01, S20-S02, S21-S12).
```

The trace identity gives `tr(C)=-2 tr(M)` and the explicit inverse
`M=C-tr(C)I/2`, so the mixed kernel is zero. The tangential kernel is exactly a
symmetric `3x3` `S`, with six components. This independently yields rank 12
and nullity 6.

Rationale: The core distinction is whether a=varpi is substituted before variation or a remains an independent fixed/dynamical datum. Exact polynomial gradients and rational linear algebra expose that distinction and the claimed rank without random sampling.

## Scientific reconstruction and validation

The branch gradients reconstructed from `D005` equations (22), (24), and (30)
are

| branch | `dL/domega` | `dL/dvarpi` | `dL/da` | eliminant |
|---|---|---|---|---|
| `a=varpi` before variation | `Q+lambda` | `-(Q+lambda)-Pminus` | tied to `varpi` | `Pminus=0` |
| distinct fixed `a` | `Q+lambda` | `-lambda-Pminus` | absent | `Q=Pminus` |
| distinct free `a` | `Q+lambda` | `-lambda-Pminus` | `-Q` | `Q=0` |

For the planar triad, explicit ordered `c,d` summation gives

```text
(1/4) epsilon_03cd e^c wedge e^d = +(1/2) e1 wedge e2,
(1/4) epsilon_13cd e^c wedge e^d = -(1/2) e0 wedge e2,
(1/4) epsilon_23cd e^c wedge e^d = +(1/2) e0 wedge e1.
```

Thus `Q-Pminus` is exactly `(b-kappa4_inv)` times a nonzero base form,
and the rank-three branch requires `b=kappa4_inv`. Sequential substitution
then gives
`tau*ell_star*kappa5_inv=kappa4_inv`.

For four coframe one-forms on a three-dimensional interface, every coefficient
of `e^c wedge e^d` is a `2x2` coframe minor. O004 checks all 18 universal
identities, checks that the six-dimensional internal epsilon map is invertible,
and checks all 144 pivot identities

```text
x[p,q]*x[i,j] - x[i,q]*x[p,j] = a signed 2x2 minor.
```

If all entries vanish the rank is zero; otherwise a nonzero pivot and these
identities factor the matrix over the fraction field as rank one. Conversely,
the universal rank-one parametrization `x[i,j]=u[i]v[j]` has every minor zero.
This is the encoded equivalence
`Pminus=0 <=> all 2x2 minors=0 <=> rank<=1`, conditional on nonzero
`kappa4_inv` and the integral-domain assumption.

The certified nonflat kernel witness is

```text
K01=du2,  K02=-du1,  K12=du0,  K03=K13=K23=0.
```

It is the `S=I` solution, and with flat reference and constant coefficients the
exact curvature component is `R01=-du0 wedge du1`, so `H(K)=0` does not imply
flatness.

## Acceptance criterion

Pass iff exact differentiation and elimination give reference-free gradients Q+lambda and -(Q+lambda)-Pminus and hence Pminus=0; fixed-reference gradients Q+lambda and -lambda-Pminus and hence Q=Pminus; freely varied reference gradient -Q and hence Q=0; the planar rank-three epsilon map gives the exact factor b-kappa4_inv and tau*ell_star*kappa5_inv=kappa4_inv; Pminus=0 is equivalent to vanishing 2x2 coframe minors and rank at most one; the rational H matrix has rank 12 and nullity 6; a certified nonzero kernel vector has a nonzero exact K wedge K curvature component; and all reference, sign, factor, rank, and mutation controls are detected. Fail on any exact mismatch. Inconclusive only if the triad is not exactly rank three, the coefficient domain has zero divisors, or the requested reference case lies outside the three declared branches; implementation exceptions are errors.

There are no thresholds, tolerances, precision choices, or sample sizes. The
criterion above is the allocation-time mathematical criterion and has not been
weakened or changed after implementation.

## Controls

Positive controls recover all three branch tables, the three nonzero planar
epsilon signs, the coupling substitution, all universal minors, exact H rank
and nullity by both methods, six symmetric-`S` kernel generators, and the
nonflat curvature witness.

Negative and mutation controls verify that the check rejects:

- identifying `a` only after independent variation;
- the wrong exterior Palatini sign;
- omission of the second ordered antisymmetric term (a factor-of-two error);
- a rational rank-two coframe;
- a reversed H sign, despite unchanged rank and kernel;
- a zeroed H row (rank 11);
- broken off-diagonal `S` symmetry; and
- a nonzero but flat one-generator H-kernel element as the required nonflat
  witness.

The process-local mutation `O004_INTENTIONAL_MUTATION=exterior-sign` alters the
encoded exterior sign only for that process. It must return exit 1 and does not
write a canonical result.

## Infrastructure used

The specification fingerprints the entire
`research/computation/exact_graded/` directory, including implementation,
tests, documentation, and extant package contents, plus root `pyproject.toml`
and `uv.lock` and the materially used orchestration paths
`scripts/run_check.py` and `scripts/_research.py`. The kernel provides
`Polynomial`, `ExteriorAlgebra`, `levi_civita_sign`, and `RationalMatrix`; it
is methodology, not evidence. Its README records 45 passing infrastructure
contract tests. O004 does not modify or rerun that reusable substrate and does
not delegate to Engineer.

The trusted surface is Python/Fraction, those four public exact primitives,
the explicit claim-specific index/basis construction, and the deterministic
wrapper. A general-purpose CAS is not trusted or used. The direct branch table
and M/S analysis use materially different helper paths from polynomial
differentiation and RREF, but share the same transcription of the D004-D005
conventions and therefore are not fully independent scientific verification.

## How to run

Run the sensitivity test directly first:

```bash
O004_INTENTIONAL_MUTATION=exterior-sign \
  uv run --locked python research/checks/O004/run.py
```

Expected direct outcome: exit 1. Then create or replace the canonical result
only with:

```bash
uv run --locked python scripts/run_check.py O004
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

Sensitivity was run first with the documented process-local mutation. It exited
`1` as required: 60 assertions were evaluated, 52 passed controls remained
intact, and the eight branch-gradient/elimination assertions affected by the
reversed exterior sign failed. This direct run did not create `result.json`.

Canonical execution then used only the deterministic wrapper:

```text
uv run --locked python scripts/run_check.py O004
```

`research/checks/O004/result.json` records **passed**, process exit `0`, at
`2026-08-20T14:08:32Z`. All 60 exact assertions passed and none failed. The
primary and analytic methods both recorded H rank 12 and nullity 6. The
aggregate infrastructure fingerprint is
`0b4aeb783458e144f6b86641ad631d0cb62dcc12398b414a552434f00d211b97`;
the complete `exact_graded` directory fingerprint within it is
`197024e3f37dff868c931141ce25949e26e2249bd4850d0213ff06e81449268b`.
The canonical run used CPython 3.12.12, recorded a dirty worktree, and produced
no auxiliary artifacts. `result.json` and `logs/` are authoritative.

## Interpretation and limitations

Exact success would establish only the finite equations, coefficient factors,
determinantal implication, H rank/kernel, and one nonflat witness under the
assumptions above. The scalar branch action relies on componentwise linearity
after dressing; the planar basis does not represent arbitrary global bundles or
smooth fields. The minor argument is pointwise over a fraction field. The
curvature witness assumes a flat reference and closed constant planar coframe.
Exact canonical equality is only as faithful as the declared signs, basis, and
ring relations, which remain scientific inputs for independent review.

Producer for the O004 specification, documentation, scientific encoding, and
claim-specific runner: `openai/gpt-5.6-sol`. The materially used
`exact_graded` infrastructure was also produced by Engineer model
`openai/gpt-5.6-sol`; deterministic execution does not make these same-model
artifacts independent.
