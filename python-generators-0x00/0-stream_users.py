import mysql.connector
from mysql.connector import Error


def stream_users():
    """Generator to stream users one by one from user_data table"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Chrispine",
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)  # Return rows as dicts
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
