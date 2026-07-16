# Letter Count

## Question: 
## Return the first word with the greatest number of repeated letters.

from collections import Counter

def letter_count(sentence):
    best_word = "-1"
    best_repeat_count = 1

    for word in sentence.split():
        counts = Counter(word.lower())
        max_repeat = max(counts.values())

        if max_repeat > best_repeat_count:
            best_repeat_count = max_repeat
            best_word = word

    return best_word

## Example: 
## "Today, is the greatest day ever!" → "greatest"
## Interview note: 
## Counter is clean and readable for frequency problems.
## Complexity: O(n)