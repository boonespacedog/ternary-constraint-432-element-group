# GAP Enumeration Scripts

## Main Results

- `enum_conservation.g`: Finds 432 operators (conservation only)
- `enum_v5_working.g`: Finds 108 operators (conservation + non-annihilation)
- `enum_v5_all_three.g`: Finds 54 operators (all three constraints)

## Usage

```bash
gap enum_conservation.g        # → 432 operators
gap enum_v5_working.g          # → 108 operators
gap enum_v5_all_three.g        # → 54 operators
```

## Output

Results saved to `../outputs/`:
- `conservation_432_operators.csv`
- `nonannihilation_108_operators.csv`
- `all_constraints_54_operators.json`

## Execution Time

Each script runs in approximately 1-2 minutes on modern hardware.