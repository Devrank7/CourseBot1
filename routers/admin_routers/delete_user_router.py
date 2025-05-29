from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from db.psql.enums.enums import Roles
from db.psql.service import run_sql, UpdateUserRoleByUsername

router = Router()


@router.callback_query(F.data.startswith("delete_user_"))
async def delete_user(query: CallbackQuery):
    username = query.data.split("_")[2]
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="כן", callback_data=f"rem_user_{username}")],
        [InlineKeyboardButton(text="לא", callback_data="back_3")]
    ])
    await query.message.edit_text("האם אתה בטוח?", reply_markup=markup)

@router.callback_query(F.data.startswith("rem_user_"))
async def remove_user(query: CallbackQuery, state: FSMContext):
    username = query.data.split("_")[2]
    await run_sql(UpdateUserRoleByUsername(username, Roles.USER))
    await query.message.edit_text(f"הגישה של המשתמש @{username} לקורסים בוטלה ❌")
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="הוספת משתמש חדש לקורסים 🔑", callback_data="add_user")],
        [InlineKeyboardButton(text="משתמשים עם גישה לקורסים 📝", callback_data="list_users")],
        [InlineKeyboardButton(text="⬅️", callback_data="back_0")]
    ])
    text = ("פאנל ניהול משתמשים 🛡️ \n"
            "בחר פעולה:")
    await state.update_data(bt1=text)
    await state.update_data(br1=markup)
    await query.message.answer(text, reply_markup=markup)