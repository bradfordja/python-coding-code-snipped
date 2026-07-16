# Super Increasing

## Question: 
## Return "true" if every number is greater than the sum of all previous numbers.

def super_increasing(arr):
    running_sum = 0

    for num in arr:
        if num <= running_sum:
            return "false"

        running_sum += num

    return "true"

## Interview note: 
## Maintain a running sum instead of recalculating.
## Complexity: O(n)