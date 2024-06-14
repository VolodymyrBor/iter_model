from typing import Iterable, AsyncIterable, TypeVar, ParamSpec

T = TypeVar('_T')
R = TypeVar('_R')
P = ParamSpec('_P')


async def to_async_iter(it: Iterable[T]) -> AsyncIterable[T]:
    for item in it:
        yield item
