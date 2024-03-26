from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from bot_app.database.models import User
from bot_app.mailing.mailing import mailing_by_user_tg_id, meeting_mailing


TEXT_FOR_EXTRA = """
Привет!На этой неделе в нашем проекте «Кофе вслепую» нечетное количество
участников, поэтому имя коллеги тебе придет на следующей неделе.
Но сейчас не теряй возможность, пригласи на чашечку кофе любого
коллегу и предложи ему присоединиться к нашему проекту
(конечно, если он еще не участвует)!
Отличного дня и продуктивной недели😊
"""


def get_unique_pairs(users: List):
    """Making pairs."""
    return list(zip(users[:len(users)], reversed(users[len(users) // 2:])))


async def distribution(session: AsyncSession):
    """Distribution algorithm."""
    actives = await User.get_all_activated(session)
    if len(actives) > 1:
        await User.first_to_end_db(actives[0], session)
        if len(actives) % 2:
            i = len(actives) // 2
            extra = actives[i]
            del actives[i]
            await mailing_by_user_tg_id(
                chat_id=extra.tg_id, text=TEXT_FOR_EXTRA
            )
            await User.first_to_end_db(extra, session)

        await User.set_is_sent_status_true(actives, session)
        pairs = get_unique_pairs(actives)
        await meeting_mailing(pairs)
