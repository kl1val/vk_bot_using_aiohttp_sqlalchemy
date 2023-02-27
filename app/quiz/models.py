from dataclasses import dataclass

from typing import Optional

from app.store.database.sqlalchemy_base import db
from sqlalchemy.orm import relationship

from sqlalchemy import (
    Column, 
    Integer, 
    ForeignKey, 
    Boolean, 
    VARCHAR
    )


@dataclass
class Theme:
    id: Optional[int]
    title: str


@dataclass
class Question:
    id: Optional[int]
    title: str
    theme_id: int
    answers: list["Answer"]


@dataclass
class Answer:
    title: str
    is_correct: bool


class ThemeModel(db):
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(VARCHAR(2000), nullable=False, unique=True)
    questions = relationship("QuestionModel", backref="questions", cascade="all, save-update, delete-orphan")

    def create_dataclass(self, class_: Theme) -> Theme:
        return class_(id=self.id,title=self.title)
    
    def __repr__(self):
        return f"<ThemeModel(id='{self.id}', title='{self.title}')>"


class QuestionModel(db):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True,)
    title = Column(VARCHAR(2000), nullable=False, unique=True, index=True)
    theme_id = Column(
        Integer,
        ForeignKey("themes.id", ondelete='CASCADE'),
        nullable=False,
    )
    answers = relationship("AnswerModel", backref="answers", lazy='selectin')

    def create_dataclass(self, class_: Question):
        return class_(
            id=self.id, 
            title=self.title, 
            theme_id=self.theme_id,
            answers=[answer.create_dataclass(class_=Answer) for answer in self.answers] if self.answers else []
            )
    
    def __repr__(self):
        return f"<QuestionModel(id='{self.id}', title='{self.title}')>"


class AnswerModel(db):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True,)
    title = Column(VARCHAR(2000), nullable=False, )
    is_correct = Column(Boolean(), index=True)
    question_id = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)

    def create_dataclass(self, class_: Answer):
        return class_(title=self.title, is_correct=self.is_correct)

    def __repr__(self):
        return f"<AnswerModel(id='{self.id}', title='{self.title}', is_correct='{self.is_correct}')>"
