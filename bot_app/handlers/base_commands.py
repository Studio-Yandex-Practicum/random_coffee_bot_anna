from aiogram import F, Router, types
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud import activate_deactivate_user
from keyboards.reply import REGISTER_KBRD

START_MSG = 'Привет, я бот'
ABOUT_PROJECT = 'О проекте'
ABOUT_MSG = 'Наш крутой проект'
COMMENTS = 'Наши коллеги про'
ABOUT_PROJECT_MSG = 'Вот что о нас думают'
STOP_PARTICIPATE = 'Приостановить участие'
STOP_PARTICIPATE_MSG = 'Вы приостановили участие'
CANT_STOP = 'Не удалось приостановить участие'
RESTART_PARTICIPATE = 'Возобновить участие'
RESTART_PARTICIPATE_MSG = 'Вы возобновили участие'
CANT_RESTART_PARTICIPATE = 'Не удалось возобновить участие'


base_commands_router = Router()


@base_commands_router.message(CommandStart())
async def start(message: types.Message):
    """Команда /start."""
    await message.answer(START_MSG, reply_markup=REGISTER_KBRD)


@base_commands_router.message(F.text == ABOUT_PROJECT)
async def about(message: types.Message):
    """Информация о проекте."""
    await message.answer(ABOUT_MSG)


@base_commands_router.message(F.text.contains(COMMENTS))
async def about_coll(message: types.Message):
    """Что о нас думают."""
    await message.answer(ABOUT_PROJECT_MSG)


@base_commands_router.message(F.text == STOP_PARTICIPATE)
async def stop(message: types.Message, session: AsyncSession):
    """Остановить участие."""
    if await activate_deactivate_user(session, int(message.from_user.id)):
        await message.answer(STOP_PARTICIPATE_MSG)
    else:
        await message.answer(CANT_STOP)


@base_commands_router.message(F.text == RESTART_PARTICIPATE)
async def up(message: types.Message, session: AsyncSession):
    """Возобновить участие."""
    if await activate_deactivate_user(session, int(message.from_user.id)):
        await message.answer(RESTART_PARTICIPATE_MSG)
    else:
        await message.answer(CANT_RESTART_PARTICIPATE)
