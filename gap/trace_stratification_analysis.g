# 432 Doubly Stochastic Matrices Over F₃
# Paper: "Doubly Stochastic Matrices Over F₃: Binary Trace Stratification"
# Repository: https://github.com/boonespacedog/ternary-constraint-432-element-group
# Updated: 2025-11-09

# File: trace_stratification_analysis.g
# Purpose: Verify trace stratification of 54 doubly stochastic matrices
# Author: Oksana Sudoma, Claude (Anthropic)
# Date: 2025-11-09
#
# TDD Protocol Applied:
# - NO hardcoded expectations (18-18-18)
# - Independent enumeration from GL(3,F₃)
# - Report actual results, do NOT compare to expected values
# - Provenance: All matrices enumerated from first principles
#
# Anti-patterns AVOIDED:
# - ❌ NO "if Length(trace_0) = 18 then Print('PASS')"
# - ❌ NO loading from JSON to verify enumeration
# - ❌ NO fitting to expected distributions
#
# What this script DOES:
# - ✅ Enumerate all doubly stochastic matrices independently
# - ✅ Compute trace for each matrix from diagonal elements
# - ✅ Stratify by trace value (mod 3)
# - ✅ Report actual distribution (let it be discovery)
# - ✅ Verify group structure properties

LoadPackage("SmallGrp");

# === FIELD AND GROUP SETUP ===
F3 := GF(3);
GL3F3 := GL(3, F3);

Print("========================================\n");
Print("TRACE STRATIFICATION ANALYSIS\n");
Print("========================================\n\n");

# === CONSTRAINT CHECKING FUNCTIONS ===

# CheckDoublyStochastic: Verify both row AND column sums ≡ 1 (mod 3)
# Provenance: Independent checks, no assumption of relationship
CheckDoublyStochastic := function(M)
    local i, j, row_sum, col_sum;

    # Check row sums independently
    for i in [1..3] do
        row_sum := (M[i][1] + M[i][2] + M[i][3]) mod 3;
        if row_sum <> 1 then
            return false;
        fi;
    od;

    # Check column sums independently
    for j in [1..3] do
        col_sum := (M[1][j] + M[2][j] + M[3][j]) mod 3;
        if col_sum <> 1 then
            return false;
        fi;
    od;

    return true;
end;

# ComputeTrace: Compute trace from diagonal elements
# Provenance: Direct calculation, no external dependencies
ComputeTrace := function(M)
    return (M[1][1] + M[2][2] + M[3][3]) mod 3;
end;

# === ENUMERATION FROM FIRST PRINCIPLES ===

Print("Phase 1: Enumerating doubly stochastic matrices from GL(3,F₃)...\n");

all_elements := Elements(GL3F3);
Print("Total GL(3,F₃) elements: ", Size(GL3F3), "\n\n");

doubly_stochastic := [];

for g in all_elements do
    M := List(g, row -> List(row, x -> IntFFE(x)));

    if CheckDoublyStochastic(M) then
        Add(doubly_stochastic, M);
    fi;
od;

# Report ACTUAL count (not "expected")
Print("Found ", Length(doubly_stochastic), " doubly stochastic matrices\n");
Print("(No expectations - this is the discovered count)\n\n");

# === TRACE STRATIFICATION ===

Print("Phase 2: Stratifying by trace (mod 3)...\n");

# Initialize trace classes
trace_distribution := [[], [], []];  # Lists for trace 0, 1, 2

for M in doubly_stochastic do
    trace_val := ComputeTrace(M);

    # Add to appropriate class
    # trace_val is in {0,1,2}, use as index+1 for GAP 1-indexing
    Add(trace_distribution[trace_val + 1], M);
od;

# Report actual distribution
Print("\nTrace Stratification (actual results):\n");
for k in [0..2] do
    Print("  Trace ≡ ", k, " (mod 3): ", Length(trace_distribution[k+1]), " matrices\n");
od;
Print("\n");

# === GROUP STRUCTURE ANALYSIS ===

Print("Phase 3: Analyzing group structure...\n");

