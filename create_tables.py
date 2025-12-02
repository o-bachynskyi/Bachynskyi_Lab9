import psycopg2

conn = psycopg2.connect(
    host="db",
    database="library_db",
    user="library_user",
    password="library_pass"
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

print("Таблиці успішно створено")