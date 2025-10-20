"""
Database Base Configuration
SQLAlchemy setup and base class
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL - use SQLite for demo, PostgreSQL for production
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'sqlite:///./fineguard.db'  # Default to SQLite for demo
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if 'sqlite' in DATABASE_URL else {},
    echo=False  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class
Base = declarative_base()


def get_db():
    """
    Get database session
    
    Usage:
        db = next(get_db())
        try:
            # Use db
        finally:
            db.close()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully")


def drop_db():
    """Drop all tables - use with caution!"""
    Base.metadata.drop_all(bind=engine)
    print("⚠️  All tables dropped")

