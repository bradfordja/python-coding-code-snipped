# Powers of Two

## Question: 
## Return "true" if a number is a power of two.

def powers_of_two(num):
    if num <= 0:
        return "false"

    return "true" if num & (num - 1) == 0 else "false"

## Interview note: 
## A power of two has only one set bit.
## Complexity: O(1)