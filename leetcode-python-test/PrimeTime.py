# Prime Time

## Question: 
## Return "true" if a number is prime.

def prime_time(num):
    if num < 2:
        return "false"

    if num == 2:
        return "true"

    if num % 2 == 0:
        return "false"

    # Only check odd divisors up to sqrt(num)
    divisor = 3
    while divisor * divisor <= num:
        if num % divisor == 0:
            return "false"
        divisor += 2

    return "true"

## Interview note: 
## Avoid checking all numbers up to num; checking up to √n is enough.
## Complexity: O(√n)