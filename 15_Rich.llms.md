# Rich

Here’s **everything you need to know about [rich](https://rich.readthedocs.io/en/latest/)** — the Python library for **beautiful terminal output**.

Author

Benedict Thekkel

## 🖼️ What is Rich?

**`rich`** is a Python library for **rich text and beautiful formatting** in the terminal — including:

- 🌈 Colored text & styles
- 📊 Tables, progress bars, trees
- 🪵 Log rendering
- 📦 JSON + syntax highlighting
- 🖼️ Markdown and emoji rendering

It’s used in projects like **Textual**, **FastAPI**, **Typer**, **pipx**, and **Pydantic**.

------------------------------------------------------------------------

## 🚀 Installation

``` bash
pip install rich
```

Or with `uv`:

``` bash
uv pip install rich
```

------------------------------------------------------------------------

## 🧱 Basic Usage

``` python
from rich import print

print("[bold magenta]Hello[/bold magenta] [green]World![/green] :rocket:")
```

✅ Output with colors and emoji.

### Rich Console

``` python
from rich.console import Console

console = Console()
console.print("Hello [cyan]World[/cyan]!", style="bold")
```

------------------------------------------------------------------------

## 🧾 Text Formatting

Supports:

- Styles: `bold`, `italic`, `underline`, `strike`
- Colors: names, hex (`#ff00ff`), RGB tuples
- Emoji shortcodes (like `:rocket:`)

``` python
console.print("This is [bold red]error[/bold red] and [green]success[/green]!")
```

------------------------------------------------------------------------

## 📐 Layouts

### ✅ Tables

``` python
from rich.table import Table

table = Table(title="User Info")
table.add_column("Name", style="cyan")
table.add_column("Email", style="magenta")
table.add_row("Ben", "ben@example.com")
table.add_row("Kiera", "kiera@example.com")

console.print(table)
```

### 🌳 Trees

``` python
from rich.tree import Tree

tree = Tree("📁 Root")
tree.add("📄 File1.txt")
branch = tree.add("📂 Folder")
branch.add("📄 NestedFile.txt")

console.print(tree)
```

### 🔄 Progress Bars

``` python
from rich.progress import track
import time

for step in track(range(10), description="Processing..."):
    time.sleep(0.1)
```

### ⏳ Manual Progress Bars

``` python
from rich.progress import Progress

with Progress() as progress:
    task = progress.add_task("Downloading...", total=100)
    while not progress.finished:
        progress.update(task, advance=10)
        time.sleep(0.2)
```

------------------------------------------------------------------------

## 🐞 Logging with Rich

``` python
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level="DEBUG",
    handlers=[RichHandler()],
    format="%(message)s",
)

logger = logging.getLogger("rich")
logger.info("Info log")
logger.error("Error log")
```

------------------------------------------------------------------------

## 🧬 Syntax Highlighting

``` python
from rich.syntax import Syntax

code = '''
def greet(name):
    print(f"Hello, {name}")
'''

syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
console.print(syntax)
```

------------------------------------------------------------------------

## 📚 Pretty Print JSON

``` python
from rich.pretty import pprint
from rich.json import JSON

pprint({"foo": "bar", "baz": [1, 2, 3]})

console.print(JSON('{"key": "value", "list": [1, 2, 3]}'))
```

------------------------------------------------------------------------

## ✨ Markdown Rendering

``` python
from rich.markdown import Markdown

md = Markdown("# Title\n\n**Bold** and *italic* text.")
console.print(md)
```

------------------------------------------------------------------------

## 💥 Error Tracebacks

``` python
from rich.traceback import install
install()

# Raise any exception after this and it'll show a beautiful traceback
raise ValueError("Oops!")
```

------------------------------------------------------------------------

## 🧪 Testing & Integration

### Django Logging

Use `RichHandler` in `settings.py`:

``` python
LOGGING = {
    "version": 1,
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "level": "DEBUG",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
```

------------------------------------------------------------------------

## 🧵 Combining Components

``` python
from rich.panel import Panel
from rich.align import Align

panel = Panel.fit(
    Align.center("[bold green]Task Complete![/bold green]"),
    border_style="green",
    title="Status",
)

console.print(panel)
```

------------------------------------------------------------------------

## ⚙️ Advanced: Live Dashboards

``` python
from rich.live import Live
from rich.table import Table
import time

table = Table()
table.add_column("Task")
table.add_column("Progress")

with Live(table, refresh_per_second=4):
    for i in range(5):
        table.add_row(f"Task {i}", f"{i*20}%")
        time.sleep(0.5)
```

------------------------------------------------------------------------

## 📦 Rich CLI

``` bash
rich [FILE]          # Pretty-print file content
rich --traceback     # See a rich traceback on crash
```

------------------------------------------------------------------------

# 🧮 Rich Ecosystem

- [`textual`](https://github.com/Textualize/textual): TUI apps (terminal GUIs) with Rich
- `rich-click`: Combine `click` and Rich
- `typer`: Uses Rich under the hood
- `rich-prompt-toolkit`: Fancy prompts and input
- `rich-argparse`: Pretty CLI help output

------------------------------------------------------------------------

## 📊 Summary Cheat Sheet

| Feature             | Module                     |
|---------------------|----------------------------|
| Styled text         | `console.print()`          |
| Tables              | `rich.table.Table`         |
| Progress Bars       | `rich.progress.Progress`   |
| Logging             | `rich.logging.RichHandler` |
| Syntax Highlighting | `rich.syntax.Syntax`       |
| JSON/Pretty Print   | `rich.json`, `rich.pretty` |
| Markdown            | `rich.markdown.Markdown`   |
| Error Tracebacks    | `rich.traceback.install()` |

------------------------------------------------------------------------

Let me know if you’d like:

- A **custom CLI logger setup**
- A **Rich-based dashboard**
- A **Textual app starter** I can scaffold one for you.

------------------------------------------------------------------------

Back to top
