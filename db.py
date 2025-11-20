import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please set it in your .env file or environment."
    )

logger = logging.getLogger(__name__)


def get_db_connection():
    """
    Establish a connection to the PostgreSQL database using the database URL.
    """
    try:
        connection = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return connection
    except psycopg2.Error as e:
        logger.error(f"Error connecting to the database: {e}")
        raise


def initialize_database():
    """
    Initialize the database by creating the scan_results table if it does not exist.
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS scan_results (
                    id SERIAL PRIMARY KEY,
                    file_name VARCHAR(255) NOT NULL,
                    result_type VARCHAR(50) NOT NULL,
                    result_value TEXT NOT NULL,
                    classification VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            logger.info("Database and table initialized successfully.")
        connection.commit()
    finally:
        connection.close()


def insert_scan_result(file_name, result_type, result_value, classification):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO scan_results (file_name, result_type, result_value, classification)
                VALUES (%s, %s, %s, %s)
                """,
                (file_name, result_type, result_value, classification),
            )
        connection.commit()
    finally:
        connection.close()



