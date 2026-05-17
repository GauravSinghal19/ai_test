import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", 4779)),
    "user": os.getenv("DB_USER", "epc_developer"),
    "password": os.getenv("DB_PASS", "rrWSn28n"),
    "database": "epc_translation",
}

def inspect_columns():
    try:
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            print("--- Columns in epc_translation.ep_messages ---")
            cursor.execute("DESCRIBE ep_messages")
            for column in cursor.fetchall():
                print(column)
            
            print("\n--- Columns in epc_orch.epc_create_auto_pdf ---")
            cursor.execute("DESCRIBE epc_orch.epc_create_auto_pdf")
            for column in cursor.fetchall():
                print(column)
        connection.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_columns()
