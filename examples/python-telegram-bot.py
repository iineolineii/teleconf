from telegram.ext import Application
from teleconf import Config

config = Config(request_bot_token=True)

application = Application.builder().token(config.bot_token).build()