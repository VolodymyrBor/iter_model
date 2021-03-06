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

    def test_to_tuple(self):
        r = range(5)
        it = SyncIter(r)
        actual_tuple = it.to_tuple()
        assert isinstance(actual_tuple, tuple)
        assert actual_tuple == tuple(r)

    def test_to_set(self):
        r = range(5)
        it = SyncIter(r)
        actual_set = it.to_set()
        assert isinstance(actual_set, set)
        assert actual_set == set(r)

    @pytest.mark.parametrize('start', (-5, 0, 1, 5))
    def test_enumerate(self, start: int):
        list_ = ['First', 'Second', 'Third']
        assert SyncIter(list_).enumerate(start).to_list() == list(enumerate(list_, start=start))

    @pytest.mark.parametrize('count', (0, 5, 100))
    def test_take(self, count: int):
        r = range(10)
        assert SyncIter(r).take(count).to_list() == list(itertools.islice(r, count))

    def test_map(self):
        r = range(10)
        assert SyncIter(r).map(lambda x: x ** 2).to_list() == [x ** 2 for x in range(10)]

    @pytest.mark.parametrize('count', (0, 5, 100))
    def test_skip(self, count: int):
        r = range(10)
        assert SyncIter(r).skip(count).to_list() == list(r)[count:]

    @pytest.mark.parametrize(
        ['items', 'condition'],
        (
            (list(range(10)), lambda x: x < 5),
            (list(range(10)), lambda x: x > 5),
        ),
    )
    def test_skip_while(self, items, condition):
        """Skips leading elements while conditional is satisfied"""
        return SyncIter(items).skip_while(condition).to_list() == list(itertools.dropwhile(condition, items))

    @pytest.mark.parametrize('count', (0, 1, 100))
    def test_count(self, count: int):
        r = range(count)
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

    def test_first(self):
        items = [4, 2, 3]
        assert SyncIter(items).first() == items[0]

    def test_first_err(self):
        with pytest.raises(StopIteration):
            assert SyncIter([]).first()

    def test_last(self):
        items = [4, 2, 3]
        assert SyncIter(items).last() == items[-1]

    def test_last_err(self):
        with pytest.raises(StopIteration):
            assert SyncIter([]).last()

    def test_chain(self):
        l1 = [3, 5, 7]
        l2 = [1, 2, 3]
        assert SyncIter(l1).chain(l2).to_list() == l1 + l2

    @pytest.mark.parametrize('items', (
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 0],
    ))
    def test_all(self, items):
        assert SyncIter(items).all() == all(items)

    @pytest.mark.parametrize('items', (
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 0],
    ))
    def test_any(self, items):
        assert SyncIter(items).any() == any(items)

    def test_next(self):
        it1 = SyncIter(range(5))
        it2 = SyncIter(range(5))
        assert it1.next() == it2.first()

    def test_next_empty(self):
        with pytest.raises(StopIteration):
            SyncIter([]).next()

    @pytest.mark.parametrize(
        ('it', 'expected'),
        (
            ([], []),
            (['a', 'b', 'c'], [('a', True), ('b', False), ('c', False)]),
        ),
    )
    def test_mark_first(self, it, expected):
        assert SyncIter(it).mark_first().to_list() == expected

    @pytest.mark.parametrize(
        ('it', 'expected'),
        (
            ([], []),
            (['a', 'b', 'c'], [('a', False), ('b', False), ('c', True)]),
        ),
    )
    def test_mark_last(self, it, expected):
        assert SyncIter(it).mark_last().to_list() == expected

    @pytest.mark.parametrize(
        ('it', 'expected'),
        (
            ([], []),
            (['a', 'b', 'c'], [('a', True, False), ('b', False, False), ('c', False, True)]),
        ),
    )
    def test_mark_first_last(self, it, expected):
        assert SyncIter(it).mark_first_last().to_list() == expected


def test_sync_iter():
    r = range(10)

    @sync_iter
    def generator():
        yield from r

    it = generator()
    assert isinstance(it, SyncIter)
    assert it.to_list() == list(r)
