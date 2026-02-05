from sqlalchemy.orm import Mapped
from datetime import datetime, date
from typing import Optional
from ... import db
from .enums import Role, Gender

class User(db.Model):
    __bind_key__ = 'users'
    __tablename__ = 'users'

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(100), nullable=False)
    surname: Mapped[str] = db.Column(db.String(100), nullable=False)
    email: Mapped[str] = db.Column(db.String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = db.Column(db.String(255), nullable=False)
    date_of_birth: Mapped[date] = db.Column(db.Date, nullable=False)
    gender: Mapped[str] = db.Column(Gender, nullable=False)
    country: Mapped[str] = db.Column(db.String(100), nullable=False)
    street: Mapped[str] = db.Column(db.String(255), nullable=False)
    number: Mapped[str] = db.Column(db.String(20), nullable=False)
    account_balance: Mapped[float] = db.Column(db.Numeric(10, 2), default=0.00)
    role: Mapped[str] = db.Column(Role, default='USER')
    profile_image: Mapped[Optional[str]] = db.Column(db.Text)
    failed_login_attempts: Mapped[int] = db.Column(db.Integer, default=0)
    blocked_until: Mapped[Optional[datetime]] = db.Column(db.DateTime)
    created_at: Mapped[datetime] = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at: Mapped[datetime] = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Session(db.Model):
    __bind_key__ = 'users'
    __tablename__ = 'sessions'

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    user_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    token: Mapped[str] = db.Column(db.String(500), unique=True, nullable=False)
    expires_at: Mapped[datetime] = db.Column(db.DateTime, nullable=False)
    created_at: Mapped[datetime] = db.Column(db.DateTime, default=db.func.current_timestamp())