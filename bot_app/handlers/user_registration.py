from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.crud import get_user_by_id, orm_add_user
from keyboards.reply import REGISTER_KBRD, MAIN_MENU_KBRD
from sqlalchemy.ext.asyncio import AsyncSession


REGISTER = 'Регистрация'
CANT_REGISTER = 'Вы уже зарегистрированы'
ADD_NAME = 'Ведите своё имя'
CANCEL = 'отмена'
CANCSEL_MSG = 'Действия отменены'
BACK = 'назад'
NO_STEP = 'Предыдущего шага нет, введите имя напишите "отмена"'
ADD_LAST_NAME = 'Введите фамилию'
ADD_EMAIL = 'Введите почту'
EMAIL_DOMAIN = 'mail.ru'
COMPLITE_MSG = 'Регистрация прошла успешно'
INVALID_EMAIL = 'Вы ввели не корпаративную почту'


user_reg_router = Router()


class AddUser(StatesGroup):
    name = State()
    last_name = State()
    mail = State()

    texts = {
        'AddUser:name': 'Введите имя заново:',
        'AddUser:last_name': 'Введите фамилию заново:',
        'AddUser:mail': 'Введите мэйл заново:',
    }


@user_reg_router.message(StateFilter(None), F.text == REGISTER)
async def add_name(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession
):
    """Начало регистрации пользователя."""
    user = await get_user_by_id(session, int(message.from_user.id))
    if user:
        await message.answer(
            CANT_REGISTER,
            reply_markup=MAIN_MENU_KBRD
        )
        await state.clear()
        return
    else:
        await message.answer(
            ADD_NAME,
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.set_state(AddUser.name)


@user_reg_router.message(StateFilter('*'), Command(CANCEL))
@user_reg_router.message(StateFilter('*'), F.text.casefold() == CANCEL)
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """Отмена всех действий регистрации."""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(CANCSEL_MSG, reply_markup=REGISTER_KBRD)


@user_reg_router.message(StateFilter('*'), Command(BACK))
@user_reg_router.message(StateFilter('*'), F.text.casefold() == BACK)
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    """Шаг назад для регистрации."""
    current_state = await state.get_state()
    if current_state == AddUser.name:
        await message.answer(NO_STEP)
        return
    previous = None
    for step in AddUser.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                f"""Вы вернулись к предыдущему шагу
                {AddUser.texts[previous.state]}"""
            )
            return
        previous = step


@user_reg_router.message(AddUser.name, F.text)
async def add_last_name(message: types.Message, state: FSMContext):
    """Добавление фамилии."""
    await state.update_data(name=message.text)
    await message.answer(ADD_LAST_NAME)
    await state.set_state(AddUser.last_name)


@user_reg_router.message(AddUser.last_name, F.text)
async def add_mail(message: types.Message, state: FSMContext):
    """Добавление почты."""
    await state.update_data(last_name=message.text)
    await message.answer(ADD_EMAIL)
    await state.set_state(AddUser.mail)


@user_reg_router.message(AddUser.mail, F.text.contains(EMAIL_DOMAIN))
async def refister(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession
):
    """Окончание регистрации."""
    await state.update_data(mail=message.text)
    await message.answer(COMPLITE_MSG, reply_markup=MAIN_MENU_KBRD)
    data = await state.get_data()
    data['tg_id'] = message.from_user.id
    await orm_add_user(session, data)
    await state.clear()


@user_reg_router.message(AddUser.mail)
async def invalid_mail(message: types.Message, state: FSMContext):
    """Сообщение о неккоректной почте."""
    await message.answer(INVALID_EMAIL)
