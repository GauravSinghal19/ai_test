import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection parameters
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Construct the database URL for pymysql
# Format: mysql+pymysql://user:password@host:port/dbname
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the sync engine
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
)

# Create a session factory
SessionLocal = sessionmaker(
    bind=engine, expire_on_commit=False
)

def get_db_session():
    """
    Returns a database session factory.
    The caller should use 'with get_db_session() as session:'.
    """
    print(f"DEBUG DB: Attempting to create sync session for {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    return SessionLocal()
