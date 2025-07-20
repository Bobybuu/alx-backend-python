import sqlite3
import functools

# ─────────────────────────────────────────────
# Decorator to handle DB connection
def with_db_connection(func):
    """Opens and closes a SQLite database connection for the wrapped function"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

# ─────────────────────────────────────────────
# Decorator to handle transactions
def transactional(func):
    """Wraps a DB operation in a transaction (commit or rollback)"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("Transaction committed.")
            return result
        except Exception as e:
            conn.rollback()
            print("Transaction rolled back due to error:", e)
            raise
    return wrapper

# ─────────────────────────────────────────────
# Update user email with transaction safety
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print(f"Email updated for user_id {user_id}")

# ─────────────────────────────────────────────
# Run the update
if __name__ == "__main__":
    update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
