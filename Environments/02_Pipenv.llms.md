# Pipenv

Pipenv

Author

Benedict Thekkel

## Installation of pipenv

``` sh
pip install pipenv
```

## Create a env

``` sh
pipenv install
```

## Create a env

``` sh
pipenv install django
```

## Remove an env

``` sh
pipenv --rm
```

## Activate already created pipenv environment

``` sh
pipenv shell
```

## To Deactivate

``` sh
deactivate
```

## Install/Uninstall dependencies

``` sh
pipenv install django
pipenv uninstall django
```

### Install dev dependencies

``` sh
pipenv install nose --dev
```

### Install from requirements.txt

``` sh
pipenv install -r requirements.txt
```

### Check security vulnerabilities

``` sh
pipenv check
```

### Check dependency graph

``` sh
pipenv graph
```

Back to top
