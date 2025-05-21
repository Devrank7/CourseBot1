from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from db.psql.enums.enums import Roles
from db.psql.service import run_sql, ReadUserByUsername, CreateUser, UpdateUserName
from utils.security_util import is_admin

REASON = "Доступ к боту и предоставляемым курсам запрещен 🔒"
class MsgMiddleware(BaseMiddleware):

    def __init__(self, reason: str = REASON, roles: list[Roles] = None):
        if roles is None:
            roles = [Roles.ADMIN]
        self.roles = roles
        self.reason = reason

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        username = event.from_user.username or f"user{event.from_user.id}"
        user = await run_sql(ReadUserByUsername(username))
        if user is None:
            user = await run_sql(
                CreateUser(tg_id=event.from_user.id, username=username, first_name=event.from_user.first_name,
                           last_name=event.from_user.last_name,
                           roles=Roles.ADMIN if is_admin(username) else Roles.USER))
        if user.tg_id == -1:
            user = await run_sql(UpdateUserName(username, tg_id=event.from_user.id, first_name=event.from_user.first_name,
                                         last_name=event.from_user.last_name))
        print("User: ", username)
        if user.roles in self.roles:
            data["user"] = user
            return await handler(event, data)
        await event.answer(self.reason)


class CallbackMiddleware(BaseMiddleware):

    def __init__(self, reason: str = REASON, roles: list[Roles] = None):
        if roles is None:
            roles = [Roles.ADMIN]
        self.roles = roles
        self.reason = reason

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        username = event.from_user.username or f"user{event.from_user.id}"
        user = await run_sql(ReadUserByUsername(username))
        if user is None:
            user = await run_sql(
                CreateUser(tg_id=event.from_user.id, username=username, first_name=event.from_user.first_name,
                           last_name=event.from_user.last_name,
                           roles=Roles.ADMIN if is_admin(username) else Roles.USER))
        if user.tg_id == -1:
            user = await run_sql(UpdateUserName(username, tg_id=event.from_user.id, first_name=event.from_user.first_name,
                                         last_name=event.from_user.last_name))
        print("User: ", username)
        if user.roles in self.roles:
            data["user"] = user
            return await handler(event, data)
        await event.answer(self.reason, show_alert=True)
