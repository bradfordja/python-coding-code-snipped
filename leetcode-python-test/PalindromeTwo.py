# Palindrome Two

## Question: 
## # Return "true" if a string is a palindrome after removing punctuation and spaces.

def palindrome_two(s):
    cleaned = []

    for ch in s.lower():
        if ch.isalnum():
            cleaned.append(ch)

    cleaned = "".join(cleaned)
    return "true" if cleaned == cleaned[::-1] else "false"

## Interview note: Normalize first, then compare with reverse.
## Complexity: O(n)