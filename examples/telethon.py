from telethon import TelegramClient
from teleconf import Config

config = Config(request_api_id=True, request_api_hash=True)

client = TelegramClient(
    session="My Telethon Client",
    api_id=config.api_id,
    api_hash=config.api_hash
)

await client.start(bot_token=config.bot_token) # pyright: ignore