import time
import sqlite3
import functools

# Decorator to handle DB connection
def with_db_connection(func):
    """Opens and closes a SQLite database connection for the wrapped function"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Decorator to retry on transient failures
def retry_on_failure(retries=3, delay=2):
    """Retries a function if it raises an exception, with delay between retries"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        time.sleep(delay)
                    else:
                        print("All retry attempts failed.")
                        raise
        return wrapper
    return decorator

# Function to fetch users with retry logic
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Run the function
if __name__ == "__main__":
    users = fetch_users_with_retry()
    print(users)
