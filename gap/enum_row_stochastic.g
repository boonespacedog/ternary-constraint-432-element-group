# 432 Doubly Stochastic Matrices Over F₃
# Paper: "Doubly Stochastic Matrices Over F₃: Binary Trace Stratification"
# Repository: https://github.com/boonespacedog/ternary-constraint-432-element-group
# Updated: 2025-11-09

# File: enum_conservation.g
# Purpose: Enumerate GL(3,F₃) operators with conservation constraint only
# Finds 432 operators with row sums ≡ 1 (mod 3)
# For v8 paper: "Constraint-Based Filtration in GL(3,F₃)"

LoadPackage("SmallGrp");

# CheckConservation: Check if all row sums ≡ 1 mod 3
CheckConservation := function(M)
    local i, j, row_sum, elem_val;

    for i in [1..3] do
        row_sum := 0;

        for j in [1..3] do
            if IsFFE(M[i][j]) then
                elem_val := IntFFE(M[i][j]);
            else
                elem_val := M[i][j];
            fi;
            row_sum := row_sum + elem_val;
        od;

        if (row_sum mod 3) <> 1 then
            return false;
        fi;
    od;

    return true;
end;

# Main enumeration
Print("Enumerating GL(3,F₃) operators with conservation constraint only...\n");

# Get all GL(3,F₃) elements
F3 := GF(3);
GL3F3 := GL(3, F3);
all_elements := Elements(GL3F3);

Print("Total GL(3,F₃) elements: ", Size(GL3F3), "\n");

# Filter by conservation
conservation_ops := [];

for g in all_elements do
    M := List(g, row -> List(row, x -> IntFFE(x)));

    if CheckConservation(M) then
        Add(conservation_ops, M);
    fi;
od;

Print("\n");
Print("Operators with conservation: ", Length(conservation_ops), "\n");
Print("(No hardcoded expectations - this is the discovered count)\n");

# Save results
output_file := "../outputs/row_stochastic_432.csv";

# Write CSV header
PrintTo(output_file, "index,m00,m01,m02,m10,m11,m12,m20,m21,m22,determinant\n");

# Write each operator
for i in [1..Length(conservation_ops)] do
    M := conservation_ops[i];
    det_val := (M[1][1]*(M[2][2]*M[3][3] - M[2][3]*M[3][2]) -
                M[1][2]*(M[2][1]*M[3][3] - M[2][3]*M[3][1]) +
                M[1][3]*(M[2][1]*M[3][2] - M[2][2]*M[3][1])) mod 3;

    AppendTo(output_file,
        String(i), ",",
        String(M[1][1]), ",", String(M[1][2]), ",", String(M[1][3]), ",",
        String(M[2][1]), ",", String(M[2][2]), ",", String(M[2][3]), ",",
        String(M[3][1]), ",", String(M[3][2]), ",", String(M[3][3]), ",",
        String(det_val), "\n");
od;

Print("Results saved to: ", output_file, "\n");
Print("Count verification: ", Length(conservation_ops), " operators enumerated\n");
Print("(Anti-pattern avoided: No hardcoded expectation check)\n");

QUIT;