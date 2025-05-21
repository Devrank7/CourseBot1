from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

from db.psql.enums.enums import Roles
from db.psql.service import ReadUserByUsername, run_sql, CreateUser, UpdateUserRoleByUsername

router = Router()

class UserToAdd(StatesGroup):
    username = State()

@router.callback_query(F.data == "add_user")
async def add_user(query: CallbackQuery, state: FSMContext):
    await state.set_state(UserToAdd.username)
    await query.message.edit_text("הכנס את שם המשתמש עם @ \n"
                                  "לדוגמה: @abcd1234")

@router.message(UserToAdd.username)
async def add_user(message: Message, state: FSMContext):
    if message.text[0] != "@":
        await message.answer("שם המשתמש שהזנת שגוי ❌\n"
                             "נסה להזין שם משתמש שמתחיל ב-@ \n"
                             "לדוגמה: @abcd1234")
        return
    username = message.text[1:]
    user = await run_sql(ReadUserByUsername(username))
    if user is None:
        await run_sql(CreateUser(tg_id=-1, username=username, roles=Roles.STUDENT))
    else:
        await run_sql(UpdateUserRoleByUsername(username, Roles.STUDENT))
    await state.set_state(None)
    await message.answer(f"גישה לקורסים ניתנה בהצלחה למשתמש @{username} ✅")
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="הוספת משתמש חדש לקורסים 🔑", callback_data="add_user")],
        [InlineKeyboardButton(text="משתמשים עם גישה לקורסים 📝", callback_data="list_users")],
        [InlineKeyboardButton(text="⬅️", callback_data="back_0")]
    ])
    text = ("פאנל ניהול משתמשים 🛡️ \n"
            "בחר פעולה:")
    await state.update_data(bt1=text)
    await state.update_data(br1=markup)
    await message.answer(text, reply_markup=markup)