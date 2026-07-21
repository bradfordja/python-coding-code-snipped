# Python Interview “Gotcha” Question

### Question

What is the output of the following code, and why?

```py
def add_item(item, items=[]):
    items.append(item)
    return items


print(add_item("Apple"))
print(add_item("Banana"))
print(add_item("Orange"))
```

### Output

```text
['Apple']
['Apple', 'Banana']
['Apple', 'Banana', 'Orange']
```

### Explanation

The empty list `[]` is created only once—when Python defines the function.

Every function call reuses the same list. Therefore, values from earlier calls remain in the list.

This is called the **mutable default argument gotcha**.

### Correct solution

Use `None` as the default value and create a new list inside the function.

```py
def add_item(item, items=None):
    # Create a new list for each call when one is not provided
    if items is None:
        items = []

    # Add the item to the new or provided list
    items.append(item)

    return items


print(add_item("Apple"))
print(add_item("Banana"))
print(add_item("Orange"))
```

### Correct output

```text
['Apple']
['Banana']
['Orange']
```

You can still provide an existing list when you intentionally want to modify it:

```py
shopping_cart = ["Milk"]

result = add_item("Bread", shopping_cart)

print(result)
```

Output:

```text
['Milk', 'Bread']
```

### Short interview answer

> Mutable default arguments are created once when the function is defined, not every time it is called. Therefore, using a list or dictionary as a default can accidentally preserve state between calls. I use `None` as the default and create the mutable object inside the function.
