# Database Operations with Context Managers and Async/Await

## Overview
This project demonstrates advanced Python techniques for managing database connections and executing queries using context managers and asynchronous programming. It provides three key implementations: a custom context manager for database connections, a reusable query executor, and concurrent asynchronous database operations.

## Learning Objectives
- Implement class-based context managers using `__enter__` and `__exit__` methods
- Understand resource management and automatic cleanup with context managers
- Master asynchronous database operations using `aiosqlite`
- Implement concurrent query execution with `asyncio.gather`
- Handle database connections and queries in a Pythonic way

## Key Concepts
- **Context Managers**: Ensure proper resource acquisition and release using the `with` statement pattern
- **Database Connection Management**: Prevent resource leaks and ensure database integrity
- **Asynchronous Programming**: Enable non-blocking database operations using `async/await` syntax
- **Concurrent Execution**: Allow multiple asynchronous operations to run simultaneously with `asyncio.gather()`

## Tools and Libraries
- `sqlite3`: Standard Python library for SQLite database interactions
- `aiosqlite`: Async-compatible SQLite library for asynchronous operations
- `asyncio`: Python's built-in asynchronous programming framework
- `contextlib`: Utilities for creating context managers

## Project Structure

### Task 0: Custom Class-Based Context Manager for Database Connection
**File**: `0-databaseconnection.py`

Implement a class-based context manager `DatabaseConnection` that:
- Uses `__enter__` and `__exit__` methods
- Automatically handles database connection opening and closing
- Executes the query `SELECT * FROM users` and prints the results

### Task 1: Reusable Query Context Manager
**File**: `1-execute.py`

Implement a class-based custom context manager `ExecuteQuery` that:
- Takes a query and parameters as input
- Executes the query `SELECT * FROM users WHERE age > ?` with parameter `25`
- Returns the result of the query
- Ensures proper resource cleanup using `__enter__()` and `__exit__()` methods

### Task 2: Concurrent Asynchronous Database Queries
**File**: `3-concurrent.py`

Implement asynchronous database operations using `aiosqlite`:
- Write two async functions: `async_fetch_users()` and `async_fetch_older_users()`
- Use `asyncio.gather()` to execute both queries concurrently
- Use `asyncio.run(fetch_concurrently())` to run the concurrent fetch

## Real-World Use Cases
- **Web Application Backends**: Prevent connection leaks in high-traffic applications
- **Data Processing Pipelines**: Simplify ETL processes with reusable query context managers
- **Analytics Dashboards**: Fetch multiple datasets simultaneously for faster load times
- **Microservices Architecture**: Handle multiple concurrent requests efficiently
- **Automated Testing**: Ensure proper database cleanup after test cases

## Setup and Execution
1. Ensure you have Python 3.7+ installed
2. Install required dependencies: `pip install aiosqlite`
3. Run each script individually:
   ```bash
   python 0-databaseconnection.py
   python 1-execute.py
   python 3-concurrent.py
   ```
