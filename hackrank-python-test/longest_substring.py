def length_of_longest_substring(s: str) -> int:
    
    seen = set()
    left = 0
    max_length = 0
    
    for right, char in enumerate(list(s)):
        while char in seen:
            seen.remove(s[left])
            left += 1
        seen.add(char)
        max_length = max(max_length, right - left + 1)
    return max_length

print(length_of_longest_substring("abcabcbb"))
print(length_of_longest_substring("bbbbb"))
print(length_of_longest_substring("pwwkew"))
