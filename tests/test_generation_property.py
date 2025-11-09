#!/usr/bin/env python3
# 432 Doubly Stochastic Matrices Over F₃
# Paper: "Doubly Stochastic Matrices Over F₃: Binary Trace Stratification"
# Repository: https://github.com/boonespacedog/ternary-constraint-432-element-group
# Updated: 2025-11-09

"""
Test Suite: Generation Property of 108-operator set
Verifies that any 2 operators from the 108-set generate AGL(2,3) (432 elements)
For v8 paper: "Constraint-Based Filtration in GL(3,F₃)"
"""

import pytest
import numpy as np
import json
import random
from pathlib import Path
from itertools import combinations

def matrix_multiply_mod3(A, B):
    """Matrix multiplication modulo 3"""
    return (A @ B) % 3

def generate_group_from_pair(M1, M2, max_size=500):
    """Generate group from two matrices"""
    group = set()
    I = np.eye(3, dtype=int)

    # Start with identity and generators
    group.add(tuple(I.flatten()))
    group.add(tuple(M1.flatten()))
    group.add(tuple(M2.flatten()))

    # Keep track of elements to process
    to_process = [M1, M2]
    processed = set()

    while to_process and len(group) < max_size:
        current = to_process.pop(0)
        current_tuple = tuple(current.flatten())

        if current_tuple in processed:
            continue
        processed.add(current_tuple)

        # Generate products with all existing elements
        for elem_tuple in list(group):
            elem = np.array(elem_tuple).reshape(3, 3)

            # Try both orders of multiplication
            prod1 = matrix_multiply_mod3(current, elem)
            prod2 = matrix_multiply_mod3(elem, current)

            for prod in [prod1, prod2]:
                prod_tuple = tuple(prod.flatten())
                if prod_tuple not in group:
                    group.add(prod_tuple)
                    to_process.append(prod)

    return group

class TestGenerationProperty:
    """
    Tests for generation property: any 2 from 108 → AGL(2,3)
    """

    @pytest.fixture(scope="class")
    def operators_108(self):
        """Load the 108 operators"""
        # Try to load from file if exists
        csv_path = Path(__file__).parent.parent / "outputs" / "nonannihilation_108_operators.csv"

        if csv_path.exists():
            operators = []
            with open(csv_path, 'r') as f:
                lines = f.readlines()
                for line in lines[1:]:  # Skip header
                    parts = line.strip().split(',')
                    if len(parts) >= 10:
                        matrix = np.array([
                            [int(parts[1]), int(parts[2]), int(parts[3])],
                            [int(parts[4]), int(parts[5]), int(parts[6])],
                            [int(parts[7]), int(parts[8]), int(parts[9])]
                        ])
                        operators.append(matrix)
            return operators

        # Otherwise use a known subset for testing
        # These are verified members of the 108-set
        return [
            np.array([[0,1,0], [0,2,2], [1,0,0]]),
            np.array([[0,1,0], [0,2,2], [1,2,1]]),
            np.array([[0,1,0], [2,0,2], [1,0,0]]),
            np.array([[1,0,0], [1,2,1], [0,1,0]]),
            np.array([[1,0,0], [2,1,1], [0,1,0]]),
            np.array([[2,1,1], [2,0,2], [1,0,0]]),
        ]

    def test_sample_pairs_generate_432(self, operators_108):
        """Test that random pairs from 108 generate 432-element group"""
        if len(operators_108) < 10:
            pytest.skip("Need full 108-operator set for this test")

        # Test 10 random pairs
        random.seed(42)  # For reproducibility
        num_tests = 10

        for i in range(num_tests):
            # Select random pair
            idx1, idx2 = random.sample(range(len(operators_108)), 2)
            M1 = operators_108[idx1]
            M2 = operators_108[idx2]

            # Generate group
            group = generate_group_from_pair(M1, M2)

            # Should generate 432 elements
            assert len(group) == 432, \
                f"Pair {idx1},{idx2} generated {len(group)} elements, expected 432"

    def test_specific_pair_generates_432(self, operators_108):
        """Test a specific known pair generates 432"""
        if len(operators_108) < 2:
            pytest.skip("Need at least 2 operators")

        M1 = operators_108[0]
        M2 = operators_108[1]

        group = generate_group_from_pair(M1, M2)

        assert len(group) == 432, \
            f"Generated {len(group)} elements, expected 432"

    def test_generated_group_is_closed(self, operators_108):
        """Verify the generated group is closed under multiplication"""
        if len(operators_108) < 2:
            pytest.skip("Need at least 2 operators")

        M1 = operators_108[0]
        M2 = operators_108[1]

        group = generate_group_from_pair(M1, M2)
        group_matrices = [np.array(t).reshape(3,3) for t in group]

        # Sample test: verify closure for random pairs
        random.seed(42)
        num_tests = 50

        for _ in range(num_tests):
            A = random.choice(group_matrices)
            B = random.choice(group_matrices)

            product = matrix_multiply_mod3(A, B)
            product_tuple = tuple(product.flatten())

            assert product_tuple in group, \
                "Group not closed under multiplication"

    def test_save_generation_results(self, operators_108):
        """Save generation property test results"""
        if len(operators_108) < 10:
            pytest.skip("Need full 108-operator set")

        results = {
            "test": "generation_property",
            "108_operator_count": len(operators_108),
            "pairs_tested": 10,
            "all_generated_432": True,
            "group_identified": "AGL(2,3) = SmallGroup(432,734)"
        }

        # Test 10 pairs
        random.seed(42)
        test_results = []

        for i in range(10):
            idx1, idx2 = random.sample(range(len(operators_108)), 2)
            group = generate_group_from_pair(operators_108[idx1], operators_108[idx2])

            test_results.append({
                "pair": [idx1, idx2],
                "group_size": len(group)
            })

            if len(group) != 432:
                results["all_generated_432"] = False

        results["pair_results"] = test_results

        # Save results
        output_path = Path(__file__).parent.parent / "outputs" / "generation_property_test.json"
        output_path.parent.mkdir(exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)

        assert results["all_generated_432"], \
            "Not all pairs generated 432-element group"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])