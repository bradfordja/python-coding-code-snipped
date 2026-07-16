# Bracket Matcher

## Question: 
## Return 1 if parentheses are balanced, otherwise 0.

def bracket_matcher(s):
    count = 0

    for ch in s:
        if ch == "(":
            count += 1
        elif ch == ")":
            count -= 1

        if count < 0:
            return 0

    return 1 if count == 0 else 0

## Interview note: 
## Uses O(1) space because only one bracket type exists.
## Complexity: O(n) time, O(1) space.
