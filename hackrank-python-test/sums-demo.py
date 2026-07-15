nums = [2, 4, 6, 8, 10]
target = 10

def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}

    for index, number in enumerate(nums):
        needed = target - number

        if needed in seen:
            return [seen[needed], index] # if seen[needed] != index else [index, seen[needed]]
        seen[number] = index             # if number not in seen else seen[number]
    return []                            # None

print(two_sum(nums, target))
