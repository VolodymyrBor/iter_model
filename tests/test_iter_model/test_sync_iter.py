import itertools
from typing import Callable

import pytest

from iter_model import SyncIter, sync_iter


class TestSyncIter:

    def test_to_list(self):
        r = range(5)
        it = SyncIter(r)
        actual_list = it.to_list()
        assert isinstance(actual_list, list)
        assert actual_list == list(r)

    @pytest.mark.parametrize('start', (-5, 0, 1, 5))
    def test_enumerate(self, start: int):
        list_ = ['First', 'Second', 'Third']
        assert SyncIter(list_).enumerate(start).to_list() == list(enumerate(list_, start=start))

    @pytest.mark.parametrize('count', (0, 5, 100))
    def test_take(self, count: int):
        r = range(10)
        assert SyncIter(r).take(count).to_list() == list(itertools.islice(r, count))

    @pytest.mark.parametrize('count', (0, 5, 100))
    def test_skip(self, count: int):
        r = range(10)
        assert SyncIter(r).skip(count).to_list() == list(r)[count:]

    @pytest.mark.parametrize('count', (0, 1, 100))
    def test_count(self, count: int):
        r = range(10)
        assert SyncIter(r).count() == len(r)

    @pytest.mark.parametrize(
        ['items', 'condition', 'result'],
        (
            (['here'], lambda x: True, 'here'),
            (['wrong_answer', 'here', 'wrong_answer'], lambda x: len(x) == 4, 'here'),
            (['wrong_answer', 'wrong_answer', 'here'], lambda x: len(x) == 4, 'here'),
        ),
    )
    def test_first_where(self, items: list[str], condition: Callable, result: str):
        assert SyncIter(items).first_where(condition) == result

    @pytest.mark.parametrize(
        ['items', 'condition'],
        (
            ([], lambda x: True),
            (['to_long', 'to_long_long'], lambda x: len(x) == 2),
        ),
    )
    def test_first_where_with_exception(self, items: list[str], condition: Callable):
        with pytest.raises(ValueError):
            SyncIter(items).first_where(condition)

    @pytest.mark.parametrize(
        ['items', 'condition', 'result'],
        (
            (list(range(10)), lambda x: x % 2 == 0, [x for x in range(10) if x % 2 == 0]),
            (list(range(10)), lambda x: x % 2 != 0, [x for x in range(10) if x % 2 != 0]),
        ),
    )
    def test_where(self, items: list[int], condition: Callable, result: list[int]):
        assert SyncIter(items).where(condition).to_list() == result

    @pytest.mark.parametrize(
        ['items', 'condition', 'result'],
        (
            (list(range(10)), lambda x: x < 5, [x for x in range(10) if x < 5]),
            (list(range(10)), lambda x: x > 5, []),
        ),
    )
    def test_take_while(self, items: list[int], condition: Callable, result: list[int]):
        assert SyncIter(items).take_while(condition).to_list() == result

    def test_map(self):
        r = range(10)
        assert SyncIter(r).map(lambda x: x ** 2).to_list() == [x ** 2 for x in range(10)]


def test_sync_iter():
    r = range(10)

    @sync_iter
    def generator():
        yield from r

    it = generator()
    assert isinstance(it, SyncIter)
    assert it.to_list() == list(r)
