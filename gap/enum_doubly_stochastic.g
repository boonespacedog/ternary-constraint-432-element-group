# 432 Doubly Stochastic Matrices Over F₃
# Paper: "Doubly Stochastic Matrices Over F₃: Binary Trace Stratification"
# Repository: https://github.com/boonespacedog/ternary-constraint-432-element-group
# Updated: 2025-11-09

# File: enum_all_three_fixed.g
# Purpose: Enumerate GL(3,F₃) operators with all three constraints
# Finds 54 operators with conservation, non-annihilation, and phase rigidity
# For v8 paper: "Constraint-Based Filtration in GL(3,F₃)"

LoadPackage("SmallGrp");

# Field
F3 := GF(3);
GL3F3 := GL(3, F3);

# CheckConservation: Row sums ≡ 1 mod 3
CheckConservation := function(M)
    local i, row_sum;
    for i in [1..3] do
        row_sum := (M[i][1] + M[i][2] + M[i][3]) mod 3;
        if row_sum <> 1 then
            return false;
        fi;
    od;
    return true;
end;

# CheckPhaseRigidity: Column sums ≡ 1 mod 3
CheckPhaseRigidity := function(M)
    local j, col_sum;
    for j in [1..3] do
        col_sum := (M[1][j] + M[2][j] + M[3][j]) mod 3;
        if col_sum <> 1 then
            return false;
        fi;
    od;
    return true;
end;

# CheckNonAnnihilation: Preserves H = ker([1,1,1])
# Test with basis vectors of H
CheckNonAnnihilation := function(M)
    local v, w, sum_w;

    # Test basis vector (1,2,0)
    v := [1, 2, 0];
    w := [(v[1]*M[1][1] + v[2]*M[2][1] + v[3]*M[3][1]) mod 3,
          (v[1]*M[1][2] + v[2]*M[2][2] + v[3]*M[3][2]) mod 3,
          (v[1]*M[1][3] + v[2]*M[2][3] + v[3]*M[3][3]) mod 3];
    sum_w := (w[1] + w[2] + w[3]) mod 3;
    if sum_w <> 0 then
        return false;
    fi;

    # Test basis vector (0,1,2)
    v := [0, 1, 2];
    w := [(v[1]*M[1][1] + v[2]*M[2][1] + v[3]*M[3][1]) mod 3,
          (v[1]*M[1][2] + v[2]*M[2][2] + v[3]*M[3][2]) mod 3,
          (v[1]*M[1][3] + v[2]*M[2][3] + v[3]*M[3][3]) mod 3];
    sum_w := (w[1] + w[2] + w[3]) mod 3;
    if sum_w <> 0 then
        return false;
    fi;

    return true;
end;

# Main enumeration
Print("========================================\n");
Print("Enumerating GL(3,F₃) with all 3 constraints\n");
Print("========================================\n\n");

all_elements := Elements(GL3F3);
Print("Total GL(3,F₃) elements: ", Size(GL3F3), "\n\n");

# Apply filters progressively to see cascade
conservation_ops := [];
two_constraint_ops := [];
three_constraint_ops := [];

for g in all_elements do
    M := List(g, row -> List(row, x -> IntFFE(x)));

    # Check conservation
    if CheckConservation(M) then
        Add(conservation_ops, M);

        # Check non-annihilation
        if CheckNonAnnihilation(M) then
            Add(two_constraint_ops, M);

            # Check phase rigidity
            if CheckPhaseRigidity(M) then
                Add(three_constraint_ops, M);
            fi;
        fi;
    fi;
od;

Print("=== FILTRATION CASCADE ===\n");
Print("Conservation only: ", Length(conservation_ops), " operators\n");
Print("+ Non-annihilation: ", Length(two_constraint_ops), " operators\n");
Print("+ Phase rigidity: ", Length(three_constraint_ops), " operators\n\n");

# Save all three sets
# 1. Conservation only (432 expected)
output_file := "../outputs/conservation_only_432.csv";
PrintTo(output_file, "index,m00,m01,m02,m10,m11,m12,m20,m21,m22\n");
for i in [1..Length(conservation_ops)] do
    M := conservation_ops[i];
    AppendTo(output_file,
        String(i), ",",
        String(M[1][1]), ",", String(M[1][2]), ",", String(M[1][3]), ",",
        String(M[2][1]), ",", String(M[2][2]), ",", String(M[2][3]), ",",
        String(M[3][1]), ",", String(M[3][2]), ",", String(M[3][3]), "\n");
od;

# 2. Two constraints (108 expected)
output_file := "../outputs/two_constraints_108.csv";
PrintTo(output_file, "index,m00,m01,m02,m10,m11,m12,m20,m21,m22\n");
for i in [1..Length(two_constraint_ops)] do
    M := two_constraint_ops[i];
    AppendTo(output_file,
        String(i), ",",
        String(M[1][1]), ",", String(M[1][2]), ",", String(M[1][3]), ",",
        String(M[2][1]), ",", String(M[2][2]), ",", String(M[2][3]), ",",
        String(M[3][1]), ",", String(M[3][2]), ",", String(M[3][3]), "\n");
od;

# 3. All three constraints (54 expected - doubly stochastic)
output_file := "../outputs/doubly_stochastic_54.json";
PrintTo(output_file, "{\n");
AppendTo(output_file, "  \"count\": ", Length(three_constraint_ops), ",\n");
AppendTo(output_file, "  \"operators\": [\n");
for i in [1..Length(three_constraint_ops)] do
    M := three_constraint_ops[i];
    AppendTo(output_file, "    [[",
        M[1][1], ",", M[1][2], ",", M[1][3], "],[",
        M[2][1], ",", M[2][2], ",", M[2][3], "],[",
        M[3][1], ",", M[3][2], ",", M[3][3], "]]");
    if i < Length(three_constraint_ops) then
        AppendTo(output_file, ",\n");
    else
        AppendTo(output_file, "\n");
    fi;
od;
AppendTo(output_file, "  ]\n}\n");

Print("Results saved to outputs/\n\n");

# Verify expected counts
Print("=== VERIFICATION ===\n");
if Length(conservation_ops) = 432 then
    Print("✓ Conservation: 432 (PASS)\n");
else
    Print("✗ Conservation: Expected 432, got ", Length(conservation_ops), "\n");
fi;

if Length(two_constraint_ops) = 108 then
    Print("✓ Two constraints: 108 (PASS)\n");
else
    Print("✗ Two constraints: Expected 108, got ", Length(two_constraint_ops), "\n");
fi;

if Length(three_constraint_ops) = 54 then
    Print("✓ All three: 54 (PASS)\n");
else
    Print("✗ All three: Expected 54, got ", Length(three_constraint_ops), "\n");
fi;

QUIT;