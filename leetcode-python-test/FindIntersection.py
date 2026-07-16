# Find Intersection

## Question: 
## Given two sorted comma-separated number strings, return their common values.

def find_intersection(str_arr):
    a = [int(x.strip()) for x in str_arr[0].split(",")]
    b = [int(x.strip()) for x in str_arr[1].split(",")]

    i = j = 0
    result = []

    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            result.append(str(a[i]))
            i += 1
            j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1

    return ",".join(result) if result else "false"

## Interview note: 
## Since arrays are sorted, two pointers are better than nested loops.
## Complexity: O(n + m) time.