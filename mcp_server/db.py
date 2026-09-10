import sqlite3
from pathlib import Path

from mcp_server.errors import (
    DatabaseConnectionError,
    DatabaseTimeoutError,
)


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# SQLite database location
DB_PATH = BASE_DIR / "database" / "personal_loan.db"

# Database timeout in seconds
DB_TIMEOUT = 5


def get_connection():
    """
    Create and return a SQLite database connection.
    """

    try:
        connection = sqlite3.connect(
            DB_PATH,
            timeout=DB_TIMEOUT
        )

        # Allows row["column_name"] access
        connection.row_factory = sqlite3.Row

        # Enable foreign key constraints
        connection.execute("PRAGMA foreign_keys = ON")

        return connection

    except sqlite3.OperationalError as e:

        if "locked" in str(e).lower():
            raise DatabaseTimeoutError(
                "Database is locked or unavailable."
            ) from e

        raise DatabaseConnectionError(
            f"Unable to connect to database: {e}"
        ) from e

    except sqlite3.Error as e:

        raise DatabaseConnectionError(
            f"Database connection failed: {e}"
        ) from e


def execute_query(query: str, params: tuple = ()):
    """
    Execute INSERT, UPDATE, or DELETE queries.

    SQL must be supplied by application code.
    Parameters are passed separately to prevent SQL injection.

    Returns:
        Number of affected rows.
    """

    connection = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(query, params)

        connection.commit()

        return cursor.rowcount

    except sqlite3.OperationalError as e:

        if "locked" in str(e).lower():
            raise DatabaseTimeoutError(
                "Database operation timed out because the database is locked."
            ) from e

        if connection:
            connection.rollback()

        raise DatabaseConnectionError(
            f"Database operation failed: {e}"
        ) from e

    except sqlite3.Error as e:

        if connection:
            connection.rollback()

        raise DatabaseConnectionError(
            f"Database query failed: {e}"
        ) from e

    finally:

        if connection:
            connection.close()


def fetch_one(query: str, params: tuple = ()):
    """
    Execute a SELECT query and return one row.
    """

    connection = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(query, params)

        return cursor.fetchone()

    except sqlite3.OperationalError as e:

        if "locked" in str(e).lower():
            raise DatabaseTimeoutError(
                "Database operation timed out because the database is locked."
            ) from e

        raise DatabaseConnectionError(
            f"Database fetch failed: {e}"
        ) from e

    except sqlite3.Error as e:

        raise DatabaseConnectionError(
            f"Database fetch failed: {e}"
        ) from e

    finally:

        if connection:
            connection.close()


def fetch_all(query: str, params: tuple = ()):
    """
    Execute a SELECT query and return all matching rows.
    """

    connection = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(query, params)

        return cursor.fetchall()

    except sqlite3.OperationalError as e:

        if "locked" in str(e).lower():
            raise DatabaseTimeoutError(
                "Database operation timed out because the database is locked."
            ) from e

        raise DatabaseConnectionError(
            f"Database fetch failed: {e}"
        ) from e

    except sqlite3.Error as e:

        raise DatabaseConnectionError(
            f"Database fetch failed: {e}"
        ) from e

    finally:

        if connection:
            connection.close()