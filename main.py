import asyncio
import config
import keyboard
import orders
import audit
import utils

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

dp = Dispatcher()
bot = Bot(config.TELEGRAM_TOKEN)


@dp.message(CommandStart())
@utils.allowed_users_only
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Бот запущен!", reply_markup=keyboard.get_keyboard().as_markup())


@dp.message(F.text, Command("orders"))
@utils.allowed_users_only
async def orders_handler(message: types.Message) -> None:
    await message.answer('⏳ Получение данных с сервера МойСклад...', parse_mode='HTML')
    try:
        await message.answer(orders.create_orders_answer(), parse_mode='HTML',
                             reply_markup=keyboard.get_keyboard().as_markup())
    except Exception as e:
        await message.answer(f'❗️❗️❗ Ошибка: {e}',
                             parse_mode='HTML', reply_markup=keyboard.get_keyboard().as_markup())


@dp.message(F.text, Command("audit"))
@utils.allowed_users_only
async def audit_handler(message: types.Message) -> None:
    await message.answer('⏳ Получение данных с сервера МойСклад...', parse_mode='HTML')
    try:
        await message.answer(audit.create_audit_answer(), parse_mode='HTML',
                             reply_markup=keyboard.get_keyboard().as_markup())
    except Exception as e:
        await message.answer(f'❗️❗️❗ Ошибка: {e}',
                             parse_mode='HTML', reply_markup=keyboard.get_keyboard().as_markup())


@dp.callback_query(lambda call: True)
@utils.allowed_users_only
async def process_callback_button(call: types.CallbackQuery):
    if call.data == "audit":
        await bot.answer_callback_query(call.id, text="Получение данных с сервера Мой Склад...")
        await bot.send_message(call.from_user.id, text=audit.create_audit_answer(), parse_mode='HTML',
                               reply_markup=keyboard.get_keyboard().as_markup())
    elif call.data == "orders":
        await bot.answer_callback_query(call.id, text="Получение данных с сервера Мой Склад...")
        await bot.send_message(call.from_user.id, text=orders.create_orders_answer(), parse_mode='HTML',
                               reply_markup=keyboard.get_keyboard().as_markup())


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
