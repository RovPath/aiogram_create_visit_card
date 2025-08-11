from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.state import Create_Visit
import app.keyboards as kb
from app.handlers.create_handlers import user_cards

router = Router()


@router.message(F.text == "Изменить визитную карточку")
async def edit_cards(message: Message):
    user_id = message.from_user.id
    if user_id not in user_cards:
        await message.answer("❌ Вы ещё не создали карточку.")
        return
    text = "Вы уверны что хотите изменить визитную карточку?"
    await message.answer(text=text, reply_markup=kb.edit_card)


@router.callback_query(F.data == "edit_yes")
async def edit_confirm(callback: CallbackQuery, state: FSMContext):
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
    await callback.message.answer(text, parse_mode="HTML")


@router.callback_query(F.data == "edit_no")
async def edit_cancel(callback: CallbackQuery):
    await callback.message.answer("❌ Изменение отменено")
