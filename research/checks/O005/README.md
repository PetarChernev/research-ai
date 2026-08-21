# O005: D006 interface cut rank and moment maps

Exact claim-linked obligation for the finite cut-rank and moment-map assertions
of `D006`. `spec.yaml` preserves the allocation-time question and criterion,
`run.py` decides them, and only the deterministic wrapper may create
`result.json`.

## Targets

Claims: C016

Derivations: D006

## Question tested

On the D006 planar rank-three interface background, do exact canonical Lorentz-algebra and exterior-form matrices give rank(dQ)=5, fixed-reference cut rank 12 off shell and zero after imposing Pi=delta Pi=0, Stueckelberg cut rank 22 off shell and rank 10/nullity 4 for its (v,e) block on shell, together with the stated Lorentz moment-map signs and a nonzero Q_03 corner-charge witness?

## What this does not test

O005 does not supply or represent the core/exterior bulk symplectic potentials,
Lorentz Gauss generators, secondary constraints, boundary counterterms, or a
choice of temporal/lateral corner polarization. It therefore cannot decide
whether the rank-ten shell block is physical, second class, or removed by a
first-class total generator. It does not decide which transformations of a
fixed reference or Stueckelberg seed are admitted gauge, prove charge
integrability, or address global bundles, large gauge sectors, moving
interfaces, nonbasic modes, full `SO(1,4)`, hyperbolicity, or positivity. It
checks the declared planar pointwise finite algebra only and is not independent
verification of C016 or D006.

## Assumptions encoded in the implementation

- The cut calculation is pointwise in the fixed-interface, basic, horizontal,
  theta-independent persistent `SO(1,3)` sector. Only the interface/edge
  potential is represented.
- `epsilon_0123=+1`, `eta=diag(-,+,+,+)`, Lorentz pairs are ordered
  `(01,02,03,12,13,23)`, and the cut exterior basis is `dx1<dx2`.
- On the cut, `(e0,e1,e2,e3)=(0,dx1,dx2,0)`. The temporal leg `e0=dt` is
  included separately when certifying that the full interface triad has rank
  three.
- The exact nonzero rank scale is set to `b=1`. The result restores `b`
  symbolically: `Q03=(b/2) dx1 wedge dx2`. Scaling by nonzero `b` does not
  alter rank.
- `T_ab` obey the standard explicitly encoded Lorentz bracket with lower
  canonical pairs. The invariant bivector pairing has diagonal entries
  `eta_aa eta_bb`; no implicit raising/lowering operation is used.
- `Omega=delta Theta` with right Maurer--Cartan variables. A block from
  `<p,delta h h^-1>` is represented as `[[A_p,-G],[G,0]]`.
- Off shell, `delta lambda` makes `delta Pi` arbitrary. On the imported shell,
  `Pi=0`, tangent vectors satisfy `delta Pi=0`, and `lambda=-Q` cancels only
  the `g` block in B.
- All coefficients are `Fraction` values. Equality, rank, nullity, exterior
  signs, and nonzero tests are exact. There are no floats, tolerances, samples,
  inverse coframes, CAS simplifications, or unstated algebraic relations.

## Method

Exact rational Lorentz-algebra/exterior-matrix construction with a materially
different analytic block-rank path and explicit gauge-vector contractions.
The alternate path is a correlated cross-check, not independent verification.

Rationale: The conclusion-critical finite assertions are exact ranks, null directions, signs, and a nonzero witness. Canonical rational matrices decide them without sampling, while the missing bulk Gauss interpretation remains explicitly outside the obligation.

## Representation and trust-surface assessment

1. **Mathematical domain.** The represented objects are the rational form of
   `so(1,3)` on six ordered antisymmetric pairs, the exterior algebra of a
   two-dimensional cut, the linear map from eight coframe variations to six
   bivector coefficients, and finite presymplectic matrices.
2. **Operations needed.** Only epsilon parity, two-form wedge/coefficient
   extraction, Lorentz brackets and pairings, exact matrix assembly,
   rank/nullspace/matvec, transpose/direct sum, and gauge-vector contraction are
   needed.
3. **Exact representation.** Every input on the adapted planar background is
   rational. `b` is a nonzero common scale and can faithfully be set to one for
   rank, with `b/2` restored in the witness.
4. **Decidable equality.** Exterior forms have canonical sparse maps and
   matrices have canonical `Fraction` entries; equality is exact. Deterministic
   RREF decides all represented ranks and nullspaces.
5. **Encoded conventions.** Orientation, metric, pair order, cut basis,
   ordered epsilon sum, bracket, pairing, Maurer--Cartan/presymplectic sign,
   off-shell momentum freedom, and shell tangent condition are all explicit in
   the spec and runner.
6. **CAS trust.** A CAS would add parser, assumption, simplifier, matrix, and
   sign-convention surfaces without helping this small rational problem. None
   is used.
7. **Small-kernel value.** A small domain-specific exact kernel materially
   reduces trust versus symbolic tensor automation, but that kernel already
   exists; another one is unnecessary.
8. **Existing-substrate adequacy.** `exact_graded` supplies precisely the public
   `ExteriorAlgebra`, `levi_civita_sign`, and `RationalMatrix` primitives needed.
   Lorentz and block formulas are claim-specific loops, not missing reusable
   infrastructure.
9. **Custom-infrastructure risk.** A new generic presymplectic or Lie-algebra
   framework for one matrix would add API and convention risk. No Engineer is
   provisioned and the existing substrate is unchanged.
