# keyboards/calendar.py
from datetime import date, timedelta
from typing import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

MONTHS_RU = [
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь",
]


def _month_range(year: int, month: int) -> tuple[date, date]:
    first = date(year, month, 1)
    if month == 12:
        last = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last = date(year, month + 1, 1) - timedelta(days=1)
    return first, last


def calendar_keyboard(
    year: int,
    month: int,
    available_dates: Iterable[str],
    min_date: date,
    max_date: date,
) -> InlineKeyboardMarkup:
    """
    Календарь на месяц. Кликабельны только даты,
    у которых есть свободные слоты (available_dates).
    """
    available_set = {date.fromisoformat(d) for d in available_dates}

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=f"{MONTHS_RU[month - 1]} {year}",
            callback_data="cal_ignore",
        )
    )

    week_days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    builder.row(
        *[
            InlineKeyboardButton(text=d, callback_data="cal_ignore")
            for d in week_days
        ]
    )

    first_day, last_day = _month_range(year, month)
    cur = first_day

    # Сдвиг до первого понедельника
    offset = (cur.weekday())  # 0 = Пн
    row: list[InlineKeyboardButton] = []
    for _ in range(offset):
        row.append(InlineKeyboardButton(text=" ", callback_data="cal_ignore"))

    while cur <= last_day:
        is_in_range = min_date <= cur <= max_date
        if is_in_range and cur in available_set:
            cb_data = f"cal_day:{cur.isoformat()}"
            text = str(cur.day)
        else:
            cb_data = "cal_ignore"
            text = "·"

        row.append(InlineKeyboardButton(text=text, callback_data=cb_data))

        if len(row) == 7:
            builder.row(*row)
            row = []

        cur += timedelta(days=1)

    if row:
        # добиваем пустыми ячейками
        while len(row) < 7:
            row.append(InlineKeyboardButton(text=" ", callback_data="cal_ignore"))
        builder.row(*row)

    # Навигация по месяцам
    this_first, _ = _month_range(year, month)
    prev_month = this_first - timedelta(days=1)
    next_month = last_day + timedelta(days=1)

    # Кнопка "назад"
    buttons_nav = []
    if prev_month >= min_date.replace(day=1):
        buttons_nav.append(
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"cal_prev:{prev_month.year}-{prev_month.month}",
            )
        )
    else:
        buttons_nav.append(
            InlineKeyboardButton(text=" ", callback_data="cal_ignore")
        )

    # Кнопка "вперёд"
    if next_month <= max_date.replace(day=1) + timedelta(days=31):
        buttons_nav.append(
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"cal_next:{next_month.year}-{next_month.month}",
            )
        )
    else:
        buttons_nav.append(
            InlineKeyboardButton(text=" ", callback_data="cal_ignore")
        )

    builder.row(*buttons_nav)
    return builder.as_markup()
