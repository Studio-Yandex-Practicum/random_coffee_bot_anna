from typing import List

from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard(
    *btns: str,
    placeholder: str = None,
    request_contact: int = None,
    request_location: int = None,
    sizes: List[int] = [2],
):
    '''
    Parameters request_contact and request_location must be as indexes
    of btns args for buttons you need.
    Example:
    get_keyboard(
            'О нас',
            'Регистрация',
            'Приостановить общение',
            request_contact=4,
            sizes=(2, 2, 1)
        )
    '''
    keyboard = ReplyKeyboardBuilder()
    for index, text in enumerate(btns, start=0):
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))
    return keyboard.adjust(*sizes).as_markup(
            resize_keyboard=True, input_field_placeholder=placeholder)


MAIN_MENU_KBRD = get_keyboard(
    'О проекте',
    'Наши коллеги про проект «Кофе вслепую»',
    'Приостановить участие',
    'Возобновить участие',
    sizes=[1, 1, 2]
)


ADMIN_KBRD = get_keyboard(
    'Список всех пользователей',
    'Удалить пользователя',
    'Деактивировать пользователя',
    'Главное меню',
    'Добавить пользователя в админы',
    'Удалить пользователя из админов',
    sizes=[2, 2]
)

REGISTER_KBRD = get_keyboard('Регистрация')

NEXT_KBRD = get_keyboard(
    'Следующий комментарий',
    'Главное меню',
    sizes=[2, ]
)

MORE_KBRD = get_keyboard(
    'Ещё комментарий',
    'Главное меню',
    sizes=[2, ]
)
