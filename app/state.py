from aiogram.fsm.state import State, StatesGroup


class Create_Visit(StatesGroup):
    full_name = State()
    Specialization = State()
    email = State()
    location = State()
    add_website = State()
    custom_website_name = State()
    custom_website_link = State()
    messenger = State()
    photo = State()
