# Number Search

## Question: 
## Add all digits in a string, then divide by the number of letters. Round to nearest integer.

def number_search(s):
    digit_sum = 0
    letter_count = 0

    for ch in s:
        if ch.isdigit():
            digit_sum += int(ch)
        elif ch.isalpha():
            letter_count += 1

    return round(digit_sum / letter_count) if letter_count else 0

## Interview note: 
## Scan once and track only needed totals.
## Complexity: O(n)