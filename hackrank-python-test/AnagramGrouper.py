from collections import defaultdict

def group_anagrams(strs):
    if not strs:
        return []
    
    anagrams = defaultdict(list)
    for s in strs:
        # Sort the string and use it as a key
        sorted_str = ''.join(sorted(s))
        anagrams[sorted_str].append(s)
    
    # Return all grouped anagrams as a list
    return list(anagrams.values())

def main():
    strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    grouped_anagrams = group_anagrams(strs)
    print("Grouped Anagrams:", grouped_anagrams)

if __name__ == "__main__":
    main()
