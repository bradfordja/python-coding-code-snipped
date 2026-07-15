def get_larges_numbers(numbers, k):
    numbers.sort()          # sort the list in ascending order

    return numbers[-k:]     # return the last k elements

print(get_larges_numbers([2, 4, 16, 8, 10], 2))     # [16, 10]
