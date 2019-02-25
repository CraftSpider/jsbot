"""
    Stub file for Talos admin commands

    author: CraftSpider
"""

from typing import Callable, Dict, Union
from collections import defaultdict
from discord_talos.talos import Talos
import logging
import utils.dutils as dutils
import discord
import discord.ext.commands as commands

secure_keys: defaultdict = ...
log: logging.Logger = ...

def dev_check() -> Callable: ...

class AdminCommands(dutils.TalosCog):

    LEVELS: Dict[str, int] = ...
    cog_check: Callable[[AdminCommands, commands.Context], bool] = ...

    async def nick(self, ctx: commands.Context, *, nickname: str) -> None: ...

    async def repeat(self, ctx: commands.Context, *, text: str) -> None: ...

    async def purge(self, ctx: commands.Context, number: str = ..., *key: str) -> None: ...

    async def kick(self, ctx: commands.Context, user: discord.Member, reason: str = ...): ...

    async def ban(self, ctx: commands.Context, user: discord.Member, reason: str = ...): ...

    async def silence(self, ctx: commands.Context, user: discord.Member, length: str = ...): ...

    async def talos_perms(self, ctx: commands.Context) -> None: ...

    @commands.group()
    def ops(self, ctx: commands.Context) -> None: ...

    async def _ops_add(self, ctx: commands.Context, member: discord.Member) -> None: ...

    async def _ops_remove(self, ctx: commands.Context, member: str) -> None: ...

    async def _ops_list(self, ctx: commands.Context) -> None: ...

    async def _ops_all(self, ctx: commands.Context) -> None: ...

    @commands.group()
    def perms(self, ctx: commands.Context) -> None: ...

    async def _p_create(self, ctx: commands.Context, command: str, level: str, allow: str, name: str = ..., priority: int = ...) -> None: ...

    async def _p_remove(self, ctx: commands.Context, command: str = ..., level: str = ..., name: str = ...) -> None: ...

    async def _p_list(self, ctx: commands.Context) -> None: ...

    async def _p_all(self, ctx: commands.Context) -> None: ...

    @commands.group()
    def options(self, ctx: commands.Context) -> None: ...

    async def _opt_set(self, ctx: commands.Context, option: str, value: str) -> None: ...

    async def _opt_list(self, ctx: commands.Context) -> None: ...

    async def _opt_default(self, ctx: commands.Context, option: str) -> None: ...

    async def _opt_all(self, ctx: commands.Context) -> None: ...

    @commands.group()
    def command(self, ctx: commands.Context) -> None: ...

    async def _c_add(self, ctx: commands.Context, name: str, *, text: str) -> None: ...

    async def _c_edit(self, ctx: commands.Context, name: str, *, text: str) -> None: ...

    async def _c_remove(self, ctx: commands.Context, name: str) -> None: ...

    async def _c_list(self, ctx: commands.Context) -> None: ...

    @commands.group()
    async def event(self, ctx: commands.Context) -> None: ...

    async def _e_add(self, ctx: commands.Context, name: str, period: str, *, text: str) -> None: ...

    async def _e_edit(self, ctx: commands.Context, name: str, *, text: str) -> None: ...

    async def _e_remove(self, ctx: commands.Context, name: str) -> None: ...

    async def _e_list(self, ctx: commands.Context) -> None: ...

    @commands.group()
    async def quote(self, ctx: commands.Context, author: Union[str, int] = ..., *, quote: str = ...) -> None: ...

    async def _q_add(self, ctx: commands.Context, author: str, *, quote: str) -> None: ...

    async def _q_remove(self, ctx: commands.Context, num: int) -> None: ...

    async def _q_list(self, ctx: commands.Context, page: int) -> None: ...

def admin_check(self: AdminCommands, ctx: commands.Context) -> bool: ...

def setup(bot: Talos) -> None: ...
