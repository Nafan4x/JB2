import asyncio
import signal
from vkbottle.bot import Bot, Message
from vkbottle.tools import PhotoMessageUploader
from db.db import Database
from logic.main import handle_message
from fsm import FSM
import sys

from dotenv import load_dotenv
import os

load_dotenv()  # по умолчанию ищет .env в текущей папке

vk_token = os.getenv("VK_TOKEN")
db_host = os.getenv("DB_HOST")

bot = Bot(token=vk_token)
uploader = PhotoMessageUploader(bot.api)
db = Database(dsn=db_host)

user_fsms = {}


@bot.on.message(text="/start")
async def start_handler(message: Message):
    user_id = message.from_id
    fsm = user_fsms.get(user_id)
    if not fsm:
        fsm = FSM(user_id, db)
        await fsm.load_state()
        user_fsms[user_id] = fsm
    response = await handle_message(fsm, "/start")
    await message.answer(
        response["text"],
        keyboard=response.get("keyboard"),
        attachment=response.get("photos"),
    )


@bot.on.message()
async def message_handler(message: Message):
    user_id = message.from_id
    fsm = user_fsms.get(user_id)
    if not fsm:
        fsm = FSM(user_id, db)
        await fsm.load_state()
        user_fsms[user_id] = fsm

    response = await handle_message(fsm, message.text)
    attachment = None
    if response.get("photos"):
        attachment = await upload_many_photos(user_id, response.get("photos"))

    await message.answer(
        response["text"],
        keyboard=response.get("keyboard"),
        attachment=attachment,
    )


async def startup():
    await db.connect()
    await db.create_tables()


async def upload_many_photos(user_id, paths):
    attachments = []
    for path in paths:
        photo = await uploader.upload(file_source=path, peer_id=user_id)
        attachments.append(photo)
    return attachments


async def shutdown():
    await db.close()


def main():
    if sys.version_info >= (3, 10):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()
    loop.run_until_complete(startup())

    try:
        bot.run_forever()  # запускает цикл событий самостоятельно
    finally:
        # Закрываем соединение после остановки бота
        loop.run_until_complete(shutdown())
        loop.close()


if __name__ == "__main__":
    main()
