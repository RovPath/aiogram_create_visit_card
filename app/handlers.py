from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.state import Create_Visit

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("test", reply_markup=kb.main_non_reg)


@router.message(F.text == "Создать визитную карточку")
async def F1_create_visit(message: Message, state: FSMContext):
    text = (
        "🧾 <b>Шаг 1 из 8</b>\n"
        "👤 <b>Ваше имя и фамилия</b>\n"
        "\n"
        "Пожалуйста, напишите ваше полное имя и фамилию.\n"
        "Это будет отображаться в вашей визитной карточке.\n"
        "\n"
        "📌 <i>Пример:</i> <code>Иван Иванов</code>"
    )
    await state.set_state(Create_Visit.full_name)
    await message.answer(text, parse_mode="HTML")


@router.message(Create_Visit.full_name, F.text)
async def F2_create_visit(message: Message, state: FSMContext):
    text = (
        "🧾 <b>Шаг 2 из 8</b>\n"
        "👔 <b>Ваша должность</b>\n"
        "\n"
        "Введите вашу специализацию или должность.\n"
        "Она будет указана в вашей карточке.\n"
        "\n"
        "📌 <i>Пример:</i> <code>Программист</code>"
    )
    await state.update_data(full_name=message.text)
    await state.set_state(Create_Visit.Specialization)
    await message.answer(text, parse_mode="HTML")


@router.message(Create_Visit.Specialization, F.text)
async def F3_create_visit(message: Message, state: FSMContext):
    text = (
        "🧾 <b>Шаг 3 из 8</b>\n"
        "📧 <b>Ваш email для связи</b>\n"
        "\n"
        "Пожалуйста, укажите ваш email.\n"
        "На него смогут писать потенциальные клиенты или коллеги.\n"
        "\n"
        "📌 <i>Пример:</i> <code>ivanov@example.com</code>"
    )
    await state.update_data(Specialization=message.text)
    await state.set_state(Create_Visit.email)
    await message.answer(text, parse_mode="HTML")


@router.message(Create_Visit.email, F.text)
async def F4_create_visit(message: Message, state: FSMContext):
    text = (
        "🧾 <b>Шаг 4 из 8</b>\n"
        "📍 <b>Ваш город и страна</b>\n"
        "\n"
        "Укажите ваш город и страну проживания.\n"
        "Это поможет лучше понять ваше местоположение.\n"
        "Если вы не хотите указывать — нажмите «Пропустить».\n"
        "\n"
        "📌 <i>Пример:</i> <code>Москва, Россия</code>"
    )
    await state.update_data(email=message.text)
    await state.set_state(Create_Visit.location)
    await message.answer(text, parse_mode="HTML", reply_markup=kb.skip_keyboard_location)


@router.message(Create_Visit.location, F.text & ~F.text.startswith("⬅️ Пропустить"))
async def F4_create_visit_location(message: Message, state: FSMContext):
    text = (
        "🧾 <b>Шаг 5 из 8</b>\n"
        "🔗 <b>Добавьте ссылку для связи</b>\n"
        "\n"
        "Выберите из популярных платформ ниже,\n"
        "или укажите свою ссылку в следующем шаге.\n"
        "Если не нужно — нажмите «Пропустить»."
    )
    await state.update_data(location=message.text)
    await state.set_state(Create_Visit.add_website)
    await message.answer(text, parse_mode="HTML", reply_markup=kb.website_keyboard())


@router.callback_query(F.data == "skip_location", Create_Visit.location)
async def F5_create_visit(callback: CallbackQuery, state: FSMContext):
    text = (
        "🧾 <b>Шаг 5 из 8</b>\n"
        "🔗 <b>Добавьте ссылку для связи</b>\n"
        "\n"
        "Выберите из популярных платформ ниже,\n"
        "или укажите свою ссылку в следующем шаге.\n"
        "Если не нужно — нажмите «Пропустить»."
    )
    await state.update_data(location=None)
    await state.set_state(Create_Visit.add_website)
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=kb.website_keyboard())
    await callback.answer()


