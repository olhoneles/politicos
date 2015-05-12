from __future__ import with_statement
import os

from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig


config = context.config
fileConfig(config.config_file_name)
target_metadata = None


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    alembic_config = config.get_section(config.config_ini_section)

    username = os.environ.get('MYSQL_USER', 'root')
    password = os.environ.get('MYSQL_PASSWORD', None)

    if password is not None:
        user_id = "%s:%s@" % (username, password)
    else:
        user_id = "%s@" % username

    database = alembic_config['sqlalchemy.url'].split('/')[-1]

    sqlalchemy_connection_string = "mysql+mysqldb://%s%s:%d/%s" % (
        user_id,
        os.environ.get('MYSQL_HOST', 'localhost'),
        int(os.environ.get('MYSQL_PORT', 3306)),
        os.environ.get('MYSQL_DATABASE_NAME', database),
    )

    alembic_config['sqlalchemy.url'] = sqlalchemy_connection_string

    engine = engine_from_config(
        alembic_config,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
