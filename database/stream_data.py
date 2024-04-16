import psycopg2
import logging
import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.create_table import create_table
import database.constants_db as cst
from database.videos import video


def create_postgres_connection():
    try:
        conn = psycopg2.connect(
            host=cst.host,
            port=cst.port,
            database=cst.dbname,
            user=cst.user,
            password=cst.password
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
            SELECT * FROM HealthEdBot;
        """
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                print(row)
            print("read successful")
        except Exception as e:
            connection.rollback()
            print("read failed: %s", e)


def query_videodata():
    return video()

def insert_video_data(connection, video_response):
    with connection.cursor() as cursor:
        try:
            for video in video_response.get('items', []):
                video_details = {
                    'title': video['snippet']['title'],
                    'description': video['snippet']['description'],
                    'thumbnail_url': video['snippet']['thumbnails']['high']['url'],
                    'video_url': f"https://www.youtube.com/watch?v={video['id']}",
                    'view_count': int(video['statistics']['viewCount']),
                }
                # print(json.dumps(video_details, indent=4, ensure_ascii=False))

                cursor.execute("""
                INSERT INTO HealthEdBot (title, description, thumbnail_url, video_url, view_count)
                VALUES (%s, %s, %s, %s, %s);
                """, (video_details['title'], video_details['description'], 
                video_details['thumbnail_url'], video_details['video_url'], video_details['view_count']))
            connection.commit()
        except Exception as e:
            connection.rollback()
            print("insert failed: %s", e)



def stream_to_postgres():
    "Write the API data into PostgreSQL database"
    connection = create_postgres_connection()
    if connection:
        print("database connect successful")
        logging.info("Creating table ...")
        create_table(connection)
        print("table create successful")
        logging.info("Table creation has finished.")
        video_response = query_videodata()
        logging.info("Processing the data ...")
        insert_video_data(connection, video_response)
        # insert_into_postgres(connection)
        read_from_postgres(connection)
        logging.info("Inserting the data in the postgres database ...")
        logging.info("Check the number of rows in the HealthEdBot table ...")
        # n_rows = count_rows(
        #     host=cst.host,
        #     port=cst.port,
        #     database=cst.dbname,
        #     user=cst.user,
        #     password=cst.password
        # )
        # logging.info("The number of rows in the HealthEdBot table is %s", n_rows)
        connection.close()



if __name__ == "__main__":
    stream_to_postgres()