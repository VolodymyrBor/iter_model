from functools import wraps
from asyncio import iscoroutine
from typing import AsyncIterable, TypeVar, Callable, Generic, ParamSpec, Awaitable, TypeAlias

T = TypeVar('T')
R = TypeVar('R')
P = ParamSpec('P')
ConditionFunc: TypeAlias = Callable[[T], bool | Awaitable[bool]]


def async_iter(func: Callable[P, AsyncIterable[T]]) -> Callable[P, 'AsyncIter[T]']:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> 'AsyncIter[T]':
        return AsyncIter(func(*args, **kwargs))
    return wrapper


class AsyncIter(Generic[T]):

    def __init__(self, it: AsyncIterable[T]):
        self._it = aiter(it)

    def __aiter__(self) -> AsyncIterable[T]:
        return self._it

    async def to_list(self) -> list[T]:
        return [item async for item in self]

    @async_iter
    async def enumerate(self, start: int = 0) -> 'AsyncIter[tuple[int, T]]':
        index = start
        async for item in self:
            yield index, item
            index += 1

    @async_iter
    async def take(self, limit: int) -> 'AsyncIter[T]':
        async for index, item in self.enumerate():
            if index >= limit:
                break
            yield item

    @async_iter
    async def map(self, func: Callable[[T], R | Awaitable[R]]) -> 'AsyncIter[R]':
        async for item in self:
            result = func(item)
            if iscoroutine(result):
                result = await result
            yield result

    @async_iter
    async def skip(self, count: int) -> 'AsyncIter[T]':
        async for index, item in self.enumerate():
            if index >= count:
                yield item

    async def count(self) -> int:
        count_ = 0
        async for _ in self:
            count_ += 1
        return count_

    async def first_where(self, func: ConditionFunc) -> T:
        async for item in self:
            result = func(item)
            if iscoroutine(result):
                result = await result
            if result:
                return item
        raise ValueError('Item not found')

    @async_iter
    async def where(self, func: ConditionFunc) -> 'AsyncIter[T]':
        async for item in self:
            result = func(item)
            if iscoroutine(result):
                result = await result
            if result:
                yield item

    @async_iter
    async def take_while(self, func: ConditionFunc) -> 'AsyncIter[T]':
        async for item in self:
            result = func(item)
            if iscoroutine(result):
                result = await result
            if result:
                yield item
            else:
                break
