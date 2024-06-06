import asyncio
import config
import keyboard
import orders
import audit

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

dp = Dispatcher()
bot = Bot(config.TELEGRAM_TOKEN)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if Message.message_id in config.ID_USERS_LIST:
        await message.answer(f"Бот запущен!")
    else:
        await message.answer(f'У вас нет прав доступа к боту!')


@dp.message(F.text, Command("orders"))
async def orders_handler(message: types.Message) -> None:
    if message.from_user.id in config.ID_USERS_LIST:
        await message.answer('⏳ Получение данных с сервера МойСклад...', parse_mode='HTML',
                             reply_markup=keyboard.get_keyboard())
        try:
            await message.answer(orders.create_orders_answer(), parse_mode='HTML',
                                 reply_markup=keyboard.get_keyboard())
        except Exception as e:
            await message.answer(f'❗️❗️❗⌛️ Время ожидания истекло. Ответ от МойСклад не пришёл. Ошибка{e}',
                                 parse_mode='HTML', reply_markup=keyboard.get_keyboard())
    else:
        await message.answer(f'❗️❗️❗ У вас нет прав доступа к боту!')


@dp.message(F.text, Command("audit"))
async def audit_handler(message: types.Message) -> None:
    if message.from_user.id in config.ID_USERS_LIST:
        await message.answer('⏳ Получение данных с сервера МойСклад...', parse_mode='HTML')
        try:
            await message.answer(audit.create_audit_answer(), parse_mode='HTML',
                                 reply_markup=keyboard.get_keyboard())
        except Exception as e:
            await message.answer(f'❗️❗️❗⌛️ Время ожидания истекло. Ответ от МойСклад не пришёл. Ошибка{e}',
                                 parse_mode='HTML', reply_markup=keyboard.get_keyboard())
    else:
        await message.answer(f'❗️❗️❗ У вас нет прав доступа к боту!')


@dp.callback_query(lambda call: True)
async def process_callback_button(call: types.CallbackQuery):
    if call.data == "audit":
        await bot.answer_callback_query(call.id, text="Получение данных с сервера Мой Склад...")
        await bot.send_message(call.from_user.id, text=audit.create_audit_answer(), parse_mode='HTML',
                               reply_markup=keyboard.get_keyboard())
    elif call.data == "orders":
        await bot.answer_callback_query(call.id, text="Получение данных с сервера Мой Склад...")
        await bot.send_message(call.from_user.id, text=orders.create_orders_answer(), parse_mode='HTML',
                               reply_markup=keyboard.get_keyboard())


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
