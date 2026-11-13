# Nbdev

Details on setting up nbdev Setup

Author

Benedict Thekkel

## Installation

- Python
- A Python package manager: we recommend conda or pip - download anaconda
- Jupyter Notebook - see below
- nbdev - see below
- Quarto - see quarto setup

------------------------------------------------------------------------

### To get Jupyter labs

``` sh
pip install jupyterlab
```

``` sh
mamba install -c conda-forge jupyterlab
```

To launch jupyter labs

``` sh
jupyter lab
```

To install nbdev

``` sh
pip install nbdev
```

``` sh
mamba install -c fastai nbdev
```

> get instructin for quarto with

``` sh
nbdev_install_quarto
```

Install the extension by entering:

``` sh
pip install jupyterlab-quarto
```

## Create an empty GitHub repo

- make it public
- add a gitignore file

------------------------------------------------------------------------

- clone it into project location

``` sh
git clone https://github.com/PROEJECT_NAME.git
```

## RUN Nbdev

Initialise your nbdev repo by entering:

``` sh
nbdev_new
```

It may ask you to enter information that it couldn’t infer from git or GitHub.

- Do a git push to make sure everything is working

``` sh
git add .
git commit -m'Initial commit'
git push
```

> Go to settings on Github, go to pages, Change Branch to gh-pages

- Then check on Actions

## Useful commands

The next step is to install your package by entering this into your terminal:

``` sh
pip install -e '.[dev]'
```

This is the recommended way to make a Python package importable from anywhere in your current environment:

- -e – short for “editable”, lets you immediately use changes made to your package without having to reinstall, which is convenient for development.
- . – refers to the current directory.
- \[dev\] – includes “development” requirements: other packages that your notebooks use solely for documentation or testing.

Start the preview by entering this into your terminal:

``` sh
nbdev_preview
```

Before every git push, run :

``` sh
nbdev_prepare
```

Which is the combination of:

``` sh
nbdev_export
```

Builds the .py modules from Jupyter notebooks

``` sh
nbdev_test
```

Tests your notebooks

``` sh
nbdev_clean
```

Cleans your notebooks to get rid of extreanous output for git

``` sh
nbdev_readme
```

Updates your repo’s README.md file from your index notebook.

## Directives for documentation:

``` sh
#|hide
```

> Hide cell input and output.

``` sh
#|echo: <true|false>
```

> Toggle the visibility of code-cell inputs.

``` sh
#|output: <true|false|asis>
```

> Setting this to false hides the output of a cell. Setting this to asis renders the output as raw markdown.

``` sh
#|hide_line
```

> Hide a specific line of code in an input cell.

``` sh
#|code-fold: <show|true>
```

> The \#\|code-fold directive allows you to collapse code cells. When set to true, the element is collapsed by default, when set to show show the element is shown by default.

### Exports

``` sh
#|default_exp <name>
```

> Names the module where cells with the \#\|export directive will be exported to by default.

``` sh
#|export
```

> Exports the items in the cell into the generated module and documentation.

``` sh
#|exports
```

> A source export. Like \#\|export but in addition to showing docs via showdoc.show_doc, it also shows the source code.

``` sh
#|exec_doc
```

> Ensures that a cell is executed each time before generating docs. When a cell does not have this annotation, it is run according to the default rules described here.

``` sh
#|eval: <true|false>
```

> When set to false, the cell is ignored during testing.

## Testing

``` python
def say_hello(to):
    "Say hello to somebody"
    return f'Hello {to}!'
```

``` python
say_hello("Isaac")
```

    'Hello Isaac!'

This is a test too! When you run nbdev_test it will execute this cell (and all other test cells) and fail if they raise any exceptions.

For tests, it’s preferred to use more explicit asserts:

``` python
assert say_hello("Hamel") == "Hello Hamel!"
```

``` python
from fastcore.test import *
```

``` python
test_eq(say_hello("Hamel"), "Hello Hamel!")
```

Using

``` sh
$$\sum_{i=1}^{k+1}i$$
```

Which is rendered as: $$\sum_{i=1}^{k+1}i$$

``` sh
This version is displayed inline: $\sum_{i=1}^{k+1}i$ . You can include text before and after.
```

> Becomes: This version is displayed inline: $\sum_{i=1}^{k+1}i$ . You can include text before and after.

Back to top
