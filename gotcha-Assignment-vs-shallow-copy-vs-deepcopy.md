# Python Gotcha: Shallow Copy vs. Deep Copy

### Question

What is the output, and why does changing the copied list also affect the original list?

```python
original = [[1, 2], [3, 4]]
copied = original.copy()

copied[0].append(99)

print(original)
print(copied)
```

### Output

```text
[[1, 2, 99], [3, 4]]
[[1, 2, 99], [3, 4]]
```

### Answer

`list.copy()` creates a **shallow copy**:

* The outer list is new.
* The nested lists are still shared.
* Modifying a nested list affects both variables.

```python
print(original is copied)       # False: different outer lists
print(original[0] is copied[0]) # True: same nested list
```

### Correct solution: Deep copy

Use `copy.deepcopy()` when the nested objects must also be copied.

```python
import copy

original = [[1, 2], [3, 4]]

# Create independent copies of the outer and nested lists
copied = copy.deepcopy(original)

# Modify only the copied nested list
copied[0].append(99)

print(original)
print(copied)
```

### Correct output

```text
[[1, 2], [3, 4]]
[[1, 2, 99], [3, 4]]
```

### Assignment vs. shallow copy vs. deep copy

```python
import copy

original = [[1, 2], [3, 4]]

assigned = original
shallow = copy.copy(original)
deep = copy.deepcopy(original)

print(assigned is original)          # True
print(shallow is original)           # False
print(shallow[0] is original[0])     # True
print(deep[0] is original[0])        # False
```

### Short interview answer

> A shallow copy creates a new outer object but continues sharing nested mutable objects. A deep copy recursively creates independent copies of nested objects. I use `deepcopy()` only when full independence is required because it uses more memory and processing time.
