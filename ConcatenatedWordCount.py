def get_concatenate_word_count(stream1, stream2):
    word_count_map = {}

    # Count words from the first stream
    for word in stream1:
        word_count_map[word] = word_count_map.get(word, 0) + 1

    # Count words from the second stream
    for word in stream2:
        word_count_map[word] = word_count_map.get(word, 0) + 1
    
    return word_count_map

if __name__ == "__main__":
    stream1 = ["cat", "rat", "dog"]
    stream2 = ["cat", "dog", "cow", "dock"]

    word_count_map = get_concatenate_word_count(stream1, stream2)

    # Print the concatenated word count
    for word, count in word_count_map.items():
        print(f"{word}: {count}")
