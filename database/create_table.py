from typing import Any
import logging

# from .constants_db import DB_FIELDS

logger = logging.getLogger(__name__)


def try_execute_sql(connection: Any, sql: str):
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            connection.commit()
            logger.info("Executed table creation successfully")
            print("create table success")
        except Exception as e:
            logger.info("Couldn't execute table creation due to exception: %s", e)
            connection.rollback()
            print("create table failed: %s", e)


def create_table(connection):
    create_table_sql = """
        DROP TABLE IF EXISTS employee;
        Create TABLE employee (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            salary DECIMAL(15, 2),
            join_date DATE NOT NULL
        );
    """
    try_execute_sql(connection, create_table_sql)
