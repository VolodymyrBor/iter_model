import functools
import itertools
import operator
from typing import AsyncIterable, Callable, Iterable, Any, Sequence

import pytest

from tests.utils import to_async_iter
from iter_model import AsyncIter, async_iter
from iter_model.async_utils import asyncify


async def asyncify_iterable(iterable: Iterable) -> AsyncIterable:
    for item in iterable:
        yield item


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

    @pytest.mark.parametrize('counts', (
        (0, 4, 3),
        (0, 1, 10),
        (2, 100),
    ))
    async def test_take(self, counts: tuple[int]):
        r = range(10)
        sync_iter_ = AsyncIter.from_sync(r)
        it = iter(r)
        for count in counts:
            assert await sync_iter_.take(count).to_list() == list(itertools.islice(it, count))

    @pytest.mark.parametrize('func', (lambda x: x ** 2, asyncify(lambda x: x ** 2)))
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
            (list(range(10)), asyncify(lambda x: x < 5), [6, 7, 8, 9]),
            (list(range(10)), lambda x: x > 5, []),
        ),
    )
    async def test_skip_while(self, items, condition, result):
        """Skips leading elements while conditional is satisfied"""
        return await AsyncIter.from_sync(items).skip_while(condition).to_list() == result

    @pytest.mark.parametrize(
        ['items', 'condition', 'result'],
        (
            (list(range(10)), lambda x: x % 2 == 0, [x for x in range(10) if x % 2 != 0]),
            (list(range(10)), lambda x: x % 2 != 0, [x for x in range(10) if x % 2 == 0]),
            (list(range(10)), asyncify(lambda x: x % 2 != 0), [x for x in range(10) if x % 2 == 0]),
        ),
    )
    async def test_skip_where(self, items: list[int], condition: Callable, result: list[int]):
        assert await AsyncIter(to_async_iter(items)).skip_where(condition).to_list() == result

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
            (['wrong_answer', 'wrong_answer', 'here'], asyncify(lambda x: len(x) == 4), 'here'),
        ),
    )
    async def test_first_where(self, items: list[str], condition: Callable, result: str):
        assert await AsyncIter(to_async_iter(items)).first_where(condition) == result

    @pytest.mark.parametrize(
        ['items', 'condition'],
        (
            ([], lambda x: True),
            (['to_long', 'to_long_long'], lambda x: len(x) == 2),
            (['to_long', 'to_long_long'], asyncify(lambda x: len(x) == 2)),
        ),
    )
    async def test_first_where_with_exception(self, items: list[str], condition: Callable):
        with pytest.raises(ValueError):
            await AsyncIter(to_async_iter(items)).first_where(condition)

    async def test_first_where_with_default(self):
        default = object()
        assert await AsyncIter.empty().first_where(bool, default=default) is default

    @pytest.mark.parametrize(
        ['items', 'condition', 'result'],
        (
            (['here'], lambda x: True, 'here'),
            (['wrong_answer', 'here', 'wrong_answer'], lambda x: len(x) == 4, 'here'),
            (['wrong_answer', 'wrong_answer', 'here'], lambda x: len(x) == 4, 'here'),
            (['wrong_answer', 'wrong_answer', 'here'], asyncify(lambda x: True), 'here'),
        ),
    )
    async def test_last_where(self, items: list[str], condition: Callable, result: str):
        assert await AsyncIter(to_async_iter(items)).last_where(condition) == result

    @pytest.mark.parametrize(
        ['items', 'condition'],
        (
            ([], lambda x: True),
            (['to_long', 'to_long_long'], lambda x: len(x) == 2),
            (['to_long', 'to_long_long'], asyncify(lambda x: len(x) == 2)),
        ),
    )
    async def test_last_where_with_exception(self, items: list[str], condition: Callable):
        with pytest.raises(ValueError):
            await AsyncIter(to_async_iter(items)).last_where(condition)

    async def test_last_where_with_default(self):
        default = object()
        assert await AsyncIter.empty().last_where(bool, default=default) is default

    @pytest.mark.parametrize(
        ['items', 'condition', 'result'],
        (
            (list(range(10)), lambda x: x % 2 == 0, [x for x in range(10) if x % 2 == 0]),
            (list(range(10)), lambda x: x % 2 != 0, [x for x in range(10) if x % 2 != 0]),
            (list(range(10)), asyncify(lambda x: x % 2 != 0), [x for x in range(10) if x % 2 != 0]),
        ),
    )
    async def test_where(self, items: list[int], condition: Callable, result: list[int]):
        assert await AsyncIter(to_async_iter(items)).where(condition).to_list() == result

    @pytest.mark.parametrize(
        ['items', 'condition', 'result'],
        (
            (list(range(10)), lambda x: x < 5, [x for x in range(10) if x < 5]),
            (list(range(10)), lambda x: x <= 10, [x for x in range(10) if x <= 10]),
            (list(range(10)), asyncify(lambda x: x < 5), [x for x in range(10) if x < 5]),
            (list(range(10)), lambda x: x > 5, []),
        ),
    )
    async def test_take_while(self, items: list[int], condition: Callable, result: list[int]):
        assert await AsyncIter(to_async_iter(items)).take_while(condition).to_list() == result

    async def test_last(self):
        items = [4, 2, 3]
        assert await AsyncIter.from_sync(items).last() == items[-1]

    async def test_last_err(self):
        with pytest.raises(StopAsyncIteration):
            assert await AsyncIter.empty().last()

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
        assert await it1.next() == await anext(it2)

    async def test_next_empty(self):
        with pytest.raises(StopAsyncIteration):
            await AsyncIter.empty().next()

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

    @pytest.mark.parametrize(
        ('it', 'key'),
        (
            (range(5), None),
            (range(5), int.bit_count),
            ((-10, 10), None),
        ),
    )
    async def test_max(self, it: Iterable, key: Callable):
        assert await AsyncIter.from_sync(it).max(key=key) == max(it, key=key)

    async def test_max_default(self):
        default = 'default'
        assert await AsyncIter.from_sync(()).max(default=default) == default

    async def test_max_empty_error(self):
        with pytest.raises(ValueError):
            await AsyncIter.from_sync(()).max()

    @pytest.mark.parametrize(
        ('it', 'key'),
        (
            (range(5), None),
            (range(5), int.bit_count),
            ((-10, 10), None),
            ((10, -10), None),
        ),
    )
    async def test_min(self, it: Iterable, key: Callable):
        assert await AsyncIter.from_sync(it).min(key=key) == min(it, key=key)

    async def test_min_default(self):
        default = 'default'
        assert await AsyncIter.from_sync(()).min(default=default) == default

    async def test_min_empty_error(self):
        with pytest.raises(ValueError):
            await AsyncIter.from_sync(()).min()

    @pytest.mark.parametrize(
        ('it', 'func', 'initial'),
        (
            (range(5), operator.add, 1),
            (range(5), operator.sub, -10),
            ((-10, 10), operator.mul, 20),
        ),
    )
    async def test_reduce(self, it: Iterable, func: Callable, initial: int):
        assert await AsyncIter.from_sync(it).reduce(
            func=func,
            initial=initial,
        ) == functools.reduce(func, it, initial)

    async def test_reduce_empty(self):
        with pytest.raises(ValueError):
            await AsyncIter.from_sync(()).reduce(func=operator.add)

    @pytest.mark.parametrize(
        ('it', 'func', 'initial'),
        (
            (range(5), operator.add, 1),
            (range(5), operator.sub, -10),
            ((-10, 10), operator.mul, 20),
            ((), operator.mul, None),  # empty
        ),
    )
    async def test_accumulate(self, it: Iterable, func: Callable, initial: int):
        assert await AsyncIter.from_sync(it).accumulate(
            func=func,
            initial=initial
        ).to_list() == list(itertools.accumulate(it, func, initial=initial))

    @pytest.mark.parametrize(
        ('iterables',),
        (
            ((range(5), range(5)),),
            ((range(5), range(3)),),
            ((range(3), range(5)),),
        ),
    )
    async def test_zip(self, iterables: Iterable[Iterable]):
        r = range(3)
        it = AsyncIter.from_sync(r)
        assert await it.zip(
            *map(AsyncIter.from_sync, iterables),  # type: ignore
        ).to_list() == list(map(list, zip(r, *iterables)))  # noqa: W291

    async def test_zip_strict(self):
        with pytest.raises(ValueError):
            assert await AsyncIter.from_sync(range(3)).zip(AsyncIter.from_sync(range(4)), strict=True).to_list()

    @pytest.mark.parametrize(
        ('iterables', 'fillvalue'),
        (
            ((range(5), range(5)), None),
            ((range(5), range(3)), 1),
            ((range(3), range(5)), 'string'),
        ),
    )
    async def test_zip_longest(self, iterables: Iterable[Iterable], fillvalue: Any):
        r = range(3)
        it = AsyncIter.from_sync(r)
        assert await it.zip_longest(
            *map(AsyncIter.from_sync, iterables),  # type: ignore
            fillvalue=fillvalue,
        ).to_list() == list(map(list, itertools.zip_longest(r, *iterables, fillvalue=fillvalue)))

    @pytest.mark.parametrize(
        ('iterable', 'slice_'),
        (
            (range(10), {'start': 0}),
            (range(10), {'start': 2, 'stop': 7, 'step': 2}),
            (range(10), {'start': 4, 'stop': 7}),
            (range(10), {'start': 4, 'stop': 8, 'step': 3}),
        ),
    )
    async def test_slice(self, iterable: Iterable, slice_: dict):
        assert await AsyncIter.from_sync(iterable).islice(**slice_).to_list() == list(iterable)[slice(
            slice_.get('start'),
            slice_.get('stop'),
            slice_.get('step'),
        )]

    async def test_append_right(self):
        r = range(5)
        item = -10
        assert await AsyncIter.from_sync(r).append_right(item).to_list() == [*r, item]

    async def test_append_left(self):
        r = range(5)
        item = -10
        assert await AsyncIter.from_sync(r).append_left(item).to_list() == [item, *r]

    @pytest.mark.parametrize(
        'position',
        (
            0,
            3,
            100,
        ),
    )
    async def test_append_at(self, position: int):
        r = range(5)
        item = -10
        list_ = list(r)
        list_.insert(position, item)
        assert await AsyncIter.from_sync(r).append_at(position, item).to_list() == list_

    async def test_item_at(self):
        items = ['wrong', 'here', 'wrong']
        index = items.index('here')
        assert await AsyncIter.from_sync(items).item_at(index) == items[index]

    async def test_item_at_exception(self):
        items = ['wrong', 'wrong', 'wrong']
        with pytest.raises(IndexError):
            await AsyncIter.from_sync(items).item_at(len(items))

    @pytest.mark.parametrize(
        ['items', 'item', 'result'],
        (
            ((1, 2, 3), 1, True),
            ((1, 2, 3), 3, True),
            ((1, 2, 3), -1, False),
        ),
    )
    async def test_contains(self, items: Sequence[int], item: int, result: bool):
        assert await AsyncIter.from_sync(items).contains(item) is result

    async def test_is_empty(self):
        assert await AsyncIter.empty().is_empty()

    @pytest.mark.parametrize('items', ([], range(1), range(2), range(3), range(5)))
    async def test_pairwise(self, items: Sequence[int]):
        it: AsyncIter[int] = AsyncIter.from_sync(items)
        assert await it.pairwise().to_list() == list(itertools.pairwise(items))

    @pytest.mark.parametrize('slice_', (
        slice(None),
        slice(None, None),
        slice(2, None),
        slice(None, 4),
        slice(100, None),
        slice(100),
        slice(None, None, 2),
        slice(None, 5, 2),
        slice(5, None, 3),
    ))
    async def test_getitem_dander_method_slice(self, slice_: slice):
        r = range(10)
        it: AsyncIter[int] = AsyncIter.from_sync(r)
        assert await it[slice_].to_list() == list(r)[slice_]

    @pytest.mark.parametrize('index', (
        0, 1, 5,
    ))
    async def test_getitem_dander_method(self, index: int):
        r = range(10)
        assert await AsyncIter.from_sync(r)[index] == list(r)[index]

    @pytest.mark.parametrize('index', (
        -1, -5, 100,
    ))
    async def test_getitem_dander_method_exception(self, index: int):
        with pytest.raises(IndexError):
            await AsyncIter.from_sync(range(5))[index]

    async def test_empty(self):
        it = AsyncIter.empty()
        assert await it.is_empty()

    async def test_not_empty(self):
        assert not await AsyncIter.from_sync(range(5)).is_empty()

    @pytest.mark.parametrize(['it', 'batch_size', 'expected'], (
        (tuple(range(10)), 3, ((0, 1, 2), (3, 4, 5), (6, 7, 8), (9, ))),
        (tuple(range(9)), 3, ((0, 1, 2), (3, 4, 5), (6, 7, 8))),
        (tuple(range(1)), 3, ((0, ), ), ),
        (tuple(range(6)), 4, ((0, 1, 2, 3), (4, 5))),
        (tuple(range(0)), 100, ()),
    ))
    async def test_batches(
        self,
        it: Sequence[int],
        batch_size: int,
        expected: tuple,
    ):
        sync_it = AsyncIter.from_sync(it)
        batches = sync_it.batches(batch_size)
        assert await batches.map(tuple).to_tuple() == expected  # type: ignore

    @pytest.mark.parametrize(['it', 'expected'], (
        ((range(3), range(3, 7)), (0, 1, 2, 3, 4, 5, 6)),
        ((asyncify_iterable(range(3)), asyncify_iterable(range(3, 7))), (0, 1, 2, 3, 4, 5, 6)),
    ))
    async def test_flatten(
        self,
        it: tuple[range | AsyncIter[int]],
        expected: tuple[int, ...],
    ):
        async_it: AsyncIter = AsyncIter.from_sync(it)  # type: ignore
        assert await async_it.flatten().to_tuple() == expected  # type: ignore

    async def test_flatten_bad_type(self):
        async_it: AsyncIter = AsyncIter.from_sync((range(3), range(4), 1))
        async_it = async_it.flatten()
        assert await async_it.take(3).to_list() == list(range(3))
        assert await async_it.take(4).to_list() == list(range(4))
        with pytest.raises(TypeError):
            await async_it.next()


async def test_async_iter():
    r = range(10)

    @async_iter
    async def generator():
        for item in r:
            yield item

    it = generator()
    assert isinstance(it, AsyncIter)
    assert await it.to_list() == list(r)