@router.callback_query(F.data == "skip_website", Create_Visit.add_website)
async def F6_skip_website(callback: CallbackQuery, state: FSMContext):
    text = (
        "💬 <b>Шаг 6 из 8</b>\n"
        "<b>Ваш мессенджер для связи</b>\n\n"
        "Введите ваш Telegram-никнейм (с @) или любой другой мессенджер.\n"
        "Он будет использоваться для связи с вами.\n\n"
        "📌 <i>Пример:</i> <code>@ivanov</code>"
    )

    await state.update_data(add_website=None)
    await state.set_state(Create_Visit.messenger)

    await callback.answer()
    await callback.message.edit_text(text, parse_mode="HTML", disable_web_page_preview=True)


@router.callback_query(F.data.startswith("site_"), Create_Visit.add_website)
async def F6_create_visit(callback: CallbackQuery, state: FSMContext):
    data = callback.data

    if data == "site_other":
        text = (
            "🖋️ <b>Название платформы</b>\n\n"
            "Пожалуйста, напишите название платформы, на которую хотите добавить ссылку.\n"
            "Например: <code>ВКонтакте</code>, <code>Telegram</code>, <code>Discord</code> и т.п."
        )
        await state.set_state(Create_Visit.custom_website_name)

    else:
        website_name = data.replace("site_", "").capitalize()
        await state.update_data(add_website=website_name)
        await state.set_state(Create_Visit.custom_website_link)

        text = (
            f"🔗 <b>Ссылка на профиль</b>\n\n"
            f"Теперь введите ссылку на ваш профиль на платформе:\n"
            f"<b>{website_name}</b>"
        )

    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.answer()


# --- Ввод названия кастомной платформы ---
@router.message(Create_Visit.custom_website_name, F.text)
async def process_custom_website_name(message: Message, state: FSMContext):
    await state.update_data(custom_website_name=message.text)
    await state.set_state(Create_Visit.custom_website_link)

    text = "🔗 <b>Ссылка на профиль</b>\n\n" "Теперь введите ссылку на ваш профиль на этой платформе."
    await message.answer(text, parse_mode="HTML")


@router.message(Create_Visit.custom_website_link, F.text)
async def process_custom_website_link(message: Message, state: FSMContext):
    data = await state.get_data()

    if "custom_website_name" in data:
        website_name = data["custom_website_name"]
        link = message.text.strip()
        final_value = f"{website_name} ({link})"
    else:
        website_name = data["add_website"]
        link = message.text.strip()
        final_value = f"{website_name}: {link}"

    await state.update_data(add_website=final_value)
    await state.set_state(Create_Visit.messenger)

    text = (
        "💬 <b>Шаг 6 из 8</b>\n"
        "<b>Ваш мессенджер для связи</b>\n\n"
        "Введите ваш Telegram-никнейм (с @) или любой другой мессенджер.\n"
        "Он будет использоваться для связи с вами.\n\n"
        "📌 <i>Пример:</i> <code>@ivanov</code>"
    )
    await message.answer(text, parse_mode="HTML")


@router.message(Create_Visit.messenger, F.text)
async def F7_create_visit(message: Message, state: FSMContext):
    text = (
        "📸 <b>Шаг 7 из 8</b>\n"
        "🖼️ <b>Добавьте своё фото</b>\n\n"
        "Пожалуйста, загрузите своё фото — лучше всего подойдёт портретное изображение.\n"
        "Оно будет отображаться в вашей визитной карточке.\n\n"
        "Если не хотите добавлять фото — нажмите «Пропустить»."
    )
    await state.update_data(messenger=message.text)
    await state.set_state(Create_Visit.photo)
    await message.answer(text, parse_mode="HTML")


@router.message(Create_Visit.photo, F.photo)
async def F8_create_visit(message: Message, state: FSMContext):
    text = "Подтвердить?"
    await state.update_data(photo=message.photo)
    await message.answer(text, reply_markup=kb.confirm_keyboard)
    await state.clear()
