# Snowflake Interview Prep (Senior Python / Data Engineer)

> **Interview Goal:** Understand Snowflake's architecture, how it differs from traditional databases, how to connect using Python, and how it fits into modern ETL and analytics workflows.

---

# Table of Contents

1. What is Snowflake?
2. Why Snowflake?
3. Snowflake Architecture
4. Core Components
5. Virtual Warehouses
6. Databases, Schemas, and Tables
7. Storage Layers
8. Compute Layers
9. Services Layer
10. Snowflake Data Types
11. SQL in Snowflake
12. Python Connectivity
13. Loading Data
14. Querying Data
15. Snowpark for Python
16. Semi-Structured Data
17. Time Travel
18. Zero-Copy Cloning
19. Data Sharing
20. Security
21. Performance Optimization
22. ETL Workflow
23. Snowflake vs Databricks
24. Snowflake vs SQL Server
25. Common Interview Questions
26. Python ETL Example
27. Senior Interview Tips

---

# 1. What is Snowflake?

## Interview Answer

Snowflake is a **cloud-native data warehouse platform** designed for storing, processing, and analyzing massive amounts of structured and semi-structured data.

Unlike traditional databases, Snowflake separates **storage** from **compute**, allowing each to scale independently.

---

# Why Companies Use Snowflake

- Cloud-native
- High performance
- Automatic scaling
- Secure data sharing
- Built-in data compression
- Near-zero administration
- Excellent support for analytics

---

# Common Use Cases

- Enterprise Reporting
- Business Intelligence
- Data Warehousing
- ETL Pipelines
- Machine Learning
- Data Lakes
- Financial Reporting

---

# 2. Snowflake Architecture

```
              Users

                 │

                 ▼

         Services Layer

                 │

     Authentication
     Security
     Metadata
     Query Optimizer

                 │

                 ▼

        Virtual Warehouse
          (Compute)

                 │

                 ▼

         Storage Layer

                 │

                 ▼

       Cloud Storage
```

---

# Three Main Layers

## Storage Layer

Stores

- Tables
- Files
- Data
- Metadata

Automatically compressed.

---

## Compute Layer

Uses **Virtual Warehouses**.

Responsibilities

- Execute SQL
- Run ETL
- Transform data
- Analytics

Multiple warehouses can access the same data simultaneously.

---

## Services Layer

Manages

- Authentication
- Security
- Metadata
- Query Optimization
- Transactions
- Access Control

---

# 3. Virtual Warehouses

A Virtual Warehouse is Snowflake's compute engine.

Think of it like:

```
CPU + Memory
```

It performs all processing while storage remains separate.

---

# Warehouse Sizes

- X-Small
- Small
- Medium
- Large
- X-Large
- 2X-Large
- 3X-Large

Warehouses can scale automatically.

---

# Auto Suspend

Automatically stops a warehouse after inactivity.

Benefits

- Saves money
- Reduces compute costs

---

# Auto Resume

Automatically starts when a query arrives.

---

# 4. Database Hierarchy

```
Organization

    │

Account

    │

Database

    │

Schema

    │

Table

    │

Rows
```

---

# Example

```
CompanyDB

    │

HR

    │

Employees
```

---

# 5. Snowflake Data Types

Numeric

```
NUMBER
INT
FLOAT
DECIMAL
```

Text

```
VARCHAR
CHAR
TEXT
```

Date

```
DATE
TIME
TIMESTAMP
```

Boolean

```
BOOLEAN
```

Semi-Structured

```
VARIANT
ARRAY
OBJECT
```

---

# 6. Creating a Table

```sql
CREATE TABLE Employee (

    EmployeeID INT,

    Name STRING,

    Salary NUMBER,

    HireDate DATE
);
```

---

# 7. Querying Data

```sql
SELECT *

FROM Employee;
```

Filter

```sql
SELECT *

FROM Employee

WHERE Salary > 80000;
```

Group By

```sql
SELECT

Department,

AVG(Salary)

FROM Employee

GROUP BY Department;
```

---

# 8. Connecting from Python

Install

```bash
pip install snowflake-connector-python
```

---

# Python Connection

```python
import snowflake.connector

connection = snowflake.connector.connect(

    user="USER",

    password="PASSWORD",

    account="ACCOUNT",

    warehouse="COMPUTE_WH",

    database="CompanyDB",

    schema="HR"

)

cursor = connection.cursor()
```

---

# Execute Query

```python
cursor.execute(

    "SELECT * FROM Employee"

)

rows = cursor.fetchall()

for row in rows:

    print(row)
```

---

# Close Connection

```python
cursor.close()

connection.close()
```

---

# 9. Using Pandas

```python
import pandas as pd

df = pd.read_sql(

    "SELECT * FROM Employee",

    connection

)
```

---

# 10. Snowpark for Python

Snowpark allows developers to write data transformations using Python instead of SQL.

Example

```python
from snowflake.snowpark import Session
```

Filter

```python
employees.filter(

    employees.salary > 80000

)
```

---

# Why Snowpark?

- Python code
- DataFrames
- Pushes execution into Snowflake
- Better performance
- No data movement

---

# 11. Loading Data

CSV

```
CSV

↓

Stage

↓

COPY INTO

↓

Table
```

---

# Stage

Temporary storage before loading.

Internal Stage

External Stage

- AWS S3
- Azure Blob
- Google Cloud Storage

---

# COPY INTO

```sql
COPY INTO Employee

FROM @EmployeeStage

FILE_FORMAT = (

TYPE = CSV

FIELD_OPTIONALLY_ENCLOSED_BY='"'

SKIP_HEADER=1

);
```

