import functools
import itertools
import operator
from functools import wraps
from typing import Iterable, TypeVar, Callable, Generic, ParamSpec, TypeAlias, Iterator

from .empty_iterator import EmptyIterator

T = TypeVar('T')
R = TypeVar('R')
P = ParamSpec('P')
DefaultT = TypeVar('DefaultT')

KeyFunc: TypeAlias = Callable[[T], R]
BinaryFunc: TypeAlias = Callable[[T, T], T]
ConditionFunc: TypeAlias = Callable[[T], bool]
_EMPTY = object()


def sync_iter(func: Callable[P, Iterable[T]]) -> Callable[P, 'SyncIter[T]']:
    """Convert result of the func to SyncIter

    Usage:
    ```python
    @sync_iter
    def my_generator() -> SyncIter[int]:
        for i in range(10):
            yield i
    ```

    :param func: function that returns iterable
    :return: new function
    """
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> 'SyncIter[T]':
        return SyncIter(func(*args, **kwargs))
    return wrapper


class SyncIter(Generic[T]):

    __slots__ = ('_it', )

    def __init__(self, it: Iterable[T] | Iterator[T]):
        self._it: Iterator[T] = iter(it)

    def __iter__(self) -> Iterator[T]:
        return self._it

    def __next__(self) -> T:
        return next(self._it)

    @classmethod
    def empty(cls) -> 'SyncIter[T]':
        """Create empty iterable

        :return: empty iterable
        """
        return cls(EmptyIterator())

    def to_list(self) -> list[T]:
        """Convert to list

        :return: list of items
        """
        return list(self._it)

    def to_tuple(self) -> tuple[T, ...]:
        """Convert to tuple

        :return: tuple of items
        """
        return tuple(self._it)

    def to_set(self) -> set[T]:
        """Convert to set

        :return: set of items
        """
        return set(self._it)

    def enumerate(self, start: int = 0) -> 'SyncIter[tuple[int, T]]':
        """Returns a tuple containing a count (from start which defaults to 0)
        and the values obtained from iterating over self.

        :param start: start of count
        :return: interator of tuple[count, item]
        """
        return SyncIter(enumerate(self, start=start))

    def take(self, count: int) -> 'SyncIter[T]':
        """Take 'count' items from iterator

        :return: iterable that contains 'count' items
        """
        return SyncIter(itertools.islice(self, count))

    def map(self, func: Callable[[T], R]) -> 'SyncIter[R]':
        """Return an iterator that applies function to every item of iterable,
         yielding the results

         :return: async iterable
         """
        return SyncIter(map(func, self))

    @sync_iter
    def skip(self, count: int) -> 'SyncIter[T]':
        """Skip 'count' items from iterator

        :return: async iterable
        """
        for index, item in self.enumerate():
            if index >= count:
                yield item

    def skip_while(self, func: ConditionFunc) -> 'SyncIter[T]':
        """Skips leading elements while conditional is satisfied

        :return: async iterable
        """
        return SyncIter(itertools.dropwhile(func, self))

    def count(self) -> int:
        """Return count of items in iterator

        :return: count of items
        """
        count_ = 0
        for _ in self:
            count_ += 1
        return count_

    def first_where(
        self,
        func: ConditionFunc,
        default: DefaultT = _EMPTY,
    ) -> T | DefaultT:
        """Find first item for which the conditional is satisfied

        :param func: condition function
        :param default: default value

         :return: item

        :raise ValueError: the item was not found and default was not provided
        """
        for item in self:
            if func(item):
                return item

        if default is not _EMPTY:
            return default

        raise ValueError('Item not found')

    def last_where(
        self,
        func: ConditionFunc,
        default: DefaultT = _EMPTY,
    ) -> T | DefaultT:
        """Find last item for which the conditional is satisfied

        :param func: condition function
        :param default: default value

        :return: item

        :raise ValueError: the item was not found and default was not provided
        """
        last_item = _EMPTY
        for item in self:
            if func(item):
                last_item = item

        if last_item is not _EMPTY:
            return last_item

        if default is not _EMPTY:
            return default

        raise ValueError('Item not found')

    def where(self, func: ConditionFunc) -> 'SyncIter[T]':
        """Filter items by condition

        :return: iterable
        """
        return SyncIter(filter(func, self))

    def take_while(self, func: ConditionFunc) -> 'SyncIter[T]':
        """Take items while the conditional is satisfied

        :return: iterable
        """
        return SyncIter(itertools.takewhile(func, self))

    def next(self) -> T:
        """Returns the next item

        :return: first item
        """
        try:
            return next(self)
        except StopIteration:
            raise StopIteration('Iterable is empty')

    def last(self) -> T:
        """Return the last item

        :return: last item
        """
        last_item = initial = object()
        for item in self:
            last_item = item

        if last_item is initial:
            raise StopIteration('Iterable is empty')

        return last_item

    def chain(self, *iterables: Iterable[T]) -> 'SyncIter[T]':
        """Chain with other iterables

        :return: iterable
        """
        return SyncIter(itertools.chain(self, *iterables))

    def all(self) -> bool:
        """Checks whether all elements of this iterable are true

        :return: True if all elements is true else False
        """
        return all(self)

    def any(self) -> bool:
        """Checks whether any element of this iterable is true

        :return: True if any elements are true else False
        """
        return any(self)

    def first(self) -> T:
        """Return first item. The same as next()

        :return: first item
        """
        return self.next()

    @sync_iter
    def mark_first(self) -> 'SyncIter[tuple[T, bool]]':
        """Mark first item.

        :return: Yields: tuple[item, is_first]
        """
        try:
            first = self.next()
        except StopIteration:
            return

        yield first, True
        yield from self.map(lambda item: (item, False))

    @sync_iter
    def mark_last(self) -> 'SyncIter[tuple[T, bool]]':
        """Mark last item

        :return: Yields: tuple[item, is_last]
        """
        try:
            previous_item = self.next()
        except StopIteration:
            return

        for current_item in self:
            yield previous_item, False
            previous_item = current_item
        yield previous_item, True

    @sync_iter
    def mark_first_last(self) -> 'SyncIter[tuple[T, bool, bool]]':
        """Mark first and last item

        :return: Yields: tuple[item, is_first, is_last]
        """
        try:
            previous_item = self.next()
        except StopIteration:
            return

        first = True
        for current_item in self:
            yield previous_item, first, False
            first = False
            previous_item = current_item
        yield previous_item, first, True

    def reduce(
        self,
        func: BinaryFunc,
        initial: T = _EMPTY,
    ) -> T | DefaultT:
        """Apply the func of two arguments cumulatively to the items of an iterable,
         from left to right, to reduce the iterable to a single value.

        :param func: func[accumulated value, next item]
        :param initial: initial value of iterable. Serves like default value if iterable is empty.

        :return: reduced value

        :raise ValueError: if initial is not provided and iterable is empty
        """
        if initial is _EMPTY:
            try:
                return functools.reduce(func, self)
            except TypeError:
                raise ValueError('Iterator is empty')
        else:
            return functools.reduce(func, self, initial)

    def max(
        self,
        key: KeyFunc | None = None,
        default: DefaultT = _EMPTY,
    ) -> T | DefaultT:
        """Return the biggest item.

        :param key: the result of the function will be used to compare the elements.
        :param default: default value in case iterable is empty

        :return: the biggest item

        :raise ValueError: when iterable is empty and default value is not provided
        """
        if default is _EMPTY:
            return max(self, key=key)
        else:
            return max(self, key=key, default=default)

    def min(
        self,
        key: KeyFunc | None = None,
        default: DefaultT = _EMPTY,
    ) -> T | DefaultT:
        """Return the smallest item.

        :param key: the result of the function will be used to compare the elements.
        :param default: default value in case iterable is empty

        :return: the smallest item

        :raise ValueError: when iterable is empty and default value is not provided
        """
        if default is _EMPTY:
            return min(self, key=key)
        else:
            return min(self, key=key, default=default)

    def accumulate(self, func: BinaryFunc = operator.add, initial: T | None = None) -> 'SyncIter[T]':
        """Return series of accumulated sums (by default).

        :param func: func[accumulated value, next value], by default operator.add
        :param initial: initial value of series

         :return: iterable
        """
        return SyncIter(itertools.accumulate(self, func=func, initial=initial))

    @sync_iter
    def append_left(self, item: T) -> 'SyncIter[T]':
        """Append an item to left of the iterable (start)

         :return: iterable
        """
        yield item
        yield from self

    @sync_iter
    def append_right(self, item: T) -> 'SyncIter[T]':
        """Append an item to right of the iterable (end)

         :return: iterable
        """
        yield from self
        yield item

    @sync_iter
    def append_at(self, index: int, item: T) -> 'SyncIter[T]':
        """Append at the position in to the iterable

         :return: iterable
        """
        i = 0
        for i, item_ in self.enumerate():
            if i == index:
                yield item
            yield item_
        if index > i:
            yield item

    def zip(self, *iterables: Iterable[T], strict: bool = False) -> 'SyncIter[tuple[T, ...]]':
        """The zip object yields n-length tuples, where n is the number of iterables
        passed as positional arguments to zip().  The i-th element in every tuple
        comes from the i-th iterable argument to zip().  This continues until the
        shortest argument is exhausted.

        :return: iterable

        :raise ValueError: when strict is true and one of the arguments is exhausted before the others
        """
        return SyncIter(zip(self, *iterables, strict=strict))

    def zip_longest(self, *iterables: Iterable[T], fillvalue: R = None) -> 'SyncIter[tuple[T | R, ...]]':
        """The zip object yields n-length tuples, where n is the number of iterables
        passed as positional arguments to zip().  The i-th element in every tuple
        comes from the i-th iterable argument to zip().  This continues until the
        longest argument is exhausted.

        :return: iterable

        :param fillvalue: when the shorter iterables are exhausted, the fillvalue is substituted in their place
        """
        return SyncIter(itertools.zip_longest(self, *iterables, fillvalue=fillvalue))

    def get_slice(self, start: int = 0, stop: int | None = None, step: int = 1) -> 'SyncIter[T]':
        """Return slice from the iterable

        :return: iterable
        """
        return SyncIter(itertools.islice(self, start, stop, step))

    def item_at(self, index: int) -> T:
        """Return item at index

        :return: item
        """
        for i, item in self.enumerate():
            if i == index:
                return item
        raise IndexError(f'item at {index} index is not found')

    def contains(self, item: T) -> bool:
        """Return True if the iterable contains item

        :return: bool
        """
        return self.first_where(lambda x: x == item, default=None) is not None

    def is_empty(self) -> bool:
        """Return True if the iterable is empty

        :return: bool
        """
        try:
            self.next()
        except StopIteration:
            return True
        return False

    def is_not_empty(self) -> bool:
        """Return True if iterable is not empty

        :return: bool
        """
        return not self.is_empty()

    def pairwise(self) -> 'SyncIter[tuple[T, T]]':
        """Return an iterable of overlapping pairs

        :return: tuple[item_0, item_1], tuple[item_1, item_2], ...
        """
        return SyncIter(itertools.pairwise(self))

    def get_len(self) -> int:
        """Return len of iterable

        :return: length
        """
        count = 0
        for _ in self:
            count += 1
        return count

    @sync_iter
    def batches(self, batch_size: int) -> 'SyncIter[tuple[T, ...]]':
        """Create iterable of tuples whose length = batch_size

        :return: iterable of tuples whose length = batch_size
        """
        while True:
            try:
                item = self.next()
            except StopIteration:
                break
            it = self.append_left(item)
            batch = it.take(batch_size).to_tuple()
            yield batch

    def __len__(self) -> int:
        return self.get_len()

    def __getitem__(self, index: int | slice) -> T | 'SyncIter[T]':
        if isinstance(index, slice):
            return self.get_slice(
                start=index.start or 0,
                stop=index.stop or None,
                step=index.step or 1,
            )
        return self.item_at(index)

    def __contains__(self, item: T) -> bool:
        return self.contains(item)
