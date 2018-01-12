"""
    Talos stub file for typing and such

    author: CraftSpider
"""
from typing import List, Tuple, Union, Any, Optional, Dict, Pattern
import logging
import discord
import discord.ext.commands as commands
import datetime
import mysql.connector.abstracts
import utils

SQL_ADDRESS = ... # type: str
TOKEN_FILE = ... # type: str
_mentions_transforms = ... # type: Dict[str, str]
_mention_pattern = ... # type:Pattern
log = ... # type: logging.Logger

class Talos(commands.Bot):

    VERSION = ... # type: str
    BOOT_TIME = ... # type: datetime
    PROMPT_TIME = ... # type: int
    DEFAULT_PREFIX = ... # type: str
    EXTENSION_DIRECTORY = ... # type: str
    STARTUP_EXTENSIONS = ... # type: List[str]
    DEVS = ... # type: Tuple[int, ...]
    discordbots_token = ... # type: str
    database = ... # type: utils.TalosDatabase
    session = ... # type: utils.TalosHTTPClient

    def __init__(self, sql_conn: Optional[mysql.connector.abstracts.MySQLConnectionAbstract] = ..., **kwargs: Any) -> None: ...

    def load_extensions(self, extensions: Optional[list] = ...) -> int: ...

    def unload_extensions(self, extensions: Optional[list] = ...) -> None: ...

    def skip_check(self, author_id: int, self_id: int) -> bool: ...

    def should_embed(self, ctx: commands.Context) -> bool: ...

    def get_timezone(self, ctx: commands.Context) -> datetime.timezone: ...

    async def logout(self) -> None: ...

    async def close(self) -> None: ...

    async def _talos_help_command(self, ctx: commands.Context, *args: str) -> None: ...

    def run(self, token: str, *args, **kwargs) -> None: ...

    async def start(self, *args, **kwargs) -> None: ...

    async def on_ready(self) -> None: ...

    async def on_guild_join(self, guild: discord.Guild) -> None: ...

    async def on_guild_remove(self, guild: discord.Guild) -> None: ...

    async def on_command(self, ctx: commands.Context) -> None: ...

    async def on_command_error(self, ctx: commands.Context, exception: commands.CommandError) -> None: ...

    async def get_context(self, message: discord.Message, *, cls: commands.Context=commands.Context) -> commands.Context: ...

def custom_creator(invoker: str, text: str) -> commands.Command: ...

def talos_prefix(bot: Talos, message: discord.Message) -> Union[List[str], str]: ...

def string_load(filename: str) -> List[str]: ...

def load_token() -> str: ...

def load_botlist_token() -> str: ...

def load_nano_login() -> List[str]: ...

def load_btn_key() -> str: ...

def load_sql_data() -> List[str]: ...

def main() -> None: ...
