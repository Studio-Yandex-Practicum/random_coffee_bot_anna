from sqlalchemy import (Boolean, CheckConstraint, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column)


MEETING = (
    'id: {id}, пользователь_1: {user_1} - пользователь_2: {user_2}'
)
USER = ('id пользователя: {user_id}, имя: {first_name}, '
        'фамилия: {last_name}, email: {email}, '
        'участвует: {available}')


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False
    )

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class User(Base):
    # user_id: Mapped[int] = mapped_column(
    #     Integer, primary_key=True, nullable=False
    # )
    tg_id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True
    )
    name: Mapped[str] = mapped_column(
        String(150), nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(150), nullable=False
    )
    mail: Mapped[str] = mapped_column(
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
            user_id=self.user_id,
            first_name=self.last_name,
            last_name=self.last_name,
            email=self.mail,
            available=self.is_active
        )


class Meeting(Base):
    __table_args__ = (
        UniqueConstraint('user_1', 'user_1'),
        CheckConstraint('user_1 != user_2')
    )
    # id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
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
