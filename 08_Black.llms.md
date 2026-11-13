# Black

**Black** is a Python code formatter that focuses on producing consistent and clean code by enforcing a strict style. It’s often referred to as the “uncompromising code formatter” because it makes all formatting decisions for you, eliminating debates over style.

Author

Benedict Thekkel

## **1. What is Black?**

- **Purpose**: Black formats Python code to follow a consistent style. It automates formatting, saving time and avoiding manual reformatting errors.
- **Philosophy**: Code formatting should be deterministic, and Black prioritizes code readability and simplicity.

------------------------------------------------------------------------

## **2. Key Features**

- **Deterministic Formatting**: Given the same code, Black will always produce the same output.
- **Minimal Configuration**: Black enforces a single style with very few customization options.
- **Speed and Safety**: It’s fast and guarantees that formatting will not change your code’s functionality.
- **Support for Python Versions**: Black supports Python 3.6+ and Python 2.7 (with reduced functionality for legacy versions).

------------------------------------------------------------------------

## **3. Installation**

Install Black via `pip`:

``` bash
pip install black
```

Alternatively, use `pipx` for an isolated environment:

``` bash
pipx install black
```

------------------------------------------------------------------------

## **4. Usage**

Run Black on a file or directory:

``` bash
black filename.py
black path/to/code/
```

### **Common Options**

- **Check for Formatting**: Check if code is formatted without changing it:

  ``` bash
  black --check .
  ```

- **Show Changes**: See what changes Black would make:

  ``` bash
  black --diff .
  ```

- **Exclude Files**: Skip specific files or directories:

  ``` bash
  black --exclude "migrations|env"
  ```

- **Line Length**: Adjust line length (default is 88):

  ``` bash
  black --line-length 79 .
  ```

- **Safe Mode**: Skip files with syntax errors:

  ``` bash
  black --safe .
  ```

------------------------------------------------------------------------

## **5. Configuration**

### **Using `pyproject.toml`**

Black can be configured via a `pyproject.toml` file:

``` toml
[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.mypy_cache
  | \.pytest_cache
  | \.tox
  | _build
  | buck-out
  | build
  | dist
)/
'''
```

Place the `pyproject.toml` file in the root directory of your project.

------------------------------------------------------------------------

## **6. Features**

### **a. Line Wrapping**

- Lines exceeding the specified length (`--line-length`) are automatically wrapped.
- Black prioritizes readability when wrapping.

### **b. String Normalization**

- By default, Black normalizes all strings to double quotes (`"`):

  ``` python
  print("This is Black-formatted.")
  ```

Disable this behavior with the `--skip-string-normalization` flag:

``` bash
black --skip-string-normalization .
```

### **c. Implicit vs. Explicit Line Joins**

- Black uses parentheses for line continuations instead of backslashes.

Example:

``` python
# Before
x = 1 + 2 + \
    3

# After
x = (
    1 + 2 +
    3
)
```

------------------------------------------------------------------------

## **7. Integration**

### **a. IDE Integration**

- **VS Code**:
  1.  Install the Python extension.
  2.  Set Black as the formatter:
      - Go to `Settings` \> Search for “Python Formatting Provider” \> Select `Black`.
  3.  Enable “Format on Save”:
      - Go to `Settings` \> Search for “Format on Save” \> Enable it.
- **PyCharm**:
  1.  Install Black globally or in your virtual environment.
  2.  Set up a File Watcher:
      - Go to **File \> Settings \> Tools \> File Watchers**.
      - Add a new watcher for `Black`.

### **b. Pre-commit Hooks**

Use `pre-commit` to enforce Black before committing code:

1.  Install `pre-commit`:

    ``` bash
    pip install pre-commit
    ```

2.  Add `.pre-commit-config.yaml`:

    ``` yaml
    repos:
    - repo: https://github.com/psf/black
      rev: 23.1.0  # Replace with the latest version
      hooks:
      - id: black
    ```

3.  Install the hook:

    ``` bash
    pre-commit install
    ```

4.  Now, Black will automatically run on changed files before every commit.

------------------------------------------------------------------------

## **8. Continuous Integration**

### **Example: GitHub Actions**

Add Black to your CI pipeline:

``` yaml
name: Python Linting

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.9
    - name: Install dependencies
      run: pip install black
    - name: Run Black
      run: black --check .
```

------------------------------------------------------------------------

## **9. Combining Black with isort**

**isort** formats imports. Use it alongside Black:

1.  Install isort:

    ``` bash
    pip install isort
    ```

2.  Run isort and Black together:

    ``` bash
    isort . && black .
    ```

3.  Add both to your `pre-commit` hooks:

    ``` yaml
    repos:
    - repo: https://github.com/pycqa/isort
      rev: 5.10.1
      hooks:
      - id: isort

    - repo: https://github.com/psf/black
      rev: 23.1.0
      hooks:
      - id: black
    ```

------------------------------------------------------------------------

## **10. Advantages of Black**

- **Consistency**: Eliminates debates over style.
- **Automation**: Saves time with automatic formatting.
- **Collaboration**: Teams can focus on functionality instead of style.
- **Tool Integration**: Works seamlessly with IDEs, pre-commit, and CI tools.

------------------------------------------------------------------------

## **11. Limitations**

- **No Custom Styles**: Black enforces a strict style with minimal customization.
- **Changes Code Structure**: Some developers may find the formatting disruptive (e.g., line wrapping decisions).
- **Formatting-First**: Black does not lint for correctness; use tools like flake8 for that.

------------------------------------------------------------------------

## **12. Common Issues**

### **a. Black Not Formatting Code**

Ensure Black is installed and the Python environment

------------------------------------------------------------------------

``` python
x = 1 + 2 + \
    3
```

Back to top
