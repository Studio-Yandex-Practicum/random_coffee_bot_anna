from aiogram import F, Router, types
from aiogram.filters import CommandStart
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot_app.database.models import User
from bot_app.keyboards.reply import (
    REGISTER_KBRD,
    NEXT_KBRD,
    MORE_KBRD,
    MAIN_MENU_ACTIVE_KBRD,
    MAIN_MENU_DEACTIVE_KBRD
)
from bot_app.handlers.constants import BaseCommands, InfoMessage

logger.add("error_logs.log", rotation="500 MB", backtrace=True, diagnose=True)


base_commands_router = Router()


@base_commands_router.message(CommandStart())
async def start(message: types.Message, session: AsyncSession):
    """Command /start."""
    try:
        tg_user = await User.get(session, message.from_user.id)
        if tg_user:
            if tg_user.is_active:
                await message.answer(
                    InfoMessage.START_MSG,
                    reply_markup=MAIN_MENU_ACTIVE_KBRD
                )
            else:
                await message.answer(
                    InfoMessage.START_MSG,
                    reply_markup=MAIN_MENU_DEACTIVE_KBRD
                )
        else:
            await message.answer(
                InfoMessage.START_MSG,
                reply_markup=REGISTER_KBRD
            )
    except Exception as e:
        logger.error(f"Error in start function: {e}")


@base_commands_router.message(F.text == BaseCommands.ABOUT_PROJECT)
async def about(message: types.Message):
    """Information about the project."""
    try:
        await message.answer(InfoMessage.ABOUT_MSG)
    except Exception as e:
        logger.error(f"Error in about function: {e}")


@base_commands_router.message(F.text.contains(BaseCommands.COMMENTS))
async def about_coll(message: types.Message):
    """What they think of us thirst."""
    try:
        await message.answer(
            InfoMessage.ABOUT_PROJECT_MSG,
            reply_markup=NEXT_KBRD
        )
    except Exception as e:
        logger.error(f"Error in about_coll function: {e}")


@base_commands_router.message(F.text == BaseCommands.NEXT_COMMENT)
async def aboutss(message: types.Message):
    """What they think of us second."""
    try:
        await message.answer(
            InfoMessage.COMMENTS_MSG,
            reply_markup=MORE_KBRD
        )
    except Exception as e:
        logger.error(f"Error in aboutss function: {e}")


@base_commands_router.message(F.text == BaseCommands.MORE_COMMENT)
async def about_one(message: types.Message):
    """What they think of us third."""
    try:
        await message.answer(
            InfoMessage.REVIEW_MSG,
            reply_markup=MAIN_MENU_ACTIVE_KBRD
        )
    except Exception as e:
        logger.error(f"Error in about_one function: {e}")


@base_commands_router.message(F.text == BaseCommands.MAIN_MENU)
async def menu(message: types.Message, session: AsyncSession):
    """Return to main menu."""
    try:
        tg_user = await User.get(session, message.from_user.id)
        if tg_user.is_active:
            await message.answer(
                BaseCommands.RETURN_TO_MENU,
                reply_markup=MAIN_MENU_ACTIVE_KBRD
            )
        else:
            await message.answer(
                BaseCommands.RETURN_TO_MENU,
                reply_markup=MAIN_MENU_DEACTIVE_KBRD
            )
    except Exception as e:
        logger.error(f"Error in menu function: {e}")


@base_commands_router.message(F.text == BaseCommands.STOP_PARTICIPATE)
async def stop(message: types.Message, session: AsyncSession):
    """Stop participation."""
    try:
        tg_user = await User.get(session, int(message.from_user.id))
        if await User.activate_deactivate_user(session, tg_user.email):
            await message.answer(
                BaseCommands.STOP_PARTICIPATE_MSG,
                reply_markup=MAIN_MENU_DEACTIVE_KBRD
            )
        else:
            await message.answer(BaseCommands.CANT_STOP)
    except Exception as e:
        logger.error(f"Error in stop function: {e}")


@base_commands_router.message(F.text == BaseCommands.RESTART_PARTICIPATE)
async def up(message: types.Message, session: AsyncSession):
    """Resume participation."""
    try:
        tg_user = await User.get(session, int(message.from_user.id))
        if await User.activate_deactivate_user(session, tg_user.email):
            await message.answer(
                BaseCommands.RESTART_PARTICIPATE_MSG,
                reply_markup=MAIN_MENU_ACTIVE_KBRD
            )
        else:
            await message.answer(BaseCommands.CANT_RESTART_PARTICIPATE)
    except Exception as e:
        logger.error(f"Error in up function: {e}")
