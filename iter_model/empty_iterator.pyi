from collections.abc import AsyncIterator, Iterator
from typing import Any

class EmptyIterator(Iterator):
    def __next__(self) -> Any: ...

class EmptyAsyncIterator(AsyncIterator):
    async def __anext__(self) -> Any: ...
