# Arith Geo

## Question: 
## Return "Arithmetic" if sequence is arithmetic, "Geometric" if geometric, otherwise -1.

def arith_geo(arr):
    if len(arr) < 2:
        return -1

    diff = arr[1] - arr[0]
    ratio = arr[1] / arr[0] if arr[0] != 0 else None

    is_arithmetic = True
    is_geometric = ratio is not None

    for i in range(2, len(arr)):
        if arr[i] - arr[i - 1] != diff:
            is_arithmetic = False

        if ratio is None or arr[i - 1] == 0 or arr[i] / arr[i - 1] != ratio:
            is_geometric = False

    if is_arithmetic:
        return "Arithmetic"

    if is_geometric:
        return "Geometric"

    return -1

print(arith_geo([2, 4, 6, 8]))  # Arithmetic
print(arith_geo([2, 6, 18, 54]))  # Geometric
print(arith_geo([1, 2, 4, 8]))  # -1

## Interview note: 
## Check both patterns in one pass.
## Complexity: O(n)