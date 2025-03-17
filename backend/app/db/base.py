from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, event
from app.core.config import settings
from app.db.base_class import Base
from app.models.user import User
from app.models.message import Message, Conversation
from app.models.notification import Notification

# Create MySQL engine with specific configuration
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_size=5,  # Maximum number of permanent connections
    max_overflow=10,  # Maximum number of connections that can be created beyond pool_size
    echo=False,  # Set to True to log all SQL queries
)

# Configure MySQL session settings
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Configure MySQL connection for proper UTF-8 handling
@event.listens_for(engine, 'connect')
def set_mysql_charset(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute('SET NAMES utf8mb4')
    cursor.execute('SET CHARACTER SET utf8mb4')
    cursor.execute('SET character_set_connection=utf8mb4')
    cursor.close()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Import all models here that are needed by Alembic
__all__ = ["User", "Message", "Conversation", "Notification"] 