import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import SQLALCHEMY_DATABASE_URL
from models import User, Role

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine)


def create_user(username: str, password: str, role_id: int):
    """
    Create a new user and assign them to a specified role.

    Parameters:
    - username: The username of the new user.
    - password: The password of the new user (will be encrypted before storage).
    - role_id: The ID of the role to which the user should be assigned.
    """

    # Encrypt the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Create a new session
    session = Session()

    # Fetch the role by ID
    role = session.query(Role).filter_by(role_id=role_id).first()
    if not role:
        print(f"Role with ID {role_id} does not exist.")
        return

    # Create and add the user
    user = User(username=username, roles=[role])
    user.hashed_password = hashed_password.decode(
        "utf-8"
    )  # Storing the hashed password as a string in the database
    session.add(user)

    # Commit the changes
    session.commit()
    print(f"User '{username}' created and assigned to role '{role.role_name}'.")


if __name__ == "__main__":
    # Fetch available roles
    session = Session()
    roles = session.query(Role).all()
    if not roles:
        print("No roles available. Please create roles first.")
        exit()

    print("Available roles:")
    for idx, role in enumerate(roles, start=1):
        print(f"{idx}. {role.role_name}")

    # Take user inputs
    username_input = input("Enter the username: ")
    password_input = input("Enter the password: ")
    role_choice = int(input("Choose a role by entering its number: "))

    # Validate role choice
    if role_choice < 1 or role_choice > len(roles):
        print("Invalid role choice.")
        exit()

    chosen_role_id = roles[role_choice - 1].role_id
    create_user(username_input, password_input, chosen_role_id)
