# Second Greatest Low

## Question: 
## Return the second lowest and second greatest numbers.

def second_great_low(arr):
    unique_nums = sorted(set(arr))

    if len(unique_nums) == 1:
        return f"{unique_nums[0]} {unique_nums[0]}"

    return f"{unique_nums[1]} {unique_nums[-2]}"

## Example: [7, 7, 12, 98, 106] → "12 98"
## Interview note: 
## Use set to remove duplicates before sorting.
## Complexity: O(n log n)