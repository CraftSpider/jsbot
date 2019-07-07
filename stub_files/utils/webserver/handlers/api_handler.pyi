
from typing import Dict, Any, Callable, Optional, Awaitable
import aiohttp.web as web
import utils.webserver.handlers.base_handler as bh

_H = Callable[[str, Dict[str, Any]], Awaitable[None]]

def api_handler(name: str) -> Callable[[Callable], Callable]: ...

class APIHandler(bh.BaseHandler):

    __slots__ = ()

    _handlers: Dict[str, _H]

    def __init_subclass__(cls, **kwargs: Any) -> None: ...

    def _check_token(self, user: str, token: str) -> bool: ...

    def _path_to_name(self, path: str) -> str: ...

    async def get(self, request: web.Request) -> web.Response: ...

    async def post(self, request: web.Request) -> web.Response: ...

    async def dispatch_request(self, method: str, request: web.Request) -> web.Response: ...

    def _get_handler(self, method: str, name: str) -> Optional[_H]: ...

    async def dispatch(self, path: str, method: str, data: Dict[str, Any]) -> web.Response: ...
