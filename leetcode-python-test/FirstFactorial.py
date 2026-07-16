#First Factorial

## Question: 
## Return the factorial of a number.

def first_factorial(num):
    result = 1

    # Multiply from 1 to num
    for i in range(1, num + 1):
        result *= i

    return result

print(first_factorial(5))

## Output
## 120

## Complexity: O(n)

## Interview note: 
## “I used an iterative solution to avoid recursion stack issues.”
