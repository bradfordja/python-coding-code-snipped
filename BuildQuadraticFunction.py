def build_quadratic_function(a, b, c):
    return lambda x: a * x**2 + b * x + c
f = build_quadratic_function(2, 3, -5)

def main(): 
    print(f(0))
    print(f(1))
    print(f(2))
    print(f(3))
    print(build_quadratic_function(3, 0, 1)(2)) # 3 * 2**2 + 0 * 2 + 1 = 13
    print(build_quadratic_function(3, 0, 1)(0)) # 3 * 0**2 + 0 * 0 + 1 = 1

if __name__ == "__main__":
    main()
