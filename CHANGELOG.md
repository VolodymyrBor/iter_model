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
