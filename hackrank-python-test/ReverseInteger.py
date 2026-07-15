def reverse_integer(number):
    """
    Reverse the digits of an integer.
    """
    reversed_number = 0
    while number != 0:
        digit = number % 10
        reversed_number = reversed_number * 10 + digit
        number //= 10  # Use floor division to ensure integer result in Python 3
    return reversed_number

# Test cases
print(reverse_integer(15))     # 51
print(reverse_integer(36))     # 63
print(reverse_integer(5))      # 5
print(reverse_integer(65432))  # 23456
