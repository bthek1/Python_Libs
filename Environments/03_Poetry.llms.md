# Poetry

Poetry

Author

Benedict Thekkel

## Install Poetry

``` sh
curl -sSL https://install.python-poetry.org | python3 -
```

Or

``` bash
pip install poetry
```

## Config Poetry

``` sh
poetry config --list
```

``` python
!poetry config --list
```

    cache-dir = "/home/ben/.cache/pypoetry"
    experimental.system-git-client = false
    installer.max-workers = null
    installer.modern-installation = true
    installer.no-binary = null
    installer.parallel = true
    keyring.enabled = true
    solver.lazy-wheel = true
    virtualenvs.create = true
    virtualenvs.in-project = true
    virtualenvs.options.always-copy = false
    virtualenvs.options.no-pip = false
    virtualenvs.options.no-setuptools = false
    virtualenvs.options.system-site-packages = false
    virtualenvs.path = "{cache-dir}/virtualenvs"  # /home/ben/.cache/pypoetry/virtualenvs
    virtualenvs.prefer-active-python = false
    virtualenvs.prompt = "{project_name}-py{python_version}"
    warnings.export = true

``` python
!poetry config virtualenvs.in-project true
```

## Initallise Poetry

``` bash
poetry init
```

## Managing Dependencies

``` bash
poetry add requests
```

## Managing Development Dependencies

``` bash
poetry add --dev pytest
```

## Updating Dependencies

``` bash
poetry update
```

## Managing Virtual Environments

``` bash
poetry install
```

## Activating the Virtual Environment

``` bash
poetry shell
```

## Deactivating the Virtual Environment

``` bash
exit
```

## Running Scripts and Commands

> You can run scripts or commands within the Poetry-managed environment without activating it explicitly:

------------------------------------------------------------------------

``` bash
poetry run python my_script.py
```

## Publishing Packages

``` bash
poetry build  # Builds the package
poetry publish  # Publishes the package to PyPI
```

## Exporting to requirements.txt

``` sh
poetry self add poetry-plugin-export
```

``` sh
poetry export -f requirements.txt -o requirements.txt --without-hashes
```

Back to top
