# Prime Mover

## Question: 
## Return the nth prime number.

def is_prime(num):
    if num < 2:
        return False

    for divisor in range(2, int(num ** 0.5) + 1):
        if num % divisor == 0:
            return False

    return True


def prime_mover(n):
    count = 0
    current = 1

    while count < n:
        current += 1

        if is_prime(current):
            count += 1

    return current

## Interview note: 
## Uses a helper function to keep the solution clean and testable.
## Complexity: Roughly O(n√p), where p is the nth prime.