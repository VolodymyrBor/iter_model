from typing import Iterable, AsyncIterable, TypeVar, ParamSpec

_T = TypeVar('_T')
_R = TypeVar('_R')
_P = ParamSpec('_P')


async def to_async_iter(it: Iterable[_T]) -> AsyncIterable[_T]:
    for item in it:
        yield item
