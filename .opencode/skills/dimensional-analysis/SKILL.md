---
name: dimensional-analysis
description: Use to check equation dimensions and units, construct natural scales or Buckingham-pi groups, identify dimensionless control parameters, and detect inconsistent unit conventions in physics work.
compatibility: OpenCode 1.18+
metadata:
  domain: theoretical-physics
  operation: consistency-check
---

# Dimensional Analysis

## 1. Fix the unit system

State the independent base dimensions and whether constants such as `c`, `hbar`, or `k_B` are set to one. Record conversions needed to restore them. Do not mix SI, Gaussian, Heaviside-Lorentz, lattice, or natural-unit conventions silently.

## 2. Inventory quantities

List every independent dimensional input, output, coupling, coordinate, derivative, measure, field normalization, and boundary parameter. Assign dimensions symbolically before substituting numbers.

## 3. Check equations locally

For each important equality, sum, exponent, logarithm, trigonometric argument, delta function, transform, action, probability, and integration measure:

- verify matching dimensions term by term;
- restore suppressed constants where useful;
- check factors introduced by variable changes;
- check reported units on numerical values and axes.

Stop at the first mismatch and identify candidate missing scales instead of forcing agreement.

## 4. Identify natural scales

Construct characteristic length, time, energy, momentum, temperature, field, or density scales from the independent quantities. Explain why each scale is physically relevant and note non-unique choices.

## 5. Form dimensionless groups

When appropriate, build the dimensional matrix, determine its rank, and construct independent Buckingham-pi groups. Relate them to known control parameters such as coupling strengths, Reynolds-like numbers, adiabaticity parameters, or finite-size ratios.

## 6. Test scaling claims

Rewrite the target relation in dimensionless form. Check asymptotic powers, extensive/intensive scaling, and whether fitted coefficients carry hidden units. Dimensional consistency is necessary, not sufficient, for correctness.

## 7. Record the check

Add a concise table of symbols and dimensions plus pass/fail findings to the relevant derivation, experiment, claim check, or verification report. Use `not-applicable` only with a reason. A passed dimensional check does not independently verify the claim.
