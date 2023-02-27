from typing import Optional

from sqlalchemy import select

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Answer,
    Question,
    Theme,
    QuestionModel,
    AnswerModel,
    ThemeModel
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme = ThemeModel(title=title)
        async with self.app.database.session() as session:
            session.add(theme)
            await session.commit()
            await session.refresh(theme)
            return theme.create_dataclass(class_=Theme)

    async def get_theme_by_title(self, title: str) -> Optional[Theme]:
        async with self.app.database.session() as session:
            query = select(ThemeModel).where(ThemeModel.title == title.strip())
            result = await session.execute(query)
            theme = result.scalars().first()
            if theme:
                return theme.create_dataclass(class_=Theme)

    async def get_theme_by_id(self, id_: int) -> Optional[Theme]:
         async with self.app.database.session() as session:
            query = select(ThemeModel).where(ThemeModel.id == id_)
            result = await session.execute(query)
            theme = result.scalars().first()
            if theme:
                return theme.create_dataclass(class_=Theme)

    async def list_themes(self) -> list[Theme]:
        async with self.app.database.session() as session:
            query = select(ThemeModel)
            result = await session.execute(query)
            theme = result.scalars()
            return [obj.create_dataclass(class_=Theme) for obj in theme]

    async def create_answers(
        self, question_id: int, answers: list[Answer]
    ) -> list[Answer]:
        async with self.app.database.session() as session:
            for answer in answers:
                res_answer = AnswerModel(title=answer['title'], is_correct=answer['is_correct'], question_id=question_id)
                session.add(res_answer)
                await session.commit()
            return answers

    async def create_question(
        self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        async with self.app.database.session() as session:
            answers = [AnswerModel(title=answer.title, is_correct=answer.is_correct) for answer in answers]
            question = QuestionModel(title=title, theme_id=theme_id, answers=answers)
            session.add(question)
            await session.commit()
            return question.create_dataclass(class_=Question)

    async def get_question_by_title(self, title: str) -> Optional[Question]:
        async with self.app.database.session() as session:
            query = select(QuestionModel).where(QuestionModel.title == title)
            result = await session.execute(query)
            question = result.scalars().first()
            if question:
                return question.create_dataclass(class_=Question)

    async def list_questions(self, theme_id: Optional[int] = None) -> list[Question]:
        async with self.app.database.session() as session:
            if theme_id:
                query = select(QuestionModel).where(QuestionModel.theme_id == theme_id)
            else:
                query = select(QuestionModel)
            result = await session.execute(query)
            questions = result.scalars().all()
            return [obj.create_dataclass(class_=Question) for obj in questions]
