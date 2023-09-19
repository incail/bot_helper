from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


kb_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Задать вопрос', callback_data='ask_question'),
            InlineKeyboardButton(text='Ответить на вопрос', callback_data='answer_question')
        ],
    ]
)

kb_start_show_questions = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Задать вопрос', callback_data='ask_question'),
            InlineKeyboardButton(text='Ответить на вопрос', callback_data='answer_question'),
        ],
        [
            InlineKeyboardButton(text='Просмотреть мои вопросы', callback_data='show_questions')
        ]
    ]
)


def kb_answer_or_next(right, left, pages_count, page, id_question):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='←', callback_data=f'to {left}'),
                InlineKeyboardButton(text=f'{page}/{pages_count}', callback_data='page'),
                InlineKeyboardButton(text='→', callback_data=f'to {right}'),
            ],
            [
                InlineKeyboardButton(text='Ответить', callback_data=f'answer {id_question}'),
            ]
        ]
    )
    return kb


def kb_delite_or_show_anwser(id_question):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Удалить вопрос', callback_data='delite_question ' + str(id_question)),
                InlineKeyboardButton(text='Просмотреть ответы', callback_data=str(id_question)),
            ]
        ]
    )
    return kb


def kb_show_anwer(id_answer):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Показать ответ', callback_data='show_answer ' + str(id_answer)),
            ]
        ]
    )
    return kb
