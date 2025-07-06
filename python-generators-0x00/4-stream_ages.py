#!/usr/bin/python3
import mysql.connector
from seed import connect_to_prodev

def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield age
    cursor.close()
    connection.close()


def average_age():
    """
    Computes the average age using the stream_user_ages generator.
    Does not load the entire dataset into memory.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        avg = total_age / count
        print(f"Average age of users: {avg:.2f}")
