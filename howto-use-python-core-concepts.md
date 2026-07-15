# Python Core Concepts Interview Prep

---

# 1. Variables

## Definition
A variable is a named reference to an object in memory. Python is dynamically typed, so you do not declare a variable's type.

## Use Cases
- Store user input
- Save calculation results
- Hold objects and collections

## Example

```python
name = "Julio"
age = 56
salary = 120000.00

print(name)
print(age)
print(salary)
```

---

# 2. Data Types

## Definition
Python has several built-in data types.

| Type | Description | Example |
|-------|-------------|---------|
| int | Integer | `10` |
| float | Decimal | `3.14` |
| bool | Boolean | `True` |
| str | Text | `"Hello"` |
| list | Ordered mutable collection | `[1,2,3]` |
| tuple | Ordered immutable collection | `(1,2,3)` |
| set | Unique values | `{1,2,3}` |
| dict | Key-value pairs | `{"name":"John"}` |

## Example

```python
x = 100
price = 19.99
active = True
name = "Python"
```

---

# 3. Strings

## Definition
Strings are immutable sequences of Unicode characters.

## Use Cases

- User input
- JSON
- Logging
- API requests

## Example

```python
first = "Hello"
last = "World"

print(first + " " + last)
print(first.upper())
print(last.lower())
```

---

# 4. Lists

## Definition
A mutable ordered collection.

## Use Cases

- Store records
- API responses
- Processing data

## Example

```python
numbers = [10,20,30]

numbers.append(40)
numbers.remove(20)

print(numbers)
```

---

# 5. Tuples

## Definition
Immutable ordered collection.

## Use Cases

- Coordinates
- Database records
- Function returns

## Example

```python
point = (10, 20)

print(point[0])
```

---

# 6. Sets

## Definition
Unordered collection of unique values.

## Use Cases

- Remove duplicates
- Fast membership lookup

## Example

```python
colors = {"red","blue","green","red"}

print(colors)
```

---

# 7. Dictionaries

## Definition
Stores key-value pairs.

## Use Cases

- JSON
- Configuration
- API payloads

## Example

```python
employee = {
    "id":101,
    "name":"Alice",
    "salary":90000
}

print(employee["name"])
```

---

# 8. Conditional Statements

## Definition
Execute different code depending on conditions.

## Example

```python
age = 18

if age >= 18:
    print("Adult")
else:
    print("Minor")
```

---

# 9. Loops

## Definition
Repeat code.

## For Loop

```python
for i in range(5):
    print(i)
```

## While Loop

```python
count = 1

while count <= 5:
    print(count)
    count += 1
```

---

# 10. Functions

## Definition
Reusable block of code.

## Example

```python
def greet(name):
    return f"Hello {name}"

print(greet("Julio"))
```

---

# 11. Lambda Functions

## Definition
Anonymous one-line function.

## Example

```python
square = lambda x: x * x

print(square(5))
```

---

# 12. List Comprehension

## Definition
Compact syntax for creating lists.

## Example

```python
squares = [x**2 for x in range(6)]

print(squares)
```

---

# 13. Dictionary Comprehension

## Example

```python
numbers = {x: x*x for x in range(5)}

print(numbers)
```

---

# 14. Generators

## Definition
Produces values lazily using `yield`.

## Use Cases

- Large files
- Streaming data
- Memory optimization

## Example

```python
def count():
    for i in range(5):
        yield i

for num in count():
    print(num)
```

---

# 15. Iterators

## Definition
Objects implementing `__iter__()` and `__next__()`.

## Example

```python
numbers = iter([1,2,3])

print(next(numbers))
print(next(numbers))
```

---

# 16. Exception Handling

## Definition
Gracefully handles runtime errors.

## Example

```python
try:
    x = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
finally:
    print("Done")
```

---

# 17. Classes

## Definition
Blueprint for creating objects.

## Example

```python
class Employee:

    def __init__(self, name):
        self.name = name

employee = Employee("Julio")

print(employee.name)
```

---

# 18. Inheritance

## Definition
Reuse functionality from another class.

