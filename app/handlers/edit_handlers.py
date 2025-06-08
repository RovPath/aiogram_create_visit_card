from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

# import app.keyboards as kb
# from app.state import Create_Visit

router = Router()


@router.message(F.text == "Изменить визитную карточку")
async def edit_visit_card(message: Message):
    await message.answer("Изменить визитную карточку")
