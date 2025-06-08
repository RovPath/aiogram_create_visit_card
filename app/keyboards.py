from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

main_non_reg = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Моя визитная карточка"), KeyboardButton(text="Создать визитную карточку")],
        [KeyboardButton(text="Изменить визитную карточку")],
    ],
    resize_keyboard=True,
)

skip_keyboard_location = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="❌ Пропустить", callback_data="skip_location")]]
)

skip_keyboard_photo = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="❌ Пропустить", callback_data="skip_photo")]]
)


def website_keyboard():
    websites = [
        ("GitHub", "site_github"),
        ("LinkedIn", "site_linkedin"),
        ("Instagram", "site_instagram"),
        ("Behance", "site_behance"),
        ("Сайт / Личная страница", "site_portfolio"),
        ("Другое", "site_other"),
        ("❌ Пропустить", "skip_website"),
    ]
    keyboard = InlineKeyboardBuilder()
    for text, callback_data in websites:
        keyboard.add(InlineKeyboardButton(text=text, callback_data=callback_data))
    return keyboard.adjust(2).as_markup()


confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_continue")],
        [InlineKeyboardButton(text="🖋️ Изменить", callback_data="confirm_edit")],
    ]
)
