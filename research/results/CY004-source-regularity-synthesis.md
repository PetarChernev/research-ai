# CY004-source-regularity synthesis

Date: 2026-08-22

## Bounded issue and decision quantity

This single-branch convergence cycle tested the ordinary-source escape left by
C021-C022 without selecting a matter Lagrangian.  The frozen open-core geometry
was

```text
E^i=w(s)dx^i, i=0,1,2;  E^3=ds;  E^4=rho(s)dtheta,
w>0, rho>0 for s>0,
w=1 for s<=0 with a C-infinity-smooth extension,
rho=ell exp[-(L/s)^nu], nu=2 or 4, for s>0 and zero otherwise.
```

Zero spin current was assumed so that the D019 torsion-free connection applies.
The required source was defined only as the effective tensor
`G_AB+Lambda_5 eta_AB=kappa_5 T_AB`, with `kappa_5>0` and finite constant
`Lambda_5`.  The decision quantities were: bounded orthonormal curvature and
stress; componentwise absolute local `L1` stress against `w^3 rho ds` on a
compact tangential cell; and the NEC for every orthonormal null vector.  The
cycle did not attempt to reverse-engineer a matter action.

## Evidence inventory

| Evidence | Recorded result | Dependence and status |
|---|---|---|
| `research/derivations/D020.md` | Exact effective tensor and all-null reduction.  For both profiles and every allowed common warp, `r=rho''/rho -> +infinity`, all warp terms are flat, curvature/stress are unbounded, both nontrivial NEC coefficients are eventually negative, but every absolute stress component is locally volume-integrable. | Exact/asymptotic derivation by `openai/gpt-5.6-sol`; imports D002/D004/D019 and does not construct matter dynamics. |
| `research/critiques/D020-2026-08-22-openai-01.md` | Reconstructed Lorentzian signs, both NEC channels, flat-germ dominance, absolute endpoint integrability, and the secondary curvature-square formula. Outcome `no-blocking-issue-found`. | Fresh session but the same model and source chain; internal critique, not independent verification. |
| O011 | Canonical outcome `passed`, 79/79 exact assertions. It reconstructs the Einstein tensor from the D019 curvature families, obtains ten off-diagonal stress zeros, both profile tables, the two NEC coefficients, the formal flat-order bridge, and the distinct unbounded/weighted-`L1` verdicts. Five semantic mutations were effective. | Self-contained exact `Fraction`/Laurent/order code by `openai/gpt-5.6-sol`; it imports the analytic flat-germ and exponential-domination premises and is correlated support. |

No experiment, external literature theorem, Engineer substrate, or Opus audit was
used.

## Integrated exact and asymptotic result

With

```text
A=w'/w,  B=rho'/rho,  p=w''/w,  q=AB,  r=rho''/rho,
F=2p+A^2+2q+r,  H=3(A^2+q),  J=3(p+A^2),
```

the complete effective orthonormal tensor is

```text
kappa_5 T_00=-(F+Lambda_5),
kappa_5 T_11=kappa_5 T_22=F+Lambda_5,
kappa_5 T_33=H+Lambda_5,
kappa_5 T_44=J+Lambda_5,
T_AB=0 for A!=B.
```

For any null vector, the `0-1-2` contribution saturates and

```text
kappa_5 T_AB k^A k^B
  =(H-F)(k^3)^2+(J-F)(k^4)^2,
H-F=2A^2+q-2p-r,
J-F=p+2A^2-2q-r.
```

Thus all-null NEC is equivalent to both displayed coefficients being
nonnegative.  For `nu in {2,4}`,

```text
B=nu L^nu s^(-nu-1),
r=nu^2 L^(2nu) s^(-2nu-2)-nu(nu+1)L^nu s^(-nu-2),
```

so `r` is positive and divergent sufficiently near zero.  Smooth extension of
`w=1` makes `A,p,A^2,q` flat even after multiplication by the fixed polynomial
divergence in `B`.  Hence `F=r+flat`, `H=flat`, and `J=flat`.  The orthonormal
`3-4` curvature diverges, `T_00 -> -infinity`, `T_11=T_22 -> +infinity`, and
both `0-3` and `0-4` null contractions are negative near the endpoint.

The singularity is nevertheless absolutely volume-integrable componentwise.
On a sufficiently small interval where `r>0`,

```text
integral rho |r| ds = integral rho'' ds
                    = rho'(epsilon)-rho'(0) < infinity.
```

All remaining source terms are bounded or flat before multiplication by the
exponentially small volume factor.  The same exponential domination makes the
volume-weighted curvature square finite, but that secondary fact does not
restore pointwise boundedness or the NEC.

| profile | bounded curvature | bounded stress | absolute local stress `L1` | all-null NEC |
|---|---|---|---|---|
| `ell exp[-(L/s)^2]` | no | no | yes | no |
| `ell exp[-(L/s)^4]` | no | no | yes | no |

## Falsification attempts and computational controls

The internal critic made three bounded attacks: a fresh Lorentzian
curvature/stress/null contraction; a search for a smooth-flat common warp whose
`q=A B` term could cancel `r`; and an absolute-value/endpoint audit of the `L1`
and curvature-square statements.  None found a blocking issue.

O011 independently within its encoded representation mutated the timelike
stress sign, one profile derivative sign, omission of each NEC channel
separately, and the inference from weighted integrability to pointwise
boundedness.  Every mutation made the process fail as predeclared.  O011 does
not prove the analytic flat-germ theorem, construct a matter action, or supply
independent verification.

## Dependence and epistemic disposition

D020, its critic, and O011 share D002/D004/D019 conventions and the same OpenAI
model.  O011 is self-contained rather than reusing `exact_graded`, but its
inputs and producer are still correlated with the derivation.  Agreement is
therefore not independent confirmation.

Adopt C023 as `derived`, with `computational_verification: passed` and
`independent_verification: not-requested`.  C023 is negative evidence for the
ordinary regular-source version of H002 and support for a restricted geometric
mechanism within H003.  It does not decide broad C002/C003, prove a universal
smooth-flat theorem, or show that any effective tensor comes from healthy local
matter.

## Cycle decision and next discriminator

Close `CY004-source-regularity`.  For the two exact D002 profiles, do not select
an ordinary bounded NEC-respecting matter model in the frozen common-warp
geometry: the geometry already requires unbounded, NEC-violating effective
stress, even though its componentwise volume integral is finite.  Functional
Hamiltonian preservation remains blocked because no physically admissible
background has been established.

Do not launch another relaxation in this cycle.  The cheapest high-information
next diagnostic is a profile-independent endpoint lemma: determine whether any
positive circle radius with `rho(0)=rho'(0)=0` in proper-normal gauge can have
bounded `rho''/rho` near an attached open collapsed side.  This would decide
whether C023 reflects only the two chosen rates or the smooth-flat geometric
class before deliberately relaxing exactly one of regularity/topology,
torsion/connection dynamics, or the diagonal metric ansatz.
