import seed

def stream_users_in_batches(batch_size):
    """Generator that yields users in batches of given size"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) FROM user_data")
    total_users = cursor.fetchone()['COUNT(*)']
    offset = 0

    while offset < total_users:
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
        batch = cursor.fetchall()
        if not batch:
            break
        yield batch
        offset += batch_size

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """Processes batches by filtering users over age 25"""
    for batch in stream_users_in_batches(batch_size):          # 1st loop
        for user in batch:                                     # 2nd loop
            if user['age'] > 25:                               # filtering logic
                print(user)
