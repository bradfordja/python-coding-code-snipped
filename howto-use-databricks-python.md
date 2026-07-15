# Databricks Interview Prep (Senior Python / Data Engineer)

> **Interview Goal:** Understand what Databricks is, how it works, its core architecture, and how it is used to build scalable data engineering, analytics, and machine learning solutions.

---

# What is Databricks?

## Interview Answer

Databricks is a **cloud-based data engineering and analytics platform** built on **Apache Spark**. It provides a collaborative workspace for data engineers, data scientists, analysts, and machine learning engineers to process massive amounts of data.

Think of Databricks as:

- Spark + Cloud
- Spark + Notebooks
- Spark + Data Lake
- Spark + Machine Learning
- Spark + SQL Analytics

---

# What Problems Does Databricks Solve?

Traditional ETL Problems

- Slow processing
- Large datasets
- Difficult cluster management
- Data silos
- Scaling challenges

Databricks Solves

- Distributed computing
- Auto scaling
- Collaborative notebooks
- Unified analytics
- Cloud-native architecture
- Machine Learning workflows

---

# Core Components

```
Cloud Storage
    │
    ▼
Data Lake
    │
    ▼
Databricks Workspace
    │
    ▼
Apache Spark Cluster
    │
    ▼
ETL
Analytics
Machine Learning
Reporting
```

---

# Databricks Architecture

```
Azure / AWS / GCP

        │

        ▼

Databricks Workspace

        │

        ▼

Spark Cluster

        │

        ▼

Data Lake

        │

        ▼

Delta Lake

        │

        ▼

SQL
Python
Scala
Machine Learning
```

---

# Apache Spark

Databricks is built on Apache Spark.

Spark provides:

- Distributed computing
- Parallel processing
- Fault tolerance
- In-memory processing
- High performance

---

# Databricks Workspace

A Workspace contains:

- Notebooks
- Clusters
- Jobs
- Dashboards
- Libraries
- Repositories

---

# Notebook Languages

Databricks supports multiple languages in the same workspace.

- Python
- SQL
- Scala
- R

Python example

```python
print("Hello Databricks")
```

SQL example

```sql
SELECT *
FROM employees;
```

---

# Clusters

A Cluster is a group of virtual machines running Apache Spark.

Responsibilities

- Execute notebooks
- Run ETL jobs
- Train ML models
- Execute SQL queries

Cluster Types

- Interactive Cluster
- Job Cluster

---

# Interactive Cluster

Used for:

- Development
- Testing
- Exploration

---

# Job Cluster

Used for:

- Scheduled ETL
- Production jobs
- Batch processing

Automatically starts and stops.

---

# Databricks Runtime

Databricks Runtime is an optimized version of Apache Spark.

Includes:

- Spark
- Delta Lake
- Optimized libraries
- Performance improvements
- Security enhancements

---

# Delta Lake

One of the most common interview topics.

## Interview Answer

Delta Lake is an open-source storage layer that adds ACID transactions, schema enforcement, versioning, and time travel to data lakes.

Benefits

- ACID Transactions
- Time Travel
- Version History
- Schema Validation
- Faster Queries
- Reliable Data Pipelines

---

# Data Formats

Most common formats

- CSV
- JSON
- Parquet
- Delta
- Avro
- ORC

Preferred production format

```
Delta
```

---

# Reading Data

CSV

```python
df = spark.read.csv(
    "/FileStore/employees.csv",
    header=True
)
```

Parquet

```python
df = spark.read.parquet(
    "/data/employees"
)
```

Delta

```python
df = spark.read.format(
    "delta"
).load("/employees")
```

---

# Writing Data

Delta

```python
df.write.format(
    "delta"
).save("/employees")
```

Overwrite

```python
df.write.mode(
    "overwrite"
).save("/employees")
```

Append

```python
df.write.mode(
    "append"
).save("/employees")
```

---

# DataFrame API

Spark DataFrames are similar to Pandas but distributed.

Filter

```python
df.filter(
    df.salary > 50000
)
```

Select

```python
df.select(
    "name",
    "salary"
)
```

Sort

```python
df.orderBy(
    "salary"
)
```

Group By

```python
df.groupBy(
    "department"
).count()
```

---

# Spark Transformations

Examples

- select()
- filter()
- withColumn()
- join()
- groupBy()
- orderBy()
- dropDuplicates()

---

# Spark Actions

Examples

```python
show()

count()

collect()

first()

take()
```

---

# Transformations vs Actions

Transformation

- Lazy
- Creates a new DataFrame

Examples

```python
filter()

select()

join()
```

Action

- Executes the Spark job

Examples

```python
show()

count()

collect()
```

---

# Lazy Evaluation

Spark does not execute immediately.

Example

```python
df = (
    spark.read.csv(file)
        .filter(...)
        .select(...)
)
```

