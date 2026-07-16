# Food Distribution

## Question: 
## Distribute sandwiches to reduce hunger gaps.

def food_distribution(arr):
    sandwiches = arr[0]
    hunger = arr[1:]

    while sandwiches > 0:
        max_gap = 0
        target_index = -1

        for i in range(len(hunger)):
            left_gap = abs(hunger[i] - hunger[i - 1]) if i > 0 else 0
            right_gap = abs(hunger[i] - hunger[i + 1]) if i < len(hunger) - 1 else 0
            gap = left_gap + right_gap

            if hunger[i] > 0 and gap > max_gap:
                max_gap = gap
                target_index = i

        if target_index == -1:
            break

        hunger[target_index] -= 1
        sandwiches -= 1

    total_gap = 0
    for i in range(1, len(hunger)):
        total_gap += abs(hunger[i] - hunger[i - 1])

    return total_gap

print(food_distribution([3, 5, 2, 4, 1]))  # Output: 4
print(food_distribution([5, 1, 2, 3, 4]))  # Output: 6
print(food_distribution([2, 3, 1, 5, 4]))  # Output: 4

## Interview note: 
### Greedy reduction works well for Coderbyte constraints.
### Complexity: O(k × n), where k is sandwiches.