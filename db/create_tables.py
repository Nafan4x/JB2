import asyncpg
import asyncio

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    type VARCHAR(50),
    name VARCHAR(100),
    avatar_path VARCHAR(255),
    gender VARCHAR(20),
    state VARCHAR(50)
);
"""


async def create_tables():
    conn = await asyncpg.connect(
        user="user", password="password", database="jb", host="localhost"
    )
    await conn.execute(CREATE_USERS_TABLE)
    await conn.close()


if __name__ == "__main__":
    asyncio.run(create_tables())