Nothing runs until

```python
df.show()
```

---

# ETL in Databricks

```
Read CSV

↓

Validate

↓

Clean Data

↓

Business Rules

↓

Join Data

↓

Save Delta

↓

Analytics
```

---

# SQL in Databricks

```sql
SELECT
    Department,
    AVG(Salary)
FROM Employee
GROUP BY Department;
```

---

# Jobs

Jobs automate notebooks.

Examples

- Daily ETL
- Weekly Reports
- ML Training
- Data Imports

---

# Scheduling

Can schedule

- Hourly
- Daily
- Weekly
- Monthly

---

# Machine Learning

Databricks supports

- MLflow
- TensorFlow
- PyTorch
- Scikit-Learn
- XGBoost

---

# MLflow

Purpose

- Track experiments
- Store models
- Model Registry
- Model Deployment

---

# Unity Catalog

Centralized governance.

Provides

- Permissions
- Data Lineage
- Security
- Auditing

---

# Security

Best Practices

- IAM Roles
- Unity Catalog
- Secret Scopes
- Encryption
- Access Control

---

# Performance Optimization

Use

- Delta Tables
- Partitioning
- Caching
- Auto Scaling
- Broadcast Joins
- Z-Ordering
- Photon Engine

Avoid

- collect()
- Large shuffles
- Small files
- Unnecessary caching

---

# Broadcast Join

Useful when one table is small.

```python
from pyspark.sql.functions import broadcast

large.join(
    broadcast(small)
)
```

---

# Partitioning

Improves query performance.

```python
df.write.partitionBy(
    "year"
)
```

---

# Caching

```python
df.cache()
```

Remove cache

```python
df.unpersist()
```

---

# Delta Time Travel

Query previous versions.

```sql
SELECT *
FROM employees
VERSION AS OF 3;
```

---

# Common Databricks Services

- Workspace
- Jobs
- Clusters
- SQL Warehouse
- Delta Lake
- Unity Catalog
- MLflow
- Repos
- Dashboards

---

# Databricks vs Spark

| Apache Spark | Databricks |
|---------------|------------|
| Processing Engine | Complete Platform |
| Open Source | Managed Cloud Service |
| Manual Setup | Managed Infrastructure |
| Basic Spark | Optimized Runtime |
| No Workspace | Collaborative Workspace |

---

# Databricks vs Snowflake

| Databricks | Snowflake |
|-------------|------------|
| ETL + ML + Analytics | Data Warehouse |
| Spark Based | SQL Based |
| Supports Python | Mostly SQL |
| Machine Learning | Limited ML |
| Data Engineering | Analytics Focus |

---

# Common Interview Questions

## What is Databricks?

A cloud-native data platform built on Apache Spark for ETL, analytics, data engineering, and machine learning.

---

## Why use Databricks?

- Massive scalability
- Distributed processing
- Auto scaling
- Collaborative notebooks
- Unified analytics
- Delta Lake support

---

## What is Delta Lake?

A storage layer that adds ACID transactions, schema enforcement, time travel, and version history to data lakes.

---

## Difference between Spark and Databricks?

Spark is the processing engine.

Databricks is the managed cloud platform built around Spark.

---

## What is Lazy Evaluation?

Spark delays execution until an action is called, allowing it to optimize the execution plan.

---

## Difference between Transformation and Action?

Transformations

- filter()
- join()
- select()

Actions

- show()
- count()
- collect()

---

## Why use Parquet or Delta instead of CSV?

- Smaller files
- Faster reads
- Columnar storage
- Compression
- Better analytics performance

---

## What is Photon?

Photon is Databricks' high-performance query engine that accelerates SQL and Spark workloads without requiring code changes.

---

## What is Unity Catalog?

A centralized governance solution that manages permissions, auditing, lineage, and access control across Databricks workspaces.

---

# Typical Production Workflow

```
REST API
CSV
Database
JSON
Kafka

        │

        ▼

Spark Read

        │

        ▼

Validation

        │

        ▼

Transform

        │

        ▼

Business Rules

        │

        ▼

Delta Lake

        │

        ▼

Machine Learning

        │

        ▼

Dashboards

        │

        ▼

Business Users
```

---

# Senior Interview Tips

- Know the relationship between **Databricks**, **Apache Spark**, and **Delta Lake**.
- Understand the difference between **Spark Transformations** and **Actions**.
- Explain **Lazy Evaluation** confidently.
- Be familiar with **Delta Lake** features (ACID, Time Travel, Schema Enforcement).
- Know when to use **Broadcast Joins**, **Partitioning**, and **Caching**.
- Understand **Unity Catalog** for governance and **MLflow** for machine learning lifecycle management.
- Be prepared to discuss how Databricks fits into modern cloud ETL pipelines on **AWS**, **Azure**, or **Google Cloud**.