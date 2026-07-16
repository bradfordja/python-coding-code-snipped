# Closest Enemy

## Question: 
## In an array, find the closest enemy 2 from player 1.

def closest_enemy(arr):
    player_index = arr.index(1)
    min_distance = float("inf")

    for i, value in enumerate(arr):
        if value == 2:
            min_distance = min(min_distance, abs(i - player_index))

    return 0 if min_distance == float("inf") else min_distance

# Interview note: One pass after locating player.Complexity: O(n)