import sys
import os
import psycopg2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.constants import DB_FIELDS

# Database connection parameters
dbname = "postgres"
user = "xaviervanausloos"
# password = os.getenv("POSTGRES_PASSWORD")
host = "localhost"

# Connect to the database
conn = psycopg2.connect(dbname=dbname, user=user, host=host)
cur = conn.cursor()


def try_execute_sql(sql: str):
    try:
        cur.execute(sql)
        conn.commit()
        print("Executed table creation successfully")
    except Exception as e:
        print(f"Couldn't execute table creation due to exception: {e}")
        conn.rollback()


def create_table():
    """
    Creates the rappel_conso table and its columns.
    """
    create_table_sql = f"""
    CREATE TABLE rappel_conso_table (
        {DB_FIELDS[0]} text PRIMARY KEY,
    """
    for field in DB_FIELDS[1:-1]:
        column_sql = f"{field} text, \n"
        create_table_sql += column_sql

    create_table_sql += f"{DB_FIELDS[-1]} text \n" + ");"
    try_execute_sql(create_table_sql)

    cur.close()
    conn.close()


if __name__ == "__main__":
    create_table()
