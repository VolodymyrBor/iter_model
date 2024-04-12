from typing import Awaitable, Callable, ParamSpec, TypeVar

T = TypeVar('T')
R = TypeVar('R')
P = ParamSpec('P')

def asyncify(func: Callable[P, R | Awaitable[R]]) -> Callable[P, Awaitable[R]]: ...
