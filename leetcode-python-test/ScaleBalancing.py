# Scale Balancing

## Question: 
## Given current scale weights and available weights, find one or two weights that balance the scale.

from itertools import combinations

def scale_balancing(str_arr):
    left, right = eval(str_arr[0])
    weights = eval(str_arr[1])

    for w in weights:
        if left + w == right or right + w == left:
            return str(w)

    for w1, w2 in combinations(weights, 2):
        if left + w1 + w2 == right:
            return f"{w1},{w2}"
        if right + w1 + w2 == left:
            return f"{w1},{w2}"
        if left + w1 == right + w2:
            return f"{w1},{w2}"
        if left + w2 == right + w1:
            return f"{w1},{w2}"

    return "not possible"

print(scale_balancing(["[5, 9]", "[1, 2, 6, 7]"]))  # Output: "2"

## Interview note: 
### Try one weight first, then all two-weight combinations.
### Complexity: O(n²)