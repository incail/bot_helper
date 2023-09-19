from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from models.models import DataBase


class CheckCategory(BaseFilter):

    async def __call__(self, message: Message) -> bool | str:
        return await DataBase().check_category(message.text)


class Questions(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        return DataBase().check_have_user_questions(message.from_user.id)


class IdQuestions(BaseFilter):

    async def __call__(self, callback: CallbackQuery) -> bool | list[str]:
        questions_id = await DataBase().get_questions_id_user(callback.from_user.id)
        return callback.data in questions_id
