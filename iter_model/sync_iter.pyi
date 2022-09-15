import operator
from typing import Generic, TypeVar, ParamSpec, TypeAlias, Callable, Awaitable, Iterable, Iterator

T = TypeVar('T')
R = TypeVar('R')
P = ParamSpec('P')
DefaultT = TypeVar('DefaultT')
KeyFunc: TypeAlias = Callable[[T], R | Awaitable[R]]
BinaryFunc: TypeAlias = Callable[[T, T], R | Awaitable[R]]
ConditionFunc: TypeAlias = Callable[[T], bool | Awaitable[bool]]
_EMPTY = object()


class SyncIter(Generic[T]):

    def __init__(self, it: Iterable[T]):
        self._it: Iterator[T] = NotImplemented

    def __iter__(self) -> Iterator[T]: ...

    def __next__(self) -> T: ...

    def to_list(self) -> list[T]: ...

    def to_tuple(self) -> tuple[T, ...]: ...

    def to_set(self) -> set[T]: ...

    def enumerate(self, start: int = 0) -> SyncIter[tuple[int, T]]: ...

    def take(self, count: int) -> SyncIter[T]: ...

    def map(self, func: Callable[[T], R]) -> SyncIter[R]: ...

    def skip(self, count: int) -> SyncIter[T]: ...

    def skip_while(self, func: ConditionFunc) -> SyncIter[T]: ...

    def count(self) -> int: ...

    def first_where(
        self,
        func: ConditionFunc,
        default: DefaultT = _EMPTY,  # type: ignore
    ) -> T | DefaultT: ...

    def where(self, func: ConditionFunc) -> SyncIter[T]: ...

    def take_while(self, func: ConditionFunc) -> SyncIter[T]: ...

    def next(self) -> T: ...

    def last(self) -> T: ...

    def chain(self, *iterables: Iterable[T]) -> SyncIter[T]: ...

    def all(self) -> bool: ...

    def any(self) -> bool: ...

    def first(self) -> T: ...

    def mark_first(self) -> SyncIter[tuple[T, bool]]: ...

    def mark_last(self) -> SyncIter[tuple[T, bool]]: ...

    def mark_first_last(self) -> SyncIter[tuple[T, bool, bool]]: ...

    def reduce(
        self,
        func: BinaryFunc,
        initial: T = _EMPTY,  # type: ignore
    ) -> T | DefaultT: ...

    def max(
        self,
        key: KeyFunc | None = None,
        default: DefaultT = _EMPTY,  # type: ignore
    ) -> T | DefaultT: ...

    def min(
        self,
        key: KeyFunc | None = None,
        default: DefaultT = _EMPTY,  # type: ignore
    ) -> T | DefaultT: ...

    def accumulate(self, func: BinaryFunc = operator.add, initial: T | None = None) -> SyncIter[T]: ...

    def append_left(self, item: T) -> SyncIter[T]: ...

    def append_right(self, item: T) -> SyncIter[T]: ...

    def append_at(self, index: int, item: T) -> SyncIter[T]: ...

    def zip(self, *iterables: Iterable[T], strict: bool = False) -> SyncIter[tuple[T, ...]]: ...

    def zip_longest(self, *iterables: Iterable[T], fillvalue: R = None) -> SyncIter[tuple[T | R, ...]]: ...

    def slice(self, start: int = 0, stop: int | None = None, step: int = 1) -> SyncIter[T]: ...


def sync_iter(
    func: Callable[P, Iterable[T] | Iterator[T]],
) -> Callable[P, SyncIter[T]]: ...
