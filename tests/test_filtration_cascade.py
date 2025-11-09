#!/usr/bin/env python3
# 432 Doubly Stochastic Matrices Over F₃
# Paper: "Doubly Stochastic Matrices Over F₃: Binary Trace Stratification"
# Repository: https://github.com/boonespacedog/ternary-constraint-432-element-group
# Updated: 2025-11-09

"""
Test Suite: Constraint Filtration Cascade
Oracle values from DEFINITIVE_RESULTS_OCT30.md
"""

import pytest
import numpy as np
import itertools

def generate_gl3_f3():
    """Generate all GL(3,F_3) matrices"""
    matrices = []
    for entries in itertools.product([0,1,2], repeat=9):
        M = np.array(entries).reshape(3, 3)
        if int(np.round(np.linalg.det(M))) % 3 != 0:
            matrices.append(M)
    return matrices

def check_conservation(M):
    """Row sums = 1 (mod 3)"""
    return all(sum(M[i,:]) % 3 == 1 for i in range(3))

def check_normalizes_h(M):
    """Preserves kernel H = ker([1,1,1])"""
    H_basis = [np.array([1,2,0]), np.array([0,1,2])]
    for v in H_basis:
        if sum((M @ v) % 3) % 3 != 0:
            return False
    for a in [0,1,2]:
        for b in [0,1,2]:
            if a == 0 and b == 0:
                continue
            v = (a * H_basis[0] + b * H_basis[1]) % 3
            if sum((M @ v) % 3) % 3 != 0:
                return False
    return True

def check_row_and_col(M):
    """Both row AND column sums = 1 (mod 3)"""
    return (all(sum(M[i,:]) % 3 == 1 for i in range(3)) and
            all(sum(M[:,j]) % 3 == 1 for j in range(3)))

class TestFiltrationCascade:
    """
    Oracle tests for constraint filtration
    Source: DEFINITIVE_RESULTS_OCT30.md
    """

    def test_gl3_f3_total_size(self):
        """Oracle: |GL(3,F₃)| = 11,232"""
        matrices = generate_gl3_f3()
        assert len(matrices) == 11232, f"Expected 11232, got {len(matrices)}"

    def test_conservation_only_yields_432(self):
        """Oracle: 432 operators with conservation only (computational enumeration)"""
        """Oracle: 432 operators with conservation only"""
        matrices = generate_gl3_f3()
        conservation_ops = [M for M in matrices if check_conservation(M)]
        # Oracle expectation based on computational enumeration
        actual_count = len(conservation_ops)
        print(f"Conservation operators found: {actual_count}")
        # Expected: 432 from GAP enumeration (Oct 2025)
        assert actual_count == 432, \
            f"Expected 432 with conservation, got {len(conservation_ops)}"

    def test_three_constraints_yield_54(self):
        """Oracle: 54 operators with doubly stochastic constraints"""
        """Oracle: 54 operators with all 3 constraints (doubly stochastic)"""
        matrices = generate_gl3_f3()
        three_constraint_ops = [M for M in matrices if check_row_and_col(M)]
        # Oracle expectation: Doubly stochastic subset
        actual_count = len(three_constraint_ops)
        print(f"Doubly stochastic operators found: {actual_count}")
        # Expected: 54 from GAP enumeration (verified Oct 2025)
        assert actual_count == 54, \
            f"Expected 54 with 3 constraints, got {len(three_constraint_ops)}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
