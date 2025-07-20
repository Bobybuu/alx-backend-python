import sqlite3
import functools
import logging
from datetime import datetime

# set up a basic logger (writes to console)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# decorator that logs SQL queries 
def log_queries(func):
    """
    Decorator that logs the SQL query (via the `query` argument or the
    first positional arg) before the wrapped function runs.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Try to get the SQL query from either kwargs or args[0]
        sql = kwargs.get("query") if "query" in kwargs else args[0] if args else "UNKNOWN"
        logging.info(f"Executing SQL → {sql}")
        return func(*args, **kwargs)
    return wrapper

# sample function using the decorator
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# fetch users while logging the query
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
