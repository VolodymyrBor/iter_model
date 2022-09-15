# SyncIter

## SyncIter

```python
class SyncIter
```

Class for Iterable objects.

### SyncIter.to_list

```python
def to_list(self) -> list[T]:
```

!!! quote ""
    Convert to list


### SyncIter.to_tuple

```python
 def to_tuple(self) -> tuple[T, ...]:
```

!!! quote ""
    Convert to tuple
    

### SyncIter.to_set

```python
 def to_set(self) -> set[T]:
```

!!! quote ""
    Convert to set
    

### SyncIter.enumerate

```python
def enumerate(self, start: int = 0) -> SyncIter[tuple[int, T]]:
```

!!! quote ""
    Returns a tuple containing a count (from start which defaults to 0)
    and the values obtained from iterating over self.

    **Parameters**:

    * `start` - start of count

    **Returns**:
    
    SyncIter of tuple[count, item]


### SyncIter.take

```python
def take(self, count: int) -> SyncIter[T]:
```

!!! quote ""
    Take `count` items from iterator

    **Parameters**:

    * `count` - count of item to take


### SyncIter.map

```python
def map(self, func: Callable[[T], R]) -> SyncIter[R]:
```

!!! quote ""
    Return an iterator that applies `func` to every item of iterable,
    yielding the results

    **Parameters**:

    * `func` - apply to each item


### SyncIter.skip

```python
def skip(self, count: int) -> SyncIter[T]:
```

!!! quote ""
    Skip `count` items from iterator

    **Parameters**:

    * `count` - count of items to skip


### SyncIter.skip_while

```python
skip_while(self, func: ConditionFunc) -> SyncIter[T]:
```

!!! quote ""
    Skips leading elements while conditional is satisfied.

    **Parameters**:

    * `func` - condition


### SyncIter.count

```python
def count(self) -> int:
```

!!! quote ""
    Return count of items in iterator


### SyncIter.first_where

```python
def first_where(
    self,
    func: ConditionFunc,
    default: DefaultT = _EMPTY,
) -> T | DefaultT:
```

!!! quote ""
    Find first item for which the conditional is satisfied.

    **Parameters**:

    * `func` - condition function
    * `default` - default value

    **Raises**:
    
    * `ValueError` - the item was not found and default was not provided


### SyncIter.where

```python
def where(self, func: ConditionFunc) -> SyncIter[T]:
```

!!! quote ""
    Filter items by condition

    **Parameters**:

    * `func` - condition


### SyncIter.take_while

```python
def take_while(self, func: ConditionFunc) -> SyncIter[T]:
```

!!! quote ""
    Take items while the conditional is satisfied

    **Parameters**:

    * `func` - condition


### SyncIter.next

```python
def next(self) -> T:
```

!!! quote ""
    Returns the next item


### SyncIter.last

```python
 def last(self) -> T:
```

!!! quote ""
    Return the last item


### SyncIter.chain

```python
def chain(self, *iterables: Iterable[T]) -> SyncIter[T]:
```

!!! quote ""
    Chain with other iterables
    
    **Parameters**:

    * `iterables` - iterables


### SyncIter.all

```python
def all(self) -> bool:
```

!!! quote ""
    Checks whether all elements of this iterable are true


### SyncIter.any

```python
def any(self) -> bool:
```

!!! quote ""
    Checks whether any element of this iterable is true


### SyncIter.first

```python
def first(self) -> T:
```

!!! quote ""
    Return first item. The same as `next()`


### SyncIter.mark_first

```python
def mark_first(self) -> SyncIter[tuple[T, bool]]:
```

!!! quote ""
    Mark first item

    Yeilds: 
    
    tuple[item, is_first]


### SyncIter.mark_last

```python
def mark_last(self) -> SyncIter[tuple[T, bool]]:
```

!!! quote ""
    Mark last item

    Yeilds: 
    
    tuple[item, is_last]


### SyncIter.mark_first_last

```python
def mark_first_last(self) -> SyncIter[tuple[T, bool, bool]]:
```

!!! quote ""
    Mark first and last item

    Yeilds: 
    
    `tuple[item, is_first, is_last]`


### SyncIter.reduce

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


### SyncIter.max

```python
def max(
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


### SyncIter.min

```python
def min(
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


### SyncIter.accumulate

```python
def accumulate(self, func: BinaryFunc = operator.add, initial: T | None = None) -> SyncIter[T]
```

!!! quote ""
    Return series of accumulated sums (by default)

    **Parameters**:

    * `func` - func[accumulated value, next value], by default operator.add
    * `default` - initial value of series


### SyncIter.append_left

```python
def append_left(self, item: T) -> SyncIter[T]:
```

!!! quote ""
    Append an item to left of the iterable (start)

    **Parameters**:

    * `item` - item


### SyncIter.append_right

```python
def append_right(self, item: T) -> SyncIter[T]:
```

!!! quote ""
    Append an item to right of the iterable (start)

    **Parameters**:

    * `item` - item


### SyncIter.append_at

```python
def append_at(self, index: int, item: T) -> SyncIter[T]:
```

!!! quote ""
    Append at the position in to the iterable

    **Parameters**:

    * `index` - index of appending
    * `item` - item


### SyncIter.zip

```python
def zip(self, *iterables: Iterable[T], strict: bool = False) -> SyncIter[tuple[T, ...]]:
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


### SyncIter.zip_longest

```python
def zip_longest(self, *iterables: Iterable[T], fillvalue: R = None) -> SyncIter[tuple[T | R, ...]]:
```

!!! quote ""
    The zip object yields n-length tuples, where n is the number of iterables
    passed as positional arguments to zip().  The i-th element in every tuple
    comes from the i-th iterable argument to zip().  This continues until the
    longest argument is exhausted.

    **Parameters**:

    * `fillvalue` - when the shorter iterables are exhausted, the fillvalue is substituted in their place


### SyncIter.slice

```python
def slice(self, start: int = 0, stop: int | None = None, step: int = 1) -> SyncIter[T]:
```

!!! quote ""
    Return slice from the iterable

    **Parameters**:

    * `start` - start of slice
    * `stop` - stop of slice
    * `step` - step of slice

