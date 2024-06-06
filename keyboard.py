from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard():
    # Создание инлайн-кнопки WebApp
    web_app = WebAppInfo(url="https://www.google.com")
    keyboard = InlineKeyboardMarkup()
    who_works = InlineKeyboardButton(text="Кто в работе", web_app=web_app)
    orders = InlineKeyboardButton(text="Заказы", callback_data="orders")
    audit = InlineKeyboardButton(text="Проверка документов", callback_data="audit")
    keyboard.add(orders, audit, who_works)
    return keyboard
