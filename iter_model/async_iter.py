import operator
from collections.abc import AsyncIterable, AsyncIterator, Awaitable, Callable, Iterable
from functools import wraps
from typing import (
    Generic,
    ParamSpec,
    TypeVar,
    cast,
)

from .async_utils import asyncify
from .empty_iterator import EmptyAsyncIterator

_T = TypeVar('_T')
_R = TypeVar('_R')
_P = ParamSpec('_P')
_DefaultT = TypeVar('_DefaultT')
_KeyFunc = Callable[[_T], _R | Awaitable[_R]]
_BinaryFunc = Callable[[_T, _T], _R | Awaitable[_R]]
_ConditionFunc = Callable[[_T], bool | Awaitable[bool]]

_EMPTY = object()


def async_iter(func: Callable[_P, AsyncIterator[_T]]) -> Callable[_P, 'AsyncIter[_T]']:
    """Convert result of the func to AsyncIter

    Usage:
    ```python
    @async_iter
    def my_generator() -> AsyncIter[int]:
        for i in range(10):
            yield i
    ```

    :param func: function that returns async iterable
    :return: new function
    """

    @wraps(func)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> 'AsyncIter[_T]':
        return AsyncIter[_T](func(*args, **kwargs))

    return wrapper


class AsyncIter(Generic[_T]):
    __slots__ = ('_it',)

    def __init__(self, it: AsyncIterator[_T] | AsyncIterable[_T]):
        self._it = aiter(it)

    def __aiter__(self):
        return self._it

    async def __anext__(self) -> _T:
        return await anext(self._it)

    @classmethod
    @async_iter
    async def from_sync(cls, it: Iterable[_T]) -> 'AsyncIter[_T]':
        """Create from sync iterable

        :param it: Iterable[_T], iterable
        :return: async iterable
        """
        for item in it:
            yield item

    @classmethod
    def empty(cls) -> 'AsyncIter[_T]':
        """Create empty iterable

        :return: empty iterable
        """
        return cls(EmptyAsyncIterator())

    async def to_list(self) -> list[_T]:
        """Convert to list

        :return: list of items
        """
        return [item async for item in self]

    async def to_tuple(self) -> tuple[_T, ...]:
        """Convert to tuple

        :return: tuple of items
        """
        return tuple([item async for item in self])

    async def to_set(self) -> set[_T]:
        """Convert to set

        :return: set of items
        """
        return {item async for item in self}

    @async_iter
    async def enumerate(self, start: int = 0) -> AsyncIterator[tuple[int, _T]]:
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
    async def take(self, limit: int) -> AsyncIterator[_T]:
        """Take 'count' items from iterator

        :return: iterable that contains 'count' items
        """

        count = 0
        while True:
            if count >= limit:
                break
            try:
                yield await self.next()
            except StopAsyncIteration:
                break
            else:
                count += 1

    @async_iter
    async def map(self, func: Callable[[_T], _R | Awaitable[_R]]) -> AsyncIterator[_R]:
        """Return an iterator that applies function to every item of iterable,
        yielding the results

        :return: iterable
        """
        func = asyncify(func)
        async for item in self:
            yield await func(item)

    @async_iter
    async def skip(self, count: int) -> AsyncIterator[_T]:
        """Skip 'count' items from iterator
        :return: iterable without first 'count' items
        """
        async for index, item in self.enumerate():
            if index >= count:
                yield item

    @async_iter
    async def skip_while(self, func: _ConditionFunc) -> AsyncIterator[_T]:
        """Skips leading elements while conditional is satisfied

        :return: iterable
        """
        func = asyncify(func)
        async for item in self:  # pragma: no cover
            if await func(item):
                break
            yield item

    @async_iter
    async def skip_where(self, func: _ConditionFunc) -> AsyncIterator[_T]:
        """Skip elements where conditional is satisfied

        :return: async iterable
        """
        func = asyncify(func)
        async for item in self:
            if not await func(item):
                yield item

    async def count(self) -> int:
        """Return count of items in iterator

        :return: count of items
        """
        count_ = 0
        async for _ in self:
            count_ += 1
        return count_

    async def first_where(
        self,
        func: _ConditionFunc,
        default: _DefaultT = _EMPTY,
    ) -> _T | _DefaultT:
        """Find first item for which the conditional is satisfied

        :param func: condition function
        :param default: default value

        :return: item

        :raise ValueError: the item was not found and default was not provided
        """
        func = asyncify(func)
        async for item in self:
            if await func(item):  # pragma: no cover
                return item

        if default is not _EMPTY:
            return default

        raise ValueError('Item not found')

    async def last_where(
        self,
        func: _ConditionFunc,
        default: _DefaultT = _EMPTY,
    ) -> _T | _DefaultT:
        """Find first item for which the conditional is satisfied

        :param func: condition function
        :param default: default value

        :return: item

        :raise ValueError: the item was not found and default was not provided
        """
        func = asyncify(func)
        last_item = _EMPTY
        async for item in self:
            if await func(item):  # pragma: no cover
                last_item = item

        if last_item is not _EMPTY:
            return last_item

        if default is not _EMPTY:
            return default

        raise ValueError('Item not found')

    @async_iter
    async def where(self, func: _ConditionFunc) -> AsyncIterator[_T]:
        """Filter item by condition

        :return: iterable
        """
        func = asyncify(func)
        async for item in self:
            if await func(item):
                yield item

    @async_iter
    async def take_while(self, func: _ConditionFunc) -> AsyncIterator[_T]:
        """Take items while the conditional is satisfied

        :return: iterable
        """
        func = asyncify(func)
        async for item in self:
            if await func(item):
                yield item
            else:
                break

    async def next(self) -> _T:
        """Returns the first item

        :return: first item
        """
        try:
            return await anext(self)
        except StopAsyncIteration as err:
            raise StopAsyncIteration('Iterable is empty') from err

    async def last(self) -> _T:
        """Returns the last item

        :return: last item
        """
        last_item = initial = object()
        async for item in self:
            last_item = item

        if last_item is initial:
            raise StopAsyncIteration('Iterable is empty')

        return last_item

    @async_iter
    async def chain(self, *iterables: AsyncIterable[_T]) -> AsyncIterator[_T]:
        """Chain with other iterables

        :return: iterable
        """
        async for item in self:
            yield item

        for iterable in iterables:
            async for item in iterable:
                yield item

    async def all(self) -> bool:
        """Checks whether all elements of this iterable are true

        :return: True if all elements is true else False
        """
        async for item in self:
            if not bool(item):  # pragma: no cover
                return False
        return True

    async def any(self) -> bool:
        """Checks whether any element of this iterable is true

        :return: True if any elements are true else False
        """
        async for item in self:
            if bool(item):  # pragma: no cover
                return True
        return False

    @async_iter
    async def mark_first(self) -> AsyncIterator[tuple[_T, bool]]:
        """Mark first item

        :return: Yields: tuple[item, is_first]
        """
        try:
            first = await self.next()
        except StopAsyncIteration:
            return

        yield first, True
        async for item in self:
            yield item, False

    @async_iter
    async def mark_last(self) -> AsyncIterator[tuple[_T, bool]]:
        """Mark last item

        :return: Yields: tuple[item, is_last]
        """
        try:
            previous_item = await self.next()
        except StopAsyncIteration:
            return

        async for current_item in self:
            yield previous_item, False
            previous_item = current_item
        yield previous_item, True

    @async_iter
    async def mark_first_last(self) -> AsyncIterator[tuple[_T, bool, bool]]:
        """Mark first and last item

        :return: Yields: tuple[item, is_first, is_last]
        """
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
        func: _BinaryFunc,
        initial: _T = _EMPTY,
    ) -> _T | _R:
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
            except StopAsyncIteration as err:
                raise ValueError('Iterator is empty') from err

        func = asyncify(func)
        async for item in self:
            initial = await func(initial, item)
        return cast(_T, initial)

    async def max(
        self,
        key: _KeyFunc | None = None,
        default: _DefaultT = _EMPTY,
    ) -> _T | _DefaultT:
        """Return the biggest item.

        :param key: the result of the function will be used to compare the elements.
        :param default: default value in case iterable is empty

        :return: the biggest item

        :raise ValueError: when iterable is empty and default value is not provided
        """
        try:
            max_item = await self.next()
        except StopAsyncIteration as err:
            if default is _EMPTY:
                raise ValueError('Iterator is empty') from err
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
        key: _KeyFunc | None = None,
        default: _DefaultT = _EMPTY,
    ) -> _T | _DefaultT:
        """Return the smallest item.

        :param key: the result of the function will be used to compare the elements.
        :param default: default value in case iterable is empty

        :return: the smallest item

        :raise ValueError: when iterable is empty and default value is not provided
        """
        try:
            max_item = await self.next()
        except StopAsyncIteration as err:
            if default is _EMPTY:
                raise ValueError('Iterator is empty') from err
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
    async def accumulate(
        self,
        func: _BinaryFunc = operator.add,
        initial: _T | None = None,
    ) -> AsyncIterator[_R]:
        """Return series of accumulated sums (by default).

        :param func: func[accumulated value, next value], by default operator.add()
        :param initial: initial value of series

        :return: iterable
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
    async def append_left(self, item: _T) -> AsyncIterator[_T]:
        """Append an item to left of the iterable (start)

        :return: iterable
        """
        yield item
        async for item_ in self:
            yield item_

    @async_iter
    async def append_right(self, item: _T) -> AsyncIterator[_T]:
        """Append an item to right of the iterable (end)

        :return: iterable
        """
        async for item_ in self:
            yield item_
        yield item

    @async_iter
    async def append_at(self, index: int, item: _T) -> AsyncIterator[_T]:
        """Append at the position in to the iterable

        :return: iterable
        """
        i = 0
        async for i, item_ in self.enumerate():
            if i == index:
                yield item
            yield item_
        if index > i:
            yield item

    @async_iter
    async def zip(self, *iterables: AsyncIterator[_T], strict: bool = False) -> AsyncIterator[list[_T]]:
        """The zip object yields n-length tuples, where n is the number of iterables
        passed as positional arguments to zip().  The i-th element in every tuple
        comes from the i-th iterable argument to zip().  This continues until the
        shortest argument is exhausted.

        :return: iterable

        :raise ValueError: when strict is true and one of the arguments is exhausted before the others
        """
        iterables = (self, *iterables)
        while True:
            batch = []
            for it in iterables:
                try:
                    batch.append(await anext(it))
                except StopAsyncIteration:
                    if not strict:
                        return
            if len(batch) != len(iterables):
                raise ValueError('lengths of iterables are not the same')
            yield batch

    @async_iter
    async def zip_longest(
        self,
        *iterables: AsyncIterable[_T],
        fillvalue: _R = None,
    ) -> AsyncIterator[list[_T | _R]]:
        """The zip object yields n-length tuples, where n is the number of iterables
        passed as positional arguments to zip().  The i-th element in every tuple
        comes from the i-th iterable argument to zip().  This continues until the
        longest argument is exhausted.

        :param fillvalue: when the shorter iterables are exhausted, the fillvalue is substituted in their place

        :return: iterable
        """
        iterables = (self, *iterables)
        while True:
            batch = []
            batch_has_any_value = False
            for it in iterables:
                try:
                    batch.append(await anext(it))
                    batch_has_any_value = True
                except StopAsyncIteration:
                    batch.append(fillvalue)
            if not batch_has_any_value:
                return
            yield batch

    @async_iter
    async def islice(self, start: int = 0, stop: int | None = None, step: int = 1) -> AsyncIterator[_T]:
        """Return slice from the iterable

        :return: iterable
        """
        it = self.skip(start)

        if stop is not None:
            it = it.take(stop - start)

        async for i, item in it.enumerate():
            if i % step == 0:
                yield item

    async def item_at(self, index: int) -> _T:
        """Return item at index

        :return: item
        """
        async for i, item in self.enumerate():
            if i == index:
                return item
        raise IndexError(f'item at {index} index is not found')

    async def contains(self, item: _T) -> bool:
        """Return True if the iterable contains item

        :return: True if the iterable contains item
        """
        return await self.first_where(lambda x: x == item, default=None) is not None

    async def is_empty(self) -> bool:
        """Return True if iterable is empty

        :return: Return True if iterable is empty
        """
        try:
            await self.next()
        except StopAsyncIteration:
            return True
        return False

    @async_iter
    async def pairwise(self) -> AsyncIterator[tuple[_T, _T]]:
        """Return an iterable of overlapping pairs

        :return: tuple[item_0, item_1], tuple[item_1, item_2], ...
        """
        try:
            previous = await self.next()
        except StopAsyncIteration:
            return
        async for item in self:
            yield previous, item
            previous = item

    @async_iter
    async def batches(self, batch_size: int) -> AsyncIterator[tuple[_T, ...]]:
        """Create iterator of tuples whose length = batch_size

        :return: iterator of tuples whose length = batch_size
        """
        while True:
            try:
                item = await self.next()
            except StopAsyncIteration:
                break
            it = self.append_left(item)
            batch = await it.take(batch_size).to_tuple()
            yield batch

    @async_iter
    async def flatten(self: 'AsyncIter[AsyncIterator[_T]]') -> AsyncIterator[_T]:
        """Return an iterator that flattens one level of nesting

        :return: async iterable of flattened items

        :raise TypeError: if an encountered item is neither an Iterable nor an AsyncIterable
        """
        async for iterable in self:
            if isinstance(iterable, Iterable):
                for item in iterable:
                    yield item
            elif isinstance(iterable, AsyncIterable):
                async for item in iterable:
                    yield item
            else:
                raise TypeError(
                    f"Item of type {type(iterable)} is not iterable"
                )
