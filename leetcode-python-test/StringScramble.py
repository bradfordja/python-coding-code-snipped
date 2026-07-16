# String Scramble

## Question: 
## Return "true" if characters in str1 can create str2.


from collections import Counter

def string_scramble(str1, str2):
    available = Counter(str1)
    needed = Counter(str2)

    for ch, count in needed.items():
        if available[ch] < count:
            return "false"

    return "true"

## Interview note: 
## Frequency counting handles duplicate letters correctly.
## Complexity: O(n + m)