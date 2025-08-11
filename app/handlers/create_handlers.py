from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.state import Create_Visit

router = Router()

user_cards = {}


@router.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        "👋 <b>Добро пожаловать!</b>\n"
        "📇 <b>Это бот для создания визитных карточек</b>\n"
        "\n"
        "✨ <b>Здесь вы можете заполнить свою визитную карточку и изменять её по своему желанию</b>"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=kb.main_non_reg)


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
async def F5_create_visit(message: Message, state: FSMContext):
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
async def F6_create_visit(callback: CallbackQuery, state: FSMContext):
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
    await message.answer(text, parse_mode="HTML", reply_markup=kb.skip_keyboard_photo)


@router.callback_query(F.data == "skip_photo", Create_Visit.photo)
async def F7_create_visit_skip(callback: CallbackQuery, state: FSMContext):
    await state.update_data(photo=None)
    await state.set_state(Create_Visit.comfirm_bot)

    data = await state.get_data()

    full_name = data.get("full_name", "Не указано")
    specialization = data.get("Specialization", "Не указано")
    email = data.get("email", "Не указано")
    location = data.get("location", "Не указано")
    add_website = data.get("add_website", "Не указано")
    messenger = data.get("messenger", "Не указано")

    card_text = (
        "🪪 <b>Визитная Карточка</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 <b>Имя:</b> <i>{full_name}</i>\n"
        f"👔 <b>Специализация:</b> <i>{specialization}</i>\n"
        f"📧 <b>Email:</b> <code>{email}</code>\n"
    )

    if location != "Не указано":
        card_text += f"\n📍 <b>Местоположение:</b> <i>{location}</i>"

    if add_website != "Не указано":
        card_text += f"\n🔗 <b>Ссылка:</b> <i>{add_website}</i>"

    if messenger != "Не указано":
        card_text += f"\n💬 <b>Мессенджер:</b> <i>{messenger}</i>"
    user_id = callback.from_user.id
    user_cards[user_id] = {"text": card_text, "photo": None, "data": data}

    await callback.message.answer(card_text, parse_mode="HTML", reply_markup=kb.confirm_keyboard)
    await callback.answer("✅ Фото пропущено, карточка создана без фото.")


@router.message(Create_Visit.photo, F.photo)
async def F8_create_visit(message: Message, state: FSMContext):
    text = (
        "✅ <b>Подтверждение данных</b>\n"
        "\n"
        "Пожалуйста, проверьте информацию, которую вы указали.\n"
        "Если всё верно — нажмите «Подтвердить».\n"
        "Если нужно что-то изменить — выберите соответствующий вариант."
    )
    await state.update_data(photo=message.photo)
    await message.answer(text, parse_mode="HTML", reply_markup=kb.confirm_keyboard)


@router.callback_query(F.data == "confirm_continue")
async def create_confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    full_name = data.get("full_name", "Не указано")
    specialization = data.get("Specialization", "Не указано")
    email = data.get("email", "Не указано")
    location = data.get("location", "Не указано")
    add_website = data.get("add_website", "Не указано")
    messenger = data.get("messenger", "Не указано")
    photo = data.get("photo")

    card_text = (
        "🪪 <b>Визитная Карточка</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 <b>Имя:</b> <i>{full_name}</i>\n"
        f"👔 <b>Специализация:</b> <i>{specialization}</i>\n"
        f"📧 <b>Email:</b> <code>{email}</code>\n"
    )

    if location != "Не указано":
        card_text += f"\n📍 <b>Местоположение:</b> <i>{location}</i>"

    if add_website != "Не указано":
        card_text += f"\n🔗 <b>Ссылка:</b> <i>{add_website}</i>"

    if messenger != "Не указано":
        card_text += f"\n💬 <b>Мессенджер:</b> <i>{messenger}</i>"

    user_id = callback.from_user.id
    user_cards[user_id] = {"text": card_text, "photo": photo, "data": data}

    await callback.answer("✅ Карточка успешно создана!")
    await state.clear()


@router.message(F.text == "Моя визитная карточка")
async def savid_visit_card(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in user_cards:
        await message.answer("❌ Вы ещё не создали карточку.")
        return

    card = user_cards[user_id]
    if card.get("photo"):
        await message.answer_photo(photo=card["photo"][-1].file_id, caption=card["text"], parse_mode="HTML")
    else:
        await message.answer(card["text"], parse_mode="HTML")
