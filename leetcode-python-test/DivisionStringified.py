# Division Stringified

## Question: 
## Divide two numbers and return the rounded result with commas.

def division_stringified(num1, num2):
    result = round(num1 / num2)
    return f"{result:,}"

## Example: 
## division_stringified(123456789, 10000) → "12,346"
## Interview note: 
## Python formatting handles comma grouping cleanly.
## Complexity: O(d), where d is number of digits.