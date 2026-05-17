import pymysql
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", 4779)),
    "user": os.getenv("DB_USER", "epc_developer"),
    "password": os.getenv("DB_PASS", "rrWSn28n"),
    "database": os.getenv("DB_NAME", "epc_orch"),
}

def test_direct_pymysql():
    print("--- Testing Direct PyMySQL ---")
    try:
        connection = pymysql.connect(**DB_CONFIG)
        if connection.open:
            print("✅ Direct PyMySQL Connection SUCCESSFUL")
            with connection.cursor() as cursor:
                cursor.execute("SELECT DATABASE();")
                print("Connected to DB:", cursor.fetchone())
        connection.close()
        return True
    except Exception as e:
        print(f"❌ Direct PyMySQL Connection FAILED: {e}")
        return False

def test_sqlalchemy():
    print("\n--- Testing SQLAlchemy ---")
    # Using the exact same string construction as in db.py
    url = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    print(f"URL: {url}")
    try:
        engine = create_engine(url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT DATABASE();"))
            print(f"✅ SQLAlchemy Connection SUCCESSFUL: {result.fetchone()}")
        return True
    except Exception as e:
        print(f"❌ SQLAlchemy Connection FAILED: {e}")
        return False

if __name__ == "__main__":
    if test_direct_pymysql():
        test_sqlalchemy()
