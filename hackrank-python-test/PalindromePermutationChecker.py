from collections import Counter

def can_permute_palindrome(s):
    # Count character frequencies using Counter
    char_counts = Counter(s)

    # Count the number of characters with an odd count
    odd_count = sum(1 for count in char_counts.values() if count % 2 != 0)

    # A string can form a palindrome if there is at most one odd count
    return odd_count <= 1

# Test the function
if __name__ == "__main__":
    input1 = "tactcoa"
    input2 = "java"
    
    print(f'Can "{input1}" permute to a palindrome? {can_permute_palindrome(input1)}')
    print(f'Can "{input2}" permute to a palindrome? {can_permute_palindrome(input2)}')
