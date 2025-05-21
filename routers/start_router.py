from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.psql.enums.enums import Roles
from db.psql.models import User
from middleware import MsgMiddleware, CallbackMiddleware

router = Router()
router.message.middleware(MsgMiddleware(roles=[Roles.ADMIN, Roles.STUDENT]))
router.callback_query.middleware(CallbackMiddleware(roles=[Roles.ADMIN, Roles.STUDENT]))


def get_text(is_admin: bool):
    return f'''
Привет! 👋
Я бот, предоставляющий доступ к курсам по подготовке к родам.

В боте доступны 3 курса. Вы можете просмотреть их, нажав на кнопку "Мои курсы 📖" или введя команду /courses.

{'''Если вы администратор, для управления пользователями нажмите кнопку "Управление пользователями ⚙️" или введите команду /admin.

В панели управления вы можете:
– Выдать доступ к курсу по username  
– Отозвать доступ к курсу  
– Просмотреть список пользователей с доступом и информацию о них

🪶 Примечание:
Чтобы вернуться в главное меню, введите /start — это может помочь, если вы застряли в навигации.''' if is_admin else ''}

{"Приятного просмотра всех курсов! 💻🤰🏼" if not is_admin else "Приятного просмотра и управления доступами к курсам! 💻⚙️"}
'''


@router.message(CommandStart())
async def start(message: Message, user: User, state: FSMContext):
    await state.clear()
    buttons = InlineKeyboardBuilder()
    if user.roles == Roles.ADMIN:
        buttons.button(text="Управление пользователями ⚙️", callback_data="admin_manage")
    buttons.row(InlineKeyboardButton(text="Мои курсы 📖", callback_data="courses"))
    markup = buttons.as_markup()
    text = get_text(user.roles == Roles.ADMIN)
    await state.update_data(bt0=text)
    await state.update_data(br0=markup)
    await message.answer(text, reply_markup=markup)
