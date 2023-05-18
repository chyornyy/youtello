import os
import asyncio
from dotenv import load_dotenv
from pytube import YouTube
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, InputFile
from aiogram.utils import exceptions, executor
from aiogram.utils.helper import HelperMode, ListItem
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.message import ContentType

import database as db

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

bot = Bot(BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


REGISTERED_USERS_TABLE = 'registered_users'
METRICS_DATA_TABLE = 'metrics'


class DownloadStates(StatesGroup):
    downloading_video = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_login_data = message.from_user.username
    chat_id_data = f'{message.chat.id}'
    command_type_data = 'start'
    await message.answer(
        'Welcome to the YouTello downloader bot.\n'
        'We hate advertising as much as you do. So there will be no ads. At all.\n\n'
        'Send me a link to a YouTube video and I will download it for you!\n\n'
        '/about - About YouTello\n'
    )
    db.register_user(REGISTERED_USERS_TABLE, user_login_data, chat_id_data)
    db.add_command_data_to_metrics(METRICS_DATA_TABLE, chat_id_data, command_type_data)


@dp.message_handler(commands=['about'])
async def about_command(message: types.Message):
    chat_id_data = f'{message.chat.id}'
    command_type_data = 'about'
    response = "I'm Youtello - a YouTube downloader bot, which allows you to download videos from YouTube in 1080p quality. I don't have any advertising at all. Also i have the potential to support other video platforms like TikTok, Twitter, Instagram Reels, Vimeo, and more that will be added in the near future.\n\nSimply send me a link to the YouTube video that you want to download, and I will take care of the rest!"
    await message.answer(response)
    db.add_command_data_to_metrics(METRICS_DATA_TABLE, chat_id_data, command_type_data)


@dp.message_handler(commands=['ping'])
async def ping_command(message: types.Message):
    await message.reply("pong")


@dp.message_handler(content_types=[ContentType.TEXT])
async def download_video(message: types.Message):
    """
    Check if the user's message contains a link to a valid YouTube video, and start downloading if it does.
    """
    user_login_data = message.from_user.username
    chat_id_data = f'{message.chat.id}'
    command_type_data = 'youtube_download'
    command_type_data_error = 'youtube_download_error'
    url = message.text
    filename = f"{user_login_data}.mp4"
    if "youtube.com" in url or "youtu.be" in url:
        try:
            yt = YouTube(url)
            video = yt.streams.filter(res="720p", file_extension='mp4').first()
            response = f"Downloading...\nTitle: {yt.title}\nPlease wait..."
            progress = types.Message("<code>...</code>").message_id
            progress_message = await message.answer(response, parse_mode=ParseMode.HTML, reply_markup=types.InlineKeyboardMarkup())
            video.download(filename=f'{filename}')
            for i in range(10):
                await asyncio.sleep(1)
                increment = (i + 1) * 10
                try:
                    await bot.edit_message_text(f"{response}\n{'🟩' * i}🟩{'⬜️' * (9 - i)} {increment}%", message_id=progress_message.message_id, chat_id=progress_message.chat.id, parse_mode=ParseMode.HTML, reply_markup=types.InlineKeyboardMarkup())
                except exceptions.MessageNotModified:
                    pass

            caption = f"Here's your video, enjoy!\nTitle: {yt.title}"
            with open(filename, 'rb') as video_file:
                await message.answer_video(video_file.read(), caption=caption)
                video_file.close()
            os.remove(filename)

            await bot.send_message(ADMIN_CHAT_ID, f"Downloaded video for @{user_login_data}")
            db.add_command_data_to_metrics(METRICS_DATA_TABLE,
                                           chat_id_data,
                                           command_type_data)
        except Exception as e:
            await message.answer("Error: " + str(e))
            db.add_command_data_to_metrics(METRICS_DATA_TABLE,
                                           chat_id_data,
                                           command_type_data_error)
    else:
        pass


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
