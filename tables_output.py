import pandas as pd
from sqlalchemy import create_engine
from tabulate import tabulate

engine = create_engine("postgresql+psycopg2://library_user:library_pass@db/library_db")

def print_table(title, query):
    print("\n"+title)

    df = pd.read_sql_query(query, engine)

    if df.empty:
        print("Таблиця порожня.")
    else:
        print(tabulate(df, headers='keys', tablefmt='psql'))

queries = [
    ("Всі книги", 
     "SELECT * FROM Books"),

    ("Всі читачі", 
     "SELECT * FROM Readers"),

    ("Всі видачі книг", 
     "SELECT * FROM Issues"),

    ("Всі книги, видані після 2001 року (сортування за назвою)", 
     "SELECT * FROM Books WHERE year > 2001 ORDER BY title"),

    ("Кількість книг кожного виду", 
     "SELECT type, COUNT(*) FROM Books GROUP BY type"),

    ("Всі читачі, які брали посібники (сортування за прізвищем)",
     """SELECT DISTINCT r.* 
        FROM Readers r
        JOIN Issues i ON r.ticket_number = i.ticket_number
        JOIN Books b ON i.book_id = b.book_id
        WHERE b.type='посібник'
        ORDER BY r.last_name"""),

    ("Всі книги за розділом 'технічна'", 
     "SELECT * FROM Books WHERE section = 'технічна'"),

    ("Кінцева дата повернення для кожної виданої книги",
     """SELECT b.title, r.last_name, r.first_name, 
               i.issue_date + b.max_days AS due_date
        FROM Issues i
        JOIN Books b ON i.book_id = b.book_id
        JOIN Readers r ON i.ticket_number = r.ticket_number"""),

    ("Кількість посібників, книг і періодичних видань у кожному розділі",
     """SELECT section,
               SUM(CASE WHEN type='посібник' THEN 1 ELSE 0 END) AS manuals,
               SUM(CASE WHEN type='книга' THEN 1 ELSE 0 END) AS books,
               SUM(CASE WHEN type='періодичне видання' THEN 1 ELSE 0 END) AS periodicals
        FROM Books
        GROUP BY section""")
]

for title, query in queries:
    print_table(title, query)
