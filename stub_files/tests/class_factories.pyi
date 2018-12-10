
from typing import List, Dict, Iterable, Any, Union, Optional, Callable, Coroutine
import discord

JsonVals = Union[str, int, bool, Dict[str, 'JsonVals'], List['JsonVals']]
JsonDict = Dict[str, JsonVals]
Callback = Callable[[Any, ...], Coroutine]
AnyChannel = Union[discord.abc.GuildChannel, discord.abc.PrivateChannel]


callbacks: Dict[str, Callback]

def get_state() -> FakeState: ...

def set_callback(cb: Callback, event: str) -> None: ...

def get_callback(event: str) -> Optional[Callback]: ...

def remove_callback(event: str) -> Optional[Callback]: ...

def _dispatch_event(event: str, *args: Any, **kwargs: Any) -> None:...


#
# More internal, dict factories
#


def make_id() -> int: ...

def _fill_optional(data: JsonDict, obj: Any, items: Iterable[str]) -> None: ...

def make_user_dict(username: str, discrim: Union[str, int], avatar: Optional[str], id_num: int, flags: int = ...,
                   bot: bool = ..., mfa_enabled: bool = ..., locale: str = ..., verified: bool = ..., email: str = ...,
                   premium_type: int = ...) -> JsonDict: ...

def dict_from_user(user: discord.User) -> JsonDict: ...

def make_member_dict(user: discord.User, roles: List[int], joined: int = ..., deaf: bool = ..., mute: bool = ...,
                     nick: str = ...) -> JsonDict: ...

def dict_from_member(member: discord.Member) -> JsonDict: ...

def make_role_dict(name: str, id_num: int, colour: int = ..., hoist: bool = ..., position: int = ..., perms: int = ...,
                   managed: bool = ..., mentionable: bool = ...) -> JsonDict: ...

def dict_from_role(role: discord.Role) -> JsonDict: ...

def make_channel_dict(ctype: int, id_num: int, guild_id: int = ..., position: int = ..., permission_overwrites: JsonDict = ...,
                      name: str = ..., topic: Optional[str] = ..., nsfw: bool = ..., last_message_id: Optional[str] = ...,
                      bitrate: int = ..., user_limit: int = ..., rate_limit_per_user: int = ..., recipients: JsonDict = ...,
                      icon: Optional[str] = ..., owner_id: int = ..., application_id: int = ..., parent_id: Optional[int] = ...,
                      last_pin_timestamp: int = ...) -> JsonDict: ...

def make_text_channel_dict(name: str, id_num: int, guild_id: int = ..., position: int = ..., permission_overwrites: JsonDict = ...,
                           topic: Optional[str] = ..., nsfw: bool = ..., last_message_id: Optional[int] = ...,
                           rate_limit_per_user: int = ..., parent_id: Optional[int]= ..., last_pin_timestamp: int = ...) -> JsonDict: ...

def dict_from_channel(channel: AnyChannel) -> JsonDict: ...

def make_message_dict(channel: AnyChannel, author: Union[discord.User, discord.Member], id_num: int, content: str = ...,
                      timestamp: int = ..., edited_timestamp: Optional[int] = ..., tts: bool = ...,
                      mention_everyone: bool = ..., mentions: List[discord.User] = ..., mention_roles: List[int] = ...,
                      attachments: List[discord.Attachment] = ..., embeds: List[discord.Embed] = ..., pinned: bool = ...,
                      type: int = ..., guild_id: int = ..., member: discord.Member = ..., reactions: List[discord.Reaction] = ...,
                      nonce: Optional[int] = ..., webhook_id: int = ..., activity: discord.Activity = ..., application: JsonDict = ...): ...

def dict_from_message(message: discord.Message) -> JsonDict: ...

def make_attachment_dict(filename: str, size: int, url: str, proxy_url: str, id_num: int, height: Optional[int] = ...,
                         width: Optional[int] = ...) -> JsonDict: ...

def dict_from_attachment(attachment: discord.Attachment) -> JsonDict: ...


#
# Outward facing, easy to use factory methods
#


def make_guild(name: str, members: List[discord.Member] = ..., channels: List[AnyChannel] = ..., roles: List[discord.Role] = ...,
               owner: bool = ..., id_num: int = ...) -> discord.Guild: ...

def make_text_channel(name: str, guild: discord.Guild, position: int = ..., id_num: int = ...) -> discord.TextChannel: ...

def make_user(username: str, discrim: Union[str, int], avatar: str = ..., id_num: int = ...) -> discord.User: ...

def make_member(user: discord.User, guild: discord.Guild, nick: str = ..., roles: List[discord.Role] = ...) -> discord.Member: ...

def make_message(content: str, author: Union[discord.User, discord.Member], channel: AnyChannel, id_num: int = ...) -> discord.Message: ...

def configure(client: discord.Client) -> None: ...

def main() -> None: ...
