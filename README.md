# Interactive configuration management made easy

Quickly collect and persist required credentials for your Telegram bot
(like API ID, hash, bot token, or phone number) with user-friendly prompts.

## Installation

```bash
pip install git+https://github.com/iineolineii/teleconf.git
```

## Usage:

This module is fully compatible with the most popular MTProto and BotAPI frameworks:

### Aiogram

```python
from aiogram import Bot
from teleconf import Config

# Works just out-of-the-box!
config = Config()

bot = Bot(token=config.bot_token)
```

### Pyrogram

```python
from pyrogram import Client
from teleconf import Config

# API ID and hash are required to start an MTProto session
config = Config(request_api_id=True, request_api_hash=True)

client = Client(
    name="My Pyrogram Client",
    api_id=config.api_id,
    api_hash=config.api_hash,
    bot_token=config.bot_token
)
```

For more framework integration examples (such as Telethon or TeleBot),
please check the `teleconf.examples` module.



## Advanced usage

You can easily customize which values you want to collect:

```python
from teleconf import Config

config = Config(
    config_file="config.json",
    request_bot_token=True,
    request_api_id=False,
    request_api_hash=False,
    request_phone_number=False,
    force_update=False
)
```

**Arguments:**

* `config_file` (`str | Path`, *optional*):

    Path to the JSON file storing configuration values.

    Defaults to `"config.json"`.

* `request_bot_token` (`bool`, *optional*):

    Prompt for bot token if missing or when `force_update` is `True`.

    Defaults to `True`.

* `request_api_id` (`bool`, *optional*):

    Prompt for API ID if missing or when `force_update` is `True`.

    Defaults to `False`.

* `request_api_hash` (`bool`, *optional*):

    Prompt for API Hash if missing or when `force_update` is `True`.

    Defaults to `False`.

* `request_phone_number` (`bool`, *optional*):

    Prompt for phone number if missing or when `force_update` is `True`.

    Defaults to `False`.

* `force_update` (`bool`, *optional*):

    Force re-prompting even if the config file already contains values.

    Defaults to `False`.

## Dependencies:
* [`prompt-toolkit`](https://pypi.org/project/prompt-toolkit/) (included in `requirements.txt`)

## License

This project is licensed under the MIT License.
