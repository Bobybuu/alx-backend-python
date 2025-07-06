import seed

def paginate_users(page_size, offset):
    """Fetch a single page of users based on offset and page size"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """Generator that lazily yields pages of users from the database"""
    offset = 0
    while True:  # Only one loop allowed
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
