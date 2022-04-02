import itertools
from functools import wraps
from typing import Iterable, TypeVar, Callable, Generic, ParamSpec, TypeAlias

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

    def __init__(self, it: Iterable[T]):
        self._it = iter(it)

    def __iter__(self) -> Iterable[T]:
        return self._it

    def to_list(self) -> list[T]:
        """Convert self to list"""
        return list(self)

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
    def skip(self, count: int) -> 'SyncIter[T]':
        """Skip 'count' items from iterator"""
        for index, item in self.enumerate():
            if index >= count:
                yield item

    def count(self) -> int:
        """Return count of items in iterator"""
        count_ = 0
        for _ in self:
            count_ += 1
        return count_

    def first_where(self, func: ConditionFunc) -> T:
        """Find first item for which the condition is met

        :raise ValueError: the item not found
        """
        for item in self:
            if func(item):
                return item
        raise ValueError('Item not found')

    def where(self, func: ConditionFunc) -> 'SyncIter[T]':
        """Filter item by condition"""
        return SyncIter(filter(func, self))

    def take_while(self, func: ConditionFunc) -> 'SyncIter[T]':
        """Take items while the condition is met"""
        return SyncIter(itertools.takewhile(func, self))
