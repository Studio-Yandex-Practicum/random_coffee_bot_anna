from database.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def orm_add_user(session: AsyncSession, data: dict):
    obj = User(
        tg_id=data["tg_id"],
        name=data["name"],
        last_name=data["last_name"],
        email=data["email"],
    )
    session.add(obj)
    await session.commit()


async def orm_delete_user(session: AsyncSession, tg_id: int):
    result = await session.execute(select(User).filter(User.tg_id == tg_id))
    user = result.scalars().one_or_none()
    if user:
        await session.delete(user)
        await session.commit()
        return True
    else:
        return False


async def orm_get_all(session: AsyncSession):
    result = await session.execute(select(User))
    return result.scalars().all()


async def activate_deactivate_user(session: AsyncSession, tg_id: int):
    result = await session.execute(select(User).filter(User.tg_id == tg_id))
    user = result.scalars().one_or_none()
    if user:
        user.is_active = not user.is_active
        await session.commit()
        return True
    return False


async def get_user_by_id(session: AsyncSession, tg_id: int):
    result = await session.execute(select(User).filter(User.tg_id == tg_id))
    user = result.scalars().one_or_none()
    if user:
        return True
    else:
        return False
