from enum import Enum


class ActiveKbrd(str, Enum):
    ABOUT_PROJECT = 'О проекте',
    OUR_COLLEAGUES = 'Наши коллеги про проект «Кофе Bслепую»',
    SUSPEND_PARTICIPATION = 'Приостановить участие',


class DeactivateKbrd(str, Enum):
    ABOUT_PROJECT = 'О проекте',
    OUR_COLLEAGUES = 'Наши коллеги про проект «Кофе Bслепую»',
    RENEW_PARTICIPATION = 'Возобновить участие',


class AdminKbrd(str, Enum):
    LIST = 'Список всех пользователей',
    DELETE = 'Удалить пользователя',
    DEACTIVATE = 'Деактивировать пользователя',
    MAIN_MENU = 'Главное меню',
    ADD_ADMIN = 'Добавить пользователя в админы',
    REMOVE_ADMIN = 'Удалить пользователя из админов',


class Register(str, Enum):
    REGISTRATION = 'Регистрация'


class NextKbrd(str, Enum):
    LISTENING_COMMENT = 'Следующий комментарий',
    MAIN_MENU = 'Главное меню',


class MoreKbrd(str, Enum):
    ANOTHER_COMMENT = 'Ещё комментарий',
    MAIN_MENU = 'Главное меню',


class CancelKbrd(str, Enum):
    CANCELLATION = 'Отмена',
    BACK = 'Назад',


class OnlyKbrd(str, Enum):
    CANCEL = 'Отменить',
