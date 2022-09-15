# AsyncIter

## AsyncIter

```python
class AsyncIter
```

Class for AsyncIterable objects.

### AsyncIter.from_sync

```python
def from_sync(cls, it: Iterable[T]) -> AsyncIter[T]:
```

!!! quote ""
    Create AsyncIter from Iterable object (sync)

### AsyncIter.to_list

```python
async def to_list(self) -> list[T]:
```

!!! quote ""
    Convert to list


### AsyncIter.to_tuple

```python
async def to_tuple(self) -> tuple[T, ...]:
```

!!! quote ""
    Convert to tuple
    

### AsyncIter.to_set

```python
async def to_set(self) -> set[T]:
```

!!! quote ""
    Convert to set
    

### AsyncIter.enumerate

```python
def enumerate(self, start: int = 0) -> AsyncIter[tuple[int, T]]:
```

!!! quote ""
    Returns a tuple containing a count (from start which defaults to 0)
    and the values obtained from iterating over self.

    **Parameters**:

    * `start` - start of count

    **Returns**:
    
    AsyncIter of tuple[count, item]


### AsyncIter.take

```python
def take(self, count: int) -> AsyncIter[T]:
```

!!! quote ""
    Take `count` items from iterator

    **Parameters**:

    * `count` - count of item to take


### AsyncIter.map

```python
def map(self, func: Callable[[T], R]) -> AsyncIter[R]:
```

!!! quote ""
    Return an iterator that applies `func` to every item of iterable,
    yielding the results

    **Parameters**:

    * `func` - apply to each item


### AsyncIter.skip

```python
def skip(self, count: int) -> AsyncIter[T]:
```

!!! quote ""
    Skip `count` items from iterator

    **Parameters**:

    * `count` - count of items to skip


### AsyncIter.skip_while

```python
def skip_while(self, func: ConditionFunc) -> AsyncIter[T]:
```

!!! quote ""
    Skips leading elements while conditional is satisfied.

    **Parameters**:

    * `func` - condition


### AsyncIter.count

```python
async def count(self) -> int:
```

!!! quote ""
    Return count of items in iterator


### AsyncIter.first_where

```python
async def first_where(self, func: ConditionFunc, default: DefaultT = _EMPTY) -> T | DefaultT:
```

!!! quote ""
    Find first item for which the conditional is satisfied.

    **Parameters**:

    * `func` - condition function
    * `default` - default value

    **Raises**:
    
    * `ValueError` - the item was not found and default was not provided


### AsyncIter.where

```python
def where(self, func: ConditionFunc) -> AsyncIter[T]:
```

!!! quote ""
    Filter items by condition

    **Parameters**:

    * `func` - condition


### AsyncIter.take_while

```python
def take_while(self, func: ConditionFunc) -> AsyncIter[T]:
```

!!! quote ""
    Take items while the conditional is satisfied

    **Parameters**:

    * `func` - condition


### AsyncIter.next

```python
async def next(self) -> T:
```

!!! quote ""
    Returns the next item


### AsyncIter.last

```python
 async def last(self) -> T:
```

!!! quote ""
    Return the last item


### AsyncIter.chain

```python
def chain(self, *iterables: AsyncIterable[T]) -> AsyncIter[T]:
```

!!! quote ""
    Chain with other iterables
    
    **Parameters**:

    * `iterables` - iterables


### AsyncIter.all

```python
async def all(self) -> bool:
```

!!! quote ""
    Checks whether all elements of this iterable are true


### AsyncIter.any

```python
async def any(self) -> bool:
```

!!! quote ""
    Checks whether any element of this iterable is true


### AsyncIter.first

```python
def first(self) -> T:
```

!!! quote ""
    Return first item. The same as `next()`


### AsyncIter.mark_first

```python
def mark_first(self) -> AsyncIter[tuple[T, bool]]:
```

!!! quote ""
    Mark first item

    Yeilds: 
    
    tuple[item, is_first]


### AsyncIter.mark_last

```python
def mark_last(self) -> AsyncIter[tuple[T, bool]]:
```

!!! quote ""
    Mark last item

    Yeilds: 
    
    tuple[item, is_last]


