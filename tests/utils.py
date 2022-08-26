from functools import wraps
from typing import Iterable, AsyncIterable, TypeVar, ParamSpec, Callable, Awaitable

T = TypeVar('T')
R = TypeVar('R')
P = ParamSpec('P')


async def to_async_iter(it: Iterable[T]) -> AsyncIterable[T]:
    for item in it:
        yield item
