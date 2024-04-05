def is_balanced(expression):
    stack = []

    for ch in expression:
        if ch in ['{', '(', '[']:
            stack.append(ch)
        elif ch in ['}', ')', ']']:
            if not stack:
                return False

            last = stack.pop()
            if not is_pair_valid(last, ch):
                return False

    return not stack

def is_pair_valid(open, close):
    pairs = { '{': '}', '(': ')', '[': ']' }
    return pairs.get(open) == close

if __name__ == "__main__":
    print(is_balanced("{{(){}}}"))  # True
    print(is_balanced("}{}{"))      # False
    print(is_balanced("({})"))      # True