from aiogram.types import WebAppInfo, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_keyboard():
    web_app = WebAppInfo(url="https://www.google.com")
    builder = InlineKeyboardBuilder()
    who_works = InlineKeyboardButton(text="Кто в работе", web_app=web_app)
    orders = InlineKeyboardButton(text="Заказы", callback_data="orders")
    audit = InlineKeyboardButton(text="Проверка документов", callback_data="audit")
    builder.add(orders, audit, who_works)
    return builder
