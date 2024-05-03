def count_unique_characters(s):
    character_count = {}

    for char in s:
        if char in character_count:
            character_count[char] += 1
        else:
            character_count[char] = 1

    return character_count

input_string = "amitraviravalilijoi"
unique_characters = count_unique_characters(input_string)

print("Unique character counts:")
for char, count in unique_characters.items():
    print(f"{char}: {count}")
