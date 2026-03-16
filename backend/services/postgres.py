import psycopg2

db_host = 'database-1.c1seomkuoece.us-east-2.rds.amazonaws.com'
db_name = 'test_name'
db_user = 'postgres'
db_pass = 'F3IHPw8H0OOKe7r3Pz39'

connect = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_pass)
print("Connected to the database")

cursor = connect.cursor()
cursor.execute("SELECT version()")
db_version = cursor.fetchone()
print(db_version)

cursor.close()