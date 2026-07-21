# Python Gotcha: `is` vs. `==`

### Question

What is wrong with the following code?

```python
value = 1000

if value is 1000:
    print("Values match")
```

### Answer

`is` checks whether two variables reference the **same object in memory**.

`==` checks whether two objects contain the **same value**.

The code may appear to work in some Python environments because Python caches certain objects, but this behavior should not be relied upon.

### Correct solution

```python
value = 1000

# Compare values using ==
if value == 1000:
    print("Values match")
```

Output:

```text
Values match
```

### Identity comparison example

```python
list_one = [1, 2, 3]
list_two = [1, 2, 3]
list_three = list_one

# The lists contain equal values
print(list_one == list_two)   # True

# They are two different objects in memory
print(list_one is list_two)   # False

# Both variables reference the same list object
print(list_one is list_three) # True
```

### When should you use `is`?

Use `is` mainly for singleton objects such as `None`.

```python
user = None

# Correct: check whether user references the None singleton
if user is None:
    print("No user was provided")
```

Avoid this:

```python
if user == None:
    print("No user was provided")
```

### Short interview answer

> `==` compares values, while `is` compares object identity. I use `==` when comparing strings, numbers, lists, or other values. I use `is` primarily when checking singleton objects such as `None`.
