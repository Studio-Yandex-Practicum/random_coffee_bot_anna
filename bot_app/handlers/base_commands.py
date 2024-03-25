from aiogram import F, Router, types
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from bot_app.database.models import User
from bot_app.keyboards.reply import (
    REGISTER_KBRD,
    NEXT_KBRD,
    MORE_KBRD,
    MAIN_MENU_ACTIVE_KBRD,
    MAIN_MENU_DEACTIVE_KBRD
)

from bot_app.handlers.constants import constants


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
async def start(message: types.Message, session: AsyncSession):
    """Команда /start."""
    tg_user = await user.get(session, message.from_user.id)
    if tg_user:
        await message.answer(constants['START_MSG'], reply_markup=MAIN_MENU_ACTIVE_KBRD)
        return
    await message.answer(constants['START_MSG'], reply_markup=REGISTER_KBRD)


@base_commands_router.message(F.text == ABOUT_PROJECT)
async def about(message: types.Message):
    """Информация о проекте."""
    await message.answer(constants['about_msg'])


@base_commands_router.message(F.text.contains(COMMENTS))
async def about_coll(message: types.Message):
    """Что о нас думают."""
    await message.answer(
        constants['about_project_msg'],
        reply_markup=NEXT_KBRD
    )


@base_commands_router.message(F.text == NEXT_COMMENT)
async def aboutss(message: types.Message):
    """Что о нас думают."""
    await message.answer(
        constants['comments_msg'],
        reply_markup=MORE_KBRD
    )


@base_commands_router.message(F.text == MORE_COMMENT)
async def about_one(message: types.Message):
    """Что о нас думают."""
    await message.answer(
        constants['review_msg'],
        reply_markup=MAIN_MENU_ACTIVE_KBRD
    )


@base_commands_router.message(F.text == MAIN_MENU)
async def menu(message: types.Message, session: AsyncSession):
    """Вернуться в главное меню."""
    tg_user = await user.get(session, message.from_user.id)
    if tg_user.is_active:
        await message.answer(
            RETURN_TO_MENU,
            reply_markup=MAIN_MENU_ACTIVE_KBRD
        )
    else:
        await message.answer(
            RETURN_TO_MENU,
            reply_markup=MAIN_MENU_DEACTIVE_KBRD
        )


@base_commands_router.message(F.text == STOP_PARTICIPATE)
async def stop(message: types.Message, session: AsyncSession):
    """Остановить участие."""
    tg_user = await user.get(session, int(message.from_user.id))
    if await user.activate_deactivate_user(session, tg_user.email):
        await message.answer(
            constants['stop_participate_msg'],
            reply_markup=MAIN_MENU_DEACTIVE_KBRD
        )
    else:
        await message.answer(CANT_STOP)


@base_commands_router.message(F.text == RESTART_PARTICIPATE)
async def up(message: types.Message, session: AsyncSession):
    """Возобновить участие."""
    tg_user = await user.get(session, int(message.from_user.id))
    if await user.activate_deactivate_user(session, tg_user.email):
        await message.answer(
            RESTART_PARTICIPATE_MSG,
            reply_markup=MAIN_MENU_ACTIVE_KBRD
    )
    else:
        await message.answer(CANT_RESTART_PARTICIPATE)
