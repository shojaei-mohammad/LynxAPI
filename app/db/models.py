"""
Module: model.py

This module defines the SQLAlchemy models representing the data structure for a Role-Based Access Control (RBAC) system.
The design includes three primary entities: User, Role, and Permission. Relationships between these entities are
managed using many-to-many association tables.

Entities:
- User: Represents the end-users of the system.
- Role: Represents a collection of permissions.
- Permission: Represents an individual action or operation that can be performed.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Many-to-Many Relationship Tables

# Association table for User and Role entities.
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.user_id")),
    Column("role_id", Integer, ForeignKey("roles.role_id")),
)

# Association table for Role and Permission entities.
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.role_id")),
    Column("permission_id", Integer, ForeignKey("permissions.permission_id")),
)


class User(Base):
    """
    User Model.

    Represents an individual user in the system. Each user can be associated with multiple roles.
    """

    __tablename__ = "users"

    user_id: int = Column(Integer, primary_key=True)
    username: str = Column(String, unique=True, nullable=False)
    roles = relationship("Role", secondary=user_roles, back_populates="users")


class Role(Base):
    """
    Role Model.

    Represents a role that can be assigned to users. Each role is associated with multiple permissions.
    """

    __tablename__ = "roles"

    role_id: int = Column(Integer, primary_key=True)
    role_name: str = Column(String, unique=True, nullable=False)
    permissions = relationship(
        "Permission", secondary=role_permissions, back_populates="roles"
    )
    users = relationship("User", secondary=user_roles, back_populates="roles")


class Permission(Base):
    """
    Permission Model.

    Represents an individual permission or operation that can be granted to roles.
    """

    __tablename__ = "permissions"

    permission_id: int = Column(Integer, primary_key=True)
    permission_name: str = Column(String, unique=True, nullable=False)
    roles = relationship(
        "Role", secondary=role_permissions, back_populates="permissions"
    )
