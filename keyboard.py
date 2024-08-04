from aiogram.types import WebAppInfo, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_keyboard():
    # web_app = WebAppInfo(url="https://95.164.0.31/")
    builder = InlineKeyboardBuilder()
    # who_works = InlineKeyboardButton(text="Кто в работе", web_app=web_app)
    who_works = InlineKeyboardButton(text="Кто в работе", url="http://95.164.0.31:6242/")
    orders = InlineKeyboardButton(text="Заказы", callback_data="orders")
    audit = InlineKeyboardButton(text="Проверка документов", callback_data="audit")
    builder.add(orders, audit, who_works)
    return builder
