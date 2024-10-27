import os

from logging.config import fileConfig

from sqlmodel import SQLModel
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from app.models import load_all_models

from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

load_all_models()

target_metadata = SQLModel.metadata


def get_url():
    user = "admin"
    password = "admin"
    server = "0.0.0.0"
    port = "5432"
    db = "postgres"
    return f"postgresql+psycopg://{user}:{password}@{server}:{port}/{db}"


def run_migrations_offline():
    url = get_url()

    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
