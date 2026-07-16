# Three Sum

## Question: 
## Return "true" if any 3 numbers sum to target.

def three_sum(arr, target):
    arr.sort()

    for i in range(len(arr) - 2):
        left = i + 1
        right = len(arr) - 1

        while left < right:
            total = arr[i] + arr[left] + arr[right]

            if total == target:
                return "true"
            elif total < target:
                left += 1
            else:
                right -= 1

    return "false"

print(three_sum([1, 2, 3, 4, 5], 9))  # Output: "true"
print(three_sum([1, 2, 3, 4, 5], 15))  # Output: "false"
print(three_sum([-1, 0, 1, 2], 0))  # Output: "true"

## Interview note: 
### Sort first, then use two pointers.
### Complexity: O(n²)