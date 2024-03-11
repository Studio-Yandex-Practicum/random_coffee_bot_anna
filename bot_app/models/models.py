from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column, relationship)

MEETING = (
    'id: {id}, пользователь_1: {user_1} - пользователь_2: {user_2}'
)
USER = ('id пользователя: {user_id}, имя: {full_amount}, '
        'фамилия: {invested_amount}, email: {fully_invested}, '
        'участвует: {available}')


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class User(Base):
    user_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(13), nullable=False, unique=True)
    available: Mapped[bool] = mapped_column(default=True)

    def __repr__(self):
        return USER.format(
            user_id=self.user_id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            available=self.available
        )


class Meeting(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_1: Mapped[int] = mapped_column(
        ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False
    )
    user_2: Mapped[int] = mapped_column(ForeignKey(
        'user.user_id', ondelete='CASCADE'), nullable=False
    )
    meeting: Mapped['User'] = relationship(backref='meeting')

    def __repr__(self):
        return MEETING.format(
            id=self.id,
            user_1=self.user_1,
            user_2=self.user_2,
        )
