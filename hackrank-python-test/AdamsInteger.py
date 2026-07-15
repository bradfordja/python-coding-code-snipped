def reverse_integer(num):
    """
    Reverse the digits of an integer.
    """
    return int(str(num)[::-1])

def is_adam_integer(num):
    """
    Check if a number is an Adam Integer.
    """
    return reverse_integer(reverse_integer(num) ** 2) == num ** 2

# Test cases
print(is_adam_integer(12))     # True
print(is_adam_integer(36))     # False
print(is_adam_integer(5))      # False
print(is_adam_integer(65432))  # False
