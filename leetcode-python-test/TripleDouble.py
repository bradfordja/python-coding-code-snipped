# Triple Double

## Question: 
## Return 1 if num1 has three repeated digits and num2 has two repeated same digits.

def triple_double(num1, num2):
    s1 = str(num1)
    s2 = str(num2)

    for digit in "0123456789":
        if digit * 3 in s1 and digit * 2 in s2:
            return 1

    return 0

## Example: 451999277, 41177722899 → 1
## Interview note: 
## String pattern matching is simpler than numeric math here.
## Complexity: O(n + m)