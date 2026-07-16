# Letter Changes

## Question: 
## Replace each letter with the next letter in the alphabet, then capitalize vowels.

## Example: hello → Ifmmp
def letter_changes(s):
    result = []

    for ch in s:
        if ch.isalpha():
            if ch.lower() == "z":
                new_ch = "a"
            else:
                new_ch = chr(ord(ch) + 1)

            if new_ch in "aeiou":
                new_ch = new_ch.upper()

            result.append(new_ch)
        else:
            result.append(ch)

    return "".join(result)

print(letter_changes("hello*3"))

## Output
## Ifmmp*3

## Complexity: O(n)

## Interview note: 
## “I used ASCII conversion with ord() and chr().”

## ⸻
