# Monkey Patch

Here’s a **complete, structured guide to monkey patching in Python**, covering everything from what it is and why it’s used, to risks, examples, and best practices — especially relevant when testing with tools like `pytest`.

Author

Benedict Thekkel

## 🧠 1. What is Monkey Patching?

> **Monkey patching** is the practice of **dynamically changing a class, method, or module at runtime**, usually to alter or extend behavior without modifying the original source code.

✅ Often used in:

- Testing/mocking
- Temporary bug fixes
- Dynamic feature injection

------------------------------------------------------------------------

## 🧪 2. Monkey Patching Use Cases

| Use Case | Example |
|----|----|
| **Testing** | Replace API calls or database functions with mocks |
| **Hotfixes** | Patch a bug in a third-party library |
| **Instrumentation** | Inject logging, metrics, or tracing code dynamically |
| **Compatibility** | Override methods for legacy or platform-specific behavior |

------------------------------------------------------------------------

## 🧩 3. Basic Monkey Patch Example

### Patching a method:

``` python
class Math:
    def add(self, x, y):
        return x + y

# Patch the method
def fake_add(self, x, y):
    return 42

Math.add = fake_add

m = Math()
print(m.add(1, 2))  # ➜ 42
```

------------------------------------------------------------------------

## 🧪 4. Monkey Patching in `pytest` (Using `monkeypatch` Fixture)

`pytest` provides a built-in fixture named `monkeypatch` to safely patch objects.

### Example:

``` python
# app.py
def get_ip():
    import requests
    return requests.get("https://ipapi.co/ip/").text
```

``` python
# test_app.py
def test_get_ip(monkeypatch):
    def mock_get(url):
        class MockResponse:
            text = "123.123.123.123"
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    from app import get_ip
    assert get_ip() == "123.123.123.123"
```

------------------------------------------------------------------------

## 🧰 5. `monkeypatch` Methods

| Method | Purpose |
|----|----|
| `setattr(obj_or_path, name, value)` | Set an attribute on an object or module |
| `delattr(obj_or_path, name)` | Delete an attribute |
| `setitem(mapping, key, value)` | Patch a dictionary or map |
| `delitem(mapping, key)` | Remove a key from a dictionary |
| `syspath_prepend(path)` | Temporarily prepend a path to `sys.path` |
| `chdir(path)` | Temporarily change current directory |
| `setenv(name, value)` | Patch environment variable |
| `delenv(name)` | Remove environment variable |

------------------------------------------------------------------------

## 🔍 6. Example: Patching a Class Method

``` python
import os

def test_env(monkeypatch):
    monkeypatch.setenv("ENV", "test")
    assert os.getenv("ENV") == "test"
```

------------------------------------------------------------------------

## ⚠️ 7. Risks of Monkey Patching

| Risk | Description |
|----|----|
| 🔄 **Global side effects** | Patches affect all usage of the object across the app |
| 😱 **Hard to trace** | Dynamic behavior can confuse maintainers or IDEs |
| ❌ **Breaks updates** | Future library updates may invalidate the patch |
| 🧪 **Unintended leakage in tests** | If not undone/reset between tests, state leaks may occur |

------------------------------------------------------------------------

## ✅ 8. Best Practices

| Tip | Description |
|----|----|
| ✔️ Use `pytest.monkeypatch` | It’s **scoped to the test** and auto-resets afterward |
| 🧪 Patch only what you need | Avoid excessive or deep patches |
| 🛑 Don’t monkeypatch in production | Unless absolutely necessary and temporary |
| 🧼 Cleanup manually if not using `monkeypatch` | Use `try/finally` or context managers |
| 📚 Document all patches | Especially in test or third-party contexts |

------------------------------------------------------------------------

## 🧪 9. Comparison: `monkeypatch` vs `unittest.mock.patch`

| Feature   | `pytest.monkeypatch`    | `unittest.mock.patch`           |
|-----------|-------------------------|---------------------------------|
| Scope     | Function-scoped fixture | Context manager / decorator     |
| Resets?   | ✅ Auto-reset           | ✅ Auto-reset if used correctly |
| Verbosity | Minimal                 | More boilerplate                |
| Style     | Functional              | Object-oriented                 |

### Example with `mock.patch`:

``` python
from unittest.mock import patch

@patch("requests.get")
def test_get_ip(mock_get):
    mock_get.return_value.text = "123.123.123.123"
    assert get_ip() == "123.123.123.123"
```

------------------------------------------------------------------------

## 📦 10. Common Monkey Patch Targets

| Target                    | Purpose                              |
|---------------------------|--------------------------------------|
| `os.getenv`, `os.environ` | Patch environment-dependent behavior |
| `requests.get` / `post`   | Replace API calls                    |
| `datetime.now`            | Freeze or control time               |
| Class methods             | Replace expensive or slow logic      |
| Third-party libraries     | Fix bugs or inject logic             |

------------------------------------------------------------------------

## 🧪 Bonus: Patch `datetime.now()`

``` python
import datetime

class FakeDatetime(datetime.datetime):
    @classmethod
    def now(cls):
        return cls(2020, 1, 1)

def test_time(monkeypatch):
    monkeypatch.setattr(datetime, "datetime", FakeDatetime)
    assert datetime.datetime.now() == datetime.datetime(2020, 1, 1)
```

------------------------------------------------------------------------

## 📌 Final Thoughts

- ✅ Monkey patching is powerful for **testing, mocking, and runtime modifications**
- ❗️Use **carefully and only when needed**
- Prefer **`pytest.monkeypatch`** in test code
- Avoid in production unless under control (e.g., well-documented, temporary hotfix)

------------------------------------------------------------------------

Back to top
