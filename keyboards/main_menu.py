# keyboards/main_menu.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Главное меню для пользователя."""
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text="📅 Записаться", callback_data="book_start"),
    )
    kb.row(
        InlineKeyboardButton(text="🗓 Моя запись", callback_data="my_booking"),
    )
    kb.row(
        InlineKeyboardButton(text="💅 Прайсы", callback_data="prices"),
    )
    kb.row(
        InlineKeyboardButton(text="📷 Портфолио", callback_data="portfolio"),
    )
    return kb.as_markup()


def subscription_keyboard(channel_link: str) -> InlineKeyboardMarkup:
    """Кнопки для проверки подписки."""
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text="Подписаться",
            url=channel_link,
        )
    )
    kb.row(
        InlineKeyboardButton(
            text="Проверить подписку",
            callback_data="check_subscription",
        )
    )
    return kb.as_markup()


def admin_menu_keyboard() -> InlineKeyboardMarkup:
    """Инлайн-меню администратора."""
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text="➕ Добавить рабочий день",
            callback_data="admin_add_day",
        )
    )
    kb.row(
        InlineKeyboardButton(
            text="➕ Добавить слот",
            callback_data="admin_add_slot",
        )
    )
    kb.row(
        InlineKeyboardButton(
            text="➖ Удалить слот",
            callback_data="admin_remove_slot",
        )
    )
    kb.row(
        InlineKeyboardButton(
            text="❌ Отменить запись клиента",
            callback_data="admin_cancel_client",
        )
    )
    kb.row(
        InlineKeyboardButton(
            text="🚫 Закрыть день",
            callback_data="admin_close_day",
        )
    )
    kb.row(
        InlineKeyboardButton(
            text="🔍 Расписание на дату",
            callback_data="admin_view_day",
        )
    )
    return kb.as_markup()
