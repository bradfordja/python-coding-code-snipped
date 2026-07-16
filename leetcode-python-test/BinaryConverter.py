# Binary Converter

## Question: 
## Convert a binary string into decimal.

def binary_converter(binary_str):
    result = 0

    for digit in binary_str:
        result = result * 2 + int(digit)

    return result

print(binary_converter("1010"))
print(binary_converter("111100"))
print(binary_converter("1000001"))

## Interview note: 
### Avoid built-in int(binary_str, 2) if interviewer wants logic.
### Complexity: O(n)
