from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


def get_unique_pairs(users: list):
    return set(zip(users[:len(users)], reversed(users[len(users) // 2:])))


async def send_message(no_pair):
    # Функция отправки сообщения
    pass


async def distribution(session: AsyncSession):
    await User.rewrite(session, await User.first_active(session))
    participating = await User.get_all_activated(session)
    if len(participating) % 2:
        no_pair = len(participating // 2)
        await User.rewrite(session, participating[no_pair])
        await send_message(no_pair)
    return get_unique_pairs(participating)
