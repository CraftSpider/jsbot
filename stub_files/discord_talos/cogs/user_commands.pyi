"""
    Stub for Talos user commands

    author: CraftSpider
"""

from discord_talos.talos import Talos
import logging
import spidertools.common as utils
import spidertools.discord as dutils
import discord
import discord.ext.commands as commands
import discord_talos.talossql as sql

log: logging.Logger = ...

def unused_role(ctx: commands.Context, role: discord.Role) -> bool: ...

def talos_colour(role: discord.Role) -> bool: ...

def lopez_colour(role: discord.Role) -> bool: ...

def unnamed_colour(role: discord.Role) -> bool: ...

def named_colour(role: discord.Role) -> bool: ...

class UserCommands(dutils.TalosCog):

    @commands.group()
    async def colour(self, ctx: commands.Context, color: str) -> None: ...

    async def _clear(self, ctx: commands.Context) -> None: ...

    async def _list(self, ctx: commands.Context) -> None: ...

    async def my_perms(self, ctx: commands.Context) -> None: ...

    async def register(self, ctx: commands.Context) -> None: ...

    async def deregister(self, ctx: commands.Context) -> None: ...

    async def profile(self, ctx: commands.Context, user: discord.User=None) -> None: ...

    @commands.group()
    async def user(self, ctx: commands.Context) -> None: ...

    class UserCtx(commands.Context):
        profile: sql.TalosUser

    async def _title(self, ctx: UserCtx, title: str = ...) -> None: ...

    async def _options(self, ctx: UserCtx) -> None: ...

    async def _stats(self, ctx: UserCtx) -> None: ...

    async def _description(self, ctx: UserCtx, *, text: str) -> None: ...

    async def _set(self, ctx: UserCtx, option: str, value: str) -> None: ...

    async def _remove(self, ctx: UserCtx, option: str) -> None: ...

def setup(bot: Talos) -> None: ...
