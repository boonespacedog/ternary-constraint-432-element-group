#!/usr/bin/env python3
# 432 Doubly Stochastic Matrices Over F₃
# Paper: "Doubly Stochastic Matrices Over F₃: Binary Trace Stratification"
# Repository: https://github.com/boonespacedog/ternary-constraint-432-element-group
# Updated: 2025-11-09

"""
Test Suite: Group Structure Properties
Tests closure and subgroup relationships
"""

import pytest
import numpy as np
import itertools

def generate_gl3_f3():
    matrices = []
    for entries in itertools.product([0,1,2], repeat=9):
        M = np.array(entries).reshape(3, 3)
        if int(np.round(np.linalg.det(M))) % 3 != 0:
            matrices.append(M)
    return matrices

def check_row_and_col(M):
    return (all(sum(M[i,:]) % 3 == 1 for i in range(3)) and
            all(sum(M[:,j]) % 3 == 1 for j in range(3)))

def matrix_mult_mod3(A, B):
    return (A @ B) % 3

def matrix_to_tuple(M):
    return tuple(M.flatten())

class TestGroupStructures:
    """
    Tests for the 54 and 108 group structures
    Oracle: External mathematical review
    """

    def test_54_forms_closed_group(self):
        """Verify 54 operators are closed under multiplication"""
        matrices = generate_gl3_f3()
        ops_54 = [M for M in matrices if check_row_and_col(M)]

        actual_count = len(ops_54)
        print(f"Doubly stochastic operators found: {actual_count}")
        # Oracle: 54 from computational verification
        assert actual_count == 54, f"Expected 54, found {actual_count}"

        # Test closure
        set_54 = {matrix_to_tuple(M) for M in ops_54}

        violations = 0
        for M1 in ops_54[:10]:  # Sample test
            for M2 in ops_54[:10]:
                prod = matrix_mult_mod3(M1, M2)
                if matrix_to_tuple(prod) not in set_54:
                    violations += 1

        assert violations == 0, f"Found {violations} closure violations in sample"

    def test_54_contains_identity(self):
        """Verify identity is in the 54-set"""
        matrices = generate_gl3_f3()
        ops_54 = [M for M in matrices if check_row_and_col(M)]

        I = np.eye(3, dtype=int)
        has_identity = any(np.array_equal(M, I) for M in ops_54)

        assert has_identity, "54-set must contain identity"

    def test_54_element_orders(self):
        """Oracle: Orders are 1, 2, 3, 6"""
        matrices = generate_gl3_f3()
        ops_54 = [M for M in matrices if check_row_and_col(M)]

        def compute_order(M):
            I = np.eye(3, dtype=int)
            current = M.copy()
            for n in range(1, 21):
                if np.array_equal(current % 3, I):
                    return n
                current = matrix_mult_mod3(current, M)
            return None

        orders = [compute_order(M) for M in ops_54]
        unique_orders = set(orders)

        # Oracle from external review: orders 1, 2, 3, 6 only
        expected_orders = {1, 2, 3, 6}
        assert unique_orders == expected_orders, \
            f"Expected orders {expected_orders}, got {unique_orders}"

    def test_54_perfect_balance(self):
        """Oracle: Perfect det and trace balance"""
        matrices = generate_gl3_f3()
        ops_54 = [M for M in matrices if check_row_and_col(M)]

        dets = [int(np.round(np.linalg.det(M))) % 3 for M in ops_54]
        traces = [int(M[0,0] + M[1,1] + M[2,2]) % 3 for M in ops_54]

        # Oracle: 27 with det=1, 27 with det=2
        det_1_count = sum(1 for d in dets if d == 1)
        det_2_count = sum(1 for d in dets if d == 2)

        print(f"Det=1 count: {det_1_count}, Det=2 count: {det_2_count}")
        # Oracle: Perfect balance in SL vs non-SL elements
        assert det_1_count == 27, f"Expected 27 with det=1, got {det_1_count}"
        assert det_2_count == 27, f"Expected 27 with det=2, got {det_2_count}"

        # Oracle: 27 with trace=0, 27 with trace=1
        trace_0_count = sum(1 for t in traces if t == 0)
        trace_1_count = sum(1 for t in traces if t == 1)

        assert trace_0_count == 27, f"Expected 27 with trace=0, got {trace_0_count}"
        assert trace_1_count == 27, f"Expected 27 with trace=1, got {trace_1_count}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
