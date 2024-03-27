from typing import Iterable, List

from sqlalchemy.ext.asyncio import AsyncSession

from bot_app.database.models import User


def get_unique_pairs(users: Iterable) -> List[tuple]:
    """Making pairs."""
    return list(
        zip(users[:len(users) // 2], reversed(users[len(users) // 2:]))
    )


async def distribute_pairs(session: AsyncSession) -> dict:
    """Distributes pairs of users.."""
    actives = await User.get_all_activated(session)
    if actives:
        await User.first_to_end_db(actives[0], session)
    if not len(actives) % 2:
        return {'pairs': get_unique_pairs(actives)}
    no_pair = actives.pop(len(actives) // 2)
    await User.first_to_end_db(no_pair, session)
    return {'pairs': get_unique_pairs(actives), 'no_pair': no_pair}
