def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def main():
    num = 7
    result = factorial(num)
    print(f"Factorial of {num} is: {result}")

if __name__ == "__main__":
    main()
