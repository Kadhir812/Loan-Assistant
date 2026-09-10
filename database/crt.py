import sqlite3
from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "database"
DB_PATH = DATABASE_DIR / "personal_loan.db"

SCHEMA_PATH = DATABASE_DIR / "schema.sql"
SEED_PATH = DATABASE_DIR / "seed.sql"


def execute_sql_file(connection, file_path):
    """Execute all SQL statements from a SQL file."""

    with open(file_path, "r", encoding="utf-8") as file:
        sql = file.read()

    connection.executescript(sql)


def setup_database():
    """Create database, tables, and seed data."""

    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    connection = None

    try:
        print("Connecting to SQLite database...")

        connection = sqlite3.connect(DB_PATH)

        print("Executing schema.sql...")
        execute_sql_file(connection, SCHEMA_PATH)

        print("Executing seed.sql...")
        execute_sql_file(connection, SEED_PATH)

        connection.commit()

        print()
        print("Database setup completed successfully.")
        print(f"Database: {DB_PATH}")

        # Verify inserted records
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                application_id,
                customer_id,
                name,
                loan_type,
                requested_loan_amount
            FROM customer_loan_profile
            ORDER BY application_id
        """)

        rows = cursor.fetchall()

        print()
        print("Inserted records:")
        print("-" * 70)

        for row in rows:
            print(row)

        print("-" * 70)
        print(f"Total applications: {len(rows)}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise

    except FileNotFoundError as e:
        print(f"SQL file not found: {e}")
        raise

    finally:
        if connection:
            connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    setup_database()