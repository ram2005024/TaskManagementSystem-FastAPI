from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

# Make a session
SessionHandler = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


# Function to start the session with the database
def get_db():
    db = SessionHandler()
    try:
        yield db
    finally:
        db.close()
