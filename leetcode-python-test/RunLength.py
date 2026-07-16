# Run Length

## Question: 
## Compress repeated characters using run-length encoding.

def run_length(s):
    if not s:
        return ""

    result = []
    count = 1

    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            result.append(str(count) + s[i - 1])
            count = 1

    result.append(str(count) + s[-1])
    return "".join(result)

## Example: wwwbbbw → 3w3b1w
## Interview note: 
## Build with a list, not repeated string concatenation.
## Complexity: O(n) time.