import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime

host = "localhost"
port=5432
user = "admin"
password = "admin123"
database_name = "library"

conn = psycopg2.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database="postgres"
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{database_name}'")
exists = cur.fetchone()
if not exists:
    cur.execute(f"CREATE DATABASE {database_name} ENCODING 'UTF8'")
    print(f"База даних '{database_name}' створена.")
else:
    print(f"База даних '{database_name}' вже існує.")

cur.close()
conn.close()

conn = psycopg2.connect(
    host=host,
    port=port,
    database=database_name,
    user=user,
    password=password
)
cur = conn.cursor()

# Таблиця Books
cur.execute("""
CREATE TABLE IF NOT EXISTS Books (
    book_id SERIAL PRIMARY KEY,
    author VARCHAR(100),
    title VARCHAR(150),
    section VARCHAR(50),
    year INTEGER,
    pages INTEGER,
    price NUMERIC(8,2),
    type VARCHAR(50),
    copies INTEGER,
    max_days INTEGER
)
""")

# Таблиця Readers
cur.execute("""
CREATE TABLE IF NOT EXISTS Readers (
    ticket_number SERIAL PRIMARY KEY,
    last_name VARCHAR(50),
    first_name VARCHAR(50),
    phone VARCHAR(15),
    address VARCHAR(100),
    course INTEGER CHECK(course BETWEEN 1 AND 4),
    group_name VARCHAR(20)
)
""")

# Таблиця Issues
cur.execute("""
CREATE TABLE IF NOT EXISTS Issues (
    issue_id SERIAL PRIMARY KEY,
    issue_date DATE,
    ticket_number INTEGER REFERENCES Readers(ticket_number) ON DELETE CASCADE,
    book_id INTEGER REFERENCES Books(book_id) ON DELETE CASCADE
)
""")

conn.commit()
cur.close()
conn.close()