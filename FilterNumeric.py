def analyze(nums):
    result = {
        "missing": [],
        "duplicated": []
    }

    # This dictionary will help track the count of numbers.
    tracker = {}

    # Iterate through the nums and update our tracker dictionary.
    for num in nums:
        if 0 < num <= 1000000:
            if num in tracker:
                tracker[num] += 1
            else:
                tracker[num] = 1

    # Now, process our tracker dictionary.
    for i in range(1, 1000001):
        count = tracker.get(i, 0)
        if count == 0:
            result["missing"].append(i)
        elif count > 1:
            result["duplicated"].append(i)

    return result

if __name__ == "__main__":
    num_array = [-10, -4, -4, 0, 1, 3, 3, 3, 3, 5, 6, 6, 999999, 1000000000, 1000000000, 1000000001]
    result = analyze(num_array)

    print("Missing:", result["missing"])
    print("Duplicated:", result["duplicated"])
