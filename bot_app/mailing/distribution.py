from typing import List
from sqlalchemy.orm.session import make_transient
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import user


async def mees_for_extra(user):
    pass


async def change_is_sent_status_true(users: List, session: AsyncSession):
    if users:
        for sent in users:
            sent.is_sent = True
        await session.commit()


async def change_is_sent_status_false(users: List, session: AsyncSession):
    if users:
        for sent in users:
            sent.is_sent = False
        await session.commit()


def get_unique_pairs(users: List):
    return list(zip(users[:len(users)], reversed(users[len(users) // 2:])))


async def moving_objects_database(session: AsyncSession):
    """Перемешиваем список пользователей."""
    obj = user.get_first_active(session)
    # метод
    # await user.remove(session, obj) перенести в модель
    # obj.id = None
    # session.expunge(obj)
    # make_transient(obj)
    # session.add(obj)
    await session.commit()


async def distribution(session):
    await moving_objects_database(session)
    actives = await user.get_all_activated(session)
    if len(actives) % 2:
        i = len(actives) // 2
        extra = actives[i]
        mees_for_extra(extra)
        # метод
        change_is_sent_status_true(actives, session)
        return get_unique_pairs(actives)
    change_is_sent_status_true(actives, session)
    return get_unique_pairs(actives)
