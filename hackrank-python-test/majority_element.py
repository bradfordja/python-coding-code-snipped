def majority_element(nums: list[int]) -> int:
    count = {}
    for num in nums:        
        # Count the frequency of each number
        count[num] = count.get(num, 0) + 1 
        # If num not in count, set count[num] to 0
    for num in count:   
        # Check if the count of num is greater than half the length of nums
        if count[num] > len(nums) // 2:  
            # floor division
            return num
    return -1  # Return -1 if no majority element found

nums = [2, 2, 1, 1, 1, 2, 2]
result = majority_element(nums)
print(result)   