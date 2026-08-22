# CY002-background-existence synthesis

Date: 2026-08-22

## Bounded issue and hypothesis discrimination

This single-branch convergence iteration tested the cheapest prerequisite for
the planned functional preservation problem: whether the frozen planar traces
actually arise from a source-free static bulk background in the minimal
unwarped D004/D005 ansatz.

The tested core coframe was

```text
E=(dt,dx,dy,ds,rho(s)dtheta),  rho>0 for s>0,
```

with `rho` extended by zero for `s<=0` in the D002 `C-infinity`-flat equalizer
class, a flat 4D exterior, constant cosmological terms, and the D005 fixed-seed
shell `a0=0`, `g=u=1`, `K=0`, `b=kappa_4^{-1}`. Matter, warping, Lovelock
terms, torsion sources, singular junctions, moving interfaces, and nonbasic
modes were excluded.

A solution would have supplied the smallest background needed to continue the
H002 trace-preservation route. Nonexistence is negative evidence for that
minimal realization and supports only the corresponding restricted H003
failure mechanism; it cannot decide broad C002/C003 or universal H003.

## Evidence inventory

| Evidence | Result | Dependence and status |
|---|---|---|
| `research/derivations/D018.md` | Exact first-order derivation: the open core is torsion free, `omega^43=rho' dtheta`, `R^34=-rho'' ds wedge dtheta`; the independent normal/circle coframe equations force `Lambda_5=0`, persistent equations force `rho''=0`, and exterior flatness forces `Lambda_4=0`. The smooth-flat endpoint data then give `rho=0`. All frozen D005 shell/orbit substitutions are nevertheless satisfied by the limiting traces. | Derived in the restricted ansatz by `openai/gpt-5.6-sol`; no general background theorem. |
| `research/critiques/D018-2026-08-22-openai-01.md` | Independently reconstructed within a fresh session the connection sign, ordered-pair Euler coefficients, endpoint implication, polar control, and shell table. Outcome `no-blocking-issue-found`. | Same model and shared source chain; useful attack, not independent verification. |
| O009 | Canonical exact check of the Cartan solve, curvature, all five 5D coframe equations, flat exterior, endpoint ranks, shell table, alternate warped-component contraction, and four semantic mutations. Outcome `passed`, 42/42 assertions. | Shares `exact_graded`, D004 conventions, and OpenAI producer provenance with earlier checks; correlated machine evidence only. |

## Integrated exact result

On the nondegenerate open core, the D004 connection equation is injective and
gives `T^A=0`. Cartan's equation then fixes

```text
omega^43 = +rho' dtheta,   omega^34 = -rho' dtheta,
R^43 = +rho'' ds wedge dtheta,
R^34 = -rho'' ds wedge dtheta.
```

Writing `k=-rho''/rho`, exact ordered-pair enumeration gives

```text
G_A = (k-Lambda_5) Xi_A/kappa_5,  A=0,1,2,
G_A = -Lambda_5 Xi_A/kappa_5,     A=3,4.
```

Every `Xi_A` is nonzero for `rho>0`. Therefore

```text
Lambda_5=0,  rho''=0,  rho=cs+d.
```

The flat 4D exterior separately requires `Lambda_4=0`. Smooth attachment to the
identically collapsed open side gives `d=rho(0)=0` and
`c=rho'(0)=0`, hence `rho` is identically zero and contradicts the positive
core radius. Only `C^1` matching is needed for this implication, although the
frozen class is `C-infinity` flat.

The candidate interface traces still satisfy

```text
Delta e=Delta omega=0, lambda=-Q, mu=0,
Q=P^-, H(K)=0, D_bar(a) Q=0.
```

Thus shell compatibility is not background existence. C015 and C020 remain
valid conditional shell/primary results, but this particular background cannot
realize them.

## Falsification attempts and controls

The internal critic attempted three serious attacks; none falsified the scoped
result:

1. reversing or rederiving the spin-connection/curvature signs;
2. recomputing every ordered-pair and cosmological coefficient and searching
   for an omitted mixed equation;
3. testing first-order degeneracy, an interface source, the affine polar cap,
   and each D005 shell substitution.

The affine control `rho=cs`, `c>0`, solves the punctured source-free bulk at
zero cosmological constant. It fails the frozen attachment because its zero
extension has a derivative jump. For `c=1` it is an ordinary polar axis only
after changing topology and removing the open collapsed exterior. It is an
escape regime, not a counterexample.

O009's mutations of the spin-connection sign, ordered-pair normalization,
circle equation coverage, and `rho'(0)=0` endpoint condition all produced the
required process failure. No obligation failed or was inconclusive.

## Computational interpretation

O009's deterministic result records exact Cartan rank 50, the sole independent
connection coefficient `(34,4)=-1` in units of `rho'/rho`, the Euler coefficient
vector

```text
(k-Lambda_5, k-Lambda_5, k-Lambda_5, -Lambda_5, -Lambda_5),
```

endpoint ranks two versus one, and a nonzero six-row shell momentum control.
The alternate component path does not call the epsilon Euler enumerator, but it
shares assumptions, arithmetic, infrastructure, and producer model. The pass
supports C021's encoded exact bridge; it does not establish that the D002
category is mandatory or that no other action/background works.

## Cycle decision

Adopt C021 as `derived` with `computational_verification: passed`. The planned
functional trace/Hamiltonian preservation calculation is no longer the immediate
next step because its presumed static unwarped background does not exist.
Do not broaden directly to matter, singular sources, moving interfaces, or a
large numerical/PDE search.

The single best next action is one bounded analytic existence test for the
minimal source-free **warped** cohomogeneity-one extension, allowing one
persistent warp factor while retaining the D002 smooth-flat attachment and the
D005 shell. It should decide whether warping supplies a regular background or
whether the same zero-jet obstruction persists. No Opus audit is nominated.
