from typing import List, Optional, Tuple

from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot_app.core.config import bot, settings
from bot_app.database.models import User
from bot_app.mailing.distribution import distribute_pairs

logger.add('bot_logs.log', rotation='500 MB', backtrace=True, diagnose=True)

MEETING_MESSAGE = '''
Ваша пара для Кофе вслепую {} {} ({}).
Договоритесь с коллегой о кофе брейке на этой неделе.
Приятного времяпровождения!
'''
MEET_OK = 'Да'
MEET_FALSE = 'Нет'
MEET_END_OF_WEEK = 'Встретимся в конце недели'
REMINDER_MAILING = '''
Удалось ли уже встретиться с коллегой и выпить чашечку кофе?
'''
TEXT_NO_PAIR = '''
Привет! На этой неделе в нашем проекте «Кофе вслепую» нечетное количество
участников, поэтому имя коллеги тебе придет на следующей неделе.
Но сейчас не теряй возможность, пригласи на чашечку кофе любого
коллегу и предложи ему присоединиться к нашему проекту
(конечно, если он еще не участвует)!
Отличного дня и продуктивной недели😊
'''
NO_ACTIVE = '''
Проект "Кофе Вслепую" не работает из-за отсутствия активных участников.
'''

meet_inline_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=MEET_OK, callback_data='button_meeting'),
         InlineKeyboardButton(text=MEET_FALSE,
                              callback_data='button_meeting')],
        [InlineKeyboardButton(text=MEET_END_OF_WEEK,
                              callback_data='button_meeting')],
    ])


async def mailing_by_user_tg_id(
    chat_id: str,
    text: str,
    inline_buttons: Optional[InlineKeyboardMarkup] = None
):
    """Mailing by tg_id."""
    await bot.send_message(chat_id=chat_id, text=text,
                           reply_markup=inline_buttons)


async def meeting_mailing(
    session: AsyncSession,
    meetings_pairs: List[Tuple[User, User]] = None
):
    """Mailing to pairs."""
    for pair in meetings_pairs:
        await mailing_by_user_tg_id(chat_id=pair[0].tg_id,
                                    text=MEETING_MESSAGE.format(pair[1].name,
                                    pair[1].last_name, pair[1].email))
        pair[0].is_sent = True
        await mailing_by_user_tg_id(chat_id=pair[1].tg_id,
                                    text=MEETING_MESSAGE.format(pair[0].name,
                                    pair[0].last_name, pair[0].email))
        pair[1].is_sent = True
        await session.commit()
        logger.info(
            f'Send meeting message to users {pair[0].name} and {pair[1].name}'
        )


async def meeting_reminder_mailing(session: AsyncSession):
    """Remainder mailing."""
    for user in await User.get_all_is_sent(session):
        await mailing_by_user_tg_id(
            chat_id=user.tg_id,
            text=REMINDER_MAILING,
            inline_buttons=meet_inline_buttons
        )
        user.is_sent = False
        await session.commit()
        logger.info(f'Send reminder message to user {user.name}')


async def newsletter_about_the_meeting(session: AsyncSession):
    data = await distribute_pairs(session)
    if data.get('pairs'):
        await meeting_mailing(session, data['pairs'])
    else:
        await bot.send_message(chat_id=settings.gen_admin_id,
                               text=NO_ACTIVE)
        logger.info(
            f'Send warning message to genadmin id {settings.gen_admin_id}'
            )
    if data.get('no_pair'):
        await mailing_by_user_tg_id(
            chat_id=data['no_pair'].tg_id, text=TEXT_NO_PAIR
        )
        logger.info(f'Send sorry message to user {data["no_pair"].name}')
