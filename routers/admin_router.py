from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message

from middleware import MsgMiddleware, CallbackMiddleware
from routers.admin_routers import add_user_router, delete_user_router, list_users_router

router = Router()
router.include_router(add_user_router.router)
router.include_router(delete_user_router.router)
router.include_router(list_users_router.router)
reason = "Вам доступ к админ панели запрещен 🔒"
router.message.middleware(MsgMiddleware(reason=reason))
router.callback_query.middleware(CallbackMiddleware(reason=reason))


@router.message(Command("admin"))
async def admin(message: Message, state: FSMContext):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить нового пользователя к курсам 🔑", callback_data="add_user")],
        [InlineKeyboardButton(text="Пользователи с доступом к курсам 📝", callback_data="list_users")],
    ])
    text = ("Административная панель по управлению пользователями 🛡️ \n"
            "Выберите действие: ")
    await state.update_data(bt1=text)
    await state.update_data(br1=markup)
    await message.answer(text, reply_markup=markup)


@router.callback_query(F.data == "admin_manage")
async def admin_manage(query: CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить пользователя 🔑", callback_data="add_user")],
        [InlineKeyboardButton(text="Пользователи с доступом к курсам 📝", callback_data="list_users")],
        [InlineKeyboardButton(text="⬅️", callback_data="back_0")]
    ])
    text = ("Административная панель по управлению пользователями 🛡️ \n"
            "Выберите действие: ")
    await state.update_data(bt1=text)
    await state.update_data(br1=markup)
    await query.message.edit_text(text, reply_markup=markup)
