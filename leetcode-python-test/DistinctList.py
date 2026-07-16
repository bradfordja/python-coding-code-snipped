# Distinct List

## Problem

## Given a list of integers, remove duplicates while preserving the original order.

## Example
## Input

[5,1,2,2,3,5,4,1]

## Output

## [5,1,2,3,4]

## ⸻

## ## Senior Python Solution
def distinct_list(nums):
    seen = set()
    result = []

    for num in nums:
        if num not in seen:
            seen.add(num)
            result.append(num)

    return result


print(distinct_list([5,1,2,2,3,5,4,1]))
## Output
## [5,1,2,3,4]

## Time Complexity
## O(n)
## because every lookup in a set is approximately O(1).
