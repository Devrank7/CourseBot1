from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from db.psql.enums.enums import Roles
from middleware import MsgMiddleware, CallbackMiddleware

router = Router()
router.message.middleware(MsgMiddleware(roles=[Roles.ADMIN, Roles.STUDENT]))
router.callback_query.middleware(CallbackMiddleware(roles=[Roles.ADMIN, Roles.STUDENT]))

@router.callback_query(F.data.startswith('back_'))
async def back(query: CallbackQuery, state: FSMContext):
    await query.answer()
    index = query.data.split("_")[1]
    data = await state.get_data()
    text_data = data.get(f"bt{index}")
    reply_data = data.get(f"br{index}")
    if query.message.text:
        await query.message.edit_text(text_data, reply_markup=reply_data)
    elif query.message.video or query.message.document or query.message.audio:
        await query.message.delete()
        await query.message.answer(text_data, reply_markup=reply_data)