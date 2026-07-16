# Matrix Determinant

## Question: 
## Return the determinant of a 2x2 or 3x3 matrix.

def matrix_determinant(matrix):
    n = len(matrix)

    if n == 2:
        a, b = matrix[0]
        c, d = matrix[1]
        return a * d - b * c

    if n == 3:
        a, b, c = matrix[0]
        d, e, f = matrix[1]
        g, h, i = matrix[2]

        return (
            a * (e * i - f * h)
            - b * (d * i - f * g)
            + c * (d * h - e * g)
        )

    raise ValueError("Only 2x2 and 3x3 matrices are supported")

print(matrix_determinant([[1, 2], [3, 4]]))  # Output: -2

## Interview note: 
### Know the direct formulas for small matrices.
### Complexity: O(1)