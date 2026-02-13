### [4.0.5] (2026-02-13)

- 🐛 Fix `contains()`  logic to handle `None` values correctly in both sync and async

---

### [4.0.4] (2025-12-07)

- 🐛 Fix package metadata to support Python 3.14

---

### [4.0.3] (2026-12-07)

- 🐛 Fix package metadata to support Python 3.14

---

### [4.0.2] (2026-12-07)

- 🐛 Fix package metadata to support Python 3.14

---

### [4.0.1] (2026-12-07)

- 🐍 Add support for Python 3.12, 3.13, and 3.14 in package metadata

---

### [4.0.0] (2026-12-04)

- 🐍 Add support for Python 3.12, 3.13, and 3.14
- ✨ Imported typing

⚠️ Breaking changes:
  - removed method `__getitem__`

---

### [3.0.0] (2024-06-27)

⚠️ Breaking changes:

- Removed methods
  - `is_not_empty()` 
  - `first()` (duplicate of `next()`)
  - `get_len()` (duplicate of `count()`)
- Renamed methods:
  - `get_slice()` => `islice()` 

---

### [2.3.2] (2024-04-12)

Add [py.typed](..%2Fiter_model%2Fpy.typed) file to package

---

### [2.3.1] (2024-04-12)

✨ New features:

* Added mypy stubs

---

### [2.3.0] (2023-11-21)

✨ New features:

* Added new method: `flatten()`

⚙️ Internal changes:

* update [pyproject.toml](pyproject.toml) to latest poetry version
* use ruff as main code linter instated of flake8
* update mkdocs-material

---

### [2.2.0] (2022-11-25)

✨ New features:
   * Added new method: `skip_where()`

---

### [2.1.0] (2022-11-10)

⚠️ Fixed a bug in method AsyncIter.take(). 

✨ New features:
   * Added new method: `batches()`
   * ⬆️ Added official support for python 3.11
   * 🎉 Update docs using mkdocstrings

---

### [2.0.0] (2022-09-25)

⚠️ Breaking changes:

* ✏️ Renamed method `slice()` -> `get_slice()`

✨ New features:

* ✨ New methods:
  * `last_where()`
  * `item_at()`
  * `contains()`
  * `is_empty()`
  * `is_not_empty()`
  * `pairwise()`
  * `get_len()`
  * implemented `__len__()` for `SyncIter`
  * implemented `__contains__()` for `SyncIter`
  * implemented `__getitem__()` for `SyncIter` and `AsyncIter`
* ✨ New constructor `empty()`: `SyncIter.empty()` and `AsyncIter.empty()`

⚙️Internal Changes:

* ✈️ Moved changelog to website

---

### [1.3.0] (2022-09-15)
✨ New features:

* ✨ Added default parameter for first_where()

⚙️Internal Changes:

* ⬆️ updated dependencies
* 💊 fixed mypy issue
* 📄updated metadata in pyproject.toml
* 📄updated docs volodymyrb
* ✨ Removed unused type ignores
* 💊 Improved stubs/typing
* 📄Updated CHANGELOG.md for the previous release
---

### [1.2.1] (2022-09-14)
  * ⚙️ Internal changes:
    * 📄Create docs using mkdocs-material
    * 💚Set up CD for docs
    * 📄Updated readme
    * ⚙️ Migrated to new poetry installer
---


### [1.2.0] (2022-08-30)
  * ✨ New features:
    * 💊 Added stubs: now the type hints should get even better. 
  * ⚙️ Internal changes:
    * 📄 Updated release template 
---

### [1.1.1] (2022-08-29)

  * 🛫 Set up full CI&CD flow

---

### [1.1.0] (2022-08-28)
 * ✨ Added new methods:
   * `reduce()`
   * `max()`
   * `min()`
   * `accumulate()`
   * `append_left()`
   * `append_right()`
   * `append_at()`
   * `zip()`
   * `zip_longest()`
   * `slice()`
 * 📑 Updated some doc-strings
 * ⚙️ Internal fixes:
   * Downgrade for flake8, to fix problems in dependencies between flake8 and pytest-flake8: [issue link](https://github.com/tholo/pytest-flake8/issues/87)
---

### [1.0.0] (2022-07-04)
 * ✨ Added new methods:
   * `next()`
   * `mark_first()`
   * `mark_last()`
   * `mark_first_last()`
 * ⚠️ Now all methods will raise StopIteration / AsyncStopIteration exceptions.
 * ⚠️ Added `__slots__` to classes

---

### [0.2.0] (2022-04-09)
 * Added mypy to tests
 * Added new methods:
   * to_tuple()
   * to_set()
   * skip_while()
   * first()
   * last()
   * chain()
   * all()
   * any()

---

### [0.1.3] (2022-04-05)
 * Added README
 * Added docstrings

---

### [0.1.2] (2022-04-01)
 * Added tests

---

### [0.1.1] (2022-03-31)
 * Removed dead code

---

### [0.1.0] (2022-03-31)
 * Initial

 
[0.1.0]: https://github.com/VolodymyrBor/iter_model/commit/c0e402688d825a9829ab8dac1f27dbc4711ed19b
[0.1.1]: https://github.com/VolodymyrBor/iter_model/commit/98f2827caf4928d24db1321d85e3ad8c34a0e661
[0.1.2]: https://github.com/VolodymyrBor/iter_model/pull/1
[0.1.3]: https://github.com/VolodymyrBor/iter_model/pull/4
[0.2.0]: https://github.com/VolodymyrBor/iter_model/pull/7
[1.0.0]: https://github.com/VolodymyrBor/iter_model/pull/8
[1.1.0]: https://github.com/VolodymyrBor/iter_model/pull/10
[1.1.1]: https://github.com/VolodymyrBor/iter_model/pull/12
[1.2.0]: https://github.com/VolodymyrBor/iter_model/pull/14
[1.2.1]: https://github.com/VolodymyrBor/iter_model/pull/16
[1.3.0]: https://github.com/VolodymyrBor/iter_model/pull/18
[2.0.0]: https://github.com/VolodymyrBor/iter_model/pull/20
[2.1.0]: https://github.com/VolodymyrBor/iter_model/pull/24
[2.2.0]: https://github.com/VolodymyrBor/iter_model/pull/26
[2.3.0]: https://github.com/VolodymyrBor/iter_model/pull/29
[2.3.1]: https://github.com/VolodymyrBor/iter_model/pull/29
[2.3.2]: https://github.com/VolodymyrBor/iter_model/pull/31
[3.0.0]: https://github.com/VolodymyrBor/iter_model/pull/33
[4.0.0]: https://github.com/VolodymyrBor/iter_model/pull/35
[4.0.1]: https://github.com/VolodymyrBor/iter_model/pull/36
[4.0.2]: https://github.com/VolodymyrBor/iter_model/pull/37
[4.0.3]: https://github.com/VolodymyrBor/iter_model/pull/38
[4.0.4]: https://github.com/VolodymyrBor/iter_model/pull/39
[4.0.5]: https://github.com/VolodymyrBor/iter_model/pull/41
