"""
Module: session.py

This module initializes the database for the Role-Based Access Control (RBAC) system and sets up a basic configuration.
It establishes a connection to the database using SQLAlchemy and provides functionality to initialize the database
with predefined entities such as permissions, roles, and users.

Key Functions:
- init_db: Initializes the database and populates it with basic entities.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import SQLALCHEMY_DATABASE_URL
from models import Base, Permission, Role


def init_db():
    """
    Initialize the database.

    This function:
    1. Connects to the specified SQLite database.
    2. Creates tables if they do not exist.
    3. Populates the tables with a basic set of entities:
       - A permission named "full_access".
       - An "Admin" role with the "full_access" permission.
    """
    # Create an engine connected to the SQLite database.
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    # Create tables in the database.
    Base.metadata.create_all(engine)

    # Create a new session bound to the engine.
    make_session = sessionmaker(bind=engine)
    session = make_session()

    # Create a new permission named "full_access".
    perm1 = Permission(permission_name="full_access")

    # Create a new role named "Admin" and assign the "full_access" permission to it.
    admin_role = Role(role_name="Admin", permissions=[perm1])

    # Add the new user to the session and commit the changes to the database.
    session.add(admin_role)
    session.commit()


# If the script is run as the main module, initialize the database.
if __name__ == "__main__":
    init_db()
