import itertools
from functools import wraps
from typing import Iterable, TypeVar, Callable, Generic, ParamSpec, TypeAlias

T = TypeVar('T')
R = TypeVar('R')
P = ParamSpec('P')
ConditionFunc: TypeAlias = Callable[[T], bool]


def sync_iter(func: Callable[P, Iterable[T]]) -> Callable[P, 'SyncIter[T]']:
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
        return list(self)

    def enumerate(self, start: int = 0) -> 'SyncIter[tuple[int, T]]':
        return SyncIter(enumerate(self, start=start))

    def take(self, count: int) -> 'SyncIter[T]':
        return SyncIter(itertools.islice(self, count))

    def map(self, func: Callable[[T], R]) -> 'SyncIter[R]':
        return SyncIter(map(func, self))

    @sync_iter
    def skip(self, count: int) -> 'SyncIter[T]':
        for index, item in self.enumerate():
            if index >= count:
                yield item

    def count(self) -> int:
        count_ = 0
        for _ in self:
            count_ += 1
        return count_

    def first_where(self, func: ConditionFunc) -> T:
        for item in self:
            if func(item):
                return item
        raise ValueError('Item not found')

    def where(self, func: ConditionFunc) -> 'SyncIter[T]':
        return SyncIter(filter(func, self))

    def take_while(self, func: ConditionFunc) -> 'SyncIter[T]':
        return SyncIter(itertools.takewhile(func, self))
