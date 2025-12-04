import asyncio
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import ParamSpec, TypeVar, cast

_T = TypeVar('_T')
_R = TypeVar('_R')
_P = ParamSpec('_P')


def asyncify(func: Callable[_P, _R | Awaitable[_R]]) -> Callable[_P, Awaitable[_R]]:

    if asyncio.iscoroutinefunction(func):
        return cast(Callable[_P, Awaitable[_R]], func)

    @wraps(func)
    async def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        return cast(_R, func(*args, **kwargs))

    return cast(Callable[_P, Awaitable[_R]], wrapper)
