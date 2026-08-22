# CY001-trace-primary synthesis

Date: 2026-08-22

## Frozen objective and regime

This focused convergence cycle asked whether a duplicated one-sided trace
presentation can faithfully represent the D005 interface system and whether the
five planar `dQ_C` directions survive as an autonomous rank-ten block after the
ordinary exterior Palatini defining primaries are reduced.

The cycle retained a fixed timelike interface, fixed circle period, basic
theta-independent persistent `SO(1,3)`, the planar rank-three shell
`b=kappa_4^{-1}`, `H(K)=0`, and

```text
Delta epsilon=Delta Omega=0, lambda=-Q, mu=0, Q=g.P^-.
```

Independent boundary copies are constrained to regular one-sided bulk traces.
They are bookkeeping variables, not presumed physical sectors. The seed is
fixed, no independent seed/corner potential is added, and small left Lorentz
transformations may be nonzero at the internal cut but vanish at temporal
endpoints and the lateral boundary. Mixed `SO(1,4)`, moving-interface,
nonbasic, global, and PDE sectors remain excluded. All producers and critics
used `openai/gpt-5.6-sol`; their agreement is correlated rather than independent
evidence.

## Evidence inventory

| Artifact | Question and result | Internal critique | Integrated disposition |
|---|---|---|---|
| D015 / C018 | With fixed gauge-equivariant locally trace-surjective trace maps and a clean constant-rank auxiliary sector, algebraic gluing elimination reproduces the intrinsic D005 Euler system and cut potential. | `no-blocking-issue-found` | Adopt as a conditional local equivalence. It does not prove that the assumed trace maps or lifts exist, or that unreduced primary matrices and post-gluing Dirac brackets are identical. |
| D016 / C019 | Every regular tangential pullback/pushforward of the 5D persistent and mixed Palatini momentum rows and their coframe derivatives vanishes before gluing. One-sided normal contraction can be nonzero. | Initial `revision-required`; revised artifact received `no-blocking-issue-found`. | Adopt the tangential zero-overlap theorem and preserve the normal-trace caveat. It supplies no presentation-independent post-gluing bracket result. |
| D017 / C020 | Pulling back the complete cut potential removes the apparent duplicated `g` kinetic term, retains six `p_g=0` primaries, and yields a combined exterior/interface primary matrix whose five `dP^-_C` directions have zero Palatini Schur self-correction. | Two `revision-required` passes forced retention of the `g` null sector and a precise preservation blocker; the final critique was `no-blocking-issue-found`. | Adopt the reduced-primary algebra under its clean-shell, nondegenerate-triad, and finite-incidence assumptions. Do not infer gauge, physical, or second-class status before preservation. |
| O008 / C018-C020 | Exact graded-form and rational-matrix reconstruction of the shell coefficients, regular 5D tangential rows, exterior matrix, complements, Schur correction, null certificates, and mutation controls. | Canonical deterministic outcome `passed`. | Correlated machine evidence for the declared finite bridge only. No functional trace adjoint, total Hamiltonian, or preservation row is encoded. |

Critique paths are `research/critiques/D015-2026-08-22-openai-01.md`,
`D016-2026-08-22-openai-01.md`, `D016-2026-08-22-openai-02.md`, and
`D017-2026-08-22-openai-01.md` through
`D017-2026-08-22-openai-03.md`.

## Integrated result

The cycle resolves the defining-primary question in the selected local
presentation but stops before first preservation.

1. The duplicated-trace action is locally faithful only conditional on the
   declared trace maps and clean algebraic gluing sector. This condition is a
   scientific assumption, not something O008 establishes.
2. Regular five-dimensional tangential Palatini rows do not supply a hidden
   overlap with the five planar interface-copy directions. Normal contractions
   are distinct operations and can be nonzero.
3. After legitimate complete-shell pullback, the cut potential is

   ```text
   Theta_I|shell = integral_C <P^-_C, delta u u^-1>,
   ```

   while the matching coordinate `g` remains as six zero-momentum primary
   directions. Primary nullness is not a quotient.
4. Adding the exterior Palatini potential gives the defining matrix

   ```text
            C_e   C_varpi  Phi_u  Psi_g
   C_e       0      -A^T     B^T     0
   C_varpi   A       0        0      0
   Phi_u    -B       0       A_P     0
   Psi_g     0       0        0      0_6,
   ```

   where `rank(A)=12`, `rank(B)=rank(dP^-_C)=5`, and `rank(A_P)=4` with
   `ker(A_P)=span(T03,T12)` at the planar point.
