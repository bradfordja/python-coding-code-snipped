# Product Digits

## Question: 
## Find the minimum number of digits needed for two numbers whose product equals num.

def product_digits(num):
    min_digits = float("inf")

    for factor in range(1, int(num ** 0.5) + 1):
        if num % factor == 0:
            other_factor = num // factor

            digit_count = len(str(factor)) + len(str(other_factor))
            min_digits = min(min_digits, digit_count)

    return min_digits

## Example: product_digits(24) → 2 because 6 * 4 = 24.
## Interview note: 
## Only loop to √n because factors come in pairs.
## Complexity: O(√n)