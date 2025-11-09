# Computational Results

Fresh outputs generated for v8 paper publication.

## Files

| File | Description | Count |
|------|-------------|-------|
| `row_stochastic_432.csv` | Row stochastic matrices (conservation only) | 432 operators |
| `doubly_stochastic_54.json` | Doubly stochastic matrices (all constraints) | 54 operators |
| `trace_stratification.json` | Trace stratification of 54 operators | 27+27+0 |
| `group_structure_verification.json` | Group structure verification | ((C3 x C3) : C3) : C2 |

## Verification

All results reproduced on: November 9, 2025
Platform: macOS (M1)
GAP version: 4.12.2
Python version: 3.13.7

## Key Findings

- 432 operators satisfy conservation (row sums ≡ 1 mod 3)
- 54 operators satisfy doubly stochastic constraints (row AND column sums ≡ 1 mod 3)
- Trace stratification: 27 with trace≡0, 27 with trace≡1, 0 with trace≡2
- Group structure: ((C3 x C3) : C3) : C2 of order 54
