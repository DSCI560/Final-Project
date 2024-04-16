import os

dbname = user = "postgres"
password = "123456"
host = "localhost"
port = "5432"

COLUMNS = [
    "ID",
    "title",
    "description",
    "thumbnail_url",
    "video_url",
    "view_count",
]

DB_FIELDS = COLUMNS