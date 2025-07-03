import asyncpg
import logging

logger = logging.getLogger("db")


class Database:
    def __init__(self, dsn):
        self.dsn = dsn
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(dsn=self.dsn)
        logger.info("Database connected")

    async def close(self):
        await self.pool.close()
        logger.info("Database connection closed")

    async def create_tables(self):
        query = """
            CREATE TABLE IF NOT EXISTS users (
            id BIGINT PRIMARY KEY,
            type VARCHAR(50),
            name VARCHAR(100),
            avatar_path VARCHAR(255),
            gender VARCHAR(20),
            state VARCHAR(50),

            -- Новые поля
            stamina INT DEFAULT 0,              -- выносливость
            agility INT DEFAULT 0,              -- ловкость
            intelligence INT DEFAULT 0,         -- интеллект

            cash_balance BIGINT DEFAULT 0,      -- наличные деньги
            bank_balance BIGINT DEFAULT 0,      -- деньги в банке
            expected_income BIGINT DEFAULT 0,   -- ожидаемый доход

            current_actions TEXT,               -- действия на этом ходу

            has_premium BOOLEAN DEFAULT FALSE,  -- наличие премиума
            renacoin_balance BIGINT DEFAULT 0,  -- баланс ренакоинов
            personal_security TEXT              -- личная охрана (можно JSON, если составная)
        );
            """
        async with self.pool.acquire() as conn:
            await conn.execute(query)
            logger.info("Table 'users' ensured")

    async def get_state(self, user_id: int) -> str | None:
        query = "SELECT state FROM users WHERE id = $1"
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow(query, user_id)
            if result:
                logger.debug(f"Loaded state for user {user_id}: {result['state']}")
                return result["state"]
            logger.debug(f"No state found for user {user_id}")
            return None

    async def save_state(self, user_id: int, state: str):
        query = """
        INSERT INTO users (id, state)
        VALUES ($1, $2)
        ON CONFLICT (id) DO UPDATE SET state = EXCLUDED.state;
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, user_id, state)
            logger.debug(f"Saved state for user {user_id}: {state}")

    async def set_arg(self, user_id: int, arg: str, value):
        # Проверяем, что имя поля безопасное (например, только буквы и цифры)
        if not arg.isidentifier():
            raise ValueError("Invalid field name")

        query = f"""
        INSERT INTO users (id, {arg})
        VALUES ($1, $2)
        ON CONFLICT (id) DO UPDATE SET {arg} = EXCLUDED.{arg};
        """

        async with self.pool.acquire() as conn:
            await conn.execute(query, user_id, value)
            logger.debug(f"Saved {arg} for user {user_id}: {value}")

    async def get_user_data(self, user_id: int):
        query = "SELECT * FROM users WHERE id = $1;"
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, user_id)
            if row:
                return dict(row)
            return None