10. **Cross-checks.** The primary path builds `dQ` through exterior forms and
    obtains matrix ranks by RREF. The alternate path reads five explicit
    pivot images, constructs three `ker(dQ)` vectors plus `T12`, and applies the
    first-order block-rank argument. A nonidentity rational Lorentz boost checks
    pairing invariance and the adjoint/coadjoint conversion. These paths reduce
    implementation risk but share conventions and are not independent
    scientific verification.

The trusted surface is CPython's integer arithmetic and `Fraction`, the three
fingerprinted `exact_graded` public primitives above, the short claim-specific
index/block construction, and the deterministic wrapper. The substrate's law
tests establish its software contract, not the scientific encoding.

## Acceptance criterion

Pass iff an exact rational implementation with eta=diag(-,+,+,+), epsilon_0123=+1, ordered planar basis, and Q_03=b/2 computes rank(dQ)=5; fixed-reference rank 12 off shell and rank 0 on Pi=delta Pi=0; Stueckelberg (v,e) block rank 10 and nullity 4, full off-shell rank 22, and shell rank 10; identifies T_12 plus three ker(dQ) null directions; reproduces J_+^A=Pi, J_-^A=-Ad_(g^-1)Pi, J_+^B=Pi, J_-^B=-Ad_(g^-1)lambda and hence shell J_-^B=Ad_(g^-1)Q; yields a nonzero exact planar Q_03 corner witness; and detects predeclared sign, factor, rank, and shell-pullback mutations. Fail on any exact mismatch. Inconclusive only if the declared planar triad is not rank three or the represented Lorentz pairing is degenerate; implementation exceptions are errors.

There are no thresholds, tolerances, precision choices, random seeds, or sample
sizes. Every comparison is exact, and the allocation-time question and
criterion have not been weakened.

## Controls

Positive controls require the rank-three triad, nondegenerate Lorentz pairing,
`Q03=+1/2`, all target ranks, four explicit null vectors, the alternate analytic
rank counts, moment-map identities, and the nonzero corner witness. Negative
controls distinguish a degenerate cut coframe and a deleted area coefficient.

Four internal mutations test the principal failure surfaces: reversing the
minus-frame sign, omitting one ordered epsilon term (factor two), deleting a
`dQ` pivot (rank four), and retaining a canonical pair after the shell pullback.
The same defects can be injected process-locally with
`O005_INTENTIONAL_MUTATION=moment-sign|q-factor|dq-rank|shell-pullback`; each
direct sensitivity run must exit `1` and must not create a canonical result.

## Infrastructure used

The specification fingerprints `research/computation/exact_graded/`, root
`pyproject.toml` and `uv.lock`, and the materially used orchestration paths
`scripts/run_check.py` and `scripts/_research.py`. The existing kernel is
methodology, not evidence. Its README records 45 passing contract tests. O005
does not modify or rerun the substrate and does not delegate to Engineer.

## How to run

```bash
for mutation in moment-sign q-factor dq-rank shell-pullback; do
  O005_INTENTIONAL_MUTATION="$mutation" \
    uv run --locked python research/checks/O005/run.py
done

uv run --locked python scripts/run_check.py O005
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

All four documented process-local sensitivity mutations were run directly
before canonical execution and each exited `1` as required. They produced no
canonical result:

| mutation | failed/total exact assertions | principal detected effects |
|---|---:|---|
| `moment-sign` | 3/40 | both minus-frame coefficients and the B lambda identity |
| `q-factor` | 4/40 | `Q03`, the exact `dQ` entries, and both corner-factor assertions |
| `dq-rank` | 10/40 | `rank(dQ)=4`, residual rank 8, full rank 20, and associated nullity/count checks |
| `shell-pullback` | 1/40 | fixed-reference shell rank remained 12 instead of zero |

The unmutated direct diagnostic evaluated 40/40 assertions successfully. The
canonical obligation was then executed only through the deterministic wrapper.
`research/checks/O005/result.json` records **passed**, process exit `0`, at
`2026-08-20T18:18:12Z`. Its authoritative observations are:

- `rank(dQ)=5`, nullity `3`, and `Q03=1/2` at the exact representative `b=1`;
- fixed-reference ranks `12` off shell and `0` on shell;
- Stueckelberg `(v,e)` rank `10`, nullity `4`, full off-shell rank `22`, and
  shell rank `10`;
- null directions `T12`, `de1^2`, `de2^1`, and `de1^1-de2^2`;
- the four declared moment-map formulas and a corner witness `+1/2`, i.e.
  `+b/2` before setting the nonzero common scale to one.

All 40 canonical exact assertions passed and none failed. Standard output is
preserved in `research/checks/O005/logs/stdout.log`; canonical standard error is
empty. The aggregate infrastructure SHA-256 is
`0b4aeb783458e144f6b86641ad631d0cb62dcc12398b414a552434f00d211b97`,
including exact-kernel directory SHA-256
`197024e3f37dff868c931141ce25949e26e2249bd4850d0213ff06e81449268b`.
The wrapper recorded CPython 3.12.12, Git commit
`6eda62c0325e4feccff7148cb0da877bc028a46b`, and a dirty worktree.

## Interpretation and limitations

The passing outcome establishes only the encoded finite exact planar
coefficients, ranks, null directions, moment-map signs, and one temporal-corner
witness. It does not establish the omitted bulk canonical interpretation or
verify C016. Exact equality remains conditional on the declared basis, bracket,
pairing, and shell semantics being the faithful transcription of D006. The
alternate sparse pivot/kernel argument is materially different from full-matrix
RREF but shares the scientific transcription and is explicitly not independent
verification.

Producer for the O005 assessment, specification completion, scientific
encoding, and claim-specific runner: `openai/gpt-5.6-sol`. No Engineer is used.
The materially reused `exact_graded` infrastructure records producer model
`openai/gpt-5.6-sol`; shared model and substrate paths are not independent.
