# Dash Insert

## Question: 
## Insert dashes between two adjacent odd digits.

def dash_insert(num):
    digits = str(num)
    result = [digits[0]]

    for i in range(1, len(digits)):
        previous_digit = int(digits[i - 1])
        current_digit = int(digits[i])

        if previous_digit % 2 == 1 and current_digit % 2 == 1:
            result.append("-")

        result.append(digits[i])

    return "".join(result)

## Example: 99946 → "9-9-946"
## Interview note: 
## Build with a list instead of repeatedly concatenating strings.
## Complexity: O(n)