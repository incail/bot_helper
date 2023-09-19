from aiogram import Router, F, Bot
from aiogram.enums.content_type import ContentType
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from aiogram.fsm.state import default_state
from keyboards.inline_keyboards import kb_start, kb_start_show_questions, kb_delite_or_show_anwser, kb_show_anwer, kb_answer_or_next
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON
from states.states import FSMAskQestion, FSMAnswerQuestion
from filters.filters import CheckCategory, Questions, IdQuestions
from models.models import DataBase
from keyboards.default_keyboards import categorys_keyboard, yes_or_no_keyboard

router: Router = Router()


@router.message(CommandStart(), Questions())
async def start_command_question(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(text=LEXICON['/start'], reply_markup=kb_start_show_questions)


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(text=LEXICON['/start'], reply_markup=kb_start)


@router.message(Command(commands='help'))
async def help_command(message: Message) -> None:
    await message.answer(text=LEXICON['/help'])


@router.message(Command(commands='clear'), Questions())
async def clear_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(text=LEXICON['/start'], reply_markup=kb_start_show_questions)


@router.message(Command(commands='clear'))
async def clear_command_question(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(text=LEXICON['/start'], reply_markup=kb_start_show_questions)


@router.callback_query(F.data == 'show_questions')
async def show_questions(callback: CallbackQuery):
    all_questions = await DataBase().get_questions_user(callback.from_user.id)
    for i in all_questions:
        await callback.message.answer(text=i[1], reply_markup=kb_delite_or_show_anwser(i[0]))


@router.callback_query(IdQuestions())
async def show_answer(callback: CallbackQuery):
    all_answer = DataBase().get_answer_for_questions(callback.data)
    if all_answer:
        for i in all_answer:
            if i[1] is None:
                await callback.message.answer(text=LEXICON['answer_for'] + 'пользователь не определён', reply_markup=kb_show_anwer(i[0]))
            else:
                await callback.message.answer(text=LEXICON['answer_for'] + i[1], reply_markup=kb_show_anwer(i[0]))
    else:
        await callback.answer(text='Ответов нет')


@router.callback_query(F.data.startswith('delite_question'))
async def delite_question(callback: CallbackQuery):
    id_question = callback.data.split()[1]
    await DataBase().delite_question(id_question)
    await callback.answer(text=LEXICON['delite_question'])
    await callback.message.delete()


@router.callback_query(F.data.startswith('show_answer'))
async def show_answer_all(callback: CallbackQuery):
    id_answer = callback.data.split()[1]
    answer = await DataBase().get_answer(id_answer)
    if answer is None:
        await callback.message.answer(text=LEXICON['answer_for'] + 'пользователь не определён' + '\n' + str(answer[1]))
    else:
        await callback.message.answer(text=LEXICON['answer_for'] + str(answer[0]) + '\n' + str(answer[1]))


@router.callback_query(F.data == 'ask_question', StateFilter(default_state))
async def choise_language(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(text=LEXICON['choice_category'], reply_markup=categorys_keyboard)
    await state.set_state(FSMAskQestion.language)


@router.callback_query(F.data == 'answer_question', StateFilter(default_state))
async def choise_language_for_answer(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(text=LEXICON['choice_category_for_answer'], reply_markup=categorys_keyboard)
    await state.set_state(FSMAnswerQuestion.category)


@router.message(StateFilter(FSMAskQestion.language), CheckCategory())
async def asq_question(message: Message, state: FSMContext):
    await state.update_data(language_id=await DataBase().get_id_category(message.text))
    await message.answer(text=LEXICON['ask_question'], reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMAskQestion.question)


@router.message(StateFilter(FSMAnswerQuestion.category), CheckCategory())
async def answer_question(message: Message, state: FSMContext, page=1):
    await state.update_data(questions=await DataBase().get_questions_for_id_category(await DataBase().get_id_category(message.text), message.from_user.id))
    data = await state.get_data()
    if data['questions']:
        pages_count = len(data['questions'])
        left = page - 1 if page != 1 else pages_count
        right = page + 1 if page != pages_count else 1
        await message.answer(text=LEXICON['/clear'], reply_markup=ReplyKeyboardRemove())
        await message.answer(text=data['questions'][page - 1][1], reply_markup=kb_answer_or_next(right, left, pages_count, page, data['questions'][page - 1][0]))
        await state.set_state(FSMAnswerQuestion.view_questions)
    else:
        await message.answer(text=LEXICON['no_questions'])


@router.callback_query(StateFilter(FSMAnswerQuestion.view_questions), F.data.startswith('to '))
async def next_question(callback: CallbackQuery, state: FSMContext):
    page = int(callback.data.split()[1])
    data = await state.get_data()
    pages_count = len(data['questions'])
    left = page - 1 if page != 1 else pages_count
    right = page + 1 if page != pages_count else 1
    await callback.message.delete()
    await callback.message.answer(text=data['questions'][page - 1][1], reply_markup=kb_answer_or_next(right, left, pages_count, page, data['questions'][page - 1][0]))


@router.callback_query(StateFilter(FSMAnswerQuestion.view_questions), F.data.startswith('answer'))
async def write_answer(callback: CallbackQuery, state: FSMContext):
    await state.update_data(id_questions=int(callback.data.split()[1]))
    print(callback.data.split()[1])
    await state.update_data(user_id_question=await DataBase().get_user_id_question(callback.data.split()[1]))
    await callback.message.answer(text=LEXICON['write_answer'])
    await state.set_state(FSMAnswerQuestion.answer)


@router.message(StateFilter(FSMAnswerQuestion.answer))
async def save_answer(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await DataBase().save_answer(message.from_user.id, message.from_user.username, data['user_id_question'], message.text, data['id_questions'])
    await state.clear()
    await bot.send_message(chat_id=data['user_id_question'], text=LEXICON['new_answer'])
    await message.answer(text=LEXICON['save_answer'])


@router.message(or_f(StateFilter(FSMAskQestion.language), StateFilter(FSMAnswerQuestion.category)))
async def warning_languages(message: Message):
    await message.answer(text=LEXICON['no_category'])


@router.message(StateFilter(FSMAskQestion.question), F.content_type == ContentType.TEXT)
async def write_question(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    data = await state.get_data()
    await DataBase().save_questions(message.from_user.id, message.text, data['language_id'])
    # добавить фильтр на проверку вопроса
    await state.clear()
    await message.answer(text=LEXICON['save_question'], reply_markup=kb_start_show_questions)
    # await message.answer(text=LEXICON['add_photo'], reply_markup=yes_or_no_keyboard)
    # await state.set_state(FSMAskQestion.photo)


# @router.message(StateFilter(FSMAskQestion.photo), F.text == 'Да')
# async def get_photo_from_user(message: Message, state: FSMContext):
#     await message.answer(text='Можешь отправлять фотографию!', reply_markup=ReplyKeyboardRemove())
#     await state.set_state(FSMAskQestion.send_photo)


# @router.message(StateFilter(FSMAskQestion.photo), F.text == 'Нет')
# async def save_question(message: Message, state: FSMContext):
#     data = await state.get_data()
#     await DataBase().save_questions(message.from_user.id, data['question'], data['language_id'])
#     await state.clear()
#     await message.answer(text=LEXICON['save_question'], reply_markup=ReplyKeyboardRemove())


# @router.message(StateFilter(FSMAskQestion.photo), F.content_type != ContentType.PHOTO)
# async def eror_input(message: Message, state: FSMContext):
#     await message.answer(text='Будешь добавлять фото к своему вопросу?(напиши "Да" или "Нет")')


# @router.message(StateFilter(FSMAskQestion.send_photo), F.content_type == ContentType.PHOTO)
# async def save_question_and_photo(message: Message, state: FSMContext):
#     await message.answer(text='четко', reply_markup=ReplyKeyboardRemove())
#     await state.clear()
