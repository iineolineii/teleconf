"""
# TeleConf: Interactive configuration management made easy.

Quickly collect and persist required credentials for your Telegram bot with user-friendly prompts.

**Fully compatible with the most popular MTProto and BotAPI frameworks:**
* Aiogram
```python
from aiogram import Bot
from teleconf import Config

# Works just out-of-the-box!
config = Config()

bot = Bot(token=config.bot_token)
```

* Pyrogram
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
please check the `teleconf.examples` module

Copyright (c) 2025 NeoLine
"""
import json
import re
import sys
from pathlib import Path
from typing import TypedDict

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.validation import Validator


class ConfigDict(TypedDict):
    api_id:       int
    api_hash:     str
    bot_token:    str
    phone_number: str


class Config:
    def __init__(
        self,
        config_file: str | Path = "config.json",
        *,
        request_bot_token:    bool = True,
        request_api_id:       bool = False,
        request_api_hash:     bool = False,
        request_phone_number: bool = False,
        force_update:         bool = False
    ) -> None:
        """
        Initialize and save configuration by loading existing values
        (if any) and prompting the user for missing credentials.

        Args:
            config_file (`str | Path`, *optional*):
                Path to the JSON file storing configuration values.
                Defaults to `"config.json"`.

            request_bot_token (`bool`, *optional*):
                Prompt for bot token if not present or if `force_update` is `True`.
                Defaults to `True`.

            request_api_id (`bool`, *optional*):
                Prompt for API ID if not present or if `force_update` is `True`.
                Defaults to `False`.

            request_api_hash (`bool`, *optional*):
                Prompt for API Hash if not present or if `force_update` is `True`.
                Defaults to `False`.

            request_phone_number (`bool`, *optional*):
                Prompt for phone number if not present or if `force_update` is `True`.
                Defaults to `False`.

            force_update (`bool`, *optional*):
                Force re-prompting even if the config file already contains values.
                Defaults to `False`.

        Examples:
            * Aiogram
            ```python
            from aiogram import Bot
            from teleconf import Config

            # Works just out-of-the-box!
            config = Config()

            bot = Bot(token=config.bot_token)
            ```

            * Pyrogram
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
        """
        # Prepare prompt session with persistent history
        self.config_file = Path(config_file).absolute()
        self.history_file = self.config_file.with_name(f".{self.config_file.name}.history")

        self.session = PromptSession(history=FileHistory(str(self.history_file)))
        self.as_dict: ConfigDict = {} # pyright: ignore[reportAttributeAccessIssue]

        # Load existing config if available
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self.as_dict = json.load(f)
            except json.JSONDecodeError:
                self.as_dict = {} # pyright: ignore[reportAttributeAccessIssue]

        # Prompt for missing values
        try:
            # API ID (must be integer)
            if request_api_id:
                self.api_id = self._get_api_id(force_update)

            # API Hash
            if request_api_hash:
                self.api_hash = self._get_api_hash(force_update)

            # Bot token
            if request_bot_token:
                self.bot_token = self._get_bot_token(force_update)

            # Phone number
            if request_phone_number:
                self.phone_number = self._get_phone_number(force_update)

        # Exit on CTRL+C
        except KeyboardInterrupt:
            print("\n\nInput canceled by user")
            sys.exit(0)

        # Save config
        self.as_dict = { # pyright: ignore[reportAttributeAccessIssue]
            "api_id":    self.api_id,
            "api_hash":  self.api_hash,
            "bot_token": self.bot_token,
        }
        with self.config_file.open("w", encoding="utf-8") as f:
            json.dump(self.as_dict, f, ensure_ascii=False, indent=4)

    def _get_api_id(self, force_update: bool) -> int:
        if ("api_id" in self.as_dict) and not force_update:
            return self.as_dict["api_id"]

        print("\nTip: To obtain your API ID and API Hash, log in to your Telegram account at: https://my.telegram.org/auth?to=apps")
        api_id_text: str = self.session.prompt(
            "➤ Enter the Telegram API ID of your application: ",
            validator=Validator.from_callable(
                lambda t: t.isdigit(),
                error_message="Enter a numeric API ID",
                move_cursor_to_end=True,
            ),
            validate_while_typing=False
        )
        return int(api_id_text.strip())


    def _get_api_hash(self, force_update: bool) -> str:
        if ("api_hash" in self.as_dict) and not force_update:
            return self.as_dict["api_hash"]

        print("\nTip: To obtain your API ID and API Hash, log in to your Telegram account at: https://my.telegram.org/auth?to=apps")
        api_hash_text: str = self.session.prompt(
            "➤ Enter the Telegram API Hash of your application: ",
            validator=Validator.from_callable(
                lambda t: bool(t.strip()),
                error_message="API Hash cannot be empty",
                move_cursor_to_end=True,
            ),
            validate_while_typing=False
        )
        return api_hash_text.strip()


    def _get_bot_token(self, force_update: bool) -> str:
        if ("bot_token" in self.as_dict) and not force_update:
            return self.as_dict["bot_token"]

        bot_token_text: str = self.session.prompt(
            "\n➤ Enter your bot token obtained from BotFather: ",
            validator=Validator.from_callable(
                lambda t: bool(t.strip()),
                error_message="Bot Token cannot be empty",
                move_cursor_to_end=True,
            ),
            validate_while_typing=False
        )
        return bot_token_text.strip()


    def _get_phone_number(self, force_update: bool) -> str:
        if ("phone_number" in self.as_dict) and not force_update:
            return self.as_dict["phone_number"]

        phone_number_text: str = self.session.prompt(
            "\n➤ Enter your phone number: ",
            validator=Validator.from_callable(
                lambda t: bool(re.match(r"^\+?[1-9]\d{6,14}$", t.strip())),
                error_message="Phone number should contain only digits, optionally starting with a +, and be 7–15 digits long.",
                move_cursor_to_end=True,
            ),
            validate_while_typing=False
        )
        return phone_number_text.strip()


__all__ = ["Config"]
