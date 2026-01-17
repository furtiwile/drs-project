from datetime import date
from sqlalchemy import Integer, String, Float, Date, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database.pgsql import Base
from app.domain.enums.gender import Gender
from app.domain.enums.role import Role

class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[Gender] = mapped_column(Enum(Gender), nullable=False, default=Gender.OTHER)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    street: Mapped[str] = mapped_column(String(50), nullable=False)
    house_number: Mapped[int] = mapped_column(Integer, nullable=False)
    account_balance: Mapped[float] = mapped_column(Float, default=0.0)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False, default=Role.USER)
    profile_picture: Mapped[str] = mapped_column(Text, nullable=True)