from functools import wraps
from asyncio import iscoroutine
from typing import (
    TypeVar,
    Generic,
    Callable,
    Iterable,
    ParamSpec,
    Awaitable,
    TypeAlias,
    AsyncIterable,
    AsyncIterator,
)

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

    __slots__ = ('_it', )

    def __init__(self, it: AsyncIterable[T]):
        self._it = aiter(it)

    def __aiter__(self) -> AsyncIterator[T]:
        return self._it

    def __anext__(self) -> Awaitable[T]:
        return anext(self._it)

    @classmethod
    @async_iter
    async def from_sync(cls, it: Iterable[T]) -> 'AsyncIter[T]':  # type: ignore
        """Create from sync iterable"""
        for item in it:
            yield item

    async def to_list(self) -> list[T]:
        """Convert to list"""
        return [item async for item in self]

    async def to_tuple(self) -> tuple[T, ...]:
        """Convert to tuple"""
        return tuple([item async for item in self])

    async def to_set(self) -> set[T]:
        """Convert to set"""
        return set([item async for item in self])

    @async_iter
    async def enumerate(self, start: int = 0) -> 'AsyncIter[tuple[int, T]]':  # type: ignore
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
    async def take(self, limit: int) -> 'AsyncIter[T]':  # type: ignore
        """Take 'count' items from iterator"""
        async for index, item in self.enumerate():
            if index >= limit:
                break
            yield item

    @async_iter
    async def map(self, func: Callable[[T], R | Awaitable[R]]) -> 'AsyncIter[R]':  # type: ignore
        """Return an iterator that applies function to every item of iterable,
        yielding the results"""
        async for item in self:
            result = func(item)
            if iscoroutine(result):
                result = await result
            yield result

    @async_iter
    async def skip(self, count: int) -> 'AsyncIter[T]':  # type: ignore
        """Skip 'count' items from iterator"""
        async for index, item in self.enumerate():
            if index >= count:
                yield item

    @async_iter
    async def skip_while(self, func: ConditionFunc) -> 'AsyncIter[T]':  # type: ignore
        """Skips leading elements while conditional is satisfied"""
        async for item in self:  # pragma: no cover
            result = func(item)
            if iscoroutine(result):
                result = await result
            if result:
                break

            yield item

    async def count(self) -> int:
        """Return count of items in iterator"""
        count_ = 0
        async for _ in self:
            count_ += 1
        return count_

    async def first_where(self, func: ConditionFunc) -> T:
        """Find first item for which the conditional is satisfied

        :raise ValueError: the item not found"""
        async for item in self:
            result = func(item)
            if iscoroutine(result):
                result = await result
            if result:  # pragma: no cover
                return item
        raise ValueError('Item not found')

    @async_iter
    async def where(self, func: ConditionFunc) -> 'AsyncIter[T]':  # type: ignore
        """Filter item by condition"""
        async for item in self:
            result = func(item)
            if iscoroutine(result):
                result = await result
            if result:
                yield item

    @async_iter
    async def take_while(self, func: ConditionFunc) -> 'AsyncIter[T]':  # type: ignore
        """Take items while the conditional is satisfied"""
        async for item in self:
            result = func(item)
            if iscoroutine(result):
                result = await result
            if result:
                yield item
            else:
                break

    async def next(self) -> T:
        """Returns the first item"""
        try:
            return await anext(self)  # type: ignore
        except StopAsyncIteration:
            raise StopAsyncIteration('Iterable is empty')

    async def last(self) -> T:
        """Returns the last item"""
        last_item = initial = object()
        async for item in self:
            last_item = item

        if last_item is initial:
            raise StopAsyncIteration('Iterable is empty')

        return last_item   # type: ignore

    @async_iter
    async def chain(self, *iterables: AsyncIterable[T]) -> 'AsyncIter[T]':  # type: ignore
        """Chain with other iterables"""
        async for item in self:
            yield item

        for iterable in iterables:
            async for item in iterable:
                yield item

    async def all(self) -> bool:
        """Checks whether all element of this iterable satisfies"""
        async for item in self:
            if not bool(item):  # pragma: no cover
                return False
        return True

    async def any(self) -> bool:
        """Checks whether any element of this iterable satisfies"""
        async for item in self:
            if bool(item):  # pragma: no cover
                return True
        return False

    async def first(self) -> T:
        """Returns first item"""
        return await self.next()

    @async_iter
    async def mark_first(self) -> 'AsyncIter[tuple[T, bool]]':  # type: ignore
        """Mark first item. Yields: tuple[item, is_first]"""
        try:
            first = await self.next()
        except StopAsyncIteration:
            return

        yield first, True
        async for item in self:
            yield item, False

    @async_iter
    async def mark_last(self) -> 'AsyncIter[tuple[T, bool]]':  # type: ignore
        """Mark last item. Yields: tuple[item, is_last]"""
        try:
            previous_item = await self.next()
        except StopAsyncIteration:
            return

        async for current_item in self:
            yield previous_item, False
            previous_item = current_item
        yield previous_item, True

    @async_iter
    async def mark_first_last(self) -> 'AsyncIter[tuple[T, bool, bool]]':  # type: ignore
        """Mark first and last item. Yields: tuple[item, is_first, is_last]"""
        try:
            previous_item = await self.next()
        except StopAsyncIteration:
            return

        first = True
        async for current_item in self:
            yield previous_item, first, False
            first = False
            previous_item = current_item
        yield previous_item, first, True
