# handlers/common.py
from datetime import date, timedelta
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from config import CHANNEL_ID, CHANNEL_LINK, ADMIN_ID
from keyboards.main_menu import main_menu_keyboard, subscription_keyboard, admin_menu_keyboard
from database.db import user_has_active_booking

router = Router()

async def is_user_subscribed(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception:
        return False

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.clear()
    text = (
        "<b>Привіт!</b>\n\n"
        "Це бот для запису до майстра манікюру 💅\n"
        "Тут ви можете швидко записатися на вільний час, "
        "переглянути свою запис або ознайомитися з прайсом і портфоліо."
    )
    await message.answer(text, reply_markup=main_menu_keyboard())

    if not await is_user_subscribed(bot, message.from_user.id):
        await message.answer(
            "Для запису обов’язково підпишіться на наш канал:",
            reply_markup=subscription_keyboard(CHANNEL_LINK),
        )

@router.callback_query(F.data == "check_subscription")
async def cb_check_subscription(callback: CallbackQuery, bot: Bot) -> None:
    if await is_user_subscribed(bot, callback.from_user.id):
        await callback.message.edit_text(
            "✅ Підписка підтверджена! Тепер ви можете записатися.",
            reply_markup=main_menu_keyboard(),
        )
    else:
        await callback.answer("Ви ще не підписані на канал.", show_alert=True)

@router.callback_query(F.data == "prices")
async def cb_prices(callback: CallbackQuery) -> None:
    text = (
        "<b>Прайс</b>\n\n"
        "Манікюр без покриття — <b>400 грн</b>\n"
        "Манікюр + гель-лак — <b>700 грн</b>"
    )
    await callback.message.answer(text)

@router.callback_query(F.data == "portfolio")
async def cb_portfolio(callback: CallbackQuery) -> None:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Переглянути портфоліо", url="https://www.instagram.com/avetisova_nails/"))
    await callback.message.answer("Ось приклади моїх робіт:", reply_markup=kb.as_markup())

@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас немає доступу до адмін-панелі.")
        return
    await message.answer("<b>Адмін-панель</b>\nОберіть дію:", reply_markup=admin_menu_keyboard())

@router.callback_query(F.data == "my_booking")
async def cb_my_booking(callback: CallbackQuery) -> None:
    slot = await user_has_active_booking(callback.from_user.id)
    if not slot:
        await callback.message.answer("У вас немає активних записів.")
        return
    text = (
        "<b>Ваша запис</b>\n\n"
        f"Дата: <b>{slot['date']}</b>\n"
        f"Час: <b>{slot['time']}</b>\n\n"
        "Щоб скасувати запис, скористайтеся кнопкою нижче."
    )
    await callback.message.answer(text)
