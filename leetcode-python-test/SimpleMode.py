# Simple Mode

## Question: 
## Return the number that appears most often. If no mode exists, return -1.

from collections import Counter

def simple_mode(arr):
    counts = Counter(arr)
    max_count = max(counts.values())

    if max_count == 1:
        return -1

    for num in arr:
        if counts[num] == max_count:
            return num

## Interview note: 
## Loop through original array to return the first mode.
## Complexity: O(n)