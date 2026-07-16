# Max Subarray

## Question: 
## Return the largest sum of a contiguous subarray.

def max_subarray(arr):
    best_sum = arr[0]
    current_sum = arr[0]

    for num in arr[1:]:
        current_sum = max(num, current_sum + num)
        best_sum = max(best_sum, current_sum)

    return best_sum

## Interview note: 
## This is Kadane’s Algorithm. It avoids checking all subarrays.
## Complexity: O(n) time, O(1) space.