import psycopg2
from psycopg2 import sql
import sys

def load_seed_file(db_config, seed_file_path):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_config)
        conn.autocommit = False  # Use transaction
        cursor = conn.cursor()

        # Read seed.sql file
        with open(seed_file_path, 'r', encoding='utf-8') as file:
            seed_sql = file.read()

        # Execute SQL
        cursor.execute(seed_sql)

        # Commit transaction
        conn.commit()
        print("✅ Seed file loaded successfully.")

    except Exception as e:
        conn.rollback()
        print("❌ Error loading seed file:", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "port": 5432,
        "dbname": "your_database_name",
        "user": "your_username",
        "password": "your_password"
    }

    seed_file_path = "seed.sql"

    load_seed_file(db_config, seed_file_path)
