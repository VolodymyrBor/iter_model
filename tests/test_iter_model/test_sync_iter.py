import functools
import itertools
import operator
from typing import Callable, Iterable, Any

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

    @pytest.mark.parametrize(
        ('it', 'key'),
        (
            (range(5), None),
            (range(5), int.bit_count),
            ((-10, 10), None),
        ),
    )
    def test_max(self, it: Iterable, key: Callable):
        assert SyncIter(it).max(key=key) == max(it, key=key)

    def test_max_default(self):
        default = 'default'
        assert SyncIter(tuple()).max(default=default) == default

    def test_max_empty_error(self):
        with pytest.raises(ValueError):
            SyncIter(tuple()).max()

    @pytest.mark.parametrize(
        ('it', 'key'),
        (
            (range(5), None),
            (range(5), int.bit_count),
            ((-10, 10), None),
        ),
    )
    def test_min(self, it: Iterable, key: Callable):
        assert SyncIter(it).min(key=key) == min(it, key=key)

    def test_min_default(self):
        default = 'default'
        assert SyncIter(tuple()).min(default=default) == default

    def test_min_empty_error(self):
        with pytest.raises(ValueError):
            SyncIter(tuple()).min()

    @pytest.mark.parametrize(
        ('it', 'func', 'initial'),
        (
            (range(5), operator.add, 1),
            (range(5), operator.sub, -10),
            ((-10, 10), operator.mul, 20),
        ),
    )
    def test_reduce(self, it: Iterable, func: Callable, initial: int):
        assert SyncIter(it).reduce(func=func, initial=initial) == functools.reduce(func, it, initial)

    def test_reduce_empty(self):
        with pytest.raises(ValueError):
            SyncIter(tuple()).reduce(func=operator.add)

    @pytest.mark.parametrize(
        ('it', 'func', 'initial'),
        (
            (range(5), operator.add, 1),
            (range(5), operator.sub, -10),
            ((-10, 10), operator.mul, 20),
            (tuple(), operator.mul, None),  # empty
        ),
    )
    def test_accumulate(self, it: Iterable, func: Callable, initial: int):
        assert SyncIter(it).accumulate(
            func=func,
            initial=initial
        ).to_list() == list(itertools.accumulate(it, func, initial=initial))

    @pytest.mark.parametrize(
        ('iterables', ),
        (
            ((range(5), range(5)), ),
            ((range(5), range(3)), ),
            ((range(3), range(5)), ),
        ),
    )
    def test_zip(self, iterables: Iterable[Iterable]):
        r = range(3)
        it = SyncIter(r)
        assert it.zip(*iterables).to_list() == list(zip(r, *iterables))

    def test_zip_strict(self):
        with pytest.raises(ValueError):
            assert SyncIter(range(3)).zip(range(4), strict=True).to_list()

    @pytest.mark.parametrize(
        ('iterables', 'fillvalue'),
        (
            ((range(5), range(5)), None),
            ((range(5), range(3)), 1),
            ((range(3), range(5)), 'string'),
        ),
    )
    def test_zip_longest(self, iterables: Iterable[Iterable], fillvalue: Any):
        r = range(3)
        it = SyncIter(r)
        assert it.zip_longest(*iterables, fillvalue=fillvalue).to_list() == list(itertools.zip_longest(
            r,
            *iterables,
            fillvalue=fillvalue,
        ))

    @pytest.mark.parametrize(
        ('iterable', 'slice_'),
        (
            (range(10), slice(0, None)),
            (range(10), slice(3, None, 2)),
            (range(10), slice(4, 7)),
            (range(10), slice(4, 7, 3)),
        ),
    )
    def test_slice(self, iterable: Iterable, slice_: slice):
        assert SyncIter(iterable).slice(
            start=slice_.start,
            stop=slice_.stop,
            step=slice_.step,
        ).to_list() == list(iterable)[slice_]

    def test_append_right(self):
        r = range(5)
        item = -10
        assert SyncIter(r).append_right(item).to_list() == [*r, item]

    def test_append_left(self):
        r = range(5)
        item = -10
        assert SyncIter(r).append_left(item).to_list() == [item, *r]

    @pytest.mark.parametrize(
        'position',
        (
            0,
            3,
            100,
        ),
    )
    def test_append_at(self, position: int):
        r = range(5)
        item = -10
        list_ = list(r)
        list_.insert(position, item)
        assert SyncIter(r).append_at(position, item).to_list() == list_


def test_sync_iter():
    r = range(10)

    @sync_iter
    def generator():
        yield from r

    it = generator()
    assert isinstance(it, SyncIter)
    assert it.to_list() == list(r)
