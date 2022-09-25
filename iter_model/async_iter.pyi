import operator
from typing import (
    TypeVar,
    Generic,
    overload,
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
DefaultT = TypeVar('DefaultT')
KeyFunc: TypeAlias = Callable[[T], R | Awaitable[R]]
BinaryFunc: TypeAlias = Callable[[T, T], R | Awaitable[R]]
ConditionFunc: TypeAlias = Callable[[T], bool | Awaitable[bool]]

_EMPTY = object()


class AsyncIter(Generic[T]):

    def __init__(self, it: AsyncIterable[T]):
        self._it: AsyncIterator[T] = NotImplemented

    def __aiter__(self) -> AsyncIterator[T]: ...

    def __anext__(self) -> Awaitable[T]: ...

    @classmethod
    def from_sync(cls, it: Iterable[T]) -> AsyncIter[T]: ...

    @classmethod
    def empty(cls) -> AsyncIter[T]: ...

    async def to_list(self) -> list[T]: ...

    async def to_tuple(self) -> tuple[T, ...]: ...

    async def to_set(self) -> set[T]: ...

    def enumerate(self, start: int = 0) -> AsyncIter[tuple[int, T]]: ...

    def take(self, limit: int) -> AsyncIter[T]: ...

    def map(self, func: Callable[[T], R | Awaitable[R]]) -> AsyncIter[R]: ...

    def skip(self, count: int) -> AsyncIter[T]: ...

    def skip_while(self, func: ConditionFunc) -> AsyncIter[T]: ...

    async def count(self) -> int: ...

    async def first_where(
        self,
        func: ConditionFunc,
        default: DefaultT = _EMPTY,  # type: ignore
    ) -> T | DefaultT: ...

    async def last_where(
        self,
        func: ConditionFunc,
        default: DefaultT = _EMPTY,  # type: ignore
    ) -> T | DefaultT: ...

    def where(self, func: ConditionFunc) -> AsyncIter[T]: ...

    def take_while(self, func: ConditionFunc) -> AsyncIter[T]:  ...

    async def next(self) -> T: ...

    async def last(self) -> T: ...

    def chain(self, *iterables: AsyncIterable[T]) -> AsyncIter[T]: ...

    async def all(self) -> bool: ...

    async def any(self) -> bool: ...

    async def first(self) -> T: ...

    def mark_first(self) -> AsyncIter[tuple[T, bool]]: ...

    def mark_last(self) -> AsyncIter[tuple[T, bool]]: ...

    def mark_first_last(self) -> AsyncIter[tuple[T, bool, bool]]: ...

    async def reduce(
        self,
        func: BinaryFunc,
        initial: T = _EMPTY,  # type: ignore
    ) -> T | R: ...

    async def max(
        self,
        key: KeyFunc | None = None,
        default: DefaultT = _EMPTY,  # type: ignore
    ) -> T | DefaultT: ...

    async def min(
        self,
        key: KeyFunc | None = None,
        default: DefaultT = _EMPTY,  # type: ignore
    ) -> T | DefaultT: ...

    def accumulate(
        self,
        func: BinaryFunc = operator.add,
        initial: T | None = None,
    ) -> AsyncIter[R]: ...

    def append_left(self, item: T) -> AsyncIter[T]: ...

    def append_right(self, item: T) -> AsyncIter[T]: ...

    def append_at(self, index: int, item: T) -> AsyncIter[T]: ...

    def zip(self, *iterables: AsyncIterable[T], strict: bool = False) -> AsyncIter[list[T]]: ...

    def zip_longest(
        self,
        *iterables: AsyncIterable[T],
        fillvalue: R = None,
    ) -> AsyncIter[list[T | R]]: ...

    def get_slice(self, start: int = 0, stop: int | None = None, step: int = 1) -> AsyncIter[T]: ...

    async def item_at(self, index: int) -> T: ...

    async def contains(self, item: T) -> bool: ...

    async def is_empty(self) -> bool: ...

    async def is_not_empty(self) -> bool: ...

    def pairwise(self) -> AsyncIter[tuple[T, T]]: ...

    async def get_len(self) -> int: ...

    @overload
    def __getitem__(self, index: int) -> Awaitable[T]: ...

    @overload
    def __getitem__(self, index: slice) -> AsyncIter[T]: ...

def async_iter(
    func: Callable[P, AsyncIterable[T] | AsyncIterator[T]],
) -> Callable[P, AsyncIter[T]]: ...
