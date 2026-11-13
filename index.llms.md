# Python Libraries

Reference notes on the Python libraries and tooling used across this collection: the numerical stack, dataframes, plotting, environments, and the language features worth knowing properly.

Author

Benedict Thekkel

This is the lookup site. When a notebook elsewhere in the collection reaches for `polars` or `pyecharts` or `asyncio`, the page explaining it is here.

The notes are deliberately uneven in depth. A few pages are exhaustive because the library repays it, with NumPy, Pandas, and the Python class model each running to hundreds of cells. Others are a page of the commands actually used. Depth tracks how often the thing is reached for, not how important it sounds.

------------------------------------------------------------------------

## Numerical Core

| Page | Covers |
|----|----|
| [NumPy](numpy.llms.md) | The largest page on the site, working through arrays, indexing, broadcasting, and the operations built on them |
| [SciPy](scipy.llms.md) | The scientific layer above NumPy |
| [NumExpr](numexpr.llms.md) | Faster evaluation of numerical expressions through multithreading, for when arrays get large enough to matter |

------------------------------------------------------------------------

## Dataframes

| Page | Covers |
|----|----|
| [Pandas](0_pandas.llms.md) | The long reference |
| [Polars](1_polars.llms.md) | The Rust-backed alternative |
| [Dask](dask.llms.md) | Parallel computing that scales from one machine to a cluster, for datasets larger than memory, integrating with NumPy, pandas, and scikit-learn |

------------------------------------------------------------------------

## Plotting and Diagrams

| Page | Covers |
|----|----|
| [Matplotlib](matplotlib.llms.md) | The default, and what everything else is measured against |
| [ECharts](Display/echarts.llms.md) | The most detailed of these, on `pyecharts`. ECharts describes a chart as one JSON-like option object covering data, axes, series, styling, and interaction. This is the charting library the deep learning notebooks are required to use |
| [Plotly](Display/plotly.llms.md) | Interactive publication-quality charts inside Jupyter |
| [Bokeh](Display/bokeh.llms.md) | Another interactive browser-rendered option |
| [Altair](Display/altair.llms.md) | Declarative interactive plots |
| [Graphviz](Display/graphviz.llms.md) | Graph and diagram layout from a text description |
| [Mermaid](Display/mermaid.llms.md) | Diagrams as markdown, which is what the diagram pages in [Software Tools](https://bthek1.github.io/Software_Tools/) are built from |
| [Manim](Display/manim.llms.md) | Programmatic mathematical animation |

------------------------------------------------------------------------

## The Language Itself

| Page | Covers |
|----|----|
| [Python Classes](Python/python_class.llms.md) | The object model at length: definition, inheritance, the dunder methods, and the protocols they implement |
| [asyncio](Python/python_asyncio.llms.md) | A complete reference targeting Python 3.11 and up, which is the meaningful floor because `TaskGroup`, `asyncio.timeout()`, and `task.uncancel()` all landed there and they change what correct code looks like |
| [Multiprocessing](Python/python_multiprocessing.llms.md) | The other concurrency route, for when the work is CPU-bound |
| [Logging](Python/python_logging.llms.md) | The standard library logging module |
| [argparse](Python/python_args.llms.md) | Command line arguments |
| [Dataclasses](dataclasses.llms.md) | The decorator that writes `__init__`, `__repr__`, and `__eq__` for you |
| [Datetime](datetime.llms.md) | Dates, times, timezones, and formatting |
| [AST](ast.llms.md) | Parsing, inspecting, and transforming Python source as a tree |

------------------------------------------------------------------------

## Environments and Packaging

Six tools that solve overlapping versions of the same problem, in roughly the order they appeared.

| Page | Covers |
|----|----|
| [venv](Environments/venv.llms.md) | The one in the standard library |
| [Pipenv](Environments/pipenv.llms.md) | Dependency resolution with a lockfile |
| [Poetry](Environments/poetry.llms.md) | Dependency management plus packaging |
| [Conda](Environments/conda.llms.md) | The scientific-stack option, which handles non-Python dependencies |
| [uv](Environments/uv.llms.md) | The Rust-based one this collection actually uses |
| [direnv](Environments/direnv.llms.md) | Loading and unloading an environment automatically on directory change |
| [Environment Variables](Environments/variables.llms.md) | How they work in Linux and how to manage them |

------------------------------------------------------------------------

## Code Quality and Testing

| Page | Covers |
|----|----|
| [Ruff](01_ruff.llms.md) | The fast Python-native linter that replaces flake8 and pylint, and overlaps Black |
| [Ruff Rule Categories](02_ruff_rule_categories.llms.md) | What each rule family prefix means, `F`, `E`, `W`, `N`, `B`, and the rest, and why you would enable it |
| [Black](black.llms.md) | The uncompromising formatter that ends style arguments by making the decisions for you |
| [pytest](0_pytest.llms.md) | Basics through fixtures, plugins, and practice |
| [Monkey Patching](1_monkey_patch.llms.md) | What it is, when it is justified, the risks, and how it shows up in pytest |

------------------------------------------------------------------------

## Notebooks and Terminal Output

| Page | Covers |
|----|----|
| [nbdev](nbdev.llms.md) | The framework this entire collection is built on, turning notebooks into libraries and docs |
| [Marimo](marimo.llms.md) | The reactive notebook alternative, and how it differs from JupyterLab |
| [ipywidgets](ipywidget.llms.md) | Interactive controls inside a notebook |
| [Rich](rich.llms.md) | Terminal output worth looking at: tables, progress, syntax highlighting |
| [tqdm](tqdm.llms.md) | A progress bar around any loop |

------------------------------------------------------------------------

## Data In

| Page | Covers |
|----|----|
| [Requests and HTTPX](request_and_httpx.llms.md) | The standard HTTP client against the one that adds async and HTTP/2 |
| [BeautifulSoup4](beautifulsoup4.llms.md) | Parsing HTML and XML, mostly for scraping |
| [duckduckgo-search](duckduckgo-search.llms.md) | Programmatic search across words, documents, images, news, and maps |
| [Kaggle](kaggle.llms.md) | Pulling competition and dataset files |
| [SQLAlchemy](sqlalchemy.llms.md) | The 2.x-style guide to Python’s ORM and query builder |
| [pytube](Other/pytube.llms.md) | Downloading video |

------------------------------------------------------------------------

## Odds and Ends

| Page | Covers |
|----|----|
| [Latexify](Other/latexify.llms.md) | Rendering a Python function as the LaTeX equation it implements |
| [Mito](Other/mito.llms.md) | A spreadsheet interface over a dataframe |
| [pivottablesjs](Other/pivottablesjs.llms.md) | Interactive pivot tables in a notebook |

------------------------------------------------------------------------

## Not Covered Yet

- **The site title says MLtools but the content is general Python.** Very little here is machine learning specific; the modelling libraries live in [ML Methods](https://bthek1.github.io/ML_methods/) and [DL Methods](https://bthek1.github.io/DL_methods/).
- **No page on `typing`**, despite type hints being unavoidable in modern Python.
- **Nothing on `pydantic`**, which is the validation layer most projects reach for.
- **`pathlib` and file handling** have no page, only incidental use elsewhere.
- **Six environment tools, no recommendation.** The pages describe each without saying which to pick, though the collection itself uses uv.
- [uv](Environments/uv.llms.md) is five cells against a tool the whole repo depends on, so it is the thinnest page relative to its importance.

------------------------------------------------------------------------

Back to top
