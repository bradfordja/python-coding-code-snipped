def subarray_sum(arr, n, s):
    current_sum = 0
    start = 0

    for end in range(n):
        current_sum += arr[end]

        while current_sum > s and start < end:
            current_sum -= arr[start]
            start += 1

        if current_sum == s:
            return [start + 1, end + 1]  # Return 1-based index

    return [-1]  # Return -1 if no subarray found

def subarray_sum2(nums: list[int], target: int) -> int:
    count = 0
    prefix_sum = 0

    prefix_count = {0: 1}  # Initialize with prefix sum 0

    for num in nums:
        prefix_sum += num
        # Calculate the current prefix sum
        count += prefix_count.get(prefix_sum - target, 0)   
        # Check if there is a prefix sum that matches the current prefix sum minus the target
        prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1
        # Increment the count for the current prefix sum

    return count

# Example usage
arr = [1, 2, 3, 7, 5]
n = len(arr)
s = 12
result = subarray_sum(arr, n, s)
print(result)

target = 3
result2 = subarray_sum2(arr, target)
print(result2)   