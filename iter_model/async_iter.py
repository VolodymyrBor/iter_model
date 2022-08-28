import operator
from functools import wraps
from typing import (
    TypeVar,
    Generic,
    Callable,
    Iterable,
    ParamSpec,
    Awaitable,
    TypeAlias,
    AsyncIterable,
    AsyncIterator, cast,
)

from .async_utils import asyncify

T = TypeVar('T')
R = TypeVar('R')
P = ParamSpec('P')
DefaultT = TypeVar('DefaultT')
KeyFunc: TypeAlias = Callable[[T], R | Awaitable[R]]
BinaryFunc: TypeAlias = Callable[[T, T], R | Awaitable[R]]
ConditionFunc: TypeAlias = Callable[[T], bool | Awaitable[bool]]

_EMPTY = object()


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
    __slots__ = ('_it',)

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
        func = asyncify(func)
        async for item in self:
            yield await func(item)

    @async_iter
    async def skip(self, count: int) -> 'AsyncIter[T]':  # type: ignore
        """Skip 'count' items from iterator"""
        async for index, item in self.enumerate():
            if index >= count:
                yield item

    @async_iter
    async def skip_while(self, func: ConditionFunc) -> 'AsyncIter[T]':  # type: ignore
        """Skips leading elements while conditional is satisfied"""
        func = asyncify(func)
        async for item in self:  # pragma: no cover
            if await func(item):
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
        func = asyncify(func)
        async for item in self:
            if await func(item):  # pragma: no cover
                return item
        raise ValueError('Item not found')

    @async_iter
    async def where(self, func: ConditionFunc) -> 'AsyncIter[T]':  # type: ignore
        """Filter item by condition"""
        func = asyncify(func)
        async for item in self:
            if await func(item):
                yield item

    @async_iter
    async def take_while(self, func: ConditionFunc) -> 'AsyncIter[T]':  # type: ignore
        """Take items while the conditional is satisfied"""
        func = asyncify(func)
        async for item in self:
            if await func(item):
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

        return last_item  # type: ignore

    @async_iter
    async def chain(self, *iterables: AsyncIterable[T]) -> 'AsyncIter[T]':  # type: ignore
        """Chain with other iterables"""
        async for item in self:
            yield item

        for iterable in iterables:
            async for item in iterable:
                yield item

    async def all(self) -> bool:
        """Checks whether all elements of this iterable are true"""
        async for item in self:
            if not bool(item):  # pragma: no cover
                return False
        return True

    async def any(self) -> bool:
        """Checks whether any element of this iterable is true"""
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

    async def reduce(
        self,
        func: BinaryFunc,
        initial: T = _EMPTY,  # type: ignore
    ) -> T | R:
        """Apply a function of two arguments cumulatively to the items of an iterable,
         from left to right, to reduce the iterable to a single value.

        :param func: func[accumulated value, next item]
        :param initial: initial value of iterable. Serves like default value if iterable is empty.
        :return: reduced value
        :raise ValueError: if initial is not provided and iterable is empty
        """
        if initial is _EMPTY:
            try:
                initial = await self.next()
            except StopAsyncIteration:
                raise ValueError('Iterator is empty')

        func = asyncify(func)
        async for item in self:
            initial = await func(initial, item)
        return cast(T, initial)

    async def max(
        self,
        key: KeyFunc | None = None,
        default: DefaultT = _EMPTY,  # type: ignore
    ) -> T | DefaultT:
        """Return the biggest item.

        :param key: the result of the function will be used to compare the elements.
        :param default: default value in case iterable is empty
        :return: the biggest item
        :raise ValueError: when iterable is empty and default value is not provided
        """
        try:
            max_item = await self.next()
        except StopAsyncIteration:
            if default is _EMPTY:
                raise ValueError('Iterator is empty')
            else:
                return default
        key = asyncify(key if key else lambda x: x)
        max_item_key = await key(max_item)
        async for item in self:
            item_key = await key(item)
            if item_key > max_item_key:
                max_item = item
                max_item_key = item_key
        return max_item

    async def min(
        self,
        key: KeyFunc | None = None,
        default: DefaultT = _EMPTY,  # type: ignore
    ) -> T | DefaultT:
        """Return the smallest item.

        :param key: the result of the function will be used to compare the elements.
        :param default: default value in case iterable is empty
        :return: the smallest item
        :raise ValueError: when iterable is empty and default value is not provided
        """
        try:
            max_item = await self.next()
        except StopAsyncIteration:
            if default is _EMPTY:
                raise ValueError('Iterator is empty')
            else:
                return default
        key = asyncify(key if key else lambda x: x)
        max_item_key = await key(max_item)
        async for item in self:
            item_key = await key(item)
            if item_key < max_item_key:
                max_item = item
                max_item_key = item_key
        return max_item

    @async_iter
    async def accumulate(  # type: ignore
        self,
        func: BinaryFunc = operator.add,
        initial: T | None = None,
    ) -> 'AsyncIter[R]':
        """Return series of accumulated sums (by default).

        :param func: func[accumulated value, next value], by default operator.add
        :param initial: initial value of series
        """
        total = initial
        if total is None:
            try:
                total = await self.next()
            except StopAsyncIteration:
                return

        func = asyncify(func)
        yield total
        async for item in self:
            total = await func(total, item)
            yield total

    @async_iter
    async def append_left(self, item: T) -> 'AsyncIter[T]':  # type: ignore
        """Append an item to left of the iterable (start)"""
        yield item
        async for item_ in self:
            yield item_

    @async_iter
    async def append_right(self, item: T) -> 'AsyncIter[T]':  # type: ignore
        """Append an item to right of the iterable (end)"""
        async for item_ in self:
            yield item_
        yield item

    @async_iter
    async def append_at(self, index: int, item: T) -> 'AsyncIter[T]':  # type: ignore
        """Append at the position in to the iterable"""
        i = 0
        async for i, item_ in self.enumerate():
            if i == index:
                yield item
            yield item_
        if index > i:
            yield item

    @async_iter
    async def zip(self, *iterables: AsyncIterable[T], strict: bool = False) -> 'AsyncIter[list[T]]':  # type: ignore
        """The zip object yields n-length tuples, where n is the number of iterables
        passed as positional arguments to zip().  The i-th element in every tuple
        comes from the i-th iterable argument to zip().  This continues until the
        shortest argument is exhausted.

        :raise ValueError: when strict is true and one of the arguments is exhausted before the others
        """
        iterables = (self, *iterables)
        while True:
            batch = []
            for it in iterables:
                try:
                    batch.append(await anext(it))  # type: ignore
                except StopAsyncIteration:
                    if not strict:
                        return
            if len(batch) != len(iterables):
                raise ValueError('lengths of iterables are not the same')
            yield batch

    @async_iter
    async def zip_longest(  # type: ignore
        self,
        *iterables: AsyncIterable[T],
        fillvalue: R = None,
    ) -> 'AsyncIter[list[T | R]]':
        """The zip object yields n-length tuples, where n is the number of iterables
        passed as positional arguments to zip().  The i-th element in every tuple
        comes from the i-th iterable argument to zip().  This continues until the
        longest argument is exhausted.

        :param fillvalue: when the shorter iterables are exhausted, the fillvalue is substituted in their place
        """
        iterables = (self, *iterables)
        while True:
            batch = []
            batch_has_any_value = False
            for it in iterables:
                try:
                    batch.append(await anext(it))  # type: ignore
                    batch_has_any_value = True
                except StopAsyncIteration:
                    batch.append(fillvalue)
            if not batch_has_any_value:
                return
            yield batch

    @async_iter
    async def slice(self, start: int = 0, stop: int | None = None, step: int = 1) -> 'AsyncIter[T]':  # type: ignore
        it = self.skip(start)

        if stop is not None:
            it = it.take(stop - start)

        async for i, item in it.enumerate():
            if i % step == 0:
                yield item
