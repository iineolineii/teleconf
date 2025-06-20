from pyrogram import Client
from teleconf import Config

config = Config(request_api_id=True, request_api_hash=True)

client = Client(
    name="My Pyrogram Client",
    api_id=config.api_id,
    api_hash=config.api_hash,
    bot_token=config.bot_token
)
