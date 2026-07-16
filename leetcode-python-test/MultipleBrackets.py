# Multiple Brackets

## Question: 
## Check if () and [] are balanced. Return 1 count, where count is matched bracket pairs.

def multiple_brackets(s):
    stack = []
    pairs = {")": "(", "]": "["}
    matched_count = 0

    for ch in s:
        if ch in "([": 
            stack.append(ch)

        elif ch in ")]":
            if not stack or stack[-1] != pairs[ch]:
                return "0"

            stack.pop()
            matched_count += 1

    if stack:
        return "0"

    return f"1 {matched_count}"

## Interview note: 
## Stack is the cleanest structure for nested bracket validation.
## Complexity: O(n)
