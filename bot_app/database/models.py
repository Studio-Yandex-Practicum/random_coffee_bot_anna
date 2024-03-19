from sqlalchemy import (Boolean, CheckConstraint, ForeignKey, Integer, String,
                        select, UniqueConstraint)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column)


MEETING = (
    'id: {id}, пользователь_1: {user_1} - пользователь_2: {user_2}'
)
USER = ('id пользователя: {id}, имя: {name}, '
        'фамилия: {last_name}, email: {email}, '
        'участвует: {is_active}, '
        'tg_id: {tg_id}, '
        'is_admin: {is_admin}')


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

    def __repr__(self):
        return USER.format(
            id=self.id,
            name=self.name,
            last_name=self.last_name,
            email=self.email,
            is_active=self.is_active,
            tg_id=self.tg_id,
            is_admin=self.is_admin,
        )

    @staticmethod
    async def create(session: AsyncSession, data: dict):
        """Создать объект."""
        session.add(User(**data))
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
    async def get_first(session: AsyncSession):
        """Получить первый объект."""
        users = await session.execute(select(User).limit(1))
        return users.scalars().one_or_none()
    
    @staticmethod
    async def active_tg(session: AsyncSession):
        """Получить tg_id всех активных пользователей."""
        users = await session.execute(
            select(User.tg_id).where(User.is_active == True)
        )
        return users.scalars().all()


class Meeting(Base):
    __table_args__ = (
        UniqueConstraint('user_1', 'user_1'),
        CheckConstraint('user_1 != user_2')
    )

    user_1: Mapped[int] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE'), nullable=False
    )
    user_2: Mapped[int] = mapped_column(ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False
    )

    def __repr__(self):
        return MEETING.format(
            id=self.id,
            user_1=self.user_1,
            user_2=self.user_2,
        )


user = User()
