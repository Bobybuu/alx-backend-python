import asyncio
import aiosqlite

async def async_fetch_users():
    """Fetch all users from the database asynchronously."""
    async with aiosqlite.connect('example.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("All users fetched:")
            for row in results:
                print(row)
            return results

async def async_fetch_older_users():
    """Fetch users older than 40 from the database asynchronously."""
    async with aiosqlite.connect('example.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            print("\nUsers older than 40 fetched:")
            for row in results:
                print(row)
            return results

async def fetch_concurrently():
    """Execute both queries concurrently using asyncio.gather()."""
    # Run both functions concurrently and wait for both to complete
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

# Run the concurrent fetch
if __name__ == "__main__":
    # Execute the concurrent operations
    all_results = asyncio.run(fetch_concurrently())
    
    # Results are returned as a list with two elements:
    # all_results[0] contains results from async_fetch_users()
    # all_results[1] contains results from async_fetch_older_users()
    print(f"\nConcurrent execution completed!")
    print(f"Total users: {len(all_results[0])}")
    print(f"Users older than 40: {len(all_results[1])}")
