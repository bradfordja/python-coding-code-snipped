# Consecutive

## Question: 
## Return how many numbers are needed to make the array consecutive.

def consecutive(arr):
    unique_nums = set(arr)

    min_num = min(unique_nums)
    max_num = max(unique_nums)

    return (max_num - min_num + 1) - len(unique_nums)

print(consecutive([4, 8, 6]))  # Output: 2
print(consecutive([1, 2, 3, 4]))  # Output: 0
print(consecutive([10, 12, 11, 15]))  # Output: 3

## Example: [4, 8, 6] → 2 because 5 and 7 are missing.
## Interview note: Use range size minus unique count.Complexity: O(n)