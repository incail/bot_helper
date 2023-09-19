from aiogram.fsm.state import State, StatesGroup


class FSMAskQestion(StatesGroup):
    language = State()
    question = State()
    send_photo = State()
    photo = State()


class FSMAnswerQuestion(StatesGroup):
    category = State()
    view_questions = State()
    answer = State()
