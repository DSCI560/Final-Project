import psycopg2
import logging
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.create_table import create_table


def create_postgres_connection():
    try:
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='HealthEdBot',
            user='postgres',
            password='123456'
        )
        return conn
    except psycopg2.OperationalError as e:
        logging.error("Database connection failed: %s", e)
        return None


def insert_into_postgres(connection):
    with connection.cursor() as cursor:
        sql = """
            INSERT INTO employee (name, email, salary, join_date)
            VALUES ('John Doe', 'john.doe@gmail.com', 55000, '2023-04-01');
        """
        try:
            cursor.execute(sql)
            connection.commit()
            print("insert successful")
        except Exception as e:
            connection.rollback()
            print("insert failed: %s", e)


def read_from_postgres(connection):
    with connection.cursor() as cursor:
        sql = """
            SELECT * FROM employee;
        """
        try:
            cursor.execute(sql)
            connection.commit()
            print("read successful")
        except Exception as e:
            connection.rollback()
            print("read failed: %s", e)


def stream_to_postgres():
    connection = create_postgres_connection()
    if connection:
        print("database connect successful")
        logging.info("Creating table ...")
        create_table(connection)
        print("table create successful")
        logging.info("Table creation has finished.")
        insert_into_postgres(connection)
        read_from_postgres(connection)



if __name__ == "__main__":
    stream_to_postgres()