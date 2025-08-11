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

# edit_card = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [InlineKeyboardButton(text="👤 Имя", callback_data="edit_full_name")],
#         [InlineKeyboardButton(text="👔 Специализация", callback_data="edit_Specialization")],
#         [InlineKeyboardButton(text="📧 Email", callback_data="edit_email")],
#         [InlineKeyboardButton(text="📍 Местоположение", callback_data="edit_location")],
#         [InlineKeyboardButton(text="🔗 Ссылка", callback_data="edit_add_website")],
#         [InlineKeyboardButton(text="💬 Мессенджер", callback_data="edit_messenger")],
#         [InlineKeyboardButton(text="🖼️ Фото", callback_data="edit_photo")],
#         [InlineKeyboardButton(text="✅ Готово", callback_data="edit_done")],
#     ]
# )

edit_card = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да", callback_data="edit_yes")],
        [InlineKeyboardButton(text="❌ Нет", callback_data="edit_no")],
    ]
)
