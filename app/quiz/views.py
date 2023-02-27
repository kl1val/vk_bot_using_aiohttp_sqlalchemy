from aiohttp.web_exceptions import (
    HTTPConflict,
    HTTPBadRequest,
    HTTPNotFound,

)
from aiohttp_apispec import request_schema, response_schema, docs
from app.quiz.models import Answer

from app.quiz.schemes import (
    QuestionSchema,
    ThemeListSchema,
    ThemeSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(AuthRequiredMixin, View):
    @docs(tags='theme', summary='Add a theme', description='Method allowing to add a theme')
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema, 200)
    async def post(self):
        title = self.data["title"]
        if await self.store.quizzes.get_theme_by_title(title=title):
            raise HTTPConflict
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    @docs(tags='theme', summary='Get list of themes', description='Method allowing to get a list themes')
    @response_schema(ThemeListSchema, 200)
    async def get(self):
        themes = await self.request.app.store.quizzes.list_themes()
        raw_themes = [ThemeSchema().dump(theme) for theme in themes]
        return json_response(data={"themes": raw_themes})


class QuestionAddView(AuthRequiredMixin, View):
    @docs(tags='theme', summary='Add a question', description='Method allowing to add a question')
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema, 200)
    async def post(self):
        answers_list = self.data["answers"]
        
        if any((
            len(tuple(filter(lambda x: x["is_correct"] is True, answers_list))) > 1,
            len(answers_list) == 1, 
            not any(map(lambda x: x["is_correct"], answers_list))
        )):
            raise HTTPBadRequest

        if await self.request.app.store.quizzes.get_question_by_title(self.data["title"]):
            raise HTTPConflict

        if not await self.request.app.store.quizzes.get_theme_by_id(self.data["theme_id"]):
            raise HTTPNotFound
 
        question = await self.request.app.store.quizzes.create_question(
            title = self.data["title"],
            theme_id = self.data["theme_id"],
            answers = [Answer(title=answer["title"], is_correct=answer["is_correct"]) for answer in answers_list]
        )
        return json_response(data=QuestionSchema().dump(question))


class QuestionListView(AuthRequiredMixin, View):
    @docs(tags='theme', summary='Get list of themes', description='Method allowing to get a list questions')
    @response_schema(QuestionSchema, 200)
    async def get(self):
        theme_id = self.request.query.get("theme_id")

        if theme_id is None:
            questions_list = await self.request.app.store.quizzes.list_questions()
            raw_questions = [QuestionSchema().dump(question) for question in questions_list]
            
            return json_response(data={"questions": raw_questions})
            
        questions_list = await self.request.app.store.quizzes.list_questions()
        questions = tuple(filter(lambda x: x.theme_id == int(theme_id), questions_list))
        raw_questions = [QuestionSchema().dump(question) for question in questions]
        
        return json_response(data={"questions": raw_questions})