# Create group from doubly stochastic matrices
# Convert integer matrices to F₃ matrices for GAP group operations
ds_group_matrices := [];
for M in doubly_stochastic do
    gap_matrix := List(M, row -> List(row, x -> x * One(F3)));
    Add(ds_group_matrices, gap_matrix);
od;

# Create group object
G_ds := Group(ds_group_matrices);

Print("Doubly Stochastic Group Properties:\n");
Print("  Order: ", Size(G_ds), "\n");
Print("  Structure: ", StructureDescription(G_ds), "\n");

# Compute center
Z_center := Center(G_ds);
Print("  Center order: ", Size(Z_center), "\n");
Print("  Center structure: ", StructureDescription(Z_center), "\n\n");

# === SAVE RESULTS TO JSON ===

output_file := "../outputs/trace_stratification.json";

PrintTo(output_file, "{\n");
AppendTo(output_file, "  \"metadata\": {\n");
AppendTo(output_file, "    \"experiment\": \"432_stochastic_cascade\",\n");
AppendTo(output_file, "    \"script\": \"trace_stratification_analysis.g\",\n");
AppendTo(output_file, "    \"date\": \"2025-11-09\",\n");
AppendTo(output_file, "    \"gap_version\": \"4.12.2\",\n");
AppendTo(output_file, "    \"provenance\": \"Independent enumeration from GL(3,F3)\",\n");
AppendTo(output_file, "    \"anti_patterns_avoided\": [\"no_hardcoded_expectations\", \"no_circular_dependencies\"]\n");
AppendTo(output_file, "  },\n");
AppendTo(output_file, "  \"results\": {\n");
AppendTo(output_file, "    \"total_doubly_stochastic\": ", Length(doubly_stochastic), ",\n");
AppendTo(output_file, "    \"trace_0_count\": ", Length(trace_distribution[1]), ",\n");
AppendTo(output_file, "    \"trace_1_count\": ", Length(trace_distribution[2]), ",\n");
AppendTo(output_file, "    \"trace_2_count\": ", Length(trace_distribution[3]), ",\n");
AppendTo(output_file, "    \"group_order\": ", Size(G_ds), ",\n");
AppendTo(output_file, "    \"group_structure\": \"", StructureDescription(G_ds), "\",\n");
AppendTo(output_file, "    \"center_order\": ", Size(Z_center), ",\n");
AppendTo(output_file, "    \"center_structure\": \"", StructureDescription(Z_center), "\"\n");
AppendTo(output_file, "  },\n");

# Save matrices by trace class
AppendTo(output_file, "  \"matrices_by_trace\": {\n");

for k in [0..2] do
    AppendTo(output_file, "    \"trace_", k, "\": [\n");

    for i in [1..Length(trace_distribution[k+1])] do
        M := trace_distribution[k+1][i];
        AppendTo(output_file, "      [[",
            M[1][1], ",", M[1][2], ",", M[1][3], "],[",
            M[2][1], ",", M[2][2], ",", M[2][3], "],[",
            M[3][1], ",", M[3][2], ",", M[3][3], "]]");

        if i < Length(trace_distribution[k+1]) then
            AppendTo(output_file, ",\n");
        else
            AppendTo(output_file, "\n");
        fi;
    od;

    if k < 2 then
        AppendTo(output_file, "    ],\n");
    else
        AppendTo(output_file, "    ]\n");
    fi;
od;

AppendTo(output_file, "  }\n");
AppendTo(output_file, "}\n");

Print("Results saved to: ", output_file, "\n\n");

# === SUMMARY (ACTUAL RESULTS, NO EXPECTATIONS) ===

Print("========================================\n");
Print("SUMMARY\n");
Print("========================================\n");
Print("Doubly stochastic matrices found: ", Length(doubly_stochastic), "\n");
Print("Trace distribution:\n");
Print("  tr≡0: ", Length(trace_distribution[1]), "\n");
Print("  tr≡1: ", Length(trace_distribution[2]), "\n");
Print("  tr≡2: ", Length(trace_distribution[3]), "\n");
Print("Group structure: ", StructureDescription(G_ds), "\n");
Print("Center: ", StructureDescription(Z_center), " (order ", Size(Z_center), ")\n");
Print("========================================\n");

QUIT;
