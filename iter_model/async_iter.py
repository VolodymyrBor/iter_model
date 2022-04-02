from functools import wraps
from asyncio import iscoroutine
from typing import AsyncIterable, TypeVar, Callable, Generic, ParamSpec, Awaitable, TypeAlias

T = TypeVar('T')
R = TypeVar('R')
P = ParamSpec('P')
ConditionFunc: TypeAlias = Callable[[T], bool | Awaitable[bool]]


def async_iter(func: Callable[P, AsyncIterable[T]]) -> Callable[P, 'AsyncIter[T]']:
    """Convert result of the func to AsyncIter

    :param func: function that returns async iterable
    :return: new function
    """
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
        """Convert self to list"""
        return [item async for item in self]

    @async_iter
    async def enumerate(self, start: int = 0) -> 'AsyncIter[tuple[int, T]]':
        """Returns a tuple containing a count (from start which defaults to 0)
        and the values obtained from iterating over self.

        :param start: start of index
        :return: interator of tuple[index, item]
        """
        index = start
        async for item in self:
            yield index, item
            index += 1

    @async_iter
    async def take(self, limit: int) -> 'AsyncIter[T]':
        """Take 'count' items from iterator"""
        async for index, item in self.enumerate():
            if index >= limit:
                break
            yield item

    @async_iter
    async def map(self, func: Callable[[T], R | Awaitable[R]]) -> 'AsyncIter[R]':
        """Return an iterator that applies function to every item of iterable,
        yielding the results"""
        async for item in self:
            result = func(item)
            if iscoroutine(result):
                result = await result
            yield result

    @async_iter
    async def skip(self, count: int) -> 'AsyncIter[T]':
        """Skip 'count' items from iterator"""
        async for index, item in self.enumerate():
            if index >= count:
                yield item

    async def count(self) -> int:
        """Return count of items in iterator"""
        count_ = 0
        async for _ in self:
            count_ += 1
        return count_

    async def first_where(self, func: ConditionFunc) -> T:
        """Find first item for which the condition is met

        :raise ValueError: the item not found"""
        async for item in self:
            result = func(item)
            if iscoroutine(result):
                result = await result
            if result:  # pragma: no cover
                return item
        raise ValueError('Item not found')

    @async_iter
    async def where(self, func: ConditionFunc) -> 'AsyncIter[T]':
        """Filter item by condition"""
        async for item in self:
            result = func(item)
            if iscoroutine(result):
                result = await result
            if result:
                yield item

    @async_iter
    async def take_while(self, func: ConditionFunc) -> 'AsyncIter[T]':
        """Take items while the condition is met"""
        async for item in self:
            result = func(item)
            if iscoroutine(result):
                result = await result
            if result:
                yield item
            else:
                break
