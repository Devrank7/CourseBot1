from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from db.psql.enums.enums import Roles
from db.psql.service import ReadUserByUsername, run_sql, CreateUser, UpdateUserRoleByUsername

router = Router()

class UserToAdd(StatesGroup):
    username = State()

@router.callback_query(F.data == "add_user")
async def add_user(query: CallbackQuery, state: FSMContext):
    await state.set_state(UserToAdd.username)
    await query.message.edit_text("Введите username пользователя c @ \n"
                                  "Пример: @abcd1234")

@router.message(UserToAdd.username)
async def add_user(message: Message, state: FSMContext):
    if message.text[0] != "@":
        await message.answer("Вы ввели не корректное имя пользователя ❌\n"
                             "Попробуйте ввести username пользователя c @ \n"
                                  "Пример: @abcd1234")
        return
    username = message.text[1:]
    user = await run_sql(ReadUserByUsername(username))
    if user is None:
        await run_sql(CreateUser(tg_id=-1, username=username, roles=Roles.STUDENT))
    else:
        await run_sql(UpdateUserRoleByUsername(username, Roles.STUDENT))
    await state.clear()
    await message.answer(f"Пользователю @{username} успешно выдан доступ к курсам ✅")