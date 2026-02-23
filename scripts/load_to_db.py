import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT')
)

cur = conn.cursor()

# Load schema
with open("sql/schema.sql", "r") as f:
    sql_script = f.read()

cur.execute(sql_script)
conn.commit()
print("Schema created successfully!")

# Load seed data
seed_files = [
    "quickcart_data/seed_orders.sql",
    "quickcart_data/seed_payments.sql",
    "quickcart_data/seed_bank_settlements.sql"
]

for seed_file in seed_files:
    try:
        with open(seed_file, "r") as f:
            sql_script = f.read()
        
        cur.execute(sql_script)
        conn.commit()
        print(f"Loaded {seed_file}")
    
    except Exception as e:
        conn.rollback()
        print(f"Error loading {seed_file}: {e}")

cur.close()
conn.close()

print("All data loaded successfully!")
