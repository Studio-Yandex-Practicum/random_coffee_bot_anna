from aiogram import F, Router, types
from aiogram.filters import CommandStart
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot_app.database.models import user
from bot_app.handlers.constants import constants
from bot_app.keyboards.reply import (MAIN_MENU_KBRD, MORE_KBRD, NEXT_KBRD,
                                     REGISTER_KBRD)

logger.add("error_logs.log", level="ERROR")


ABOUT_PROJECT = 'О проекте'
COMMENTS = 'Наши коллеги про'
STOP_PARTICIPATE = 'Приостановить участие'
CANT_STOP = 'Не удалось приостановить участие'
RESTART_PARTICIPATE = 'Возобновить участие'
RESTART_PARTICIPATE_MSG = 'Вы возобновили участие'
CANT_RESTART_PARTICIPATE = 'Не удалось возобновить участие'
NEXT_COMMENT = 'Следующий комментарий'
MORE_COMMENT = 'Ещё комментарий'
MAIN_MENU = 'Главное меню'
RETURN_TO_MENU = 'Вы вернулись в главное меню'

base_commands_router = Router()


@base_commands_router.message(CommandStart())
async def start(message: types.Message):
    """Команда /start."""
    try:
        await message.answer(constants['START_MSG'], reply_markup=REGISTER_KBRD)
    except Exception as e:
        logger.error(f"Error in start function: {e}")


@base_commands_router.message(F.text == ABOUT_PROJECT)
async def about(message: types.Message):
    """Информация о проекте."""
    try:
        await message.answer(constants['about_msg'])
    except Exception as e:
        logger.error(f"Error in about function: {e}")


@base_commands_router.message(F.text.contains(COMMENTS))
async def about_coll(message: types.Message):
    """Что о нас думают."""
    try:
        await message.answer(
            constants['about_project_msg'],
            reply_markup=NEXT_KBRD
        )
    except Exception as e:
        logger.error(f"Error in about_coll function: {e}")


@base_commands_router.message(F.text == NEXT_COMMENT)
async def aboutss(message: types.Message):
    """Что о нас думают."""
    try:
        await message.answer(
            constants['comments_msg'],
            reply_markup=MORE_KBRD
        )
    except Exception as e:
        logger.error(f"Error in aboutss function: {e}")


@base_commands_router.message(F.text == MORE_COMMENT)
async def about_one(message: types.Message):
    """Что о нас думают."""
    try:
        await message.answer(
            constants['review_msg'],
            reply_markup=MAIN_MENU_KBRD
        )
    except Exception as e:
        logger.error(f"Error in about_one function: {e}")


@base_commands_router.message(F.text == MAIN_MENU)
async def menu(message: types.Message):
    """Вернуться в главное меню."""
    try:
        await message.answer(RETURN_TO_MENU, reply_markup=MAIN_MENU_KBRD)
    except Exception as e:
        logger.error(f"Error in menu function: {e}")


@base_commands_router.message(F.text == STOP_PARTICIPATE)
async def stop(message: types.Message, session: AsyncSession):
    """Остановить участие."""
    try:
        if await user.activate_deactivate_user(session, int(message.from_user.id)):
            await message.answer(constants['stop_participate_msg'])
        else:
            await message.answer(CANT_STOP)
    except Exception as e:
        logger.error(f"Error in stop function: {e}")


@base_commands_router.message(F.text == RESTART_PARTICIPATE)
async def up(message: types.Message, session: AsyncSession):
    """Возобновить участие."""
    try:
        if await user.activate_deactivate_user(session, int(message.from_user.id)):
            await message.answer(RESTART_PARTICIPATE_MSG)
        else:
            await message.answer(CANT_RESTART_PARTICIPATE)
    except Exception as e:
        logger.error(f"Error in up function: {e}")
