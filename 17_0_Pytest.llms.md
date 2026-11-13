# Pytest

Here’s a **comprehensive and structured guide to `pytest`**, covering everything from basics to advanced features, plugins, and best practices — tailored for professional Python developers like yourself.

Author

Benedict Thekkel

## 🧰 1. What is `pytest`?

**`pytest`** is a powerful, Pythonic testing framework used to write, run, and organize tests with **minimal boilerplate**.

- Supports unit, integration, and functional testing
- Works out-of-the-box with Python’s `assert`
- Automatically discovers test files and functions

------------------------------------------------------------------------

## 🚀 2. Getting Started

### 📦 Installation

``` bash
pip install pytest
```

### 🏃 Running Tests

``` bash
pytest                # Run all tests
pytest test_file.py   # Run a specific file
pytest -k "name"      # Run tests matching "name"
```

### 📄 File & Function Naming Conventions

- Files: `test_*.py` or `*_test.py`
- Functions: `test_*`

------------------------------------------------------------------------

## 🧪 3. Writing Basic Tests

``` python
def add(x, y):
    return x + y

def test_add():
    assert add(2, 3) == 5
```

### ✅ Advantages

- No need for classes
- No need for `self.assert*` syntax

------------------------------------------------------------------------

## ⚙️ 4. Fixtures

Fixtures manage setup and teardown for tests. You can **reuse resources like DBs, clients, configs**.

### Example:

``` python
import pytest

@pytest.fixture
def sample_data():
    return {"x": 10, "y": 20}

def test_sum(sample_data):
    assert sample_data["x"] + sample_data["y"] == 30
```

- Scope options: `function` (default), `class`, `module`, `session`

------------------------------------------------------------------------

## 🎯 5. Parametrization

Write a single test function that runs with different inputs:

``` python
import pytest

@pytest.mark.parametrize("a,b,result", [
    (1, 1, 2),
    (2, 3, 5),
    (5, 5, 10)
])
def test_add(a, b, result):
    assert a + b == result
```

------------------------------------------------------------------------

## 🧵 6. Grouping with Classes (Optional)

``` python
class TestMath:
    def test_add(self):
        assert 1 + 2 == 3
```

- No need to inherit from `unittest.TestCase`

------------------------------------------------------------------------

## 🔌 7. Plugins & Extensions

Some powerful plugins:

| Plugin            | Purpose                       |
|-------------------|-------------------------------|
| `pytest-django`   | Django testing integration    |
| `pytest-mock`     | Simplified mocking            |
| `pytest-cov`      | Test coverage reporting       |
| `pytest-xdist`    | Run tests in parallel         |
| `pytest-asyncio`  | Support async tests           |
| `pytest-env`      | Set env vars during test runs |
| `pytest-randomly` | Randomize test order          |

Install with:

``` bash
pip install pytest-cov pytest-mock pytest-django
```

------------------------------------------------------------------------

## 📊 8. Coverage

``` bash
pytest --cov=my_module
```

- Shows % of code covered by tests
- Use `--cov-report=html` for an HTML report

------------------------------------------------------------------------

## 🧪 9. Mocks & Patching

Use `pytest-mock` or `unittest.mock`:

``` python
def test_api_call(mocker):
    mock_request = mocker.patch("requests.get")
    mock_request.return_value.status_code = 200
    ...
```

------------------------------------------------------------------------

## 🧪 10. Async Testing

Install:

``` bash
pip install pytest-asyncio
```

Then:

``` python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result == "done"
```

------------------------------------------------------------------------

## 🧪 11. Advanced CLI Options

``` bash
pytest -x                  # Stop after first failure
pytest -v                  # Verbose output
pytest --tb=short          # Shorter tracebacks
pytest -n auto             # Parallel test execution (requires `xdist`)
```

------------------------------------------------------------------------

## 📁 12. Test Structure Example

    my_project/
    ├── app/
    │   └── logic.py
    ├── tests/
    │   ├── conftest.py       # shared fixtures
    │   ├── test_logic.py
    │   └── test_api.py

------------------------------------------------------------------------

## 📑 13. `conftest.py` – Centralized Fixtures

``` python
# tests/conftest.py
import pytest

@pytest.fixture
def config():
    return {"ENV": "test"}
```

Auto-discovered across test files in the same directory tree.

------------------------------------------------------------------------

## 🧪 14. Best Practices

✅ Use descriptive test function names ✅ Keep tests **fast, isolated, and repeatable** ✅ Avoid hardcoding test data – use fixtures and parametrization ✅ Use `pytest-cov` to ensure meaningful coverage ✅ Run in CI pipelines (GitHub Actions, GitLab, etc.) ✅ Structure tests like your app structure

------------------------------------------------------------------------

## 🧰 15. CI/CD Integration

``` yaml
# GitHub Actions example
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - run: pip install -r requirements.txt
      - run: pytest --cov=my_app
```

------------------------------------------------------------------------

## 🧠 Bonus: Debugging Tips

- `pytest --pdb`: drop into debugger on failure
- `pytest -s`: allow print() output
- `pdb.set_trace()` inside your test or app logic

------------------------------------------------------------------------

## 🧠 Example: Test Case with Fixture + Parametrize + Mock

``` python
import pytest

@pytest.fixture
def sample_user():
    return {"name": "Ben", "role": "engineer"}

@pytest.mark.parametrize("role", ["admin", "guest"])
def test_user_roles(sample_user, role):
    sample_user["role"] = role
    assert sample_user["role"] in ["admin", "guest"]
```

------------------------------------------------------------------------

Back to top
