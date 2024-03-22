from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from bot_app.database.models import User
from bot_app.mailing.mailing import mailing_by_user_tg_id, meeting_mailing


TEXT_FOR_EXTRA = 'Привет, так уж вышло, ты в пролете'


def get_unique_pairs(users: List):
    return list(zip(users[:len(users)], reversed(users[len(users) // 2:])))


# async def moving_objects_database(session: AsyncSession):
#     """Перемешиваем список пользователей."""
#     obj = await User.get_first_active(session)
#     await User.first_to_end_db(obj, session)


async def distribution(session):
    # await moving_objects_database(session)
    actives = await User.get_all_activated(session)
    await User.first_to_end_db(actives[0], session)
    if len(actives) % 2:
        i = len(actives) // 2
        extra = actives[i]
        del actives[i]
        await mailing_by_user_tg_id(chat_id=extra.tg_id, text=TEXT_FOR_EXTRA)
        await User.first_to_end_db(extra, session)

    await User.set_is_sent_status_true(actives, session)
    pairs = get_unique_pairs(actives)
    await meeting_mailing(pairs)
