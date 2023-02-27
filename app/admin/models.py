from dataclasses import dataclass
from hashlib import sha256
from typing import Optional

from app.store.database.sqlalchemy_base import db

from sqlalchemy import (
    Column,
    Integer, 
    VARCHAR,
)


@dataclass
class Admin:
    id: int
    email: str
    password: Optional[str] = None

    def is_password_valid(self, password: str):
        return self.password == sha256(password.encode()).hexdigest()

    @classmethod
    def from_session(cls, session: Optional[dict]) -> Optional["Admin"]:
        return cls(id=session["admin"]["id"], email=session["admin"]["email"])


class AdminModel(db):
    __tablename__ = "admins"

    id = Column(Integer, nullable=False, index=True, primary_key=True)
    email = Column(VARCHAR(100), index=True, nullable=False, unique=True)
    password = Column(VARCHAR(100), nullable=False)

    def create_dataclass(self, class_: Admin) -> Admin:
        return class_(id=self.id, email=self.email, password=self.password)
    
    def __repr__(self):
        return f"<AdminModel(id='{self.id}', email='{self.email}', password='{self.password}')>"
