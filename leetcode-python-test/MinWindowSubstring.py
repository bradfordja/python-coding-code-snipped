# Min Window Substring

## Question: 
## Find the smallest substring in N containing all characters from K.

from collections import Counter, defaultdict

def min_window_substring(str_arr):
    s, target = str_arr
    need = Counter(target)
    window = defaultdict(int)

    required = len(need)
    formed = 0
    left = 0
    best = float("inf"), None, None

    for right, ch in enumerate(s):
        window[ch] += 1

        if ch in need and window[ch] == need[ch]:
            formed += 1

        while formed == required:
            if right - left + 1 < best[0]:
                best = right - left + 1, left, right

            left_ch = s[left]
            window[left_ch] -= 1

            if left_ch in need and window[left_ch] < need[left_ch]:
                formed -= 1

            left += 1

    return s[best[1]:best[2] + 1] if best[1] is not None else ""

## Interview note: 
## This is a classic sliding-window frequency problem.
## Complexity: O(n) time.