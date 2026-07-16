# Hamming Distance

## Question: 
## Count positions where two equal-length strings are different.

def hamming_distance(str_arr):
    s1, s2 = str_arr
    count = 0

    for i in range(len(s1)):
        if s1[i] != s2[i]:
            count += 1

    return count

print(hamming_distance(["abcde", "bcdef"]))  # Output: 5
## Interview note: 
### Compare character-by-character.
### Complexity: O(n)