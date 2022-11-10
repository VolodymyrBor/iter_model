# AsyncIter

## class AsyncIter
:::iter_model.async_iter.AsyncIter

## Support Operators and Build-in func

### Slice

!!! quote "Example"
    ```python
    AsyncIter.from_sync(range(5))[2:]
    ``` 

### Get item by index

!!! quote "Example"
    ```python
    await AsyncIter.from_sync(range(5))[2]
    >>> 2
    ``` 

## async_iter
:::iter_model.async_iter.async_iter