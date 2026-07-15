# Pandas Interview Prep Cheat Sheet (Senior Python Developer)

> **Interview Tip:** Pandas is one of the most common libraries used in Python interviews for Data Engineering, Data Science, Machine Learning, and Backend development. Interviewers expect you to understand how to manipulate, clean, transform, and analyze structured data efficiently.

---

# Table of Contents

1. What is Pandas?
2. Installing Pandas
3. Importing Pandas
4. Series
5. DataFrame
6. Reading Data
7. Viewing Data
8. Selecting Columns
9. Filtering Rows
10. loc vs iloc
11. Creating Columns
12. Updating Data
13. Handling Missing Data
14. Sorting Data
15. Group By
16. Aggregation
17. Merge (SQL Join)
18. Concatenate
19. Apply
20. Map
21. Unique Values
22. Removing Duplicates
23. Renaming Columns
24. Working with Dates
25. Exporting Data
26. Performance Best Practices
27. Pandas vs NumPy
28. Common Interview Questions
29. Java / JavaScript Comparison
30. Senior Coding Example

---

# 1. What is Pandas?

## Interview Answer

Pandas is an open-source Python library used for data manipulation and analysis. It provides powerful data structures like **Series** and **DataFrame** that make it easy to clean, transform, analyze, and export structured data.

### Common Uses

- Reading CSV files
- Reading Excel files
- Reading JSON
- Reading SQL databases
- Cleaning data
- Data transformation
- ETL pipelines
- Reporting
- Machine Learning preprocessing

---

# 2. Installing Pandas

```bash
pip install pandas
```

Verify installation:

```python
import pandas as pd

print(pd.__version__)
```

---

# 3. Importing Pandas

```python
import pandas as pd
```

Nearly every Pandas project begins with this import.

---

# 4. Series

A **Series** is a one-dimensional labeled array.

Think of it as:

- One Excel column
- One SQL column
- Java List<Integer>

Example:

```python
import pandas as pd

ages = pd.Series([25, 30, 35])

print(ages)
```

Output

```
0    25
1    30
2    35
dtype: int64
```

---

# 5. DataFrame

A **DataFrame** is a two-dimensional table.

Think of it as:

- Excel spreadsheet
- SQL table
- Java List<Employee>
- JavaScript Array of Objects

```python
employees = pd.DataFrame({
    "Name": ["John", "Mary"],
    "Salary": [80000, 90000],
    "Department": ["IT", "HR"]
})

print(employees)
```

Output

```
   Name  Salary Department
0  John   80000         IT
1  Mary   90000         HR
```

---

# 6. Reading Data

## CSV

```python
df = pd.read_csv("employees.csv")
```

## Excel

```python
df = pd.read_excel("employees.xlsx")
```

## JSON

```python
df = pd.read_json("employees.json")
```

## SQL

```python
df = pd.read_sql(query, connection)
```

---

# 7. Viewing Data

First rows

```python
df.head()
```

Last rows

```python
df.tail()
```

General information

```python
df.info()
```

Statistics

```python
df.describe()
```

Shape

```python
df.shape
```

Column names

```python
df.columns
```

---

# 8. Selecting Columns

Single column

```python
df["Salary"]
```

Multiple columns

```python
df[["Name", "Salary"]]
```

---

# 9. Filtering Rows

Salary greater than 80,000

```python
df[df["Salary"] > 80000]
```

Department equals IT

```python
df[df["Department"] == "IT"]
```

Multiple conditions

```python
df[
    (df["Department"] == "IT") &
    (df["Salary"] > 80000)
]
```

---

# 10. loc vs iloc

## loc

Uses labels.

```python
df.loc[0]
```

Specific columns

```python
df.loc[:, ["Name", "Salary"]]
```

---

## iloc

Uses integer positions.

```python
df.iloc[0]
```

Rows 0-2

```python
df.iloc[0:3]
```

---

## Interview Answer

```
loc = labels

iloc = integer positions
```

---

# 11. Creating Columns

```python
df["Bonus"] = df["Salary"] * 0.10
```

Output

```
Salary    Bonus

80000      8000
90000      9000
```

---

# 12. Updating Data

```python
df.loc[0, "Salary"] = 85000
```

---

# 13. Handling Missing Data

Check for nulls

```python
df.isnull()
```

Count missing values

```python
df.isnull().sum()
```

Drop missing rows

```python
df.dropna()
```

Replace with zero

```python
df.fillna(0)
```

Replace with average

```python
df["Salary"] = df["Salary"].fillna(df["Salary"].mean())
```

---

# 14. Sorting Data

Ascending

```python
df.sort_values("Salary")
```

Descending

```python
df.sort_values("Salary", ascending=False)
```

---

# 15. Group By

Average salary by department

```python
df.groupby("Department")["Salary"].mean()
```

Count employees

```python
df.groupby("Department").size()
```

Sum salaries

```python
df.groupby("Department")["Salary"].sum()
```

