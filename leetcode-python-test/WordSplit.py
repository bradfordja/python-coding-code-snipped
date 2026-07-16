# Word Split

## Question: 
## Determine if a string can be split into two dictionary words.

def word_split(str_arr):
    target = str_arr[0]
    dictionary = set(str_arr[1].split(","))

    for i in range(1, len(target)):
        left = target[:i]
        right = target[i:]

        if left in dictionary and right in dictionary:
            return f"{left},{right}"

    return "not possible"

print(word_split(["hellocat", "hello,cat,dog"]))  # Output: "hello,cat"
## Interview note: 
### Optimization: Use a set for O(1) dictionary lookup.
### Complexity: O(n)