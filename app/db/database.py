from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import SQLALCHEMY_DATABASE_ABS_URL

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_ABS_URL)

# Create a local session factory bound to the engine
SessionLocal = sessionmaker(bind=engine)


def get_db():
    """
    Generator function to get a database session.

    This function establishes a new session that can be used by the caller. Once the caller is
    done with the session, the session is closed to free up resources.

    Yields:
        db: The session object for database operations.

    Example:
        with get_db() as db:
            # use the db for operations
    """
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Yield the session for use by the caller
    finally:
        db.close()  # Ensure the session is closed after use
