# Simple Symbols

## Question: 
## Return "true" if every letter is surrounded by +.

def simple_symbols(s):
    for i, ch in enumerate(s):
        if ch.isalpha():
            left_is_plus = i > 0 and s[i - 1] == "+"
            right_is_plus = i < len(s) - 1 and s[i + 1] == "+"

            if not left_is_plus or not right_is_plus:
                return "false"

    return "true"

print(simple_symbols("+d+=3=+s+"))  # Output: "true"
print(simple_symbols("++d+==+s+"))  # Output: "false"
print(simple_symbols("+d+==+s+"))  # Output: "false"

# Example: "+d+=3=+s+" → "true"
# Complexity: O(n)