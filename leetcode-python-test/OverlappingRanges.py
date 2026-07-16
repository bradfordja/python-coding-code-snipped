# Overlapping Ranges

## Question: 
## Return "true" if two ranges overlap by at least x numbers.

def overlapping_ranges(arr):
    start1, end1, start2, end2, required = arr

    overlap_start = max(start1, start2)
    overlap_end = min(end1, end2)

    overlap_count = max(0, overlap_end - overlap_start + 1)

    return "true" if overlap_count >= required else "false"

## Interview note: 
## Find the intersection of two ranges mathematically.
## Complexity: O(1)