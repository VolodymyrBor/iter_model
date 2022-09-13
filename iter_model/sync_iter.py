import functools
import itertools
import operator
from functools import wraps
from typing import Iterable, TypeVar, Callable, Generic, ParamSpec, TypeAlias, Iterator

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

        :param start: start of count
        :return: interator of tuple[count, item]
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

        :raise ValueError: the item was not found
        """
        for item in self:
            if func(item):
                return item
        raise ValueError('Item not found')

    def where(self, func: ConditionFunc) -> 'SyncIter[T]':
        """Filter items by condition"""
        return SyncIter(filter(func, self))

    def take_while(self, func: ConditionFunc) -> 'SyncIter[T]':
        """Take items while the conditional is satisfied"""
        return SyncIter(itertools.takewhile(func, self))

    def next(self) -> T:
        """Returns the next item"""
        try:
            return next(self)
        except StopIteration:
            raise StopIteration('Iterable is empty')

    def last(self) -> T:
        """Return the last item"""
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
        """Checks whether all elements of this iterable are true"""
        return all(self)

    def any(self) -> bool:
        """Checks whether any element of this iterable is true"""
        return any(self)

    def first(self) -> T:
        """Return first item. The same as next()"""
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

    def reduce(
        self,
        func: BinaryFunc,
        initial: T = _EMPTY,  # type: ignore
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
        default: DefaultT = _EMPTY,  # type: ignore
    ) -> T | DefaultT:
        """Return the biggest item.

        :param key: the result of the function will be used to compare the elements.
        :param default: default value in case iterable is empty
        :return: the biggest item
        :raise ValueError: when iterable is empty and default value is not provided
        """
        if default is _EMPTY:
            return max(self, key=key)  # type: ignore
        else:
            return max(self, key=key, default=default)  # type: ignore

    def min(
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
        if default is _EMPTY:
            return min(self, key=key)  # type: ignore
        else:
            return min(self, key=key, default=default)  # type: ignore

    def accumulate(self, func: BinaryFunc = operator.add, initial: T | None = None) -> 'SyncIter[T]':
        """Return series of accumulated sums (by default).

        :param func: func[accumulated value, next value], by default operator.add
        :param initial: initial value of series
        """
        return SyncIter(itertools.accumulate(self, func=func, initial=initial))

    @sync_iter
    def append_left(self, item: T) -> 'SyncIter[T]':  # type: ignore
        """Append an item to left of the iterable (start)"""
        yield item
        yield from self

    @sync_iter
    def append_right(self, item: T) -> 'SyncIter[T]':  # type: ignore
        """Append an item to right of the iterable (end)"""
        yield from self
        yield item

    @sync_iter
    def append_at(self, index: int, item: T) -> 'SyncIter[T]':  # type: ignore
        """Append at the position in to the iterable"""
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

        :raise ValueError: when strict is true and one of the arguments is exhausted before the others
        """
        return SyncIter(zip(self, *iterables, strict=strict))

    def zip_longest(self, *iterables: Iterable[T], fillvalue: R = None) -> 'SyncIter[tuple[T | R, ...]]':
        """The zip object yields n-length tuples, where n is the number of iterables
        passed as positional arguments to zip().  The i-th element in every tuple
        comes from the i-th iterable argument to zip().  This continues until the
        longest argument is exhausted.

        :param fillvalue: when the shorter iterables are exhausted, the fillvalue is substituted in their place
        """
        return SyncIter(itertools.zip_longest(self, *iterables, fillvalue=fillvalue))

    def slice(self, start: int = 0, stop: int | None = None, step: int = 1) -> 'SyncIter[T]':
        return SyncIter(itertools.islice(self, start, stop, step))
