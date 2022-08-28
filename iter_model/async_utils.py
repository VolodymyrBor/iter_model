import asyncio
from functools import wraps
from typing import TypeVar, ParamSpec, Callable, Awaitable, cast

T = TypeVar('T')
R = TypeVar('R')
P = ParamSpec('P')


def asyncify(func: Callable[P, R | Awaitable[R]]) -> Callable[P, Awaitable[R]]:

    if asyncio.iscoroutinefunction(func):
        return cast(Callable[P, Awaitable[R]], func)

    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return cast(R, func(*args, **kwargs))

    return cast(Callable[P, Awaitable[R]], wrapper)
