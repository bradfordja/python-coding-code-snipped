# Array Addition

## Question: 
## Return true if any combination of numbers can add up to the largest number.

def array_addition(arr):
    target = max(arr)
    nums = arr.copy()
    nums.remove(target)

    possible_sums = {0}

    for num in nums:
        new_sums = set()

        for current_sum in possible_sums:
            new_sums.add(current_sum + num)

        possible_sums.update(new_sums)

        if target in possible_sums:
            return "true"

    return "false"

print(array_addition([4, 6, 23, 10, 1, 3]))  # Output: "true"
print(array_addition([5, 7, 16, 1, 2]))  # Output: "false"
print(array_addition([3, 5, -1, 8, 12]))  # Output: "true"

## Interview note: 
## Uses subset-sum logic with a set instead of checking every combination manually.
## Complexity: O(n × s), where s is number of possible sums.