# Mean Mode

## Question: 
## Return 1 if the mean equals the mode, otherwise 0.

from collections import Counter

def mean_mode(arr):
    mean = sum(arr) / len(arr)

    counts = Counter(arr)
    mode = max(counts, key=counts.get)

    return 1 if mean == mode else 0

## Interview note: 
## For Coderbyte, there is usually one clear mode.
## Complexity: O(n)