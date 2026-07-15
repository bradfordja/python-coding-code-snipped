# ETL Workflows in Python - Senior Interview Prep

> **Interview Goal:** Be able to explain what ETL is, how to build an ETL pipeline in Python, and which libraries, design patterns, and best practices are commonly used in production systems.

---

# Table of Contents

1. What is ETL?
2. ETL Architecture
3. Python ETL Workflow
4. Common Python ETL Libraries
5. Extract Phase
6. Transform Phase
7. Load Phase
8. ETL Project Structure
9. Data Validation
10. Error Handling
11. Logging
12. Configuration Management
13. Database Connections
14. Working with APIs
15. Working with Large Files
16. Scheduling ETL Jobs
17. Cloud ETL
18. Performance Optimization
19. Security Best Practices
20. ETL Design Patterns
21. Common Interview Questions
22. Complete ETL Example
23. Senior-Level Best Practices

---

# 1. What is ETL?

**ETL** stands for:

- **E**xtract
- **T**ransform
- **L**oad

It is the process of moving data from one or more source systems into a destination after cleaning and transforming the data.

```
Database
CSV
Excel
REST API
JSON
XML

        ↓

     Extract

        ↓

    Transform

        ↓

        Load

        ↓

Data Warehouse
Database
Data Lake
Analytics
Machine Learning
```

---

# Interview Answer

> ETL is a data integration process where data is extracted from one or more sources, transformed into a usable format, and loaded into a destination such as a database, data warehouse, or data lake.

---

# 2. ETL Architecture

Typical production workflow

```
CSV Files
REST APIs
SQL Server
Oracle
PostgreSQL
MongoDB

        │

        ▼

Extract Layer

        │

        ▼

Validation

        │

        ▼

Transformation

        │

        ▼

Business Rules

        │

        ▼

Load Layer

        │

        ▼

Warehouse / Analytics
```

---

# 3. Python ETL Workflow

Typical workflow

```text
Start

↓

Read Source

↓

Validate Data

↓

Clean Data

↓

Transform Data

↓

Business Rules

↓

Save Results

↓

Logging

↓

Finish
```

---

# 4. Common Python ETL Libraries

| Library | Purpose |
|----------|---------|
| pandas | Data manipulation |
| numpy | Numerical processing |
| sqlalchemy | Database access |
| psycopg2 | PostgreSQL |
| pyodbc | SQL Server |
| requests | REST APIs |
| boto3 | AWS services |
| openpyxl | Excel |
| pathlib | File handling |
| logging | Logging |
| json | JSON |
| csv | CSV |
| datetime | Date operations |

---

# 5. Extract Phase

Extract means reading data.

Examples

- CSV
- Excel
- Database
- REST API
- JSON
- XML
- AWS S3

---

## Read CSV

```python
import pandas as pd

df = pd.read_csv("employees.csv")
```

---

## Read Excel

```python
df = pd.read_excel("employees.xlsx")
```

---

## Read JSON

```python
df = pd.read_json("employees.json")
```

---

## Read SQL

```python
from sqlalchemy import create_engine

engine = create_engine(connection_string)

df = pd.read_sql(
    "SELECT * FROM Employee",
    engine
)
```

---

## REST API

```python
import requests

response = requests.get(url)

data = response.json()
```

---

# 6. Transform Phase

Transformation applies business rules.

Examples

- Remove duplicates
- Remove null values
- Rename columns
- Convert data types
- Normalize data
- Aggregate
- Join datasets
- Calculate fields

---

Remove duplicates

```python
df = df.drop_duplicates()
```

---

Fill missing salary

```python
df["Salary"] = df["Salary"].fillna(0)
```

---

Convert string to datetime

```python
df["HireDate"] = pd.to_datetime(df["HireDate"])
```

---

Rename columns

```python
df.rename(columns={
    "EmpName": "EmployeeName"
})
```

---

Create new column

```python
df["Bonus"] = df["Salary"] * .10
```

---

Filter records

```python
df = df[df["Salary"] > 50000]
```

---

# 7. Load Phase

Load stores processed data.

Examples

- SQL Server
- Oracle
- PostgreSQL
- Snowflake
- Redshift
- BigQuery
- CSV
- Excel
- AWS S3

---

Save CSV

```python
df.to_csv("output.csv")
```

---

Save SQL

```python
df.to_sql(
    "Employee",
    engine,
    if_exists="append",
    index=False
)
```

---

# 8. ETL Project Structure

```
etl_project/

│
├── main.py
├── config.py
├── requirements.txt
│
├── extract/
│     csv_reader.py
│     api_reader.py
│     database_reader.py
│
├── transform/
│     cleaning.py
│     validation.py
│     business_rules.py
│
├── load/
│     database_writer.py
│     csv_writer.py
│
├── utils/
│     logger.py
│
└── tests/
```

---

# 9. Data Validation

Examples

Check missing values

```python
df.isnull().sum()
```

---

Required columns

```python
required = [
    "EmployeeId",
    "Salary"
]

missing = set(required) - set(df.columns)
```

---

Validate salary

```python
df = df[df["Salary"] >= 0]
```

---

# 10. Error Handling

```python
try:

    df = pd.read_csv("employees.csv")

except FileNotFoundError:

    print("File not found")

except Exception as ex:

    print(ex)
```

---

