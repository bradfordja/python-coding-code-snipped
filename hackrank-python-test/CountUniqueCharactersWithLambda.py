from functools import reduce
from itertools import groupby

def count_unique_characters(s):
    # Prepare the string by sorting it, necessary for groupby to function correctly
    sorted_chars = sorted(s)

    # Use groupby to group characters and count occurrences using reduce inside a map
    grouped_chars = groupby(sorted_chars)
    char_counts = map(lambda x: (x[0], reduce(lambda acc, _: acc + 1, x[1], 0)), grouped_chars)

    # Convert to dictionary
    return dict(char_counts)

input_string = "amitraviravalilijoi"
unique_characters = count_unique_characters(input_string)

print("Unique character counts:")
print(unique_characters); # {'a': 4, 'i': 5, 'j': 1, 'l': 2, 'm': 1, 'o': 1, 'r': 2, 't': 1, 'v': 2}
for char, count in unique_characters.items():
    print(f"{char}: {count}")


'''
Explanation:
1. Sort the Characters: The string is first sorted to ensure that groupby can correctly group all identical elements together.

2. Group by Character: The groupby function from the itertools module groups the characters. It requires the data (in this case, characters of the string) to be sorted.

3. Count Occurrences: For each group, reduce is used inside a map to count the occurrences of each character. The lambda inside reduce increments the accumulator for each character in the group.

4. Conversion to Dictionary: The result of the map is a list of tuples, which is converted to a dictionary for easy access and readability.
This version achieves a similar effect to using RxJS in JavaScript by applying Python's functional programming capabilities, although Python's approach is less centered on streaming and more on batch processing due to the language's design and standard library features.
'''