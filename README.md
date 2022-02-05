# Telegram bot with with style transfer

Just send image to the bot and it will sent a stylized image back.

My implementation based on VGG19 convolution network trained on Imagenet dataset with Adam optimizer.

The bot use batch of style image and for each image looking for the most suitable style image. In my implementation I use oil paintings of [wonderful painters.](https://instagram.com/lizplease.art?utm_medium=copy_link) 

You may use your own style images just put its to `styles` folder and run the `style_images_processing.py`. This script returns predictions for each style image and put they to `styles_classes` folder.

## Quick start

For start your owh bot you need to install `requirenments.txt` to your venv and setting up the environment variable `BOT_TOKEN` with your bot token (ask @BotFather).

The next step is generating style images. As I mentioned before you should put their to the `styles` foler and run the `style_images_processing.py` script. Please run it each time after add/remove styles from the folder.

My implementation - @FlydreamBot