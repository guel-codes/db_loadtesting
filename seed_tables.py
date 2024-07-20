import psycopg2
from faker import Faker
import uuid
import random

# Connect to the PostgreSQL database
USERNAME = "postgres"
PASSWORD = "postgres"
ADDRESS = "localhost"
PORT = "5432"
DBNAME = "loadtesting_db"

# Create a cursor object to interact with the database
conn = psycopg2.connect(
    database=DBNAME, user=USERNAME, password=PASSWORD, host=ADDRESS, port=PORT
)

cursor = conn.cursor()

fake = Faker()

num_records = 100

for _ in range(num_records):
    # user table
    user_uuid = str(uuid.uuid4())
    name = fake.name()
    email = fake.email()

    # invoice_table
    invoice_id = str(uuid.uuid4())
    user_id = user_uuid
    amount = random.randint(1, 1000)
    invoice_date = fake.date_time_this_year()

    # Construct the SQL query
    query1 = f"INSERT INTO loadtesting.user (id, name, email) VALUES ('{user_uuid}', '{name}', '{email}')"
    query2 = f"INSERT INTO loadtesting.invoice (id, user_id, amount, invoice_date) VALUES ('{invoice_id}', '{user_id}', {amount}, '{invoice_date}')"

    # Execute the queries
    cursor.execute(query1)
    cursor.execute(query2)

conn.commit()

cursor.close()
conn.close()