## Example

```python
class Animal:

    def speak(self):
        print("Animal")

class Dog(Animal):

    def bark(self):
        print("Woof")

dog = Dog()

dog.speak()
dog.bark()
```

---

# 19. Polymorphism

## Definition
Same method, different behavior.

## Example

```python
class Dog:

    def speak(self):
        print("Woof")

class Cat:

    def speak(self):
        print("Meow")

animals = [Dog(), Cat()]

for animal in animals:
    animal.speak()
```

---

# 20. Encapsulation

## Definition
Hide implementation details using private attributes.

## Example

```python
class Bank:

    def __init__(self):
        self.__balance = 100

bank = Bank()
```

---

# 21. File Handling

## Definition
Read and write files.

## Example

```python
with open("sample.txt", "w") as file:
    file.write("Hello Python")

with open("sample.txt") as file:
    print(file.read())
```

---

# 22. Modules

## Definition
A Python file containing reusable code.

## Example

```python
import math

print(math.sqrt(25))
```

---

# 23. Packages

## Definition
Collection of Python modules.

## Example

```
project/

    app/
        __init__.py
        users.py
        products.py
```

---

# 24. Decorators

## Definition
Modify a function without changing its code.

## Example

```python
def logger(func):

    def wrapper():
        print("Before")
        func()
        print("After")

    return wrapper

@logger
def hello():
    print("Hello")

hello()
```

---

# 25. Context Managers

## Definition
Automatically manage resources.

## Example

```python
with open("data.txt") as file:
    print(file.read())
```

---

# 26. Virtual Environments

## Definition
Isolated Python environments for dependencies.

## Commands

```bash
python -m venv .venv

source .venv/bin/activate

pip install requests
```

Windows:

```cmd
.venv\Scripts\activate
```

---

# 27. Type Hints

## Definition
Improve readability and IDE support.

## Example

```python
def add(x: int, y: int) -> int:
    return x + y

print(add(3,4))
```

---

# 28. Dataclasses

## Definition
Automatically generate boilerplate methods like `__init__`, `__repr__`, and `__eq__`.

## Example

```python
from dataclasses import dataclass

@dataclass
class Employee:
    id: int
    name: str

employee = Employee(1, "Julio")

print(employee)
```

---

# 29. Async Programming

## Definition
Concurrent programming using `async` and `await`.

## Example

```python
import asyncio

async def hello():
    print("Hello")

asyncio.run(hello())
```

---

# 30. Popular Built-in Functions

| Function | Purpose |
|----------|----------|
| len() | Length |
| range() | Sequence of numbers |
| sum() | Sum values |
| max() | Largest value |
| min() | Smallest value |
| sorted() | Sort collection |
| zip() | Combine iterables |
| map() | Transform values |
| filter() | Filter values |
| enumerate() | Index + value |
| any() | Any True |
| all() | All True |

Example

```python
numbers = [1,2,3,4]

print(sum(numbers))
print(max(numbers))
print(sorted(numbers))
```

---

# Python Interview Tips

## Know the difference between

- List vs Tuple
- List vs Generator
- Generator vs Iterator
- is vs ==
- copy vs deepcopy
- Mutable vs Immutable
- @staticmethod vs @classmethod
- *args vs **kwargs
- Threading vs Multiprocessing
- map() vs filter()
- append() vs extend()
- sorted() vs sort()
- remove() vs pop()
- yield vs return
- global vs nonlocal
- shallow copy vs deep copy

---

# Common Interview Topics

- Object-Oriented Programming (OOP)
- Functional Programming
- Exception Handling
- Collections
- Comprehensions
- Decorators
- Context Managers
- Generators
- Iterators
- Lambda Functions
- File Handling
- Modules & Packages
- Virtual Environments
- Type Hints
- Dataclasses
- Async Programming
- Testing with pytest
- Logging
- REST API Development (FastAPI/Flask/Django)
- ETL Workflows
- Pandas & NumPy
- SQL Integration
- Concurrency and Multiprocessing
- Memory Management
- Performance Optimization
