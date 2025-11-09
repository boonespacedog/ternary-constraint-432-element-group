# Doubly Stochastic Matrices Over F₃

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.17443365-blue.svg)](https://doi.org/10.5281/zenodo.17443365)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Computational verification code for**: "Doubly Stochastic Matrices Over F₃: Binary Trace Stratification and the Impossibility of Trace-2"

**Author**: Oksana Sudoma
**Status**: Pre-print

---

## Overview

This repository provides complete computational verification for the first enumeration of doubly stochastic 3×3 matrices over the finite field F₃. We discover 54 such matrices forming group DS₃(F₃) ≅ ((C₃ × C₃) : C₃) : C₂, and prove that their trace values exhibit binary stratification: 27 matrices with trace ≡ 0, 27 with trace ≡ 1, and **0 with trace ≡ 2**—a constraint-induced F₃→F₂ field reduction.

**Key discoveries**:
- **54 doubly stochastic matrices** over F₃ (first enumeration)
- **27-27-0 trace distribution** (binary stratification)
- **Trace-2 impossibility** (proven algebraically)
- **432-element row-stochastic group** ≅ AGL(2,3)

---

## Quick Start

### Prerequisites

- GAP 4.12.2+ ([download](https://www.gap-system.org))
- Python 3.9+
- pytest (install: `pip install pytest`)

### One-Command Verification

```bash
# Run all GAP computations (generates 4 output files)
python3 run_all_verifications.py

# Expected runtime: 5-10 minutes
# Outputs: row_stochastic_432.csv, doubly_stochastic_54.json,
#          trace_stratification.json, group_structure_verification.json
```

### Run Tests

```bash
python3 -m pytest tests/ -v

# Expected: 7 tests passing
```

---

## Main Results

### Constraint Cascade

| Constraint | Count | Group Structure | Description |
|------------|-------|-----------------|-------------|
| Row-stochastic (row sums ≡ 1) | 432 | AGL(2,3) ≅ (((C₃×C₃):Q₈):C₃):C₂ | Affine general linear group |
| Doubly stochastic (+column sums ≡ 1) | 54 | DS₃(F₃) ≅ ((C₃×C₃):C₃):C₂ | Index-8 subgroup with center C₃ |

### Trace Distribution (Novel Discovery)

| Trace Value | Count | Interpretation |
|-------------|-------|----------------|
| tr(M) ≡ 0 (mod 3) | 27 | Normal subgroup (kernel) |
| tr(M) ≡ 1 (mod 3) | 27 | Unique coset |
| tr(M) ≡ 2 (mod 3) | **0** | Proven impossible (all trace-2 matrices singular) |

**Mathematical significance**: First documented case of constraint-induced field reduction (F₃→F₂) in finite matrix groups.

---

## Repository Structure

```
ternary-constraint-432-element-group/
├── gap/                    GAP enumeration scripts (4 files)
│   ├── enum_row_stochastic.g
│   ├── enum_doubly_stochastic.g
│   ├── trace_stratification_analysis.g
│   └── verify_group_structures.g
├── outputs/                Verified computational results (4 files)
│   ├── row_stochastic_432.csv
│   ├── doubly_stochastic_54.json
│   ├── trace_stratification.json
│   └── group_structure_verification.json
├── tests/                  Python verification suite (3 test files)
├── run_all_verifications.py
└── README.md
```

---

## Mathematical Background

**Doubly stochastic matrices** satisfy both:
- Row sums: Σⱼ Mᵢⱼ ≡ 1 (mod 3) for all rows i
- Column sums: Σᵢ Mᵢⱼ ≡ 1 (mod 3) for all columns j

Working over finite field F₃ = {0,1,2}, these constraints define a 54-element group—the first such enumeration in the literature. Prior work explicitly excluded F₃ from general theorems (Linear Algebra and Its Applications, 1976).

**Novel phenomenon**: Despite operating in ternary field F₃, the trace observable takes values only in binary field F₂ = {0,1}. This F₃→F₂ reduction arises from the doubly stochastic constraint geometry.

---

## Reproducibility

All results are computationally verified and fully reproducible:

1. **Run complete suite**: `python3 run_all_verifications.py`
2. **Individual scripts**: `gap gap/enum_doubly_stochastic.g`
3. **Verification tests**: `python3 -m pytest tests/ -v`

Expected runtime: 5-10 minutes on standard hardware.

---

## Citation

```bibtex
@misc{sudoma2025doubly,
  author = {Sudoma, Oksana},
  title = {Doubly Stochastic Matrices Over $\mathbb{F}_3$: Binary Trace Stratification and the Impossibility of Trace-2},
  year = {2025},
  doi = {10.5281/zenodo.17443365},
  url = {https://github.com/boonespacedog/ternary-constraint-432-element-group}
}
```

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Author

**Oksana Sudoma** - Independent Researcher

Computational verification and literature review assisted by Claude (Anthropic) and ChatGPT (OpenAI). Mathematical formalism and scientific conclusions are the author's sole responsibility.

---

## Links

- **Repository**: https://github.com/boonespacedog/ternary-constraint-432-element-group
- **Zenodo Archive**: https://doi.org/10.5281/zenodo.17443365
- **Paper**: See repository for latest version
