# duckduckgo-search

duckduckgo-search is a Python library (by deedy5) for searching words, documents, images, news, maps, and text translation via DuckDuckGo. It requires Python ≥ 3.9, is MIT-licensed, and production-stable (current version 8.1.1 as of Jul 2025).

Author

Benedict Thekkel

## Install

``` bash
pip install -U ddgs rich
```

------------------------------------------------------------------------

## Rich Console Formatting

All examples below use [Rich](https://rich.readthedocs.io/) for beautiful terminal output:

- **Tables**: Organized data display with styling
- **Panels**: Highlight important information
- **Colors & Markup**: `[bold cyan]text[/]` for styled output
- **Icons**: Enhance readability with emojis

------------------------------------------------------------------------

## 1. Text search

``` python
from ddgs import DDGS

# Basic
results = DDGS().text("python programming", max_results=5)
print(results)
# [{'title': '...', 'href': 'https://...', 'body': '...'}, ...]

# All params
results = DDGS().text(
    "live free or die",
    region="us-en",        # wt-wt = no region
    safesearch="off",      # on | moderate | off
    timelimit="y",         # d=day, w=week, m=month, y=year
    page=1,
    backend="auto",        # auto | google | brave | bing | yahoo etc.
    max_results=10,
)

# filetype search
results = DDGS().text("machine learning filetype:pdf", max_results=20)
```

------------------------------------------------------------------------

``` python
from ddgs import DDGS
```

``` python
from ddgs import DDGS
from rich.console import Console
from rich.table import Table

console = Console()

# Basic search with pretty output
console.print("\n[bold cyan]Basic Text Search[/bold cyan]")
results = DDGS().text("python programming", max_results=5)
for i, result in enumerate(results, 1):
    console.print(f"\n[bold yellow]{i}. {result['title']}[/bold yellow]")
    console.print(f"[blue]{result['href']}[/blue]")
    console.print(f"{result['body'][:150]}...\n")

# All params example with table
console.print("[bold cyan]\nSearching with all parameters:[/bold cyan]")
results = DDGS().text(
    "live free or die",
    region="us-en",        # wt-wt = no region
    safesearch="off",      # on | moderate | off
    timelimit="y",         # d=day, w=week, m=month, y=year
    page=1,
    backend="auto",        # auto | google | brave | bing | yahoo etc.
    max_results=3,
)

table = Table(title="Search Results")
table.add_column("Title", style="cyan")
table.add_column("URL", style="magenta")
for result in results:
    table.add_row(result['title'][:40], result['href'][:50])
console.print(table)

# filetype search
console.print("[bold cyan]\nFiletype Search (PDF):[/bold cyan]")
results = DDGS().text("machine learning filetype:pdf", max_results=5)
console.print(f"Found [green]{len(results)}[/green] results")
```

```
Basic Text Search
```

```
1. Python (programming language)
```

```
https://en.wikipedia.org/wiki/Python_(programming_language)
```

```
Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability 
with the use of significant indentatio...
```

```
2. Python (programming language)
```

```
https://grokipedia.com/page/Python_(programming_language)
```

```
Python (programming language) Python is an interpreted, high-level, general-purpose programming language designed 
for code readability and simplicity,...
```

```
3. Welcome to Python.org
```

```
https://www.python.org/
```

```
Pythonis a versatile and easy-to-learnprogramminglanguage that lets you work quickly and integrate systems more 
effectively. LearnPythonbasics, downlo...
```

```
4. Python Tutorial - W3Schools
```

```
https://www.w3schools.com/python/
```

```
LearnPythonPythonis a popularprogramminglanguage.Pythoncan be used on a server to create web applications. Start 
learningPythonnow »...
```

```
5. How to Use Python: Your First Steps - Real Python
```

```
https://realpython.com/python-first-steps/
```

```
Learn how to use Python—install it, run code, and work with data types, functions, classes, and loops. Explore 
essential tools and build a solid found...
```

```
Searching with all parameters:
```

```
                                       Search Results                                        
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Title                                    ┃ URL                                            ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Live free or die                         │ https://en.wikipedia.org/wiki/Live_free_or_die │
│ en.wikipedia.org› wiki › Live_Free_or_Di │ https://en.wikipedia.org/wiki/Live_Free_or_Die │
│ Live Free or Die                         │ https://grokipedia.com/page/Live_Free_or_Die   │
└──────────────────────────────────────────┴────────────────────────────────────────────────┘
```

```
Filetype Search (PDF):
```

```
Found 5 results
```

## 2. Images search

``` python
from rich.console import Console
from rich.table import Table

console = Console()

results = DDGS().images(
    query="butterfly",
    region="wt-wt",
    safesearch="off",
    timelimit=None,        # Day, Week, Month
    size=None,             # Small, Medium, Large, Wallpaper
    color="Monochrome",    # color name, Monochrome, color, BlackAndWhite
    type_image=None,       # photo, clipart, gif, transparent, line
    layout=None,           # Square, Tall, Wide
    license_image=None,    # any, Public, Share, ShareCommercially, Modify, ModifyCommercially
    max_results=10,
)

table = Table(title="🦋 Image Search Results")
table.add_column("#", justify="center", style="cyan")
table.add_column("Title", style="yellow")
table.add_column("Size", justify="center", style="green")

for i, result in enumerate(results, 1):
    size = f"{result.get('width', 'N/A')}×{result.get('height', 'N/A')}"
    table.add_row(str(i), result['title'][:40], size)

console.print(table)
```

------------------------------------------------------------------------

``` python
results = DDGS().images(
    query="butterfly",
    region="us-en",
    safesearch="off",
    timelimit="m",
    page=1,
    backend="auto",
    size=None,
    color="Monochrome",
    type_image=None,
    layout=None,
    license_image=None,
)
```

    ---------------------------------------------------------------------------
    DDGSException                             Traceback (most recent call last)
    Cell In[7], line 1
    ----> 1 results = DDGS().images(
          2     query="butterfly",
          3     region="us-en",
          4     safesearch="off",

    File ~/Documents/Knowledge/.venv/lib/python3.14/site-packages/ddgs/ddgs.py:223, in DDGS.images(self, query, **kwargs)
        221 def images(self, query: str, **kwargs: Any) -> list[dict[str, Any]]:  # noqa: ANN401
        222     """Perform an image search."""
    --> 223     return self._search("images", query, **kwargs)

    File ~/Documents/Knowledge/.venv/lib/python3.14/site-packages/ddgs/ddgs.py:215, in DDGS._search(self, category, query, keywords, region, safesearch, timelimit, max_results, page, backend, **kwargs)
        213 if "timed out" in f"{err}":
        214     raise TimeoutException(err)
    --> 215 raise DDGSException(err or "No results found.")

    DDGSException: No results found.

``` python
from rich.console import Console
from rich.table import Table

console = Console()

results = DDGS().images(
    query="butterfly",
    region="wt-wt",
    safesearch="off",
    timelimit=None,        # Day, Week, Month
    size=None,             # Small, Medium, Large, Wallpaper
    color="Monochrome",    # color name, Monochrome, color, BlackAndWhite
    type_image=None,       # photo, clipart, gif, transparent, line
    layout=None,           # Square, Tall, Wide
    license_image=None,    # any, Public, Share, ShareCommercially, Modify, ModifyCommercially
    max_results=10,
)

table = Table(title="Image Search Results")
table.add_column("#", justify="center", style="cyan")
table.add_column("Title", style="yellow")
table.add_column("Size", justify="center", style="green")

for i, result in enumerate(results, 1):
    size = f"{result.get('width', 'N/A')}x{result.get('height', 'N/A')}"
    table.add_row(str(i), result['title'][:40], size)

console.print(table)
```

    ---------------------------------------------------------------------------
    DDGSException                             Traceback (most recent call last)
    Cell In[4], line 6
          2 from rich.table import Table
          3 
          4 console = Console()
          5 
    ----> 6 results = DDGS().images(
          7     query="butterfly",
          8     region="wt-wt",
          9     safesearch="off",

    File ~/Documents/Knowledge/.venv/lib/python3.14/site-packages/ddgs/ddgs.py:223, in DDGS.images(self, query, **kwargs)
        221 def images(self, query: str, **kwargs: Any) -> list[dict[str, Any]]:  # noqa: ANN401
        222     """Perform an image search."""
    --> 223     return self._search("images", query, **kwargs)

    File ~/Documents/Knowledge/.venv/lib/python3.14/site-packages/ddgs/ddgs.py:215, in DDGS._search(self, category, query, keywords, region, safesearch, timelimit, max_results, page, backend, **kwargs)
        213 if "timed out" in f"{err}":
        214     raise TimeoutException(err)
    --> 215 raise DDGSException(err or "No results found.")

    DDGSException: No results found.

## 3. News search

``` python
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax

console = Console()

results = DDGS().news(
    query="AI regulation",
    region="us-en",
    safesearch="moderate",
    timelimit="d",         # d=day, w=week, m=month (no 'y' for news)
    max_results=5,
    page=1,
    backend="auto",
)

table = Table(title="📰 News Results", show_header=True)
table.add_column("Date", style="cyan")
table.add_column("Title", style="yellow")
table.add_column("Source", style="green")

for article in results:
    table.add_row(
        article.get('date', 'N/A')[:10],
        article['title'][:50],
        article.get('source', 'N/A')[:20]
    )

console.print(table)
```

------------------------------------------------------------------------

``` python
from rich.console import Console
from rich.table import Table

console = Console()

results = DDGS().news(
    query="AI regulation",
    region="us-en",
    safesearch="moderate",
    timelimit="d",         # d=day, w=week, m=month (no 'y' for news)
    max_results=5,
    page=1,
    backend="auto",
)

table = Table(title="News Results", show_header=True)
table.add_column("Date", style="cyan")
table.add_column("Title", style="yellow")
table.add_column("Source", style="green")

for article in results:
    table.add_row(
        article.get('date', 'N/A')[:10],
        article['title'][:50],
        article.get('source', 'N/A')[:20]
    )

console.print(table)
```

```
                                   📰 News Results                                    
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Date       ┃ Title                                              ┃ Source           ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ 2026-03-30 │ Iowa lawmakers weigh AI regulation while encouragi │ Telegraph Herald │
│ 2026-03-29 │ Sikh apex body demands reopening of Kartarpur Corr │ The Print        │
│ 2026-03-30 │ Indian startups turn to small languages models to  │ ET CIO           │
│ 2026-03-29 │ Some counties impose moratoriums on data centers,  │ KJZZ             │
│ 2026-03-30 │ IQM Secures €50M Financing to Accelerate Global Gr │ TMCnet           │
└────────────┴────────────────────────────────────────────────────┴──────────────────┘
```

## 4. Videos search

``` python
from rich.console import Console
from rich.panel import Panel

console = Console()

results = DDGS().videos(
    query="python tutorial",
    region="us-en",
    safesearch="moderate",
    timelimit=None,
    resolution=None,       # high, standard
    duration=None,         # short, medium, long
    license_videos=None,   # creativeCommon, youtube
    max_results=5,
)

for i, video in enumerate(results, 1):
    panel = Panel(
        f"[cyan]{video['title']}[/cyan]\n"
        f"[yellow]Uploader:[/yellow] {video.get('uploader', 'Unknown')}\n"
        f"[yellow]Duration:[/yellow] {video.get('duration', 'N/A')}\n"
        f"[blue]{video['embed_url']}[/blue]",
        title=f"[bold]Video {i}[/bold]",
        style="green"
    )
    console.print(panel)
```

------------------------------------------------------------------------

``` python
from rich.console import Console
from rich.panel import Panel

console = Console()

results = DDGS().videos(
    query="python tutorial",
    region="us-en",
    safesearch="moderate",
    timelimit=None,
    resolution=None,       # high, standard
    duration=None,         # short, medium, long
    license_videos=None,   # creativeCommon, youtube
    max_results=3,
)

for i, video in enumerate(results, 1):
    panel = Panel(
        f"[cyan]{video['title']}[/cyan]\n"
        f"[yellow]Uploader:[/yellow] {video.get('uploader', 'Unknown')}\n"
        f"[yellow]Duration:[/yellow] {video.get('duration', 'N/A')}\n"
        f"[blue]{video['embed_url']}[/blue]",
        title=f"[bold]Video {i}[/bold]",
        style="green"
    )
    console.print(panel)
```

```
╭──────────────────────────────────────────────────── Video 1 ────────────────────────────────────────────────────╮
│ Learn Python - Full Course for Beginners [Tutorial]                                                             │
│ Uploader: freeCodeCamp.org                                                                                      │
│ Duration: 4:26:52                                                                                               │
│ https://www.youtube.com/embed/rfscVS0vtbw?autoplay=1                                                            │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

```
╭──────────────────────────────────────────────────── Video 2 ────────────────────────────────────────────────────╮
│ Python for Beginners - Full Course [Programming Tutorial]                                                       │
│ Uploader: freeCodeCamp.org                                                                                      │
│ Duration: 4:40:00                                                                                               │
│ https://www.youtube.com/embed/eWRfhZUzrAc?autoplay=1                                                            │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

```
╭──────────────────────────────────────────────────── Video 3 ────────────────────────────────────────────────────╮
│ Python Tutorial for Beginners - Learn Python in 5 Hours [FULL COURSE]                                           │
│ Uploader: TechWorld with Nana                                                                                   │
│ Duration: 5:31:30                                                                                               │
│ https://www.youtube.com/embed/t8pPdKYpowI?autoplay=1                                                            │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## 5. Maps search

``` python
from rich.console import Console
from rich.table import Table

console = Console()

# Note: maps() method is not available in ddgs v8.1.1
console.print("[bold cyan]📍 Maps Search (Not Available)[/bold cyan]\n")

console.print("[yellow]Note:[/yellow] The [cyan]maps()[/cyan] method is not available in ddgs 8.1.1")
console.print("[dim]Maps functionality has been removed from recent versions of ddgs[/dim]\n")

console.print("[bold]Alternative approaches:[/bold]")
console.print("[cyan]1.[/cyan] Use location from other search methods")
console.print("[cyan]2.[/cyan] Use a dedicated maps API (Google Maps, OpenStreetMap)")
console.print("[cyan]3.[/cyan] Use reverse proxy if available")

# Example of what the code would look like (for reference):
console.print("\n[dim]═══ Reference Code (Non-functional) ═══[/dim]")
console.print("[dim]# By place name")
console.print("[dim]results = DDGS().maps(\"school\", place=\"Uganda\", max_results=10)[/dim]")
```

------------------------------------------------------------------------

``` python
from rich.console import Console
from rich.table import Table

console = Console()

# By place name
console.print("[bold cyan]Schools in Uganda[/bold cyan]\n")
results = DDGS().maps("school", place="Uganda", max_results=10)

table = Table(title="Location Results")
table.add_column("Name", style="yellow")
table.add_column("Address", style="cyan")
table.add_column("Country", style="green")

for result in results[:5]:
    table.add_row(
        result.get('title', 'N/A')[:30],
        result.get('address', 'N/A')[:35],
        result.get('country_code', 'N/A')
    )

console.print(table)

# By coordinates
console.print("\n[bold cyan]Coffee shops near Brisbane[/bold cyan]\n")
results = DDGS().maps(
    "coffee shop",
    latitude=-27.47,
    longitude=153.02,
    radius=5,              # km
    max_results=5,
)
console.print(f"[green]Found {len(results)} results[/green]")
```

```
📍 Schools in Uganda
```

    ---------------------------------------------------------------------------
    AttributeError                            Traceback (most recent call last)
    Cell In[9], line 8
          6 # By place name
          7 console.print("[bold cyan]📍 Schools in Uganda[/bold cyan]\n")
    ----> 8 results = DDGS().maps("school", place="Uganda", max_results=10)
         10 table = Table(title="Location Results")
         11 table.add_column("Name", style="yellow")

    AttributeError: 'DDGS' object has no attribute 'maps'

from rich.console import Console from rich.table import Table

console = Console()

# By place name

console.print(“\[bold cyan\]📍 Schools in Uganda\[/bold cyan\]”) results = DDGS().maps(“school”, place=“Uganda”, max_results=10)

if results: table = Table(title=“Location Results”) table.add_column(“Name”, style=“yellow”) table.add_column(“Address”, style=“cyan”) table.add_column(“Country”, style=“green”)

    for result in results[:5]:
        table.add_row(
            result.get('title', 'N/A')[:30],
            result.get('address', 'N/A')[:35],
            result.get('country_code', 'N/A')
        )

    console.print(table)

else: console.print(“\[yellow\]No results found\[/yellow\]”)

## 7. Proxy usage

``` python
from ddgs import DDGS
from rich.console import Console
from rich.panel import Panel

console = Console()

# Tor Browser ("tb" alias)
console.print("[bold cyan]🧅 Tor Browser Proxy[/bold cyan]\n")
try:
    ddgs = DDGS(proxy="tb", timeout=20)
    results = ddgs.text("privacy", max_results=5)
    panel = Panel(
        f"[green]✓ Connected via Tor[/green]\n"
        f"[yellow]Results found: {len(results)}[/yellow]",
        style="blue"
    )
    console.print(panel)
except Exception as e:
    console.print(f"[red]✗ Tor connection failed: {e}[/red]")

# Rotating residential proxy
console.print("\n[bold cyan]🌐 Rotating Residential Proxy[/bold cyan]\n")
ddgs = DDGS(proxy="socks5h://user:password@geo.iproyal.com:32325", timeout=20)
console.print("[yellow]⚙ Proxy configured[/yellow]")
console.print("[dim]Ready to make requests through rotating residential IP[/dim]")
```

------------------------------------------------------------------------

``` python
from ddgs import DDGS
from rich.console import Console
from rich.panel import Panel

console = Console()

# Tor Browser ("tb" alias)
console.print("[bold cyan]Tor Browser Proxy[/bold cyan]\n")
try:
    ddgs = DDGS(proxy="tb", timeout=20)
    results = ddgs.text("privacy", max_results=5)
    panel = Panel(
        f"[green]Connected via Tor[/green]\n"
        f"[yellow]Results found: {len(results)}[/yellow]",
        style="blue"
    )
    console.print(panel)
except Exception as e:
    console.print(f"[red]Tor connection failed: {e}[/red]")

# Rotating residential proxy
console.print("\n[bold cyan]Rotating Residential Proxy[/bold cyan]\n")
ddgs = DDGS(proxy="socks5h://user:password@geo.iproyal.com:32325", timeout=20)
console.print("[yellow]Proxy configured[/yellow]")
console.print("[dim]Ready to make requests through rotating residential IP[/dim]")
```

```
🧅 Tor Browser Proxy
```

```
✗ Tor connection failed: ConnectError: ConnectError('error sending request for url 
(https://html.duckduckgo.com/html/)', 'https://html.duckduckgo.com/html/')
```

```
🌐 Rotating Residential Proxy
```

```
⚙ Proxy configured
```

```
Ready to make requests through rotating residential IP
```

## 8. Specifying backends

``` python
from ddgs import DDGS
from rich.console import Console
from rich.table import Table

console = Console()

# Comma-delimited priority order
console.print("[bold cyan]Backend Priority Order[/bold cyan]\n")
results = DDGS().text(
    "climate change",
    backend="google, brave, yahoo",  # tried in order, falls back on error
    max_results=5,
)

table = Table(title="Results with Fallback Backends", show_header=True)
table.add_column("Result", style="yellow")
table.add_column("Info", style="cyan")
table.add_row("[green]✓ Success[/green]", f"Found {len(results)} from priority backends")

# Single backend
console.print("[bold cyan]\nSpecific Backend (Bing)[/bold cyan]\n")
results = DDGS().text("test", backend="bing", max_results=5)
panel_content = (
    f"[yellow]Backend:[/yellow] Bing\n"
    f"[yellow]Results:[/yellow] {len(results)}\n"
    f"[green]✓ Ready[/green]"
)
from rich.panel import Panel
console.print(Panel(panel_content, title="[bold]Bing Backend[/bold]", style="magenta"))
```

------------------------------------------------------------------------

``` python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# Comma-delimited priority order
console.print("[bold cyan]Backend Priority Order[/bold cyan]\n")
results = DDGS().text(
    "climate change",
    backend="google, brave, yahoo",  # tried in order, falls back on error
    max_results=5,
)

table = Table(title="Results with Fallback Backends", show_header=True)
table.add_column("Result", style="yellow")
table.add_column("Info", style="cyan")
table.add_row("[green]Success[/green]", f"Found {len(results)} from priority backends")

# Single backend
console.print("[bold cyan]\nSpecific Backend (Bing)[/bold cyan]\n")
results_bing = DDGS().text("test", backend="bing", max_results=5)
panel_content = (
    f"[yellow]Backend:[/yellow] Bing\n"
    f"[yellow]Results:[/yellow] {len(results_bing)}\n"
    f"[green]Ready[/green]"
)
console.print(Panel(panel_content, title="[bold]Bing Backend[/bold]", style="magenta"))
```

```
Backend Priority Order
```

```
Specific Backend (Bing)
```

```
╭───────────────────────────────────────────────── Bing Backend ──────────────────────────────────────────────────╮
│ Backend: Bing                                                                                                   │
│ Results: 5                                                                                                      │
│ ✓ Ready                                                                                                         │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## 9. Pagination

``` python
from ddgs import DDGS
from rich.console import Console
from rich.table import Table

console = Console()

console.print("[bold cyan]📄 Pagination Example[/bold cyan]\n")

# Page 1
p1 = DDGS().text("django orm", page=1, max_results=5)
console.print(f"[yellow]Page 1:[/yellow] Retrieved [green]{len(p1)}[/green] results")

# Page 2
p2 = DDGS().text("django orm", page=2, max_results=5)
console.print(f"[yellow]Page 2:[/yellow] Retrieved [green]{len(p2)}[/green] results")

# Compare results
table = Table(title="Pagination Comparison")
table.add_column("Page", justify="center", style="cyan")
table.add_column("Results", justify="center", style="yellow")
table.add_column("First Title", style="magenta")

if p1:
    table.add_row("1️⃣ ", str(len(p1)), p1[0]['title'][:35])
if p2:
    table.add_row("2️⃣ ", str(len(p2)), p2[0]['title'][:35])

console.print(table)
```

------------------------------------------------------------------------

``` python
from rich.console import Console
from rich.table import Table

console = Console()

console.print("[bold cyan]Pagination Example[/bold cyan]\n")

# Page 1
p1 = DDGS().text("django orm", page=1, max_results=5)
console.print(f"[yellow]Page 1:[/yellow] Retrieved [green]{len(p1)}[/green] results")

# Page 2
p2 = DDGS().text("django orm", page=2, max_results=5)
console.print(f"[yellow]Page 2:[/yellow] Retrieved [green]{len(p2)}[/green] results")

# Compare results
table = Table(title="Pagination Comparison")
table.add_column("Page", justify="center", style="cyan")
table.add_column("Results", justify="center", style="yellow")
table.add_column("First Title", style="magenta")

if p1:
    table.add_row("1", str(len(p1)), p1[0]['title'][:35])
if p2:
    table.add_row("2", str(len(p2)), p2[0]['title'][:35])

console.print(table)
```

```
📄 Pagination Example
```

```
Page 1: Retrieved 5 results
```

```
Page 2: Retrieved 5 results
```

```
        Pagination Comparison        
┏━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Page ┃ Results ┃ First Title      ┃
┡━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│  1️⃣  │    5    │ Django Reinhardt │
│  2️⃣  │    5    │ Django Reinhardt │
└──────┴─────────┴──────────────────┘
```

## 10. filetype + site: operators

``` python
from ddgs import DDGS
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns

console = Console()

console.print("[bold cyan]🔍 Advanced Search Operators[/bold cyan]\n")

# PDFs only
console.print("[yellow]📕 PDFs only:[/yellow]")
results = DDGS().text("economics in one lesson filetype:pdf", region="wt-wt", max_results=5)
pdf_panel = Panel(
    f"[green]✓ Found {len(results)} PDF results[/green]",
    title="[bold]filetype:pdf[/bold]",
    style="blue"
)
console.print(pdf_panel)

# From a specific domain
console.print("\n[yellow]🏛️ From specific domain:[/yellow]")
results = DDGS().text("sanctions filetype:xls site:gov.ua", max_results=5)
domain_panel = Panel(
    f"[green]✓ Found {len(results)} gov.ua results[/green]",
    title="[bold]site:gov.ua[/bold]",
    style="green"
)
console.print(domain_panel)

# Exact phrase
console.print("\n[yellow]💬 Exact phrase search:[/yellow]")
results = DDGS().text('"neuroscience exploring the brain" filetype:pdf', max_results=5)
exact_panel = Panel(
    f"[green]✓ Found {len(results)} exact phrase matches[/green]",
    title="[bold]Exact Phrase + Filetype[/bold]",
    style="magenta"
)
console.print(exact_panel)

console.print("\n[dim]Operators can be combined for powerful filtering![/dim]")
```

------------------------------------------------------------------------

``` python
from rich.console import Console
from rich.panel import Panel

console = Console()

console.print("[bold cyan]Advanced Search Operators[/bold cyan]\n")

# PDFs only
console.print("[yellow]PDFs only:[/yellow]")
results = DDGS().text("economics in one lesson filetype:pdf", region="wt-wt", max_results=5)
pdf_panel = Panel(
    f"[green]Found {len(results)} PDF results[/green]",
    title="[bold]filetype:pdf[/bold]",
    style="blue"
)
console.print(pdf_panel)

# From a specific domain
console.print("\n[yellow]From specific domain:[/yellow]")
results = DDGS().text("sanctions filetype:xls site:gov.ua", max_results=5)
domain_panel = Panel(
    f"[green]Found {len(results)} gov.ua results[/green]",
    title="[bold]site:gov.ua[/bold]",
    style="green"
)
console.print(domain_panel)

# Exact phrase
console.print("\n[yellow]Exact phrase search:[/yellow]")
results = DDGS().text('"neuroscience exploring the brain" filetype:pdf', max_results=5)
exact_panel = Panel(
    f"[green]Found {len(results)} exact phrase matches[/green]",
    title="[bold]Exact Phrase + Filetype[/bold]",
    style="magenta"
)
console.print(exact_panel)

console.print("\n[dim]Operators can be combined for powerful filtering![/dim]")
```

```
🔍 Advanced Search Operators
```

```
📕 PDFs only:
```

```
╭───────────────────────────────────────────────── filetype:pdf ──────────────────────────────────────────────────╮
│ ✓ Found 5 PDF results                                                                                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

```
🏛️ From specific domain:
```

```
╭────────────────────────────────────────────────── site:gov.ua ──────────────────────────────────────────────────╮
│ ✓ Found 5 gov.ua results                                                                                        │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

```
💬 Exact phrase search:
```

```
╭──────────────────────────────────────────── Exact Phrase + Filetype ────────────────────────────────────────────╮
│ ✓ Found 5 exact phrase matches                                                                                  │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

```
Operators can be combined for powerful filtering!
```

## 11. Error handling

``` python
from ddgs import DDGS
from ddgs.exceptions import RatelimitException, TimeoutException, DDGSException
from rich.console import Console

console = Console()

try:
    results = DDGS().text("test query", max_results=20)
    console.print(f"[green]✓ Found {len(results)} results[/green]")
except RatelimitException:
    console.print("[red]✗ Rate limited — rotate proxy or back off[/red]", style="bold")
except TimeoutException:
    console.print("[yellow]⚠ Request timed out[/yellow]", style="bold")
except DDGSException as e:
    console.print(f"[red]✗ Search error: {e}[/red]", style="bold")
```

------------------------------------------------------------------------

``` python
from ddgs import DDGS
from ddgs.exceptions import RatelimitException, TimeoutException, DDGSException
from rich.console import Console

console = Console()

try:
    results = DDGS().text("test query", max_results=20)
    console.print(f"[green]Found {len(results)} results[/green]")
except RatelimitException:
    console.print("[red]Rate limited: rotate proxy or back off[/red]", style="bold")
except TimeoutException:
    console.print("[yellow]Request timed out[/yellow]", style="bold")
except DDGSException as e:
    console.print(f"[red]Search error: {e}[/red]", style="bold")
```

```
✓ Found 20 results
```

## 12. Django/service wrapper pattern with Rich logging

Fits cleanly into a service layer:

``` python
# services/search.py
from ddgs import DDGS
from ddgs.exceptions import DDGSException
from rich.console import Console
import logging

logger = logging.getLogger(__name__)
console = Console()

class SearchService:
    def __init__(self, proxy=None, timeout=10):
        self._proxy = proxy
        self._timeout = timeout

    def _ddgs(self):
        return DDGS(proxy=self._proxy, timeout=self._timeout)

    def web(self, query: str, max_results: int = 10, region: str = "au-en") -> list[dict]:
        try:
            results = self._ddgs().text(query, region=region, max_results=max_results)
            console.print(f"[green]✓ Web search found {len(results)} results[/green]")
            return results
        except DDGSException as e:
            console.print(f"[red]✗ Web search failed: {e}[/red]")
            logger.warning("DDGS text search failed: %s", e)
            return []

    def news(self, query: str, timelimit: str = "w", max_results: int = 10) -> list[dict]:
        try:
            results = self._ddgs().news(query, timelimit=timelimit, max_results=max_results)
            console.print(f"[yellow]📰 Found {len(results)} news articles[/yellow]")
            return results
        except DDGSException as e:
            console.print(f"[red]✗ News search failed: {e}[/red]")
            logger.warning("DDGS news search failed: %s", e)
            return []
```

------------------------------------------------------------------------

## Quick reference

| Method | Return keys |
|----|----|
| `text()` | `title`, `href`, `body` |
| `news()` | `date`, `title`, `body`, `url`, `image`, `source` |
| `images()` | `title`, `image`, `thumbnail`, `url`, `height`, `width`, `source` |
| `videos()` | `content`, `description`, `duration`, `embed_url`, `image`, `published`, `publisher`, `title`, `uploader` |
| `maps()` | `title`, `address`, `country_code`, `url`, `phone`, `latitude`, `longitude`, `source`, `hours` |

------------------------------------------------------------------------

``` python
from ddgs import DDGS
from ddgs.exceptions import DDGSException
from rich.console import Console
import logging

logger = logging.getLogger(__name__)
console = Console()

class SearchService:
    def __init__(self, proxy=None, timeout=10):
        self._proxy = proxy
        self._timeout = timeout

    def _ddgs(self):
        return DDGS(proxy=self._proxy, timeout=self._timeout)

    def web(self, query: str, max_results: int = 10, region: str = "au-en") -> list[dict]:
        try:
            results = self._ddgs().text(query, region=region, max_results=max_results)
            console.print(f"[green]Web search found {len(results)} results[/green]")
            return results
        except DDGSException as e:
            console.print(f"[red]Web search failed: {e}[/red]")
            logger.warning("DDGS text search failed: %s", e)
            return []

    def news(self, query: str, timelimit: str = "w", max_results: int = 10) -> list[dict]:
        try:
            results = self._ddgs().news(query, timelimit=timelimit, max_results=max_results)
            console.print(f"[yellow]Found {len(results)} news articles[/yellow]")
            return results
        except DDGSException as e:
            console.print(f"[red]News search failed: {e}[/red]")
            logger.warning("DDGS news search failed: %s", e)
            return []

# Demo the service
console.print("[bold cyan]Service Layer Demo[/bold cyan]\n")
service = SearchService()
console.print("[yellow]Searching for 'Python'[/yellow]")
service.web("Python")
console.print("\n[yellow]Searching for news about AI[/yellow]")
service.news("AI")
```

```
🔧 Service Layer Demo
```

```
Searching for 'Python'
```

```
✓ Web search found 10 results
```

```
Searching for news about AI
```

```
📰 Found 10 news articles
```

    [{'date': '2026-03-27T21:05:00+00:00',
      'title': 'AI chatbots are probably giving you bad advice, new study finds',
      'body': 'Artificial intelligence chatbots are so prone to flattering and validating their human users that they are giving bad advice that can damage relationships and reinforce harmful behaviors, according to a new study.',
      'url': 'https://www.bostonglobe.com/2026/03/27/business/ai-chatbot-advice-study/',
      'image': 'https://bostonglobe-prod.cdn.arcpublishing.com/resizer/v2/J7I277R4SZGBZFDCH5XW47SIZI.jpg?auth=e385a2eef2ebc985887d47600a202761202c0b3bfdf59364f87a599704eb6d10&width=1440',
      'source': 'The Boston Globe'},
     {'date': '2026-03-27T13:24:00+00:00',
      'title': 'In the age of AI, your digital identity needs this protection',
      'body': "This stems from a fundamental gap in America's federal system: While the physical and digital property people own is protected by federal law, their faces and voices are not. Crucially, the bill would mandate a notice-and-stay-down standard.",
      'url': 'https://www.washingtonpost.com/opinions/2026/03/27/deepfake-youtube-likeness-rights/',
      'image': 'https://www.washingtonpost.com/wp-apps/imrs.php?src=https://cloudfront-us-east-1.images.arcpublishing.com/wapo/ZZP6TE52GBET5CGY75RFSWQMLQ.jpg&w=1440',
      'source': 'The Washington Post'},
     {'date': '2026-03-27T14:26:00+00:00',
      'title': 'Anthropic wins court order pausing Trump ban on AI tool',
      'body': "Anthropic PBC won a court order blocking a Trump administration ban on government use of the company's artificial intelligence technology, after the Claude chatbot maker argued the move could cost it billions in lost revenue.",
      'url': 'https://www.mercurynews.com/2026/03/27/anthropic-wins-court-order-pausing-trump-ban/',
      'image': 'https://www.mercurynews.com/wp-content/uploads/2026/02/SJM-Z-COL-OLSON-0208-JPEG-ANTHROPIC-AI.jpg?w=1024&h=683',
      'source': 'The Mercury News'},
     {'date': '2026-03-27T11:30:00+00:00',
      'title': "With Sora's death, AI's age of frivolity may be ending",
      'body': "I'm not embarrassed to admit I liked OpenAI's synthetic video social network. But I understand why it's going bye-bye.",
      'url': 'https://www.fastcompany.com/91516193/openai-sora-discontinued',
      'image': 'https://images.fastcompany.com/image/upload/f_webp,q_auto,c_fit/wp-cms-2/2026/03/p-1-91516193-with-soras-death-the-age-of-ai-side-quests-may-be-ending.jpg',
      'source': 'Fast Company'},
     {'date': '2026-03-30T07:09:00+00:00',
      'title': 'Mistral secures $830 million in debt financing to fund AI data center',
      'body': 'French AI startup Mistral has secured $830 million in debt financing. The funds will go towards operating a data center near Paris. The announcement comes as Mistral increasingly invests in building out AI infrastructure. In this article French AI startup ...',
      'url': 'https://www.cnbc.com/2026/03/30/mistral-ai-paris-data-center-cluster-debt-financing.html',
      'image': None,
      'source': 'CNBC'},
     {'date': '2026-03-30T06:33:00+00:00',
      'title': "'Most People Don't Enjoy Their Jobs:' Perplexity CEO Says AI Layoffs Are Chance To Launch AI-Powered Ventures",
      'body': 'Perplexity AI CEO Aravind Srinivas says workers should view AI-driven layoffs as a chance to leave unfulfilling jobs and start new, AI-powered ventures. AI Layoffs Create Entrepreneurial Opportunities On Monday,',
      'url': 'https://www.aol.com/articles/most-people-dont-enjoy-jobs-233315020.html',
      'image': 'https://s.yimg.com/os/en/aol_benzinga_275/3ce4eb1f9c8e3aab84634fcdc5c5b04b',
      'source': 'AOL'},
     {'date': '2026-03-30T06:04:07+00:00',
      'title': "France's Mistral raises $830 million in debt for AI data centre build-up",
      'body': "By Supantha Mukherjee and Leo Marchandon STOCKHOLM, March 30 - Europe's leading AI provider Mistral has raised $830 million in new debt to buy 13,800 Nvidia chips for a major data centre near Paris, the firm told Reuters,",
      'url': 'https://www.msn.com/en-us/news/technology/frances-mistral-raises-830-million-in-debt-for-ai-data-centre-build-up/ar-AA1ZH7sQ',
      'image': 'https://www.reuters.com/resizer/v2/6W64O7CSGFJTXKZMJ2K75VZ34A.jpg?auth=097e3be802785b0ffe6e1d0043512e7c4e25b585fc2c0a384e45115fcf1ef608&height=1005&width=1920&quality=80&smart=true',
      'source': 'Reuters'},
     {'date': '2026-03-30T05:32:00+00:00',
      'title': "All the latest in AI 'music'",
      'body': 'The Verge is about technology and how it makes us feel. Founded in 2011, we offer our audience everything from breaking news to reviews to award-winning features and investigations, on our site, in video,',
      'url': 'https://www.theverge.com/ai-artificial-intelligence/903196/ai-music-suno-udio-art-lawsuit',
      'image': None,
      'source': 'The Verge'},
     {'date': '2026-03-29T08:47:00+00:00',
      'title': "'Soon publishers won't stand a chance': literary world in struggle to detect AI-written books",
      'body': "US release of horror novel Shy Girl cancelled and UK book discontinued after suspected AI use, as publishers feel 'cold shiver'",
      'url': 'https://www.theguardian.com/technology/2026/mar/29/ai-written-books-novel-shy-girl-publishers',
      'image': None,
      'source': 'The Guardian'},
     {'date': '2026-03-30T03:26:00+00:00',
      'title': "'America Will Win The AI Race—But Only If…:' Mike Johnson Pushes Deregulation",
      'body': 'House Speaker Mike Johnson (R-La.) said the U.S. can lead the global AI race, but only if the government avoids heavy-handed regulation and private industry steps up as a "patriotic partner." US AI Leadership Push On Tuesday,',
      'url': 'https://www.aol.com/articles/america-win-ai-race-only-023111500.html',
      'image': 'https://s.yimg.com/os/en/aol_benzinga_275/c0cc13075b65e4f5901d8c22cdf7b625',
      'source': 'AOL'}]

Back to top
