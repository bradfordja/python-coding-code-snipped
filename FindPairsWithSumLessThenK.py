def get_all_pairs_with_sum_less_than_k(A, K):
    pairs_list = []
    A.sort()  # Sort the list in ascending order
    left, right = 0, len(A) - 1

    while left < right:
        current_sum = A[left] + A[right]

        if current_sum < K:
            pairs_list.extend([(A[left], A[i]) for i in range(right, left, -1)])
            left += 1
        else:
            right -= 1

    return pairs_list

def main():
    A = [2, 7, 11, 15]
    K = 19

    result = get_all_pairs_with_sum_less_than_k(A, K)

    if result:
        print("Pairs found:")
        for pair in result:
            print(f"{pair[0]}, {pair[1]}")
    else:
        print("No such pairs found.")

if __name__ == "__main__":
    main()
