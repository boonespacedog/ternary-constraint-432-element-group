#!/usr/bin/env python3
# 432 Doubly Stochastic Matrices Over F₃
# Paper: "Doubly Stochastic Matrices Over F₃: Binary Trace Stratification"
# Repository: https://github.com/boonespacedog/ternary-constraint-432-element-group
# Updated: 2025-11-09

"""
Test Suite: Minimal Generating Set Investigation
Find the minimal number of operators from the 108-set needed to generate AGL(2,3)
Based on mathematical formalism in MINIMAL_GENERATING_SET_FORMALISM.md
"""

import numpy as np
import json
import itertools
import random
from pathlib import Path
from typing import List, Set, Tuple, Dict
import time

class MinimalGenerationInvestigator:
    """
    Investigates minimal generating sets from the 108-operator constraint set.
    """

    def __init__(self, operators_108: List[np.ndarray]):
        """Initialize with the 108-operator set."""
        self.operators = operators_108
        self.n_ops = len(operators_108)
        self.identity = np.eye(3, dtype=int)

    def matrix_multiply_mod3(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        """Matrix multiplication modulo 3."""
        return (A @ B) % 3

    def matrix_to_tuple(self, M: np.ndarray) -> tuple:
        """Convert matrix to hashable tuple."""
        return tuple(M.flatten())

    def compute_matrix_order(self, M: np.ndarray, max_order: int = 20) -> int:
        """Compute the order of a matrix in GL(3, F_3)."""
        current = M.copy()
        for n in range(1, max_order + 1):
            if np.array_equal(current % 3, self.identity):
                return n
            current = self.matrix_multiply_mod3(current, M)
        return -1  # Order exceeds max_order

    def generate_group(self, generators: List[np.ndarray], max_size: int = 500) -> Set[tuple]:
        """
        Generate group from list of generators using breadth-first search.
        Returns set of matrix tuples.
        """
        group = set()
        group.add(self.matrix_to_tuple(self.identity))

        # Add generators
        for gen in generators:
            group.add(self.matrix_to_tuple(gen))

        # BFS to generate all elements
        to_process = list(generators)
        processed = set()

        while to_process and len(group) < max_size:
            current = to_process.pop(0)
            current_tuple = self.matrix_to_tuple(current)

            if current_tuple in processed:
                continue
            processed.add(current_tuple)

            # Generate products with all existing elements
            for elem_tuple in list(group):
                elem = np.array(elem_tuple).reshape(3, 3)

                # Both orders of multiplication
                prod1 = self.matrix_multiply_mod3(current, elem)
                prod2 = self.matrix_multiply_mod3(elem, current)

                for prod in [prod1, prod2]:
                    prod_tuple = self.matrix_to_tuple(prod)
                    if prod_tuple not in group:
                        group.add(prod_tuple)
                        if len(group) >= max_size:
                            break
                        to_process.append(prod)

        return group

    def test_single_generators(self) -> Dict:
        """Test if any single operator generates the full group."""
        print("Testing single generators...")
        results = {
            'k': 1,
            'total_tested': self.n_ops,
            'generating_indices': [],
            'max_subgroup_size': 0,
            'order_distribution': {}
        }

        for i in range(self.n_ops):
            group = self.generate_group([self.operators[i]], max_size=432)
            size = len(group)

            if size == 432:
                results['generating_indices'].append(i)

            results['max_subgroup_size'] = max(results['max_subgroup_size'], size)

            # Track order of the generator
            order = self.compute_matrix_order(self.operators[i])
            if order not in results['order_distribution']:
                results['order_distribution'][order] = 0
            results['order_distribution'][order] += 1

            if (i + 1) % 20 == 0:
                print(f"  Tested {i + 1}/{self.n_ops} singles...")

        print(f"  Singles generating 432: {len(results['generating_indices'])}")
        print(f"  Max subgroup from single: {results['max_subgroup_size']}")

        return results

    def test_pairs(self, sample_size: int = None) -> Dict:
        """
        Test pairs of operators for generation.
        If sample_size is None, test all pairs. Otherwise, sample randomly.
        """
        total_pairs = self.n_ops * (self.n_ops - 1) // 2

        if sample_size is None or sample_size >= total_pairs:
            print(f"Testing all {total_pairs} pairs...")
            pairs_to_test = list(itertools.combinations(range(self.n_ops), 2))
        else:
            print(f"Testing {sample_size} random pairs out of {total_pairs}...")
            all_pairs = list(itertools.combinations(range(self.n_ops), 2))
            random.seed(42)  # For reproducibility
            pairs_to_test = random.sample(all_pairs, sample_size)

        results = {
            'k': 2,
            'total_possible': total_pairs,
            'total_tested': len(pairs_to_test),
            'generating_pairs': [],
            'subgroup_sizes': [],
            'size_distribution': {}
        }

        for idx, (i, j) in enumerate(pairs_to_test):
            group = self.generate_group([self.operators[i], self.operators[j]], max_size=432)
            size = len(group)

            if size == 432:
                results['generating_pairs'].append([i, j])

            results['subgroup_sizes'].append(size)

            if size not in results['size_distribution']:
                results['size_distribution'][size] = 0
            results['size_distribution'][size] += 1

            if (idx + 1) % 500 == 0:
                print(f"  Tested {idx + 1}/{len(pairs_to_test)} pairs...")
                print(f"    Found {len(results['generating_pairs'])} generating pairs so far")

        # Calculate statistics
        results['proportion_generating'] = len(results['generating_pairs']) / len(pairs_to_test)
        results['average_subgroup_size'] = np.mean(results['subgroup_sizes'])

        print(f"  Pairs generating 432: {len(results['generating_pairs'])} out of {len(pairs_to_test)}")
        print(f"  Proportion: {results['proportion_generating']:.2%}")

        return results

    def test_triples(self, sample_size: int = 1000) -> Dict:
        """Test random sample of triples."""
        total_triples = self.n_ops * (self.n_ops - 1) * (self.n_ops - 2) // 6

        print(f"Testing {sample_size} random triples out of {total_triples}...")

        all_triples = itertools.combinations(range(self.n_ops), 3)
        random.seed(42)
        # Convert to list for sampling (memory intensive for large sets)
        if sample_size < 10000:
            triples_to_test = []
            for _ in range(sample_size):
                # Generate random triple
                triple = sorted(random.sample(range(self.n_ops), 3))
                triples_to_test.append(triple)
        else:
            # For larger samples, might need streaming approach
            triples_to_test = random.sample(list(itertools.combinations(range(self.n_ops), 3)), sample_size)

        results = {
            'k': 3,
            'total_possible': total_triples,
            'total_tested': len(triples_to_test),
            'generating_triples': [],
            'subgroup_sizes': [],
            'size_distribution': {}
        }

        for idx, triple in enumerate(triples_to_test):
            generators = [self.operators[i] for i in triple]
            group = self.generate_group(generators, max_size=432)
            size = len(group)

            if size == 432:
                results['generating_triples'].append(list(triple))

            results['subgroup_sizes'].append(size)

            if size not in results['size_distribution']:
                results['size_distribution'][size] = 0
            results['size_distribution'][size] += 1

            if (idx + 1) % 100 == 0:
                print(f"  Tested {idx + 1}/{len(triples_to_test)} triples...")
                print(f"    Found {len(results['generating_triples'])} generating triples so far")

        # Calculate statistics
        results['proportion_generating'] = len(results['generating_triples']) / len(triples_to_test)
        results['average_subgroup_size'] = np.mean(results['subgroup_sizes'])

        print(f"  Triples generating 432: {len(results['generating_triples'])} out of {len(triples_to_test)}")
        print(f"  Proportion: {results['proportion_generating']:.2%}")

        return results

    def verify_minimality(self, generating_tuple: List[int]) -> bool:
        """
        Verify that a generating tuple is minimal.
        Returns True if removing any generator reduces the group size.
        """
        k = len(generating_tuple)
        if k == 1:
            return True  # Single generator is minimal by definition

        full_generators = [self.operators[i] for i in generating_tuple]
        full_group = self.generate_group(full_generators, max_size=432)

        if len(full_group) != 432:
            return False  # Not even a generating set

        # Check each subset with one generator removed
        for i in range(k):
            reduced_indices = generating_tuple[:i] + generating_tuple[i+1:]
            reduced_generators = [self.operators[j] for j in reduced_indices]
            reduced_group = self.generate_group(reduced_generators, max_size=432)

            if len(reduced_group) == 432:
                return False  # Not minimal, can remove generator i

        return True

    def find_minimal_k(self) -> Dict:
        """
        Main investigation: Find minimal k and characterize generating sets.
        """
        print("=" * 60)
        print("MINIMAL GENERATING SET INVESTIGATION")
        print("=" * 60)

        start_time = time.time()
        results = {
            'investigation_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'n_operators': self.n_ops,
            'results_by_k': {}
        }

        # Test k=1
        print("\n--- Testing k=1 (single generators) ---")
        single_results = self.test_single_generators()
        results['results_by_k'][1] = single_results

        if single_results['generating_indices']:
            results['minimal_k'] = 1
            results['minimal_examples'] = [[i] for i in single_results['generating_indices'][:10]]
            print(f"\nFOUND: Minimal k = 1")
        else:
            # Test k=2
            print("\n--- Testing k=2 (pairs) ---")
            # For 108 operators, C(108,2) = 5778 is feasible for full enumeration
            pair_results = self.test_pairs(sample_size=None)  # Test all pairs
            results['results_by_k'][2] = pair_results

            if pair_results['generating_pairs']:
                results['minimal_k'] = 2

                # Verify minimality of first few pairs
                print("\nVerifying minimality of generating pairs...")
                minimal_pairs = []
                for pair in pair_results['generating_pairs'][:20]:  # Check first 20
                    if self.verify_minimality(pair):
                        minimal_pairs.append(pair)

                results['minimal_examples'] = minimal_pairs[:10]
                results['verified_minimal'] = len(minimal_pairs)
                print(f"\nFOUND: Minimal k = 2")
                print(f"Verified {len(minimal_pairs)} minimal pairs")
            else:
                # Test k=3
                print("\n--- Testing k=3 (triples) ---")
                triple_results = self.test_triples(sample_size=10000)
                results['results_by_k'][3] = triple_results

                if triple_results['generating_triples']:
                    results['minimal_k'] = 3
                    results['minimal_examples'] = triple_results['generating_triples'][:10]
                    print(f"\nFOUND: Minimal k = 3")
                else:
                    results['minimal_k'] = None
                    print("\nWARNING: No generating sets found up to k=3")

        results['computation_time_seconds'] = time.time() - start_time
        print(f"\nTotal computation time: {results['computation_time_seconds']:.1f} seconds")

        return results


def load_operators_108() -> List[np.ndarray]:
    """Load the 108 operators from file."""
    # Try multiple possible locations
    possible_paths = [
        Path("/Users/mac/Desktop/egg-paper/ternary-constraint-432-element-group/archive/old_outputs/paper1_outputs_oct/conservation_nonannihilation_108_operators.csv"),
        Path(__file__).parent.parent / "outputs" / "conservation_nonannihilation_108_operators.csv",
        Path(__file__).parent.parent / "outputs" / "nonannihilation_108_operators.csv",
        Path(__file__).parent.parent / "outputs" / "verified_108_operators_v5.csv"
    ]

    for csv_path in possible_paths:
        if csv_path.exists():
            print(f"Loading operators from {csv_path}")
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

            print(f"Loaded {len(operators)} operators")
            return operators

    # If no file found, use the known 6 generators from E46
    print("Warning: Using only 6 known generators from E46")
    return [
        np.array([[0,1,0], [0,2,2], [1,0,0]]),
        np.array([[0,1,0], [0,2,2], [1,2,1]]),
        np.array([[0,1,0], [2,0,2], [1,0,0]]),
        np.array([[1,0,0], [1,2,1], [0,1,0]]),
        np.array([[1,0,0], [2,1,1], [0,1,0]]),
        np.array([[2,1,1], [2,0,2], [1,0,0]]),
    ]


def main():
    """Run the minimal generating set investigation."""
    # Load operators
    operators = load_operators_108()

    if len(operators) < 108:
        print(f"WARNING: Only {len(operators)} operators loaded (expected 108)")
        print("Results will be limited\n")

    # Create investigator
    investigator = MinimalGenerationInvestigator(operators)

    # Run investigation
    results = investigator.find_minimal_k()

    # Save results
    output_path = Path(__file__).parent.parent / "outputs" / "minimal_generation_results.json"
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, 'w') as f:
        # Convert numpy types for JSON serialization
        def convert(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj

        json.dump(results, f, indent=2, default=convert)

    print(f"\nResults saved to {output_path}")

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    if 'minimal_k' in results and results['minimal_k']:
        print(f"Minimal k = {results['minimal_k']}")

        k = results['minimal_k']
        k_results = results['results_by_k'][k]

        if k == 1:
            print(f"Found {len(k_results['generating_indices'])} single generators")
        elif k == 2:
            print(f"Found {len(k_results['generating_pairs'])} generating pairs")
            print(f"Proportion of pairs generating: {k_results['proportion_generating']:.2%}")
        elif k == 3:
            print(f"Found {len(k_results['generating_triples'])} generating triples (from sample)")
            print(f"Estimated proportion: {k_results['proportion_generating']:.2%}")

        if 'minimal_examples' in results and results['minimal_examples']:
            print(f"\nExample minimal generating sets:")
            for i, example in enumerate(results['minimal_examples'][:5]):
                print(f"  {i+1}. Operators {example}")
    else:
        print("Could not determine minimal k from available operators")


if __name__ == "__main__":
    main()