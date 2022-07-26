from aiogram import types
from aiogram.dispatcher import FSMContext

from app.models import TelegramUser
from bot.config.loader import bot, user_data
from bot.data import text_data as td
from bot.keyboards import inline as ik
from bot.states import UserRegistration
from bot.services.db import user as user_db
from bot.utils.deleter import delete_user_message
from bot.utils.state_worker import get_info_from_state


async def start_client(call: types.CallbackQuery, state: FSMContext):
    await get_panel(call.message, state)


async def start_register_client(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]
    user_id = call.message.chat.id
    if action == "1":
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=user_data[user_id]["last_bot_sent_message"],
            text=td.GET_SEX,
            reply_markup=await ik.gender()
        )
    elif action == "2":
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=user_data[user_id]["last_bot_sent_message"],
            text=td.GET_NAME
        )
        await UserRegistration.fio.set()

    elif action == "3":
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=user_data[user_id]["last_bot_sent_message"],
            text=td.GET_AGE
        )
        await UserRegistration.age.set()

    elif action == "4":
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=user_data[user_id]["last_bot_sent_message"],
            text=td.GET_EDUCATION
        )
        await UserRegistration.education.set()
    elif action == "5":
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=user_data[user_id]["last_bot_sent_message"],
            text=td.GET_SKILL
        )
        await UserRegistration.skill.set()
    else:
        await state.finish()
        await confirm_data(call)


async def get_sex(call: types.CallbackQuery, state: FSMContext):
    sex_data = call.data.replace("sex_", "")
    sex = "М" if sex_data == "m" else "Ж"
    await state.update_data({"sex": sex})
    await get_panel(call.message, state)


async def get_age(message: types.Message, state: FSMContext):
    age = message.text
    user_data[message.chat.id].update({"age": age})
    await delete_user_message(message)
    await get_panel(message, state)


async def get_fio(message: types.Message, state: FSMContext):
    fio = message.text
    await state.update_data({"fio": fio})
    await delete_user_message(message=message)
    await get_panel(message, state)


async def get_education(call: types.CallbackQuery, state: FSMContext):
    education_data = call.data.replace("edu_", "")
    await state.update_data({"education_data": education_data})
    await get_panel(call.message, state)


async def get_skill(call: types.CallbackQuery, state: FSMContext):
    lvl = call.data.replace("lvl_", "")
    await state.update_data({"lvl": lvl})
    await get_panel(call.message, state)


async def get_panel(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    tg_user: TelegramUser = await user_db.get_user(user_id=user_id)
    data = await state.get_data()
    mes_id = data.get('main_menu')
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=mes_id,
        text=td.CLIENT_REG_MENU.format(
            name=tg_user.name,
            fio=await get_info_from_state(data, "fio"),
            gender=await get_info_from_state(data, key="sex"),
            education=await get_info_from_state(data, key="education"),
            skill=await get_info_from_state(data, key="skill"),
            age=await get_info_from_state(data, key="age"),
        ),
        reply_markup=await ik.setup_client(data)
    )
    await UserRegistration.registration.set()


async def confirm_data(call: types.CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    data = await state.get_data()
    tg_user: TelegramUser = await user_db.get_user(user_id=user_id)
    fio = await get_info_from_state(data, "fio"),
    gender = await get_info_from_state(data, key="sex")
    education = await get_info_from_state(data, key="education")
    skill = await get_info_from_state(data, key="skill")
    age = await get_info_from_state(data, key="age")

    await client.add_client(user=tg_user, gender=gender, height=height, weight=weight, age=age, ims=ims)
    await client_act_menu(call=call)


async def client_act_menu(call: types.CallbackQuery):
    user_id = call.message.chat.id
    tg_user: TelegramUser = await telegram_user.select_user(user_id=user_id)
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=td.CLIENT_PROFILE.format(name=tg_user.name),
        reply_markup=await ik.client_actions()
    )
