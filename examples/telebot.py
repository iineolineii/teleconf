import telebot
from teleconf import Config

config = Config(request_bot_token=True)

bot = telebot.TeleBot(config.bot_token)