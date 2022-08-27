# Iter Model

<a href="https://pypi.org/project/iter_model" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/iter_model.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://pypi.org/project/iter_model" target="_blank">
    <img src="https://img.shields.io/pypi/v/iter_model?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://github.com/VolodymyrBor/iter_model/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/VolodymyrBor/iter_model/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
</a>

[![Supported Versions](https://img.shields.io/badge/coverage-100%25-green)](https://shields.io/)
[![Supported Versions](https://img.shields.io/badge/poetry-✅-grey)](https://shields.io/)
[![Supported Versions](https://img.shields.io/badge/async-✅-grey)](https://shields.io/)
[![Supported Versions](https://img.shields.io/badge/mypy-✅-grey)](https://shields.io/)

## Description

**Iter Model** uses a method approach instead of individual functions to work with iterable objects.

### Native approach

```python
result = list(map(
    lambda x: x ** 2,
    filter(lambda x: x % 2 == 0, range(10)),
))
```

### Iter Model approach

```python
from iter_model import SyncIter

result = (
    SyncIter(range(10))
        .where(lambda x: x % 2 == 0)
        .map(lambda x: x ** 2)
        .to_list()
)

```

### Generators

You can decorate your generator function and get SyncIter as a result

```python
from iter_model import sync_iter


@sync_iter
def some_generator():
    for item in range(10):
        yield item


result = some_generator().take_while(lambda x: x < 5).to_list()
```

### Async support

Iter Model also support async iterable and async function as condition.


```python
import asyncio

from iter_model import async_iter


@async_iter
async def some_generator():
    for item in range(10):
        yield item

        
async def condition_a(x):
    """Some async condition"""
    return x % 2 == 0 


def condition_b(x):
    """Some sync condition"""
    return x > 5 


async def main():
    result = await (
        some_generator()
            .where(condition_a)
            .take_while(condition_b)
            .to_list()
    )
    print(result)
    


asyncio.run(main())
```

### SyncIter/AsyncIter provide the following methods

- ```to_list()```
- ```to_tuple()```
- ```to_set()```
- ```enumerate()```
- ```take()```
- ```map()```
- ```skip()```
- ```skip_while()```
- ```count()```
- ```first_where()```
- ```where()```
- ```take_while()```
- ```first()```
- ```last()```
- ```chain()```
- ```all()```
- ```any()```
- ```first()```
- ```mark_first()```
- ```mark_last()```
- ```mark_first_last()```
- ```reduce()```
- ```max()```
- ```min()```
- ```accumulate()```
- ```append_left()```
- ```append_right()```
- ```append_at()```
- ```zip()```
- ```zip_longest()```
- ```slice()```
