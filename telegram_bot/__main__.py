import logging
import os
from aiogram import *
from telegram_bot.image_processing.style_transfer import apply_style
from telegram_bot.image_processing.style_images_processing import match_style_image
import pathlib

local_path = pathlib.Path().resolve()
styles_path = pathlib.Path().resolve() / 'styles'
# Configure logging
logging.basicConfig(
    filename="../app.log",
    format="%(levelname)-10s %(asctime)s %(message)s",
    level=logging.INFO
)
# Initialize bot and dispatcher
bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(content_types=['photo'])
async def apply_new_style(message: types.Message):
    await message.photo[-1].download('test.jpg')
    logging.info(f'Start image processing content image downloaded')
    image_path = local_path / 'test.jpg'
    logging.info(f'Generate image path {image_path}')
    style_image_name = match_style_image(str(image_path))
    style_image = str(styles_path) + '\\' + style_image_name
    logging.info(f'Image processing completed with style {style_image}')
    image_path = str(image_path)
    with apply_style(image_path, style_image) as photo:
        await message.reply_photo(photo, caption='New shiny image with applied style')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
