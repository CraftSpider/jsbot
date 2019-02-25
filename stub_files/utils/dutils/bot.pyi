
from typing import Optional, Any, Dict, Iterable, List, Union
from . import paginators
import utils
import utils.dutils as dutils
from discord_talos.talos import Talos
import discord
import discord.ext.commands as commands


class ExtendedBot(commands.Bot):

    all_events: Dict[str, dutils.EventLoop]

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    def add_cog(self, cog: Any) -> None: ...

    def remove_cog(self, name: str) -> None: ...

    def load_extension(self, name: str, prefix: bool = ...) -> None: ...

    def unload_extension(self, name: str, prefix: bool = ...) -> None: ...

    def run(self, token: str, *args: Any, **kwargs: Any) -> None: ...

    def add_event(self, event: dutils.EventLoop) -> None: ...

    def remove_event(self, name: str) -> Optional[dutils.EventLoop]: ...

    def load_extensions(self, extensions: Iterable) -> int: ...

    def unload_extensions(self, extensions: Optional[Iterable] = ...) -> None: ...

    def find_command(self, command: str) -> Optional[commands.Command]: ...

    def commands_dict(self) -> Dict[str, Any]: ...

def _perms_check(self: TalosCog, ctx: commands.Context) -> bool: ...

class TalosCog:

    __slots__ = ("bot", "database")
    bot: Talos
    database: utils.TalosDatabase

    def __new__(cls, bot: Talos): ...

    def __init__(self, bot: Talos): ...

    cog_check: ... = ...

class TalosFormatter(commands.HelpFormatter):

    _paginator: Union[commands.Paginator, paginators.PaginatedEmbed] = ...

    def __init__(self, width: int = ...) -> None: ...

    @property
    async def clean_prefix(self) -> str: return ...

    async def get_command_signature(self) -> str: ...

    async def get_ending_note(self) -> str: ...

    def embed_shorten(self, text: str) -> str: ...

    def _subcommands_field_value(self, _commands: List[commands.Command]) -> str: ...

    def _add_subcommands_to_page(self, max_width: int, _commands: List[commands.Command]) -> None: ...

    async def format(self) -> Union[List[str], List[discord.Embed]]: ...

    async def embed_format(self) -> List[discord.Embed]: ...

    async def string_format(self) -> List[str]: ...
