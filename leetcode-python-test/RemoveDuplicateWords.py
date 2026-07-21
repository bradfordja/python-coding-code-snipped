def remove_duplicates(arr):
    seen = set()
    unique_arr = [x for x in arr if not (x in seen or seen.add(x))]
    return unique_arr

# Example usage
words = ["apple", "banana", "apple", "pear", "banana", "orange", "apple"]
unique_words = remove_duplicates(words)
print(unique_words)  # Output: ['apple', 'banana', 'pear', 'orange']


def remove_duplicate_words(s):
    words = s.split()  # Split the string into a list of words
    unique_words = []
    seen = set()  # Create an empty set to store seen words
    
    for word in words:
        if word not in seen:  # Check if the word is already seen
            unique_words.append(word)  # Append unique words to the list
            seen.add(word)  # Add the word to the seen set
    
    return ' '.join(unique_words)  # Join the unique words back into a string

# Example usage
input_string = "Python is great and Python is dynamic"
result = remove_duplicate_words(input_string)
print(result)  # Output: "Python is great and dynamic"