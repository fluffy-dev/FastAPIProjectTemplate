from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.libs.base_model import Base


class UserModel(Base):
    """
    SQLAlchemy ORM model representing the 'users' table.

    This model maps the user entity to the relational database structure.

    Attributes:
        __tablename__ (str): The name of the table in the database ('users').
        name (Mapped[str]): The user's display name. Max length 30.
        login (Mapped[str]): The user's unique username. Max length 50.
                             Indexed and Unique constraint applied.
        email (Mapped[str]): The user's unique email. Max length 50.
                             Indexed and Unique constraint applied.
        password (Mapped[str]): The hashed password string. Max length 255.
    """
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(30))
    login: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))