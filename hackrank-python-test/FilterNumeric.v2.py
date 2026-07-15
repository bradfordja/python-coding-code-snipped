from collections import Counter

def analyze(nums):
    # Count occurrences of numbers in the valid range using a dictionary comprehension and Counter
    counts = Counter(num for num in nums if 1 <= num <= 1000000)
    
    # Determine missing numbers using a list comprehension, filtering out those present in the counts
    missing = [num for num in range(1, 1000001) if num not in counts]
    
    # Determine duplicated numbers from the counts dictionary
    duplicated = [num for num, count in counts.items() if count > 1]
    
    return {'missing': missing, 'duplicated': duplicated}

def main():
    num_array = [-10, -4, -4, 0, 1, 3, 3, 3, 3, 5, 6, 6, 999999, 1000000000, 1000000000, 1000000001]
    result = analyze(num_array)
    
    print("Missing:", result['missing'])
    print("Duplicated:", result['duplicated'])

if __name__ == "__main__":
    main()
