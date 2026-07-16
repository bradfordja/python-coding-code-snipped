# Longest Word

## Question: 
## Return the longest word from a sentence. Ignore punctuation.

import re

def longest_word(sentence):
    # Extract only words/numbers
    words = re.findall(r"[A-Za-z0-9]+", sentence)

    # Return word with max length
    return max(words, key=len)

print(longest_word("fun&!! time"))

## Output
## time

## Complexity: O(n)

## Interview note: 
## “Regex cleans punctuation, then max finds the longest word.”
