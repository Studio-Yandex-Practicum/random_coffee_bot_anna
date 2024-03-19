"""Администрирование телеграмм бота"""
from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import user
from filters.is_admin import IsAdmin
from keyboards.reply import ADMIN_KBRD, MAIN_MENU_KBRD

ADMIN_ONLY = 'Данные действия доступны только администратору'
DELETE_COMPLITE = 'Пользователь удалён'
NOT_FOUND = 'Пользователь не найден'
ADD_ID = 'Введите id'
ALL_USERS = 'Список всех пользователей'
DELETE_USER = 'Удалить пользователя'
DEACTIVATE_USER = 'Деактивировать пользователя'
DEACTIVATE_COMPLITE = 'Пользователь дективирован'
MAIN_MENU = 'Главное меню'
RETURN_TO_MENU = 'Вы вернулись в главное меню'


admin_router = Router()
admin_router.message.filter(IsAdmin())


class DelUser(StatesGroup):
    tg_id = State()


class DeactiveUser(StatesGroup):
    tg_id = State()


@admin_router.message(Command('admin'))
async def get_admin_commands(message: types.Message):
    """Команда для администрирования пользователей."""
    await message.answer(ADMIN_ONLY, reply_markup=ADMIN_KBRD)


@admin_router.message(F.text == ALL_USERS)
async def get_user_list(message: types.Message, session: AsyncSession):
    """Получить список всех пользователей."""
    user_list_str = '\n'.join(
        repr(user) for user in await user.get_all(session)
    )
    if user_list_str:
        await message.answer(user_list_str)
    else:
        await message.answer(NOT_FOUND)


@admin_router.message(StateFilter(None), F.text == DELETE_USER)
async def delete_user(message: types.Message, state: FSMContext):
    """Удалить пользователя. Ожидание id пользователя"""
    await message.answer(
        ADD_ID,
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(DelUser.tg_id)


@admin_router.message(DelUser.tg_id, F.text)
async def delete_user_id(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession
):
    """Удаление пользователя по tg_id."""
    await state.update_data(tg_id=message.text)
    if await user.remove(session, await user.get(session, int(message.text))):
        await message.answer(DELETE_COMPLITE, reply_markup=ADMIN_KBRD)
        await state.clear()
    message.answer(NOT_FOUND, reply_markup=ADMIN_KBRD)


@admin_router.message(
        StateFilter(None),
        F.text == DEACTIVATE_USER
)
async def deactive_user(message: types.Message, state: FSMContext):
    """Деактивировать пользователя. Ожидание id пользователя"""
    await message.answer(ADD_ID, reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(DeactiveUser.tg_id)


@admin_router.message(DeactiveUser.tg_id, F.text)
async def deactivate_user_id(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession
):
    """Деактивация пользователя по id."""
    await state.update_data(tg_id=message.text)
    deactive = await user.activate_deactivate_user(session, int(message.text))
    if deactive:
        await message.answer(
            DEACTIVATE_COMPLITE,
            reply_markup=ADMIN_KBRD
        )
        await state.clear()
    else:
        await message.answer(NOT_FOUND, reply_markup=ADMIN_KBRD)
        await state.clear()


@admin_router.message(F.text == MAIN_MENU)
async def menu(message: types.Message):
    """Вернуться в главное меню."""
    await message.answer(RETURN_TO_MENU, reply_markup=MAIN_MENU_KBRD)
