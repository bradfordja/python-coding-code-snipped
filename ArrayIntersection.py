def find_intersection(arr1, arr2):
    set1 = set(arr1)
    set2 = set(arr2)

    # Find the intersection of two sets
    intersection = set1 & set2

    # Convert the set back to a list (array)
    result = list(intersection)
    return result

if __name__ == "__main__":
    arr1 = [1, 2, 3, 4, 5]
    arr2 = [3, 4, 5, 6, 7]
    result = find_intersection(arr1, arr2)
    print("Intersection of Arrays: ")
    for num in result:
        print(num, end=" ")
