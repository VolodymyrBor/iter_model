from typing import Awaitable, Callable, ParamSpec, TypeVar

_T = TypeVar('_T')
_R = TypeVar('_R')
_P = ParamSpec('_P')

def asyncify(func: Callable[_P, _R | Awaitable[_R]]) -> Callable[_P, Awaitable[_R]]: ...
