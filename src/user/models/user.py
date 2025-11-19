from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.libs.base_model import Base


class UserModel(Base):
    """ SQLAlchemy model for user """
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(20))
    surname: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=False)
