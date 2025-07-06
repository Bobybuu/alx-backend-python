# 📦 Python Generators: Advanced Data Streaming and Processing

This project focuses on advanced usage of Python **generators** to handle large datasets efficiently, integrate with SQL databases, and simulate real-world scenarios such as streaming, batching, lazy pagination, and memory-efficient aggregation.

---

## 🧠 Learning Objectives

By completing this project, you will:

- ✅ Master **Python generators** and the `yield` keyword for efficient data iteration.
- ✅ Handle **large datasets** using batch processing and lazy loading.
- ✅ Simulate **live data streams** with generator-based pagination.
- ✅ Compute **aggregates like averages** without loading the entire dataset into memory.
- ✅ Combine **Python with MySQL**, using SQL queries to dynamically fetch and process data.

---

## ⚙️ Requirements

- Python 3.x
- MySQL server (or compatible database)
- `mysql-connector-python` package
- Basic understanding of SQL, database schema design, and seeding
- Git & GitHub for version control

---

## 📁 Project Structure

```

python-generators-0x00/
├── seed.py                  # Sets up DB, tables, and inserts data
├── 0-main.py                # Tests DB setup and initial data
├── 0-stream\_users.py        # Generator to stream rows one by one
├── 1-main.py
├── 1-batch\_processing.py    # Generator for batch processing and filtering
├── 2-main.py
├── 2-lazy\_paginate.py       # Generator for lazy pagination
├── 3-main.py
├── 4-stream\_ages.py         # Generator-based average age calculation
├── user\_data.csv            # CSV with sample user data
└── README.md

```

---

## ✅ Tasks Summary

### 0. Getting Started with Python Generators

- Set up `ALX_prodev` MySQL database and `user_data` table.
- Populate table using CSV data.
- **File:** `seed.py`

---

### 1. Stream Users One-by-One

- Generator `stream_users()` yields each user as a dictionary.
- Uses **one loop only**.
- **File:** `0-stream_users.py`

---

### 2. Batch Processing Large Data

- `stream_users_in_batches(batch_size)` yields batches of users.
- `batch_processing(batch_size)` filters users aged > 25.
- Uses **no more than 3 loops**.
- **File:** `1-batch_processing.py`

---

### 3. Lazy Loading Paginated Data

- Implements `lazy_pagination(page_size)` to simulate infinite scrolling.
- Fetches only the needed page using offset + limit.
- Uses **one loop and yield**.
- **File:** `2-lazy_paginate.py`

---

### 4. Memory-Efficient Aggregation

- `stream_user_ages()` yields user ages one at a time.
- Computes average age without SQL `AVG()` or loading full dataset.
- Uses only **two loops**.
- **File:** `4-stream_ages.py`

---

## 🧪 Sample Output

```

{'user\_id': '...', 'name': '...', 'email': '...', 'age': 67}
...
Average age of users: 58.34

````

---

## 🛠️ Setup & Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/alx-backend-python.git
   cd python-generators-0x00
````

2. Install MySQL and required Python package:

   ```bash
   pip install mysql-connector-python
   ```

3. Edit `seed.py` to use your MySQL credentials.

4. Run:

   ```bash
   ./0-main.py    # Set up and seed the database
   ./1-main.py    # Stream users
   ./2-main.py    # Process in batches
   ./3-main.py    # Paginate lazily
   python3 4-stream_ages.py   # Compute average
   ```

---

## 🤝 Author

* **Faith Okoth**
* ALX Software Engineering Backend Track
* GitHub: [@FaithOkoth](https://github.com/FaithOkoth)

---