### AsyncIter.mark_first_last

```python
def mark_first_last(self) -> AsyncIter[tuple[T, bool, bool]]:
```

!!! quote ""
    Mark first and last item

    Yeilds: 
    
    `tuple[item, is_first, is_last]`


### AsyncIter.reduce

```python
def reduce(
    self,
    func: BinaryFunc,
    initial: T = _EMPTY,
) -> T | DefaultT:
```

!!! quote ""
    Apply the `func` of two arguments cumulatively to the items of an iterable,
    from left to right, to reduce the iterable to a single value

    **Parameters**:

    * `func` - Calable[accumulated value, next item]
    * `initial` - initial value of iterable. Serves like default value if iterable is empty
    
    **Rises**:
    
    * `ValueError` - if initial is not provided and iterable is empty


### AsyncIter.max

```python
async def max(
    self,
    key: KeyFunc | None = None,
    default: DefaultT = _EMPTY,
) -> T | DefaultT:
```

!!! quote ""
    Return the biggest item

    **Parameters**:

    * `key` - the result of the function will be used to compare the elements
    * `default` - default value in case iterable is empty
    
    **Rises**:
    
    * `ValueError` - when iterable is empty and default value is not provided


### AsyncIter.min

```python
async def min(
    self,
    key: KeyFunc | None = None,
    default: DefaultT = _EMPTY,
) -> T | DefaultT:
```

!!! quote ""
    Return the smallest item

    **Parameters**:

    * `key` - the result of the function will be used to compare the elements
    * `default` - default value in case iterable is empty
    
    **Rises**:
    
    * `ValueError` - when iterable is empty and default value is not provided


### AsyncIter.accumulate

```python
def accumulate(self, func: BinaryFunc = operator.add, initial: T | None = None) -> AsyncIter[T]
```

!!! quote ""
    Return series of accumulated sums (by default)

    **Parameters**:

    * `func` - func[accumulated value, next value], by default operator.add
    * `default` - initial value of series


### AsyncIter.append_left

```python
def append_left(self, item: T) -> AsyncIter[T]:
```

!!! quote ""
    Append an item to left of the iterable (start)

    **Parameters**:

    * `item` - item


### AsyncIter.append_right

```python
def append_right(self, item: T) -> AsyncIter[T]:
```

!!! quote ""
    Append an item to right of the iterable (start)

    **Parameters**:

    * `item` - item


### AsyncIter.append_at

```python
def append_at(self, index: int, item: T) -> AsyncIter[T]:
```

!!! quote ""
    Append at the position in to the iterable

    **Parameters**:

    * `index` - index of appending
    * `item` - item


### AsyncIter.zip

```python
def zip(self, *iterables: AsyncIterable[T], strict: bool = False) -> AsyncIter[tuple[T, ...]]:
```

!!! quote ""
    The zip object yields n-length tuples, where n is the number of iterables
    passed as positional arguments to zip().  The i-th element in every tuple
    comes from the i-th iterable argument to zip().  This continues until the
    shortest argument is exhausted.

    **Parameters**:

    * `iterables` - iterables
    * `stric` - whether the elements must be the same `len`

    **Raises**:
    
    * `ValueError`: when strict is true and one of the arguments is exhausted before the others


### AsyncIter.zip_longest

```python
def zip_longest(self, *iterables: AsyncIterable[T], fillvalue: R = None) -> AsyncIter[tuple[T | R, ...]]:
```

!!! quote ""
    The zip object yields n-length tuples, where n is the number of iterables
    passed as positional arguments to zip().  The i-th element in every tuple
    comes from the i-th iterable argument to zip().  This continues until the
    longest argument is exhausted.

    **Parameters**:

    * `fillvalue` - when the shorter iterables are exhausted, the fillvalue is substituted in their place


### AsyncIter.slice

```python
def slice(self, start: int = 0, stop: int | None = None, step: int = 1) -> AsyncIter[T]:
```

!!! quote ""
    Return slice from the iterable

    **Parameters**:

    * `start` - start of slice
    * `stop` - stop of slice
    * `step` - step of slice