# 11. Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO
)

logging.info("ETL Started")

logging.info("Loading CSV")

logging.error("Database failed")
```

---

# 12. Configuration Management

Avoid hardcoding values.

config.py

```python
DATABASE_URL = "..."

CSV_FILE = "employees.csv"
```

Usage

```python
import config

print(config.DATABASE_URL)
```

---

# 13. Database Connections

```python
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL
)

df = pd.read_sql(
    "SELECT * FROM Employee",
    engine
)
```

---

# 14. Working with APIs

```python
import requests

response = requests.get(url)

if response.ok:

    data = response.json()
```

---

# 15. Working with Large Files

Instead of loading everything

```python
pd.read_csv(file)
```

Use chunks

```python
for chunk in pd.read_csv(
    file,
    chunksize=10000
):

    process(chunk)
```

Advantages

- Lower memory
- Faster
- Better scalability

---

# 16. Scheduling ETL Jobs

Common schedulers

- Cron
- Windows Task Scheduler
- Apache Airflow
- Prefect
- Dagster
- AWS Lambda
- Azure Data Factory

---

# 17. Cloud ETL

AWS

- S3
- Lambda
- Glue
- Athena
- Redshift

Azure

- Azure Data Factory
- Blob Storage
- Synapse

Google

- Cloud Storage
- BigQuery
- Dataflow

---

# 18. Performance Optimization

Avoid loops

❌

```python
for row in df.iterrows():
    ...
```

Use vectorization

✅

```python
df["Bonus"] = df["Salary"] * .10
```

Other optimizations

- Process in chunks
- Batch database inserts
- Use indexes
- Parallel processing
- Cache lookups

---

# 19. Security Best Practices

Never

```python
password = "admin123"
```

Use

```
Environment Variables

AWS Secrets Manager

Azure Key Vault

HashiCorp Vault
```

Always

- Encrypt connections
- Parameterized SQL
- Least privilege access
- Audit logging

---

# 20. ETL Design Patterns

Layered architecture

```
Extract

↓

Transform

↓

Load
```

Pipeline pattern

```
Reader

↓

Validator

↓

Transformer

↓

Writer
```

Dependency Injection

```
Reader

↓

Service

↓

Writer
```

---

# 21. Common Interview Questions

## What is ETL?

Extract, Transform, Load.

---

## Difference between ETL and ELT?

ETL

```
Extract

↓

Transform

↓

Load
```

ELT

```
Extract

↓

Load

↓

Transform
```

Transformation happens after loading, typically inside a cloud data warehouse.

---

## How do you handle large datasets?

- Chunk processing
- Batch inserts
- Vectorized operations
- Parallel processing
- Efficient SQL queries

---

## Why use SQLAlchemy?

- Database independent
- Connection pooling
- ORM support
- Safe parameterized queries

---

## Why use Pandas?

- Fast transformations
- Easy filtering
- Aggregation
- Cleaning
- Joining datasets

---

## How do you recover from ETL failures?

- Logging
- Retry logic
- Transaction rollback
- Alerts
- Checkpoints

---

## How do you validate data?

- Required fields
- Data types
- Duplicate detection
- Null checks
- Business rule validation

---

# 22. Complete ETL Example

```python
import pandas as pd
from sqlalchemy import create_engine

# ----------------------------
# Extract
# ----------------------------

employees = pd.read_csv(
    "employees.csv"
)

# ----------------------------
# Transform
# ----------------------------

employees = employees.drop_duplicates()

employees["Salary"] = (
    employees["Salary"]
        .fillna(0)
)

employees["Bonus"] = (
    employees["Salary"] * .10
)

employees = employees[
    employees["Salary"] > 50000
]

# ----------------------------
# Load
# ----------------------------

engine = create_engine(
    DATABASE_URL
)

employees.to_sql(
    "Employee",
    engine,
    if_exists="append",
    index=False
)
```

---

# 23. Senior-Level Best Practices

## Code Organization

- Small reusable functions
- Separate Extract, Transform, and Load modules
- Use configuration files
- Environment variables
- Dependency Injection where appropriate

---

## Reliability

- Logging
- Retry logic
- Exception handling
- Validation
- Monitoring
- Alerting

---

## Performance

- Batch inserts
- Chunk processing
- Vectorized Pandas operations
- SQL pushdown when possible
- Parallel execution

---

## Security

- Parameterized SQL
- Secrets Manager
- IAM Roles
- Encryption
- Audit logging

---

# ETL Workflow Summary

```
CSV
Database
REST API
Excel
JSON

        │

        ▼

Extract

        │

        ▼

Validate

        │

        ▼

Clean Data

        │

        ▼

Transform

        │

        ▼

Business Rules

        │

        ▼

Load

        │

        ▼

SQL Database
Data Warehouse
S3
Analytics
Machine Learning
```

---

# Senior Interview Tips

- Understand the complete ETL lifecycle from source to destination.
- Explain why data validation is critical before loading.
- Discuss error handling, retries, and logging for production systems.
- Know the difference between **ETL** and **ELT**.
- Be comfortable reading from CSVs, APIs, databases, and cloud storage.
- Emphasize modular design, configuration management, and testability.
- Be ready to discuss orchestration tools like **Apache Airflow**, **Prefect**, or **Dagster** for scheduling and monitoring ETL workflows.

