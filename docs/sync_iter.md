# SyncIter

## class SyncIter
:::iter_model.sync_iter.SyncIter

## Support Operators and Build-in func

### len()

!!! quote "Example"
    ```python
    len(SyncIter(range(5)))
    >>> 5
    ```    

### in

!!! quote "Example"
    ```python
    2 in SyncIter(range(5))
    >>> True
    ``` 

### Slice

!!! quote "Example"
    ```python
    SyncIter(range(5))[2:]
    ``` 

### Get item by index

!!! quote "Example"
    ```python
    SyncIter(range(5))[2]
    >>> 2
    ``` 

## async_iter
:::iter_model.sync_iter.sync_iter
