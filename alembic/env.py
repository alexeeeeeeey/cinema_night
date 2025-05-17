import asyncio
import os
import sys
from logging.config import fileConfig

from alembic import context

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import database
from core.config import settings

config = context.config
fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = database.Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_server_default=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    async with database.engine.connect() as connection:

        def do_migrations(sync_conn):
            context.configure(
                connection=sync_conn,
                target_metadata=target_metadata,
                compare_type=True,
            )
            with context.begin_transaction():
                context.run_migrations()

        await connection.run_sync(do_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