---

# 16. Aggregation

```python
df.groupby("Department").agg({
    "Salary": ["mean", "max", "min"],
    "Bonus": "sum"
})
```

---

# 17. Merge (SQL JOIN)

Employees

```
ID   Name

1    John
2    Mary
```

Departments

```
ID   Department

1    IT
2    HR
```

Merge

```python
pd.merge(emp, dept, on="ID")
```

Equivalent SQL

```sql
SELECT *
FROM employee
JOIN department
ON employee.id = department.id;
```

---

# 18. Concatenate

Append DataFrames

```python
pd.concat([df1, df2])
```

---

# 19. Apply

Create a new column

```python
df["Tax"] = df["Salary"].apply(lambda salary: salary * 0.30)
```

---

# 20. Map

```python
grades = {
    "A": 4,
    "B": 3,
    "C": 2
}

df["Points"] = df["Grade"].map(grades)
```

---

# 21. Unique Values

Unique departments

```python
df["Department"].unique()
```

Count occurrences

```python
df["Department"].value_counts()
```

---

# 22. Removing Duplicates

Entire row

```python
df.drop_duplicates()
```

Specific column

```python
df.drop_duplicates(subset="Email")
```

---

# 23. Renaming Columns

```python
df.rename(columns={
    "Salary": "AnnualSalary"
})
```

---

# 24. Working with Dates

Convert string to datetime

```python
df["HireDate"] = pd.to_datetime(df["HireDate"])
```

Extract year

```python
df["HireDate"].dt.year
```

Extract month

```python
df["HireDate"].dt.month
```

---

# 25. Exporting Data

CSV

```python
df.to_csv("employees.csv")
```

Excel

```python
df.to_excel("employees.xlsx")
```

JSON

```python
df.to_json("employees.json")
```

---

# 26. Performance Best Practices

❌ Avoid loops

```python
for row in df.iterrows():
    print(row)
```

✅ Use vectorized operations

```python
df["Bonus"] = df["Salary"] * 0.10
```

### Why?

- Faster
- Uses optimized NumPy operations
- More readable
- Better scalability

---

# 27. Pandas vs NumPy

| Feature | Pandas | NumPy |
|----------|---------|--------|
| Data Structure | DataFrame | ndarray |
| Labels | Yes | No |
| Missing Values | Excellent | Limited |
| CSV Support | Yes | No |
| SQL-like Operations | Yes | No |
| Performance | High | Very High |

---

# 28. Common Interview Questions

## What is a DataFrame?

A two-dimensional labeled data structure similar to an Excel spreadsheet or SQL table.

---

## Difference between Series and DataFrame?

Series:

- One column
- One-dimensional

DataFrame:

- Multiple columns
- Two-dimensional

---

## Difference between loc and iloc?

```
loc

Uses labels

iloc

Uses integer positions
```

---

## Difference between merge() and concat()?

merge()

- SQL JOIN
- Match rows using keys

concat()

- Stack DataFrames
- No matching keys required

---

## How do you handle missing values?

- isnull()
- notnull()
- dropna()
- fillna()

---

## Why avoid loops?

Because Pandas is optimized for **vectorized operations**, which are significantly faster than row-by-row iteration.

---

## What does groupby() do?

It splits data into groups, performs an aggregation, and combines the results.

Common aggregations include:

- mean
- sum
- count
- min
- max

---

# 29. Java / JavaScript Comparison

| JavaScript | Java | Pandas |
|------------|------|---------|
| Array of Objects | List<Employee> | DataFrame |
| filter() | stream().filter() | Boolean Indexing |
| map() | stream().map() | apply() / map() |
| reduce() | Collectors.groupingBy() | groupby().agg() |
| sort() | Collections.sort() | sort_values() |
| SQL JOIN | JPA Join | merge() |

---

# 30. Senior Interview Coding Example

**Question**

Given a CSV containing one million employee records:

- Ignore missing salaries
- Calculate average salary by department
- Return the top five departments

```python
import pandas as pd

df = pd.read_csv("employees.csv")

result = (
    df.dropna(subset=["Salary"])
      .groupby("Department")["Salary"]
      .mean()
      .sort_values(ascending=False)
      .head(5)
)

print(result)
```

## Concepts Demonstrated

- Reading CSV
- Handling missing values
- Grouping
- Aggregation
- Sorting
- Top N selection
- Method chaining
- Efficient vectorized operations

---

# Senior Interview Tips

- Prefer vectorized operations over loops.
- Understand the difference between `loc` and `iloc`.
- Be comfortable with `groupby()`, `merge()`, and `agg()`.
- Know how to clean missing and duplicate data.
- Practice reading and writing CSV, Excel, JSON, and SQL data.
- Explain how Pandas builds on NumPy for performance.
- Relate Pandas operations to SQL (`SELECT`, `WHERE`, `GROUP BY`, `JOIN`) and Java Streams to demonstrate transferable knowledge.
