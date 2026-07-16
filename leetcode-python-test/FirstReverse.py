# First Reverse

## Question: 
## Reverse the input string.

def first_reverse(s):
    # Python slicing reverses the string
    return s[::-1]

print(first_reverse("coderbyte"))

## Output
## etybredoc

## Complexity: O(n)

## Interview note: 
## “I used slicing because strings are immutable, and this creates a reversed copy.”
