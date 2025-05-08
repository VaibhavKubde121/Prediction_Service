from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Database Configuration
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DATABASE = "fake_profiles"
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "123"

DATABASE_URL = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Create Engine & Session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Function to test database connection
def test_connection():
    try:
        with engine.connect() as connection:
            print("✅ Database connected successfully!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
