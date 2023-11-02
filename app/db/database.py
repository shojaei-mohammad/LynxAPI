from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define the base directory by getting the absolute path of the directory containing this script
BASE_DIR: Path = Path(__file__).resolve().parent

# Define the SQLite database URL using the BASE_DIR
DATABASE_URL: str = f"sqlite:///{BASE_DIR}/rbac.db"

# Create the database engine
engine = create_engine(DATABASE_URL)

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
