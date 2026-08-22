# CY005-profile-independent-endpoint synthesis

Date: 2026-08-22

## Bounded issue and decision quantity

This single-branch convergence cycle asked whether the divergent
`rho''/rho` mechanism found for the two exact D002 profiles is forced by the
endpoint geometry itself. The frozen analytic class was

```text
rho in C^1([0,epsilon)) intersect C^2((0,epsilon)),
rho(0)=rho'_+(0)=0,
rho(s)>0 for s>0,
```

with `s` outward proper distance. The decision quantity was local upper or
absolute boundedness of `rho''/rho`, together with the corresponding
orthonormal radial-circle sectional curvature. No field equation, common warp,
effective source, matter action, or Hamiltonian system was assumed.

## Evidence inventory

| Evidence | Recorded result | Dependence and status |
|---|---|---|
| `research/derivations/D021.md` | Two integrating factors prove `limsup_(s->0+) rho''/rho=+infinity`. Hence `K_(s theta)=-rho''/rho` is unbounded below. A regular-lapse formula makes the coordinate-invariant content explicit. A smooth-flat oscillatory radius has both infinite-sign subsequential limits. | Exact analytic derivation by `openai/gpt-5.6-sol`; imports only the D019 curvature convention for the geometric translation. |
| `research/critiques/D021-2026-08-22-openai-01.md` | Reconstructed the theorem, sharpness witness, and lapse identity. Required length scales in the oscillatory example. | Same-model internal critique; outcome `revision-required`; not independent evidence. |
| `research/critiques/D021-2026-08-22-openai-02.md` | Confirmed the dimensional repair, derivative factors, subsequences, theorem, and curvature bridge. | Fresh same-model re-critique; outcome `no-blocking-issue-found`; not independent evidence. |
| O010/O011 | Previously passed checks support the inherited D019 curvature family and the two explicit D002 profile formulas. | Correlated prior evidence only; neither obligation tests the universal comparison theorem. |

No new machine obligation, experiment, literature search, Engineer substrate, or
Opus audit was used.

## Exact result

Suppose for contradiction that `rho''/rho<=M` on an endpoint neighborhood.
Positivity gives `rho''<=M rho`. Choose `lambda>=0` with
`lambda^2>=max(M,0)`. Then

```text
[exp(-lambda s)(rho'+lambda rho)]'
  =exp(-lambda s)(rho''-lambda^2 rho) <= 0.
```

The two continuous zero endpoint data imply `rho'+lambda rho<=0`, and hence
`[exp(lambda s)rho]'<=0`. Its zero endpoint value forces `rho<=0`, contradicting
strict positivity. Therefore, on every punctured endpoint neighborhood,

```text
sup rho''/rho = +infinity,
limsup_(s->0+) rho''/rho = +infinity.
```

Absolute boundedness is impossible as well. In proper-normal gauge,

```text
K_(s theta) = -rho''/rho,
```

so this orthonormal sectional component is unbounded below. In a regular lapse
chart `ds=N dx`, the same invariant is

```text
K_(s theta) = -[rho_xx-(N_x/N)rho_x]/(N^2 rho).
```

The raw coordinate ratio `rho_xx/rho` is not invariant.

## Sharpness and failed overextensions

- Dropping `rho'_+(0)=0` admits the flat polar control `rho=cs`; the slope
  condition is load-bearing.
- The dimensionally repaired smooth-flat profile
  `rho=ell exp[-(L/s)^2+(3/4)sin((L/s)^2)]` has
  `liminf rho''/rho=-infinity` and `limsup=+infinity`. It does not falsify the
  theorem, but it falsifies an all-profile actual limit, eventual positivity,
  or eventual convexity claim.
- Regular lapse changes preserve the invariant curvature and zero proper slope.
  Singular endpoint reparametrizations change the regularity problem rather
  than evade the theorem.
- The theorem does not establish effective-stress divergence after possible
  contractions/cancellations, NEC failure, componentwise `L1`, matter
  realization, curvature at the endpoint, or strong H003.

## Computational disposition

No O012 is warranted in this cycle. Exact differentiation of the oscillatory
witness or the lapse chain rule would be a useful regression but would not test
the quantified comparison theorem. A faithful machine proof would require a
formal real-analysis development and materially more infrastructure; that cost
is disproportionate to the transparent two-integrating-factor proof at this
stage. C024 therefore remains `derived` with computational verification
pending/deferred and no active required obligation.

## Epistemic disposition and pruning

Adopt C024 as `derived`, with dimensional and limiting checks passed and
independent verification not requested. C024 generalizes only C023's geometric
input from two explicit rates to every radius in the stated classical endpoint
class. D021, both critiques, D019/D020, and O010/O011 all share OpenAI and
convention provenance; their agreement is correlated rather than independent.

Changing the smooth-flat profile rate or adding another common persistent warp
cannot restore bounded radial-circle curvature while zero endpoint value and
zero proper slope are retained. Do not infer a universal continuum no-go and
do not bundle several escapes.

## Cycle decision and next discriminator

Close `CY005-profile-independent-endpoint`. The next future cycle should test
exactly one least-radical relaxation: replace the zero-slope smooth-flat
attachment by a finite-regularity/nonzero-slope polar-type endpoint while
keeping the torsion-free diagonal geometry and D004/D005 action fixed. The
task must derive the actual interface/distributional variation and decide
whether the open collapsed side remains admissible; `rho=cs` is only a limiting
control, not already a valid background. Do not launch that cycle here.
