from collections import Counter

def analyze(nums):
    # Use filter to refine nums to the valid range and count occurrences using Counter
    valid_nums = filter(lambda num: 1 <= num <= 1000000, nums)
    counts = Counter(valid_nums)
    
    # Use range and filter to determine missing numbers by checking against the counts dictionary
    missing = list(filter(lambda num: num not in counts, range(1, 1000001)))
    
    # Use filter to extract duplicated numbers from the counts dictionary
    duplicated = list(filter(lambda item: item[1] > 1, counts.items()))
    duplicated = [num for num, _ in duplicated]  # Extract just the numbers from the tuple
    
    return {'missing': missing, 'duplicated': duplicated}

def main():
    num_array = [-10, -4, -4, 0, 1, 3, 3, 3, 3, 5, 6, 6, 999999, 1000000000, 1000000000, 1000000001]
    result = analyze(num_array)
    
    print("Missing:", result['missing'])
    print("Duplicated:", result['duplicated'])

if __name__ == "__main__":
    main()
