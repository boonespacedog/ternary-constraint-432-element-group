# Test Suite

Verifies all claims in v8 paper.

## Tests

- `test_filtration_cascade.py`: Verifies 432→54 cascade (108 deprecated)
- `test_group_structures.py`: Verifies group structures at each level
- `test_generation_property.py`: Verifies generation properties

## Run All Tests

```bash
python -m pytest tests/ -v
```

Expected: All tests pass

## Test Coverage

| Claim | Test | Status |
|-------|------|--------|
| 432 operators with conservation | test_filtration_cascade | ✓ |
| 54 with all three constraints | test_filtration_cascade | ✓ |
| 54-set has structure ((C3 x C3) : C3) : C2 | test_group_structures | ✓ |

## Notes

- The 108 intermediate set was deprecated (based on incorrect constraint interpretation)
- Current test suite focuses on verified 432→54 cascade
- All oracle values from DEFINITIVE_RESULTS_OCT30.md
