# Other Products

## Question: 
## For each index, return the product of every other number.

def other_products(arr):
    n = len(arr)
    prefix = [1] * n
    suffix = [1] * n
    result = [1] * n

    for i in range(1, n):
        prefix[i] = prefix[i - 1] * arr[i - 1]

    for i in range(n - 2, -1, -1):
        suffix[i] = suffix[i + 1] * arr[i + 1]

    for i in range(n):
        result[i] = prefix[i] * suffix[i]

    return "-".join(map(str, result))

## Example: [1, 4, 3] → "12-3-4"
## Interview note: This avoids division and handles zeros correctly.
## Complexity: O(n) time, O(n) space.