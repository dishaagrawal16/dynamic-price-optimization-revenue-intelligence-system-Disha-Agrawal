from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import certifi
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# TiDB Cloud only accepts encrypted (TLS) connections.
# SSL turns on automatically for TiDB Cloud hosts; override with DB_SSL=true/false.
DB_SSL = os.getenv(
    "DB_SSL",
    "true" if "tidbcloud.com" in DB_HOST else "false"
).lower() == "true"

# URL.create safely handles special characters (@, #, %) in the password
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

connect_args = {}
if DB_SSL:
    connect_args = {
        "ssl_ca": certifi.where(),
        "ssl_verify_cert": True,
        "ssl_verify_identity": True,
    }

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,   # reconnect if TiDB closed an idle connection
    pool_recycle=300,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
