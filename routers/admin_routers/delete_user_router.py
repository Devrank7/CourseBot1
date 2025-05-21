from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from db.psql.enums.enums import Roles
from db.psql.service import run_sql, UpdateUserRoleByUsername

router = Router()


@router.callback_query(F.data.startswith("delete_user_"))
async def delete_user(query: CallbackQuery):
    username = query.data.split("_")[2]
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data=f"rem_user_{username}")],
        [InlineKeyboardButton(text="Нет", callback_data="back_3")]
    ])
    await query.message.edit_text("Вы уверены?", reply_markup=markup)

@router.callback_query(F.data.startswith("rem_user_"))
async def remove_user(query: CallbackQuery):
    username = query.data.split("_")[2]
    await run_sql(UpdateUserRoleByUsername(username, Roles.USER))
    await query.message.edit_text(f"Пользователь @{username} больше не имеет доступа к вашим курсам ❌")