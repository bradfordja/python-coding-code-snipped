# commonly used Python built-in functions

Below are the most commonly used Python built-in functions that frequently appear in Python coding interviews, with a short description, common use case, and a sample code snippet.

⸻

Python Common Functions Interview Cheat Sheet

## print()

Description
Displays output to the console.
Use Case

* Debugging
* Logging simple output
* Displaying results

name = "Julio"
print(name)

Output

Julio

⸻

# len()

Description

Returns the number of items in an object.

Use Case

* Count characters
* Count list items
* Validate collections

names = ["Tom", "Bob", "Sam"]
print(len(names))

Output

3

⸻

# type()

Description

Returns the object’s data type.

Use Case

* Debugging
* Type checking

age = 35
print(type(age))

Output

<class 'int'>

⸻

# input()

Description

Reads user input.

Use Case

* CLI applications
* User interaction

name = input("Enter your name: ")
print(name)

⸻

# int()

Description

Converts a value into an integer.

Use Case

* Convert form input
* Convert strings to numbers

age = int("25")
print(age)

Output

25

⸻

# float()

Description
Converts a value into a floating-point number.
Use Case

* Currency
* Calculations

price = float("10.99")
print(price)

Output

10.99

⸻

# str()

Description
Converts a value into a string.
Use Case

* Logging
* String concatenation

age = 25
print("Age: " + str(age))

⸻

# bool()

Description
Converts a value to a Boolean.
Use Case

* Conditional logic

print(bool(1))
print(bool(0))

Output

True
False

⸻

# list()

Description
Creates a list.
Use Case

* Convert iterable objects

letters = list("Python")
print(letters)

Output

['P', 'y', 't', 'h', 'o', 'n']

⸻

# tuple()

Description
Creates an immutable tuple.
Use Case

* Read-only collections

numbers = tuple([1, 2, 3])
print(numbers)

⸻

# set()

Description
Creates a collection of unique values.
Use Case

* Remove duplicates
* Fast lookups

numbers = set([1, 2, 2, 3])
print(numbers)

Output

{1,2,3}

⸻

# dict()

Description
Creates a dictionary.
Use Case

* Key-value storage

person = dict(name="Tom", age=30)
print(person)

⸻

# range()

Description
Generates a sequence of numbers.
Use Case

* Loops
* Iteration
```py
for i in range(5):
    print(i)
```
Output

0
1
2
3
4

⸻

# enumerate()

Description
Returns index and value while looping.
Use Case

* Indexed loops
```py
names = ["Tom", "Bob", "Sam"]
for index, name in enumerate(names):
    print(index, name)
```
⸻

# zip()

Description
Combines multiple iterables.
Use Case

* Pair related lists
```py
names = ["Tom", "Bob"]
ages = [20, 30]
for name, age in zip(names, ages):
    print(name, age)
```
⸻

# sorted()

Description
Returns a sorted copy.
Use Case

* Sorting without modifying original data
```py
numbers = [5, 2, 8]
print(sorted(numbers))
```
Output

[2,5,8]

⸻

# reversed()

Description
Returns a reverse iterator.
Use Case

* Reverse traversal
```py
numbers = [1,2,3]
print(list(reversed(numbers)))
```
Output

[3,2,1]

⸻

# sum()

Description
Adds numbers together.
Use Case

* Totals
* Aggregation
```py
numbers = [10,20,30]
print(sum(numbers))
```
Output

60

⸻

# min()

Description

Returns the smallest value.

Use Case

* Find minimum
```py
scores = [80,95,60]
print(min(scores))
```
⸻

# max()

Description
Returns the largest value.
Use Case

* Highest score
```py
scores = [80,95,60]
print(max(scores))
```
⸻

# abs()

Description
Returns the absolute value.
Use Case

* Distance calculations
```py
print(abs(-15))
```
Output

15

⸻

# round()

Description
Rounds a floating-point number.
Use Case

* Currency
* Reports
```py
price = 10.678
print(round(price, 2))
```
Output

10.68

⸻

# any()

Description
Returns True if at least one element is true.
Use Case

* Validation
* Permission checks
```py
values = [False, False, True]
print(any(values))
```
Output

True

⸻

# all()

Description
Returns True if all elements are true.
Use Case

* Validation
```py
values = [True, True, True]
print(all(values))
```
⸻

25. map()

Description
Applies a function to every item.
Use Case

* Data transformation
```py
numbers = [1,2,3]
result = list(map(lambda x: x*x, numbers))
print(result)
```
Output

[1,4,9]

⸻

26. filter()

Description
Filters items using a condition.
Use Case

* Remove unwanted values
```py
numbers = [1,2,3,4,5]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)
```
Output

[2,4]

⸻

# sorted() with key

Description
Sorts using a custom key.
Use Case

* Sort objects
* Sort dictionaries
```py
names = ["Julio", "Amy", "Christopher"]
print(sorted(names, key=len))
```
Output

['Amy', 'Julio', 'Christopher']

⸻

# isinstance()

Description
Checks an object’s type.
Use Case

* Runtime type checking
```py
age = 35
print(isinstance(age, int))
```
Output

True

⸻

# open()

Description
Opens a file.
Use Case

* Read/write files
```py
with open("sample.txt", "r") as file:
    print(file.read())
```
⸻

# help()

Description
Displays documentation.
Use Case

* Learn APIs quickly
```py
help(len)
```
⸻

Senior Python Interview Favorites

These functions and patterns are especially common in senior-level interviews:
```sh
Function	Why Interviewers Ask
enumerate()	Cleaner loops with indexes
zip()	Combine multiple iterables elegantly
map()	Functional programming knowledge
filter()	Data processing pipelines
sorted(key=...)	Custom sorting of complex objects
any() / all()	Efficient boolean aggregation
isinstance()	Type-safe code
sum()	Simple aggregation
set()	Removing duplicates and fast membership tests (O(1) average lookup)
range()	Efficient iteration without creating unnecessary lists
```

These built-in functions are widely used in production code because they make Python programs more concise, readable, and efficient. Mastering them is excellent preparation for Python interviews, including HackerRank, LeetCode, and senior backend engineering roles.