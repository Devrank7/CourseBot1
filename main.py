import os

from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from db.psql.connect import init_db
from routers import start_router, course_router, back_router, admin_router

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher()

routers = [
    start_router.router,
    course_router.router,
    back_router.router,
    admin_router.router
]


@dispatcher.startup()
async def start():
    await init_db()
    print("Bot started")
@dispatcher.message(F.video)
async def handle_video(message: Message):
    # Получаем объект видео
    video = message.video
    video_file_id = video.file_id
    print("video_file_id: ", video_file_id)
    print("filename: ", video.file_name)
    # Отправляем видео обратно пользователю
    await message.answer_video(video_file_id, caption="Вот твоё видео!")
@dispatcher.message(Command("send"))
async def send(message: Message):
    file_id = 'BAACAgIAAxkBAAMSaC3P8c64okC5E0HNwKbr1_XKEXcAAo11AALbfXBJCFOpMpgAAS13NgQ'
    await message.answer_video(file_id, caption="ВотQQQq твоё видео!")
async def main():
    dispatcher.include_routers(*routers)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
