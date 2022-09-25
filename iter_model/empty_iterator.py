from typing import Any
from collections.abc import Iterator, AsyncIterator


class EmptyIterator(Iterator):

    __slots__: tuple = tuple()

    def __next__(self) -> Any:
        raise StopIteration


class EmptyAsyncIterator(AsyncIterator):

    __slots__: tuple = tuple()

    async def __anext__(self) -> Any:
        raise StopAsyncIteration
