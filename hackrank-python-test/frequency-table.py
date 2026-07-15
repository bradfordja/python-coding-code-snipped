from collections import Counter, defaultdict

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    return count.most_common(k)

print(top_k_frequent([1,1,1,2,2,3], 2))
print(top_k_frequent([1], 1))