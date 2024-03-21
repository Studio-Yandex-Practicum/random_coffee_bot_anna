from typing import List
from sqlalchemy.orm.session import make_transient
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import user


async def mees_for_extra(user):
    pass


def get_unique_pairs(users: List):
    return list(zip(users[:len(users)], reversed(users[len(users) // 2:])))


async def moving_objects_database(session: AsyncSession):
    """Перемешиваем список пользователей."""
    obj = user.get_first(session)
    await user.remove(session, obj)
    obj.id = None
    session.expunge(obj)
    make_transient(obj)
    session.add(obj)
    await session.commit()


async def distribution(session):
    await moving_objects_database(session)
    actives = await user.get_all_activated(session)
    if len(actives) % 2:
        i = len(actives) // 2
        extra = actives[i]
        mees_for_extra(extra)
        
    return get_unique_pairs()
