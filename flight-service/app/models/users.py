from sqlalchemy import Enum
from .. import db
from .common import UserRole, GenderType

class User(db.Model):
    __bind_key__ = 'users'
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(GenderType, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    account_balance = db.Column(db.Numeric(10, 2), default=0.00)
    role = db.Column(UserRole, default='USER')
    profile_image = db.Column(db.Text)
    failed_login_attempts = db.Column(db.Integer, default=0)
    blocked_until = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Session(db.Model):
    __bind_key__ = 'users'
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    token = db.Column(db.String(500), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())