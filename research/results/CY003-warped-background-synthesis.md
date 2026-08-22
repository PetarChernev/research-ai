# CY003-warped-background synthesis

Date: 2026-08-22

## Bounded issue and decision quantity

This focused convergence cycle tested the least-radical escape left by C021:
whether one common warp factor for the three persistent interface directions can
support a source-free, static, smooth-flat circle-collapse background while the
D004 action, D002 attachment, flat exterior, proper-normal gauge, and D005
fixed-seed shell remain unchanged.

The open-core coframe was

```text
E^i=w(s) dx^i, i=0,1,2;  E^3=ds;  E^4=rho(s)dtheta,
w>0, rho>0 for s>0,
w=1, rho=0 for s<=0 with C-infinity-flat attachment.
```

The decision quantity was exact existence, not a fit or perturbative residual.
A solution would have restored a background for the deferred C020 functional
preservation problem. Nonexistence would exclude the complete diagonal
proper-normal, common-warp, `2+1`-Poincare-symmetric source-free benchmark, but
not anisotropic, sourceful, off-diagonal, weaker-regularity, moving-interface,
or alternative-action sectors.

## Evidence inventory

| Evidence | Recorded result | Dependence and status |
|---|---|---|
| `research/derivations/D019.md` | Exact Cartan/Euler derivation gives four curvature families, the five Euler coefficients `(S,S,S,H,J)`, `(w'/rho)'=0`, and `(w^2)''+(2 Lambda_5/3)w^2=0`. Smooth-flat endpoint data force `Lambda_5=0`, `w=1`, and `rho=0`; flat exterior forces `Lambda_4=0`. Candidate traces still satisfy the D005 shell/orbit system. | Restricted exact derivation by `openai/gpt-5.6-sol`; not a general source-free theorem. |
| `research/critiques/D019-2026-08-22-openai-01.md` | Reconstructed the connection, curvature, ordered-pair coefficients, branch split, endpoint argument, topology distinction, and separate `g`/seed-orbit equations. Outcome `no-blocking-issue-found`. | Fresh session but same model and source chain; internal attack, not independent verification. |
| O010 | Canonical outcome `passed`, 74/74 exact assertions. Cartan rank 50, complete curvature/Euler vectors, both first-integral branches represented before endpoint elimination, endpoint/polar ranks two/one, six nonzero shell momentum rows, and four effective semantic mutations. | Uses the shared `exact_graded` kernel, D004/D005 conventions, and OpenAI producer. Its component/ODE path is correlated, not independent. |

No experiment or external literature theorem is used. No Opus audit was
requested.

## Integrated exact result

On the nondegenerate core, the Palatini connection equation gives zero torsion
and uniquely fixes

```text
omega^(i3)=A E^i=w' dx^i,   omega^(43)=B E^4=rho' dtheta,
A=w'/w,                     B=rho'/rho.
```

With `p=w''/w`, `q=AB`, and `r=rho''/rho`, the nonzero curvature families are

```text
R^(ij)=-A^2 E^(ij),  R^(i3)=-p E^(i3),
R^(i4)=-q E^(i4),    R^(34)=-r E^(34).
```

Exact ordered-pair enumeration of the D004 coframe equations gives a common
overall `-Xi_A/kappa_5` and coefficients

```text
S = 2p+A^2+2q+r+Lambda_5,   A=0,1,2,
H = 3A^2+3q+Lambda_5,       A=3,
J = 3p+3A^2+Lambda_5,       A=4.
```

The denominator-cleared equations remain regular at the one-sided endpoint.
Subtracting the independent `H` and `J` equations gives

```text
w'' rho-w' rho'=0,
(w'/rho)'=0 on rho>0,
w'=C rho
```

without dividing by `w'`; both `C=0` and `C!=0` branches are retained. The
circle equation is equivalently

```text
(w^2)''+(2 Lambda_5/3)w^2=0.
```

At `s=0`, `w=1` and `w'=w''=0` force `Lambda_5=0`. The same regular equation
then gives `(w w')'=0`, so its zero endpoint constant implies `w=1`. The
remaining equation becomes `rho''=0`, and `rho(0)=rho'(0)=0` implies
`rho=0`. Hence

```text
Lambda_5=Lambda_4=0,  w=1,  rho=0,
```

contradicting positive core radius. Only finite endpoint jets are used; no
analyticity assumption or inverse coframe at rank loss enters.

The limiting persistent connection vanishes because `w'(0)=0`. With the frozen
seed this determines `K=0`; it is not inferred from `H(K)=0`. Coframe and
connection matching, `lambda=-Q`, `mu=0`, `Q=P^-`, the companion equation, the
`g` equation, and the distinct fixed-seed orbit equation all hold. As in CY002,
shell compatibility is not bulk-background existence.

## Falsification attempts and computational controls

The internal critic attempted three serious attacks:

1. recomputation of every connection/curvature sign and ordered-pair Euler
   coefficient, including D018 and constant-curvature limits;
2. retention of a finite nonzero `C=w'/rho` branch despite the `0/0` endpoint,
   checking that regular equations rather than an endpoint ratio eliminate it;
3. the affine polar-axis and complete D005 shell/orbit substitutions, including
   separation of the `g` and seed-orbit equations.

None falsified C022 in its stated regime. O010 independently within its encoded
representation mutated the plane-curvature sign, cosmological normalization,
circle-equation coverage, and `rho'(0)` endpoint condition; each mutation made
the process fail as predeclared. No obligation failed or was inconclusive.

## Dependence and epistemic disposition

D019, its critic, and O010 share D002/D004/D005, one OpenAI model, and—on the
machine side—the same exact kernel used by O002-O009. Agreement is correlated.
The direct component and coordinate-ODE routes reduce transcription risk but do
not constitute an independent implementation.

Adopt C022 as `derived` with `computational_verification: passed` and
`independent_verification: not-requested`. This is stronger than C021 only in
the addition of one common persistent warp. It remains negative evidence for
the minimal H002 realization and support for a restricted H003 mechanism, not a
decision of broad C002/C003 and not a universal continuum no-go.

## Cycle decision and next discriminator

Close the common-warp escape. Do not resume functional preservation around the
off-shell planar traces, and do not add several geometric or action freedoms at
once. A separate positive lapse is only radial-coordinate freedom while it
remains nondegenerate, whereas anisotropic warps abandon the frozen `2+1`
Poincare-symmetric benchmark.

The next single best bounded task is a **source-regularity diagnostic** in the
same symmetric geometry: derive the exact orthonormal stress tensor required by
a prescribed D002 smooth-flat profile (allowing the common warp), and decide
whether bounded curvature/stress, local integrability, and the null energy
condition can coexist with `rho>0` and zero endpoint jet. This tests whether
ordinary regular matter is a plausible minimal escape before selecting a
matter action, singular junction, Lovelock term, anisotropic sector, or moving
interface.
