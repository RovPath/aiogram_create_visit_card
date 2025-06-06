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

@router