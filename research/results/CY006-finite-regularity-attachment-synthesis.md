# CY006 finite-regularity attachment synthesis

Date: 2026-08-22

## Bounded issue and decision quantity

This single-branch convergence cycle tested exactly one escape from C024: keep
the torsion-free diagonal geometry and D004/D005 action fixed, but replace the
zero-slope smooth-flat attachment by

```text
rho(s)=c s for s>0,  rho=0 on the open collapsed side,  c>0.
```

The decision quantity was not punctured bulk curvature alone. It was whether
the resulting one-sided finite connection trace makes the complete split
Palatini-plus-interface variation stationary on the intended rank-three
interface under free finite transition tangents.

## Evidence inventory and dependence

| Evidence | Result | Status and dependence |
|---|---|---|
| `research/derivations/D022.md` | Separates the D002 open-collapsed quotient, a half-core polar cap, and a fixed-cylinder weak extension; derives the finite mixed D004 boundary term and the free-versus-fixed polar-data dichotomy. | Exact restricted derivation by `openai/gpt-5.6-sol`; imports D002/D004/D005 conventions and D018/D019 polar signs. |
| `research/critiques/D022-2026-08-22-openai-01.md` | Recomputed the sign, ordered-pair factor, rank-three contradiction, first-order variation logic, and absence of a D005 mixed cancellation. | Outcome `no-blocking-issue-found`; same-model internal critique, not independent evidence. |
| O012 | Reconstructed the D004 ordered-index coefficients, finite mixed trace, frozen D005 field incidence, and persistent shell table; all four semantic mutations failed as required. | Canonical outcome `passed`, 29/29 assertions. Self-contained exact arithmetic but shared conventions and OpenAI provenance make it correlated support. |
| C021--C024 / D018--D021 | Supply the smooth-flat obstruction and identify nonzero slope as the load-bearing relaxation. | Prior restricted evidence; none establishes finite-slope admissibility. |

No experiment, literature search, new reusable infrastructure, Engineer task,
or Opus audit was used.

## Exact scoped result

The D002 quotient relation still gives an open four-dimensional side for
`s<0`; changing the profile changes regularity, not this topology. On a fixed
cylinder,

```text
rho=c s_+ is Lipschitz but not C1,
g_theta_theta=c^2 s_+^2 is C1,1 but not C2,
omega^43=c H(s) dtheta,
R^43=c delta_0 ds wedge dtheta.
```

That weak extension is bookkeeping, not the physical quotient and not the
split D004 action. The open core and flat exterior are separately flat at
`Lambda_5=Lambda_4=0`. A `c=1` half-cap is an ordinary smooth polar axis only
when the extra collapsed ray is omitted; `c!=1` gives a conical half-cap.

For the actual split D004 variation, `E^4|_Sigma=0` still kills the persistent
connection channel. The newly admitted finite mixed tangent does not vanish:

```text
p_! Theta_(5,chi43)
  = +(2 pi/kappa_5) delta chi43 o_Sigma,
epsilon_(3bcd) e^b wedge e^c wedge e^d = -6 o_Sigma.
```

The unchanged D005 basic persistent action has no `omega^43` or `chi43`
variable and therefore no conjugate cancellation. Free `delta chi43` imposes
vanishing of the displayed triad volume, which is incompatible with the
intended rank-three interface. Substituting the torsion-free relation before
variation is invalid; even restricting afterward to polar-family tangents
turns the same term into `(2 pi/kappa_5) delta c o_Sigma`.

All persistent D005 shell/orbit equations nevertheless hold on the candidate
traces: `Delta e=Delta omega=K=0`, `lambda=-Q`, `Q=P^-`, `mu=0`, and both edge
covariant-derivative rows vanish. Persistent shell compatibility and complete
mixed-sector differentiability are therefore distinct.

The exact dichotomy is:

1. **Free finite polar/mixed data:** the fixed D004/D005 theory has no
   rank-three stationary bulk-plus-shell background in this ansatz.
2. **Externally fixed slope and mixed holonomy:** a separately flat
   fixed-boundary candidate exists and satisfies the persistent shell, but the
   polar datum has no Euler equation and the result establishes neither C002
   nor C003.

This is C025, a derived restricted result with passing correlated machine
support. It is not a universal continuum no-go.

## Falsification attempts and limitations

- `c=1` removes intrinsic half-cap curvature but does not remove the free mixed
  boundary row in the D002 split object.
- Direct torsion substitution gives zero weak torsion, so the obstruction is
  not an artifact of a torsionful candidate.
- Reversing orientation changes coordinate representatives consistently and
  does not remove the stationarity equation.
- Fixing only `c` is insufficient in first-order theory because `delta chi43`
  remains independent; fixing only `chi43` likewise does not supply a slope
  equation.
- O012 does not decide whether the selected finite tangent class is physically
  mandatory, whether a lower-regularity intrinsic calculus exists, or whether
  a new covariant mixed interface term can repair the action.

## Computational disposition

O012 was warranted because the conclusion depends on a mechanically decidable
sign, ordered-pair normalization, fiber factor, and absence of a mixed D005
incidence. It passed 29/29 assertions. The `core-sign`, `omit-order`,
`smooth-flat-zero`, and `fictitious-d005-cancellation` mutations each exited
with failure as predeclared. Its result fingerprints a self-contained exact
runner and the root deterministic infrastructure; no weak-geometry or general
BV implementation is claimed.

## Cycle decision and next discriminator

Close `CY006-finite-regularity-attachment`. Stop treating `rho=cs` as a free
background of the unchanged theory. The next future cycle should change only
the action-side datum exposed here: derive one minimal gauge-covariant,
field-space-integrable mixed interface completion conjugate to the finite
`43` trace, and test whether its compulsory companion equations cancel the
mixed D004 row without fixing the polar datum, degenerating the triad, or
silently introducing an uncontrolled physical edge mode. Keep the finite-slope
flat bulks, fixed interface, and persistent D005 sector otherwise unchanged.
Do not resume Hamiltonian preservation unless that complete action admits an
actual background.
