import itertools
from typing import Callable

import pytest

from iter_model import AsyncIter, async_iter
from tests.utils import to_async_iter, to_async


class TestAsyncIter:

    async def test_to_list(self):
        r = range(5)
        actual_list = await AsyncIter(to_async_iter(r)).to_list()
        assert isinstance(actual_list, list)
        assert actual_list == list(r)

    @pytest.mark.parametrize('start', (-5, 0, 1, 5))
    async def test_enumerate(self, start: int):
        list_ = ['First', 'Second', 'Third']
        assert await AsyncIter(to_async_iter(list_)).enumerate(start).to_list() == list(enumerate(list_, start=start))

    @pytest.mark.parametrize('count', (0, 5, 100))
    async def test_take(self, count: int):
        r = range(10)
        assert await AsyncIter(to_async_iter(r)).take(count).to_list() == list(itertools.islice(r, count))

    @pytest.mark.parametrize('func', (lambda x: x ** 2, to_async(lambda x: x ** 2)))
    async def test_map(self, func: Callable):
        r = range(10)
        assert await AsyncIter(to_async_iter(r)).map(func).to_list() == [x ** 2 for x in range(10)]

    @pytest.mark.parametrize('count', (0, 5, 100))
    async def test_skip(self, count: int):
        r = range(10)
        assert await AsyncIter(to_async_iter(r)).skip(count).to_list() == list(r)[count:]

    @pytest.mark.parametrize('count', (0, 1, 100))
    async def test_count(self, count: int):
        r = range(count)
        assert await AsyncIter(to_async_iter(r)).count() == len(r)

    @pytest.mark.parametrize(
        ['items', 'condition', 'result'],
        (
            (['here'], lambda x: True, 'here'),
            (['wrong_answer', 'here', 'wrong_answer'], lambda x: len(x) == 4, 'here'),
            (['wrong_answer', 'wrong_answer', 'here'], lambda x: len(x) == 4, 'here'),
            (['wrong_answer', 'wrong_answer', 'here'], to_async(lambda x: len(x) == 4), 'here'),
        ),
    )
    async def test_first_where(self, items: list[str], condition: Callable, result: str):
        assert await AsyncIter(to_async_iter(items)).first_where(condition) == result

    @pytest.mark.parametrize(
        ['items', 'condition'],
        (
            ([], lambda x: True),
            (['to_long', 'to_long_long'], lambda x: len(x) == 2),
            (['to_long', 'to_long_long'], to_async(lambda x: len(x) == 2)),
        ),
    )
    async def test_first_where_with_exception(self, items: list[str], condition: Callable):
        with pytest.raises(ValueError):
            await AsyncIter(to_async_iter(items)).first_where(condition)

    @pytest.mark.parametrize(
        ['items', 'condition', 'result'],
        (
            (list(range(10)), lambda x: x % 2 == 0, [x for x in range(10) if x % 2 == 0]),
            (list(range(10)), lambda x: x % 2 != 0, [x for x in range(10) if x % 2 != 0]),
            (list(range(10)), to_async(lambda x: x % 2 != 0), [x for x in range(10) if x % 2 != 0]),
        ),
    )
    async def test_where(self, items: list[int], condition: Callable, result: list[int]):
        assert await AsyncIter(to_async_iter(items)).where(condition).to_list() == result

    @pytest.mark.parametrize(
        ['items', 'condition', 'result'],
        (
            (list(range(10)), lambda x: x < 5, [x for x in range(10) if x < 5]),
            (list(range(10)), lambda x: x <= 10, [x for x in range(10) if x <= 10]),
            (list(range(10)), to_async(lambda x: x < 5), [x for x in range(10) if x < 5]),
            (list(range(10)), lambda x: x > 5, []),
        ),
    )
    async def test_take_while(self, items: list[int], condition: Callable, result: list[int]):
        assert await AsyncIter(to_async_iter(items)).take_while(condition).to_list() == result


async def test_async_iter():
    r = range(10)

    @async_iter
    async def generator():
        for item in r:
            yield item

    it = generator()
    assert isinstance(it, AsyncIter)
    assert await it.to_list() == list(r)
