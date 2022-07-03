import itertools
from functools import wraps
from typing import Iterable, TypeVar, Callable, Generic, ParamSpec, TypeAlias, Iterator

T = TypeVar('T')
R = TypeVar('R')
P = ParamSpec('P')
ConditionFunc: TypeAlias = Callable[[T], bool]


def sync_iter(func: Callable[P, Iterable[T]]) -> Callable[P, 'SyncIter[T]']:
    """Convert result of the func to SyncIter

    :param func: function that returns iterable
    :return: new function
    """
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> 'SyncIter[T]':
        return SyncIter(func(*args, **kwargs))
    return wrapper


class SyncIter(Generic[T]):

    __slots__ = ('_it', )

    def __init__(self, it: Iterable[T]):
        self._it = iter(it)

    def __iter__(self) -> Iterator[T]:
        return self._it

    def __next__(self) -> T:
        return next(self._it)

    def to_list(self) -> list[T]:
        """Convert to list"""
        return list(self)

    def to_tuple(self) -> tuple[T, ...]:
        """Convert to tuple"""
        return tuple(self)

    def to_set(self) -> set[T]:
        """Convert to set"""
        return set(self)

    def enumerate(self, start: int = 0) -> 'SyncIter[tuple[int, T]]':
        """Returns a tuple containing a count (from start which defaults to 0)
        and the values obtained from iterating over self.

        :param start: start of index
        :return: interator of tuple[index, item]
        """
        return SyncIter(enumerate(self, start=start))

    def take(self, count: int) -> 'SyncIter[T]':
        """Take 'count' items from iterator"""
        return SyncIter(itertools.islice(self, count))

    def map(self, func: Callable[[T], R]) -> 'SyncIter[R]':
        """Return an iterator that applies function to every item of iterable,
         yielding the results"""
        return SyncIter(map(func, self))

    @sync_iter
    def skip(self, count: int) -> 'SyncIter[T]':  # type: ignore
        """Skip 'count' items from iterator"""
        for index, item in self.enumerate():
            if index >= count:
                yield item

    def skip_while(self, func: ConditionFunc) -> 'SyncIter[T]':
        """Skips leading elements while conditional is satisfied"""
        return SyncIter(itertools.dropwhile(func, self))

    def count(self) -> int:
        """Return count of items in iterator"""
        count_ = 0
        for _ in self:
            count_ += 1
        return count_

    def first_where(self, func: ConditionFunc) -> T:
        """Find first item for which the conditional is satisfied

        :raise StopIteration: the item not found
        """
        for item in self:
            if func(item):
                return item
        raise ValueError('Item not found')

    def where(self, func: ConditionFunc) -> 'SyncIter[T]':
        """Filter item by condition"""
        return SyncIter(filter(func, self))

    def take_while(self, func: ConditionFunc) -> 'SyncIter[T]':
        """Take items while the conditional is satisfied"""
        return SyncIter(itertools.takewhile(func, self))

    def next(self) -> T:
        """Returns the first item"""
        try:
            return next(self)
        except StopIteration:
            raise StopIteration('Iterable is empty')

    def last(self) -> T:
        """Returns the last item"""
        last_item = initial = object()
        for item in self:
            last_item = item

        if last_item is initial:
            raise StopIteration('Iterable is empty')

        return last_item  # type: ignore

    def chain(self, *iterables: Iterable[T]) -> 'SyncIter[T]':
        """Chain with other iterables"""
        return SyncIter(itertools.chain(self, *iterables))

    def all(self) -> bool:
        """Checks whether all element of this iterable satisfies"""
        return all(self)

    def any(self) -> bool:
        """Checks whether any element of this iterable satisfies"""
        return any(self)

    def first(self) -> T:
        """Returns first item"""
        return self.next()

    @sync_iter
    def mark_first(self) -> 'SyncIter[tuple[T, bool]]':  # type: ignore
        """Mark first item. Yields: tuple[item, is_first]"""
        try:
            first = self.next()
        except StopIteration:
            return

        yield first, True
        yield from self.map(lambda item: (item, False))

    @sync_iter
    def mark_last(self) -> 'SyncIter[tuple[T, bool]]':  # type: ignore
        """Mark last item. Yields: tuple[item, is_last]"""
        try:
            previous_item = self.next()
        except StopIteration:
            return

        for current_item in self:
            yield previous_item, False
            previous_item = current_item
        yield previous_item, True

    @sync_iter
    def mark_first_last(self) -> 'SyncIter[tuple[T, bool, bool]]':  # type: ignore
        """Mark first and last item. Yields: tuple[item, is_first, is_last]"""
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