5. Reducing any legal twelve-row Palatini complement gives zero `Phi_u`
   Schur self-correction because `B` couples only to the coframe-momentum half.
   The five isolated `dQ_C` cross-pairs therefore do not survive as five
   additional defining pairs in this presentation. The surviving pointwise
   primary algebra contains six Palatini connection-primary null combinations,
   a rank-four coadjoint block with two null directions, and six `g`
   zero-momentum directions.
6. The matching tangent identity and zero total cut moment map add no rank:

   ```text
   delta Q = [delta g g^-1,Q] + g.delta P^-,
   delta(-P^- - Ad_(g^-1)lambda)|shell = 0.
   ```

These statements exclude an **autonomous additive rank-ten remnant at the
defining-primary level** under the frozen assumptions. They do not show that
the remaining null directions are gauge, physical, or second class.

## Canonical computation and trust boundary

O008 passed 51/51 exact assertions. It enumerated all 18,564 candidate
twelve-row Palatini complements; eight were admissible and all eight gave zero
Schur correction. It found exact ranks `A=12`, `B=5`, `A_P=4`, complete matrix
rank 28, and residual rank 4, with six `ker(A^T)` certificates, the two
`A_P` nulls, and six `g` zero rows. Direct dense and sparse assemblies agreed.
The regular-core control gave zero tangential rows and the nonzero normal
witness `P_40=dP_40=1/(2 kappa_5)`. Four intentional mutations—shell-potential
sign, exterior incidence sign, deleted frame commutator, and spurious
connection-half coupling—each triggered the intended failure.

The check uses exact `fractions.Fraction` coefficients and the existing
`research/computation/exact_graded/` substrate. It shares conventions,
representation, infrastructure, and OpenAI producer provenance with prior
checks, so it is not an independent implementation. Its result explicitly
records `functional_trace_adjoint_encoded: false`. A pass supports the encoded
finite algebra, not the trace-existence assumptions or a Dirac classification.

## Reconciled apparent conflicts

1. **C016 rank ten versus C020 no autonomous rank ten:** C016 is the isolated
   interface shell form. C020 reduces the complete exterior-plus-interface
   defining system. These are different stages and are not contradictory.
2. **Zero total moment map versus rank-four `A_P`:** moment-map tangency is a
   shell identity; `A_P` is an intermediate primary bracket block. Neither is a
   quotient or physical reduced form.
3. **Zero regular core tangential rows versus nonzero `Q`:** D016 treats regular
   collapsed pullbacks. D005's finite `Q` is enriched incidence data. Normal
   contraction or profile-divided traces would change the declared operation.
4. **Eliminated duplicate kinetics versus retained `g`:** the complete-shell
   potential is independent of `g`, which makes `p_g=0`; it does not authorize
   deleting `g` before preserving its Hamiltonian dependence.

## Pruning and remaining gate

Pruned in the selected regime:

- additive rank counting between C016's isolated block and an unspecified bulk
  Palatini matrix;
- a hidden regular tangential 5D primary overlap as the missing classifier;
- interpreting zero total Gauss tangency as first-class reduction;
- interpreting primary `g` nullness as a seed or Lorentz quotient;
- further finite complement searches for the already exhaustive Schur result.

The exact stopping obstruction is now prior to first post-shell preservation.
A pointwise incidence map does not define the functional trace domain, boundary
pairing, or adjoint needed to compare boundary and bulk coframe variations. The
planar induced triad also does not fix the exterior curvature, temporal
coframe/connection, reference background, boundary conditions, or total
Hamiltonian. Consequently the preservation rows for the six Palatini nulls,
`Phi_u`, `p_g`, `pi_varpi0`, and `pi_e0` are not yet defined.

## Best next decision

Continue convergence rather than reopen breadth. The next bounded theory task
must declare a functional trace space and adjoint, choose a boundary-compatible
exterior/reference background, and derive the total Hamiltonian sufficiently to
perform one preservation step for every surviving primary. It must retain the
torsion/coframe equations and stop if mixed `SO(1,4)` or another frozen sector
is sourced. No new obligation should be allocated until that derivation exposes
a finite, discriminating closure/rank assertion. No Opus audit is nominated.
