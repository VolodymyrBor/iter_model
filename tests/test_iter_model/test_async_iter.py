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

    async def test_to_tuple(self):
        r = range(5)
        it = AsyncIter.from_sync(r)
        actual_tuple = await it.to_tuple()
        assert isinstance(actual_tuple, tuple)
        assert actual_tuple == tuple(r)

    async def test_to_set(self):
        r = range(5)
        it = AsyncIter.from_sync(r)
        actual_set = await it.to_set()
        assert isinstance(actual_set, set)
        assert actual_set == set(r)

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

    @pytest.mark.parametrize(
        ['items', 'condition', 'result'],
        (
            (list(range(10)), lambda x: x < 5, [6, 7, 8, 9]),
            (list(range(10)), to_async(lambda x: x < 5), [6, 7, 8, 9]),
            (list(range(10)), lambda x: x > 5, []),
        ),
    )
    async def test_skip_while(self, items, condition, result):
        """Skips leading elements while conditional is satisfied"""
        return await AsyncIter.from_sync(items).skip_while(condition).to_list() == result

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

    async def test_first(self):
        items = [4, 2, 3]
        assert await AsyncIter.from_sync(items).first() == items[0]

    async def test_first_err(self):
        with pytest.raises(StopAsyncIteration):
            assert await AsyncIter.from_sync([]).first()

    async def test_last(self):
        items = [4, 2, 3]
        assert await AsyncIter.from_sync(items).last() == items[-1]

    async def test_last_err(self):
        with pytest.raises(StopAsyncIteration):
            assert await AsyncIter.from_sync([]).last()

    async def test_chain(self):
        l1 = [3, 5, 7]
        l2 = [1, 2, 3]
        assert await AsyncIter.from_sync(l1).chain(AsyncIter.from_sync(l2)).to_list() == l1 + l2

    @pytest.mark.parametrize('items', (
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 0],
    ))
    async def test_all(self, items):
        assert await AsyncIter.from_sync(items).all() == all(items)

    @pytest.mark.parametrize('items', (
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 0],
    ))
    async def test_any(self, items):
        assert await AsyncIter.from_sync(items).any() == any(items)

    async def test_next(self):
        it1 = AsyncIter.from_sync(range(5))
        it2 = AsyncIter.from_sync(range(5))
        assert await it1.next() == await it2.first()

    async def test_next_empty(self):
        with pytest.raises(StopAsyncIteration):
            await AsyncIter.from_sync([]).next()

    @pytest.mark.parametrize(
        ('it', 'expected'),
        (
            ([], []),
            (['a', 'b', 'c'], [('a', True), ('b', False), ('c', False)]),
        ),
    )
    async def test_mark_first(self, it, expected):
        assert await AsyncIter.from_sync(it).mark_first().to_list() == expected

    @pytest.mark.parametrize(
        ('it', 'expected'),
        (
            ([], []),
            (['a', 'b', 'c'], [('a', False), ('b', False), ('c', True)]),
        ),
    )
    async def test_mark_last(self, it, expected):
        assert await AsyncIter.from_sync(it).mark_last().to_list() == expected

    @pytest.mark.parametrize(
        ('it', 'expected'),
        (
            ([], []),
            (['a', 'b', 'c'], [('a', True, False), ('b', False, False), ('c', False, True)]),
        ),
    )
    async def test_mark_first_last(self, it, expected):
        assert await AsyncIter.from_sync(it).mark_first_last().to_list() == expected


async def test_async_iter():
    r = range(10)

    @async_iter
    async def generator():
        for item in r:
            yield item

    it = generator()
    assert isinstance(it, AsyncIter)
    assert await it.to_list() == list(r)
