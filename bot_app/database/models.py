from core.config import settings
from sqlalchemy import (Boolean, CheckConstraint, ForeignKey, Integer, String,
                        UniqueConstraint, select)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column)

USER = ('{name} '
        '{last_name}\n'
        '{email}\n'
        '{tg_id}\n'
        '{is_active}'
        '{is_admin}\n')


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False
    )

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class User(Base):

    tg_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True
    )
    name: Mapped[str] = mapped_column(
        String(150), nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(150), nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(150), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    is_sent: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    def __repr__(self):
        is_admin_text = ', админ' if self.is_admin else ''
        is_active_text = 'активен' if self.is_active else 'неактивен'
        return USER.format(
            id=self.id,
            name=self.name,
            last_name=self.last_name,
            email=self.email,
            is_active=is_active_text,
            tg_id=self.tg_id,
            is_admin=is_admin_text,
        )

    @staticmethod
    async def create(session: AsyncSession, data: dict):
        """Создать объект."""
        session.add(User(**data))
        result = await session.execute(
            select(User).filter(User.tg_id == settings.gen_admin_id)
        )
        obj = result.scalars().one_or_none()
        if obj:
            obj.is_admin = True
        await session.commit()

    @staticmethod
    async def remove(session: AsyncSession, db_obj):
        """Удалить объект."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    @staticmethod
    async def get(session: AsyncSession, tg_id: int):
        """Получение объекта по tg_id"""
        db_obj = await session.execute(select(User).where(User.tg_id == tg_id))
        return db_obj.scalars().one_or_none()

    @staticmethod
    async def get_all(session: AsyncSession):
        """Получение всех объектов."""
        users = await session.execute(select(User))
        return users.scalars().all()

    @staticmethod
    async def activate_deactivate_user(session: AsyncSession, tg_id: int):
        """Активировать/деактивировать объект."""
        result = await session.execute(
            select(User).filter(User.tg_id == tg_id)
        )
        obj = result.scalars().one_or_none()
        if obj:
            obj.is_active = not obj.is_active
            await session.commit()
            return True
        return False

    @staticmethod
    async def get_all_activated(session: AsyncSession):
        """Получение всех активных объектов."""
        result = await session.execute(select(User).filter(User.is_active == 1))
        return result.scalars().all()

    @staticmethod
    async def get_all_is_sent(session: AsyncSession):
        """Получение всех обеъектов, кому сделана рассылка."""
        result = await session.execute(select(User).filter(User.is_sent == 1))
        return result.scalars().all()


user = User()