---

# 12. Semi-Structured Data

Supported

- JSON
- XML
- Avro
- Parquet

Example

```sql
SELECT

data:name

FROM Customers;
```

---

# VARIANT

Stores JSON directly.

```sql
CREATE TABLE Events(

EventData VARIANT

);
```

---

# 13. Time Travel

Recover deleted or updated data.

Example

```sql
SELECT *

FROM Employee

AT(

OFFSET => -60*5

);
```

Benefits

- Recovery
- Auditing
- Historical queries

---

# 14. Zero-Copy Cloning

Clone databases instantly.

```sql
CREATE DATABASE TestDB

CLONE ProductionDB;
```

Advantages

- Fast
- No duplicate storage
- Great for testing

---

# 15. Secure Data Sharing

Snowflake allows sharing data without copying it.

Benefits

- No ETL
- No exports
- Secure
- Real-time access

---

# 16. Security

Features

- Role-Based Access Control (RBAC)
- Multi-Factor Authentication (MFA)
- Encryption
- Network Policies
- Data Masking
- Row Access Policies

---

# Roles

Examples

```
ACCOUNTADMIN

SYSADMIN

SECURITYADMIN

USERADMIN

PUBLIC
```

---

# 17. Performance Optimization

Best Practices

- Clustering Keys
- Result Cache
- Warehouse Cache
- Query Pruning
- Auto Scaling
- Materialized Views

---

# Caching

Snowflake automatically caches

- Query Results
- Metadata
- Warehouse Data

Benefits

- Faster repeated queries
- Lower compute costs

---

# 18. ETL Workflow

```
REST API
CSV
JSON
Database

        │

        ▼

Python

        │

        ▼

Validation

        │

        ▼

Transform

        │

        ▼

Snowflake Stage

        │

        ▼

COPY INTO

        │

        ▼

Snowflake Tables

        │

        ▼

Power BI

Tableau

Machine Learning
```

---

# 19. Snowflake vs Databricks

| Snowflake | Databricks |
|------------|------------|
| Cloud Data Warehouse | Data Engineering Platform |
| SQL Focused | Spark Focused |
| Analytics | ETL + ML |
| Warehouses | Spark Clusters |
| Snowpark | Apache Spark |

---

# 20. Snowflake vs SQL Server

| SQL Server | Snowflake |
|------------|-----------|
| On-Premises | Cloud Native |
| Shared Resources | Separate Compute & Storage |
| Manual Scaling | Auto Scaling |
| DBA Intensive | Minimal Administration |
| Local Storage | Cloud Storage |

---

# 21. Common Interview Questions

## What is Snowflake?

A cloud-native data warehouse that separates compute from storage, enabling scalable analytics and high-performance querying.

---

## What is a Virtual Warehouse?

A compute cluster that executes SQL queries independently of the storage layer.

---

## Why separate Compute and Storage?

Benefits

- Independent scaling
- Lower costs
- Better concurrency
- Higher performance

---

## What is Snowpark?

A developer framework that allows writing data transformations in Python, Java, or Scala while executing inside Snowflake.

---

## What is Time Travel?

Allows querying and recovering historical versions of data.

---

## What is Zero-Copy Cloning?

Creates instant copies of databases, schemas, or tables without duplicating physical storage.

---

## What is a Stage?

A temporary storage location used to load files into Snowflake.

---

## Difference between Internal and External Stages?

Internal Stage

- Stored inside Snowflake

External Stage

- AWS S3
- Azure Blob Storage
- Google Cloud Storage

---

## Why use Snowflake instead of a traditional database?

- Automatic scaling
- Cloud-native
- High concurrency
- Minimal administration
- Secure data sharing
- Excellent analytics performance

---

# 22. Complete Python ETL Example

```python
import pandas as pd
import snowflake.connector

# -----------------------------
# Connect
# -----------------------------

conn = snowflake.connector.connect(

    user="USER",

    password="PASSWORD",

    account="ACCOUNT",

    warehouse="COMPUTE_WH",

    database="CompanyDB",

    schema="HR"

)

# -----------------------------
# Extract
# -----------------------------

employees = pd.read_csv(

    "employees.csv"

)

# -----------------------------
# Transform
# -----------------------------

employees = employees.drop_duplicates()

employees["Bonus"] = (

    employees["Salary"] * 0.10

)

# -----------------------------
# Load
# -----------------------------

cursor = conn.cursor()

for _, row in employees.iterrows():

    cursor.execute(

        """
        INSERT INTO Employee
        VALUES (%s,%s,%s,%s)
        """,

        (

            row["EmployeeID"],

            row["Name"],

            row["Salary"],

            row["Bonus"]

        )

    )

conn.commit()

cursor.close()

conn.close()
```

> **Production Note:** For large datasets, avoid inserting one row at a time. Use `write_pandas()` from the Snowflake Connector or bulk loading with **Stages** and **COPY INTO** for significantly better performance.

---

# 23. Senior Interview Tips

- Understand the **three-layer Snowflake architecture** (Storage, Compute, Services).
- Explain why **compute and storage are separated**.
- Know how **Virtual Warehouses** work and how they auto-scale.
- Be familiar with **Snowpark** and why it reduces data movement.
- Understand **Stages**, **COPY INTO**, and bulk loading strategies.
- Learn **Time Travel**, **Zero-Copy Cloning**, and **Secure Data Sharing**—these are frequently asked differentiators.
- Discuss **RBAC**, **MFA**, and encryption when asked about security.
- Compare Snowflake with **Databricks**, **SQL Server**, and **Redshift**, including the strengths and trade-offs of each.