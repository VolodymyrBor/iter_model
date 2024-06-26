from typing import Callable, Generic, Iterable, Iterator, ParamSpec, TypeVar, overload

_T = TypeVar('_T')
_R = TypeVar('_R')
_P = ParamSpec('_P')
_DefaultT = TypeVar('_DefaultT')
_KeyFunc = Callable[[_T], _R]
_BinaryFunc = Callable[[_T, _T], _T]
_ConditionFunc = Callable[[_T], bool]

def sync_iter(func: Callable[_P, Iterable[_T]]) -> Callable[_P, SyncIter[_T]]: ...

class SyncIter(Generic[_T]):
    _it: Iterator[_T]

    def __init__(self, it: Iterable[_T] | Iterator[_T]) -> None: ...
    def __iter__(self) -> Iterator[_T]: ...
    def __next__(self) -> _T: ...
    @classmethod
    def empty(cls) -> SyncIter[_T]: ...
    def to_list(self) -> list[_T]: ...
    def to_tuple(self) -> tuple[_T, ...]: ...
    def to_set(self) -> set[_T]: ...
    def enumerate(self, start: int = ...) -> SyncIter[tuple[int, _T]]: ...
    def take(self, count: int) -> SyncIter[_T]: ...
    def map(self, func: Callable[[_T], _R]) -> SyncIter[_R]: ...
    def skip(self, count: int) -> SyncIter[_T]: ...
    def skip_while(self, func: _ConditionFunc) -> SyncIter[_T]: ...
    def skip_where(self, func: _ConditionFunc) -> SyncIter[_T]: ...
    def count(self) -> int: ...
    def first_where(self, func: _ConditionFunc, default: _DefaultT = ...) -> _T | _DefaultT: ...
    def last_where(self, func: _ConditionFunc, default: _DefaultT = ...) -> _T | _DefaultT: ...
    def where(self, func: _ConditionFunc) -> SyncIter[_T]: ...
    def take_while(self, func: _ConditionFunc) -> SyncIter[_T]: ...
    def next(self) -> _T: ...
    def last(self) -> _T: ...
    def chain(self, *iterables: Iterable[_T]) -> SyncIter[_T]: ...
    def all(self) -> bool: ...
    def any(self) -> bool: ...
    def mark_first(self) -> SyncIter[tuple[_T, bool]]: ...
    def mark_last(self) -> SyncIter[tuple[_T, bool]]: ...
    def mark_first_last(self) -> SyncIter[tuple[_T, bool, bool]]: ...
    def reduce(self, func: _BinaryFunc, initial: _T = ...) -> _T | _DefaultT: ...
    def max(self, key: _KeyFunc | None = ..., default: _DefaultT = ...) -> _T | _DefaultT: ...
    def min(self, key: _KeyFunc | None = ..., default: _DefaultT = ...) -> _T | _DefaultT: ...
    def accumulate(self, func: _BinaryFunc = ..., initial: _T | None = ...) -> SyncIter[_T]: ...
    def append_left(self, item: _T) -> SyncIter[_T]: ...
    def append_right(self, item: _T) -> SyncIter[_T]: ...
    def append_at(self, index: int, item: _T) -> SyncIter[_T]: ...
    def zip(self, *iterables: Iterable[_T], strict: bool = ...) -> SyncIter[tuple[_T, ...]]: ...
    def zip_longest(self, *iterables: Iterable[_T], fillvalue: _R = ...) -> SyncIter[tuple[_T | _R, ...]]: ...
    def islice(self, start: int = ..., stop: int | None = ..., step: int = ...) -> SyncIter[_T]: ...
    def item_at(self, index: int) -> _T: ...
    def contains(self, item: _T) -> bool: ...
    def is_empty(self) -> bool: ...
    def pairwise(self) -> SyncIter[tuple[_T, _T]]: ...
    def batches(self, batch_size: int) -> SyncIter[tuple[_T, ...]]: ...
    def flatten(self) -> SyncIter[_T]: ...
    def __len__(self) -> int: ...

    @overload
    def __getitem__(self, index: int) -> _T: ...

    @overload
    def __getitem__(self, index: slice) -> SyncIter[_T]: ...

    def __contains__(self, item: _T) -> bool: ...
