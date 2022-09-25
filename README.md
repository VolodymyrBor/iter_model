<p align="center">
    <a href="https://volodymyrbor.github.io/iter_model">
        <img src="https://volodymyrbor.github.io/iter_model/img/iter_model-logos_transparent.png" alt="IterModel" width="300">
    </a>
</p>


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

---

**iter_model** - provides a convenient API for interacting with iterable objects ([Iterable]).
iter_model uses a methods approach instead of individual functions.

iter_model also provides **async** analog of all methods. 
This is useful when interacting with asynchronous iterable objects ([AsyncIterable]), 
because python does not have ready functions for these cases.

Therefore, **iter_model** provides **SyncIter** class for [Iterable],
and **AsyncIter** for [AsyncIterable].

---

## Example

```python
from iter_model import SyncIter

it = SyncIter(range(10))  # SyncIter for sync iterables
result = (
    it.where(lambda x: x % 2 == 0)  # filter only odd values
    .take(3)  # take first 3 value
    .map(lambda x: x ** 2)  # square all values
)
print(result.to_list())
```

## Links

**Source code**: [github.com/VolodymyrBor/iter_model](https://github.com/VolodymyrBor/iter_model)

**Documentation**: [iter_model](https://volodymyrbor.github.io/iter_model/)

**Changelog**: [changelog](https://volodymyrbor.github.io/iter_model/changelog)

[Iterable]: https://docs.python.org/3/library/typing.html#typing.Iterable
[AsyncIterable]: https://docs.python.org/3/library/typing.html#typing.AsyncIterable
