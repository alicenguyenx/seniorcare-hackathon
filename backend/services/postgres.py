import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_host = os.environ["DB_HOST"]
db_name = os.environ["DB_NAME"]
db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASSWORD"]

connect = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_pass)
print("Connected to the database")

cursor = connect.cursor()
cursor.execute("SELECT version()")
db_version = cursor.fetchone()
print(db_version)

cursor.close()
