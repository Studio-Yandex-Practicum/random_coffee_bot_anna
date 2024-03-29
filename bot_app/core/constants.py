from enum import Enum, IntEnum


class MailingInt(IntEnum):
    MAIL_TO_COUPLES_HOUR = 10
    MAIL_TO_COUPLES_MIN = 00
    REMIND_MAIL_HOUR = 10
    REMIND_MAIL_MIN = 00


class MailingStr(str, Enum):
    TRIGGER = 'cron'
    MAIL_TO_COUPLES_DAY = 'mon'
    REMIND_MAIL_DAY = 'thu'


class Timezone(str, Enum):
    TIMEZONE_MOSCOW = 'Europe/Moscow'


class Messages(str, Enum):
    START_UP_MSG = 'Бот запущен'
    SHUT_DOWN_MSG = 'Бот лег'
    ERROR_MSG_FOR_USER = 'Извините, я сломался :( Но меня уже чинят!'
    GARBAGE_MSG = 'Извините, я вас не понимаю. Воспользуйтесь кнопками меню.'

    def __str__(self) -> str:
        return str.__str__(self)


class Commands(str, Enum):
    BOT_RESTART = 'Перезапустить бота'
    ADMIN_PANEL = 'Панель администратора'
    HELP = 'Помощь'
