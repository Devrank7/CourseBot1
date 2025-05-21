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
שלום! 👋
אני בוט שמספק גישה לקורסים להכנה ללידה.

ישנם 3 קורסים זמינים בבוט. ניתן לצפות בהם על ידי לחיצה על הכפתור "הקורסים שלי 📖" או על ידי הזנת הפקודה /courses.

{'''אם אתה מנהל, לניהול משתמשים לחץ על הכפתור "ניהול משתמשים ⚙️" או הזן את הפקודה /admin.

בלוח הניהול תוכל:
– להעניק גישה לקורס לפי שם משתמש  
– לבטל גישה לקורס  
– לצפות ברשימת המשתמשים עם גישה ולקבל מידע עליהם

🪶 הערה:
כדי לחזור לתפריט הראשי, הזן /start — זה עשוי לעזור אם אתה נתקע בניווט.''' if is_admin else ''}

{"צפייה מהנה בכל הקורסים! 💻🤰🏼" if not is_admin else "צפייה וניהול גישה מהנים לקורסים! 💻⚙️"}
'''


@router.message(CommandStart())
async def start(message: Message, user: User, state: FSMContext):
    await state.clear()
    buttons = InlineKeyboardBuilder()
    if user.roles == Roles.ADMIN:
        buttons.button(text="ניהול משתמשים ⚙️", callback_data="admin_manage")
    buttons.row(InlineKeyboardButton(text="הקורסים שלי 📖", callback_data="courses"))
    markup = buttons.as_markup()
    text = get_text(user.roles == Roles.ADMIN)
    await state.update_data(bt0=text)
    await state.update_data(br0=markup)
    await message.answer(text, reply_markup=markup)
