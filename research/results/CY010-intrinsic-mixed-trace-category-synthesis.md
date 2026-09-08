# CY010 synthesis: boundary-trace connection descent

## Bounded question and frozen regime

`CY010-intrinsic-mixed-trace-category` asked whether the finite polar tangent

```text
delta omega^{43} = delta chi^{43} dtheta
```

is admitted, gauge, or excluded by one explicit lower-regularity connection
category. The cycle kept the exact C025 topology, `rho=c s_+`, flat punctured
bulks, fixed interface, and persistent D005 sector unchanged. It added no action,
counterterm, source, moving interface, canonical reduction, or PDE problem.

The sole theory branch was preallocated as
`research/derivations/D026.md`. Its first internal critique identified a scope
overreach from boundary descent to an unproved full connection calculus on the
singular quotient collar. D026 was narrowed to the boundary-trace theorem and a
fresh critique found no blocking issue. Both producer and critics used
`openai/gpt-5.6-sol`; this is procedural separation, not independent evidence.

## Evidence inventory

| Item | Type and regime | Result | Epistemic weight |
|---|---|---|---|
| `research/derivations/D026.md` | Exact local theory for `C1` tangential connection traces on `Y=Sigma x S1` and ordinary descent along `p:Y->Sigma` | Defines `TrConn_lr(p)`, proves its object and tangent criteria, and classifies the constant polar trace | Primary derived evidence for C029 |
| `research/critiques/D026-2026-08-23-openai-01.md` | Frozen same-model attack | `revision-required`: the original boundary equations did not control collar-normal data or establish a connection on `X_+` | Adverse history; forced the decisive scope repair |
| `research/critiques/D026-2026-08-23-openai-02.md` | Fresh same-model re-critique of the repaired artifact | `no-blocking-issue-found`; cocycle signs, holonomy criterion, tangent exclusion, and scope boundary survived | Correlated internal review, not independent evidence |
| O012 | Existing exact obligation for C025's broader free-tangent class | `passed`, 29/29; confirms the mixed D004 row and absent D005 incidence | Does not test tangent admissibility |
| O014/O015 | Existing exact obligations for C027/C028 | `passed`, 46/46 and 32/32 respectively | Assume or inherit the broader finite tangent; do not decide boundary descent |

No exploratory-literature report or focused source is used as evidence for the
new theorem. The available `SO(1,4)/SO(1,3)` source packet supplies only a
neighboring kinematic reduction template, not rank-changing connection descent.

## Exact category and result

The repaired category is deliberately a **boundary-trace** category. Let

```text
p : Y = Sigma x S1 -> Sigma,
R_p = Y x_Sigma Y.
```

An object of `TrConn_lr(p)` is a `C1` tangential connection trace `a` together
with a kernel-pair isomorphism `gamma` satisfying the cocycle and affine descent
equations

```text
gamma_12 gamma_23 = gamma_13,
p_1^* a = gamma p_2^* a gamma^{-1} - d gamma gamma^{-1}.
```

Under local bundle triviality, D026 proves the necessary-and-sufficient
criterion

```text
H_u[a] = 1,
i_(partial_theta) F_a = 0
```

for descent of the trace along `p` to a local connection on `Sigma`. Identity
fiber holonomy makes the vertical parallel-transport frame periodic; in that
frame `a_theta=0`, and zero vertical curvature makes all horizontal coefficients
fiber-independent. The converse follows from pullback connection data.

For

```text
a = c T_43 dtheta,
```

the curvature condition is automatic and the object criterion becomes

```text
exp(2 pi c T_43) = 1.
```

Thus generic `c` is excluded from `TrConn_lr(p)`. In standard vector
normalization the allowed values are the integer lattice, with `c=1` the first
positive value. At an allowed value,

```text
H^{-1} delta H = 2 pi delta chi T_43,
```

so a constant nonzero `delta chi` fails linearized descent. A periodic
infinitesimal presentation parameter would require
`-partial_theta epsilon=delta chi T_43`, whose circle integral likewise forces
`delta chi=0`. Allowing the cocycle to vary does not evade identity holonomy.

At an integer value the finite winding map sends `(a,gamma_c)` to `(0,1)`. This
is an isomorphism of boundary descent presentations. It is not an infinitesimal
path between lattice points, not an automorphism preserving the original
cocycle, and not an adapted `SO(1,3)_V` transformation. For the canonical Spin
lift of the vector-normalized generator, a `2 pi` rotation is `-1`, so identity
holonomy uses the doubled/even lattice.

## Scope repair and non-result

The first critique supplied the counterexample `A=f(theta) ds`: its tangential
trace is zero and passes the boundary criterion, while its collar curvature has
`f'(theta)dtheta wedge ds`. D026 now uses this example to state exactly what it
does **not** prove. `TrConn_lr(p)` controls neither collar-normal coefficients nor
mixed normal-angular curvature, and it does not define a connection sheaf on
the singular quotient `X_+`.

Connection-only trace descent also cannot be promoted to descent of the pair
`(A,V)`. For frozen adapted `V=e_4`,

```text
D_theta V = c T_43 V != 0
```

at every positive `c`; the stronger pair category would therefore exclude even
the connection-only `c=1` presentation. Selecting between connection-only trace
descent, pair descent, a full weak collar category, and a non-effective category
retaining circle isotropy remains a physical/modeling decision.

## Claim and hypothesis disposition

- **C029 is adopted as `derived`.** It records only the exact boundary-trace
  descent theorem and polar classification above.
- **C025 remains true in its broader declared tangent class.** C029 does not
  cancel its mixed Palatini row; on the narrower trace category the row is
  avoided because the constant tangent is absent. Generic polar traces are not
  objects, while lattice traces lie on fixed descent leaves.
- **C027 remains true.** Its coframe equation forcing `c=0` and its reduction
  field are not removed by connection-only boundary descent. Requiring `(A,V)`
  descent is strictly stronger and excludes positive `c` directly.
- **C028 remains true in its free-tangent algebraic class.** On the narrower
  C029 leaf the demand to cancel the forbidden constant tangent becomes moot;
  this changes which theorem controls the preferred model, not C028's truth.
- **H001/H002:** C029 supplies a coherent local boundary equivalence mechanism,
  but only after selecting a descent leaf and without a full quotient collar or
  action. It is not support for a complete intrinsic or resolution-equivalent
  dynamics.
- **H003:** generic polar connection traces are excluded in this one category,
  but the discrete connection-only sector survives and no continuum no-go
  follows.

## Computational disposition

No O016 is allocated. The cocycle multiplication, factor `2 pi`, and periodic
integral are transparent finite identities, but checking them would only encode
the selected category. It would not decide whether boundary-trace descent is
the physically correct category, extend it to the singular collar, or select
connection-only versus `(A,V)` descent. C029 therefore records
`computational_verification: not-applicable` for the current strategy. Failed or
passing prior obligations remain unchanged.

## Portfolio decision

Close CY010. The cycle gives a real answer only after making the category
explicit:

```text
generic c:       boundary trace excluded;
identity lattice: trace admitted as a discrete presentation,
                  constant nonzero delta chi excluded, not infinitesimal gauge;
pair (A,V):       every positive adapted polar trace fails the stronger test.
```

Do not reopen an unbounded curvature/higher-`K` action search on the basis of
C029. The next high-information task, if another cycle is authorized, is to
decide which **full field object** must descend—connection trace alone, the
reduction pair, or a specified weak collar connection—and to derive its
compatibility with the complete variational field space. Until then, no
functional preservation, mixed moment-map, hyperbolicity, or defect computation
is justified.
