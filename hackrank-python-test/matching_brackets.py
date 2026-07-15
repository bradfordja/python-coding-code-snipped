def is_valid_parentheses(text: str) -> bool:
    stack = []
    matching = {')': '(', ']': '[', '}': '{'}

    for character in text:
        if character in matching.values():
            stack.append(character)
        elif character in matching.keys():
            if stack == [] or matching[character] != stack.pop():
                return False
    return stack == []

print(is_valid_parentheses('()'))
print(is_valid_parentheses('()[]{}'))
print(is_valid_parentheses('([)]'))
print(is_valid_parentheses('{[]}'))