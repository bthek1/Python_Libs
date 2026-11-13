# ECharts in Python — A Complete Guide (pyecharts)

**ECharts** is a JavaScript charting library (Apache, originally Baidu). It renders charts in the browser by taking a single JSON-like **option object** that fully describes the chart: data, axes, series, styling, interactions.

Author

Benedict Thekkel

## Contents

1.  Setup & how rendering works in Jupyter
2.  The mental model: the option object
3.  Anatomy of a chart (the builder pattern)
4.  Basic charts: bar, line, pie, scatter
5.  Multiple series, stacking, mixed bar+line
6.  Global options (title, legend, tooltip, axis, toolbox)
7.  Series options (labels, markpoints, areastyle, itemstyle)
8.  Theming
9.  `JsCode` — the escape hatch for callbacks/formatters
10. Advanced gallery: candlestick, heatmap, radar, gauge, funnel, graph, boxplot
11. Maps / geo
12. Composition: Grid, Tab, Page, Timeline
13. Interactivity: DataZoom & VisualMap
14. Exporting (HTML / image)
15. Bridge to ECharts in JS / React

------------------------------------------------------------------------

## 1. Setup & how rendering works in Jupyter

``` bash
uv add pyecharts
```

Rendering options: - `chart.render("out.html")` -\> standalone HTML file. - `chart.render_notebook()` -\> inline in Jupyter. **This is what we use here.**

A wrinkle: pyecharts’ built-in `render_notebook()` for JupyterLab emits markup that calls `echarts.init()` but never loads the ECharts JS library (it assumes an old lab extension provides a global `echarts`). In JupyterLab 4, VS Code, and the static Quarto export that global doesn’t exist, so charts come out as a **blank box**.

The next cell fixes this once: it overrides `render_notebook()` to embed the self-contained standalone HTML (which carries its own `<script src=...echarts.min.js>`) inside an iframe. After running it, every `chart.render_notebook()` below renders correctly everywhere, including the published docs. Run it first.

------------------------------------------------------------------------

``` python
from pyecharts.globals import CurrentConfig

# assets.pyecharts.org serves an expired TLS certificate from most nodes (2026-11-11),
# so charts failed to load. jsDelivr mirrors the same assets, pinned to one commit.
CurrentConfig.ONLINE_HOST = "https://cdn.jsdelivr.net/gh/pyecharts/pyecharts-assets@f2328d558550046fc5449672a6850e848e141590/assets/v6/"

from pyecharts.globals import CurrentConfig, NotebookType

import pyecharts
print("pyecharts", pyecharts.__version__)

# --- Make render_notebook() render everywhere -----------------------------
# pyecharts' JUPYTER_LAB output calls echarts.init() but never loads the
# echarts JS library -- it assumes a JupyterLab extension exposes a global
# `echarts`. In modern JupyterLab 4, VS Code, and the static Quarto export
# that global is absent, so charts render as a blank box.
#
# Fix: override render_notebook() to embed pyecharts' self-contained
# standalone HTML (render_embed(), which ships its own <script src=...
# echarts.min.js>) inside an iframe. That renders correctly in every
# environment, including the published GitHub Pages docs.
import html as _html
from pyecharts.charts.base import Base
from pyecharts.charts.composite_charts.tab import Tab as _Tab
from pyecharts.charts.composite_charts.page import Page as _Page
from pyecharts.render.display import HTML


def _iframe_height(chart):
    h = getattr(chart, "height", None)
    try:
        return int(float(str(h).replace("px", ""))) + 42
    except (TypeError, ValueError):
        return 560  # composites (Tab/Page) report no single height


def _render_notebook_iframe(self, height=None):
    doc = _html.escape(self.render_embed())
    px = height or _iframe_height(self)
    return HTML(
        f'<iframe srcdoc="{doc}" width="100%" height="{px}" '
        f'frameborder="0" scrolling="auto" style="border:none;"></iframe>'
    )


# Base covers single charts, Grid, Timeline; Tab and Page define their own.
for _cls in (Base, _Tab, _Page):
    _cls.render_notebook = _render_notebook_iframe
```

    pyecharts 2.1.0

``` python
# Common imports used throughout
from pyecharts import options as opts
from pyecharts.charts import (
    Bar, Line, Pie, Scatter, Grid, Tab, Page, Timeline,
    Kline, HeatMap, Gauge, Radar, Funnel, Graph, Map, Boxplot,
)
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
```

## 2. The mental model: the option object

Every chart is one big config dict. pyecharts gives you a typed, chainable API that produces it. You can always inspect the raw JSON with `.dump_options()` — this is the single most useful thing to understand what pyecharts is actually doing, and it’s exactly what you’d hand to `echarts.setOption()` in JS.

------------------------------------------------------------------------

``` python
bar = (
    Bar()
    .add_xaxis(["Mon", "Tue", "Wed"])
    .add_yaxis("Visits", [120, 200, 150])
    .set_global_opts(title_opts=opts.TitleOpts(title="Tiny example"))
)

import json
opt = json.loads(bar.dump_options())
print("Top-level option keys:", list(opt.keys()))
print()
print("series ->", json.dumps(opt["series"], ensure_ascii=False, indent=2)[:400])
```

    Top-level option keys: ['animation', 'animationThreshold', 'animationDuration', 'animationEasing', 'animationDelay', 'animationDurationUpdate', 'animationEasingUpdate', 'animationDelayUpdate', 'aria', 'series', 'legend', 'tooltip', 'xAxis', 'yAxis', 'title']

    series -> [
      {
        "type": "bar",
        "name": "Visits",
        "legendHoverLink": true,
        "data": [
          120,
          200,
          150
        ],
        "realtimeSort": false,
        "showBackground": false,
        "stackStrategy": "samesign",
        "cursor": "pointer",
        "barMinHeight": 0,
        "barCategoryGap": "20%",
        "barGap": "30%",
        "large": false,
        "largeThreshold": 400,
        "seriesLayoutBy": "column",
        "

Note the keys: `series`, `xAxis`, `yAxis`, `legend`, `tooltip`, `title`. That’s the ECharts schema. pyecharts is camelCase-on-the-wire even though the Python API is snake_case.

``` python
bar.render_notebook()
```

## 3. Anatomy of a chart (the builder pattern)

pyecharts charts are built by **method chaining**, and the order matters conceptually but not syntactically:

| Step | Method | Purpose |
|----|----|----|
| 1 | `Bar(init_opts=...)` | construct, set canvas-level options (size, theme, bg) |
| 2 | `.add_xaxis(categories)` | category axis data |
| 3 | `.add_yaxis(name, data, ...)` | a **series** — call multiple times for multiple series |
| 4 | `.set_series_opts(...)` | per-series styling (labels, markers, area) |
| 5 | `.set_global_opts(...)` | everything not tied to one series (title, legend, tooltip, axes, zoom) |

`init_opts` is special: it configures the *canvas/instance*, not the option object — width, height, theme, renderer (canvas vs svg), animation.

------------------------------------------------------------------------

``` python
demo = (
    Bar(init_opts=opts.InitOpts(width="700px", height="400px", theme=ThemeType.LIGHT))
    .add_xaxis(["Cliniko", "Nookal", "Splose"])
    .add_yaxis("Clinics", [42, 18, 9])
    .add_yaxis("Active syncs", [40, 15, 7])
    .set_series_opts(label_opts=opts.LabelOpts(position="top"))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="CRM integrations", subtitle="builder pattern"),
        yaxis_opts=opts.AxisOpts(name="count"),
    )
)
demo.render_notebook()
```

## 4. Basic charts

### Bar

------------------------------------------------------------------------

``` python
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
bar = (
    Bar()
    .add_xaxis(months)
    .add_yaxis("PROMs sent", [320, 332, 301, 334, 390, 330])
    .add_yaxis("PROMs completed", [220, 282, 251, 234, 290, 281])
    .set_global_opts(title_opts=opts.TitleOpts(title="Questionnaire throughput"))
)
bar.render_notebook()
```

### Line — smooth, stepped, area

``` python
line = (
    Line()
    .add_xaxis(months)
    .add_yaxis("Completion %", [68, 85, 83, 70, 74, 85], is_smooth=True)
    .add_yaxis(
        "Target %", [80, 80, 80, 80, 80, 80],
        is_step=False,
        linestyle_opts=opts.LineStyleOpts(type_="dashed"),
        symbol="none",
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Completion rate vs target"),
        yaxis_opts=opts.AxisOpts(max_=100, axislabel_opts=opts.LabelOpts(formatter="{value}%")),
    )
)
line.render_notebook()
```

### Pie / doughnut

``` python
pie = (
    Pie()
    .add(
        "",
        [("Cliniko", 42), ("Nookal", 18), ("Splose", 9), ("Other", 4)],
        radius=["40%", "70%"],   # inner+outer radius => doughnut
        center=["50%", "55%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Clinics by CRM"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="left"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
)
pie.render_notebook()
```

Label placeholders are worth memorising: `{a}` series name, `{b}` data name/category, `{c}` value, `{d}` percent (pie only).

### Scatter

``` python
import random
random.seed(7)
xs = list(range(0, 50))
ys = [x * 1.8 + random.uniform(-12, 12) for x in xs]
scatter = (
    Scatter()
    .add_xaxis(xs)
    .add_yaxis("samples", ys, symbol_size=10)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Scatter"),
        xaxis_opts=opts.AxisOpts(type_="value"),   # numeric x, not category
        yaxis_opts=opts.AxisOpts(type_="value"),
        visualmap_opts=opts.VisualMapOpts(type_="size", max_=100, min_=0),
    )
)
scatter.render_notebook()
```

## 5. Multiple series, stacking, mixed bar+line

**Stacking**: give series the same `stack` group name.

------------------------------------------------------------------------

``` python
stack = (
    Bar()
    .add_xaxis(months)
    .add_yaxis("Email", [120, 132, 101, 134, 90, 130], stack="channel")
    .add_yaxis("SMS",   [220, 182, 191, 234, 290, 330], stack="channel")
    .add_yaxis("Portal",[150, 232, 201, 154, 190, 330], stack="channel")
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="Sends by channel (stacked)"))
)
stack.render_notebook()
```

**Mixed bar + line** uses `.overlap()`. The trick: add a **second y-axis** with `extend_axis`, then point the line series at axis index 1.

``` python
bar = (
    Bar()
    .add_xaxis(months)
    .add_yaxis("Sends", [320, 332, 301, 334, 390, 330])
    .extend_axis(yaxis=opts.AxisOpts(name="rate %", max_=100,
                 axislabel_opts=opts.LabelOpts(formatter="{value}%")))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Volume (bar) + completion rate (line)"),
        yaxis_opts=opts.AxisOpts(name="count"),
    )
)
line = (
    Line()
    .add_xaxis(months)
    .add_yaxis("Completion %", [68, 85, 83, 70, 74, 85], yaxis_index=1, is_smooth=True)
)
bar.overlap(line).render_notebook()
```

## 6. Global options

`set_global_opts` is where most configuration lives. The big ones:

- `title_opts` — title/subtitle, position, link
- `legend_opts` — which series are toggleable, orientation, position
- `tooltip_opts` — hover behaviour; `trigger="axis"` shows all series at an x, `"item"` shows one point
- `xaxis_opts` / `yaxis_opts` — `AxisOpts`: type (`value`/`category`/`time`/`log`), min/max, label formatter, splitlines
- `toolbox_opts` — built-in save-as-image / data-view / zoom buttons
- `datazoom_opts`, `visualmap_opts` — covered in §13

------------------------------------------------------------------------

``` python
rich = (
    Line()
    .add_xaxis(months)
    .add_yaxis("A", [10, 22, 28, 23, 19, 40])
    .add_yaxis("B", [15, 18, 12, 30, 25, 20])
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Global options demo", subtitle="hover, legend, toolbox"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(pos_top="8%"),
        xaxis_opts=opts.AxisOpts(boundary_gap=False, name="month"),
        yaxis_opts=opts.AxisOpts(
            name="value",
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
    )
)
rich.render_notebook()
```

## 7. Series options

`set_series_opts` controls how the drawn marks look and what annotations attach to them.

- `label_opts` — data labels (show/hide, position, formatter, color)
- `markpoint_opts` / `markline_opts` — annotate max/min/average automatically
- `areastyle_opts` — fill under a line
- `itemstyle_opts` — bar/point color, border, opacity, border radius

------------------------------------------------------------------------

``` python
area = (
    Line()
    .add_xaxis(months)
    .add_yaxis(
        "latency ms",
        [120, 132, 101, 134, 90, 230],
        is_smooth=True,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.3),
        markpoint_opts=opts.MarkPointOpts(data=[
            opts.MarkPointItem(type_="max", name="max"),
            opts.MarkPointItem(type_="min", name="min"),
        ]),
        markline_opts=opts.MarkLineOpts(data=[
            opts.MarkLineItem(type_="average", name="avg"),
        ]),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="Area + markpoint/markline"))
)
area.render_notebook()
```

``` python
# itemstyle: per-bar colour + rounded corners
styled = (
    Bar()
    .add_xaxis(["p50", "p90", "p95", "p99"])
    .add_yaxis(
        "ms",
        [
            opts.BarItem(name="p50", value=80, itemstyle_opts=opts.ItemStyleOpts(color="#2ec97e")),
            opts.BarItem(name="p90", value=140, itemstyle_opts=opts.ItemStyleOpts(color="#2e9dc9")),
            opts.BarItem(name="p95", value=190, itemstyle_opts=opts.ItemStyleOpts(color="#f4a261")),
            opts.BarItem(name="p99", value=320, itemstyle_opts=opts.ItemStyleOpts(color="#e76f51")),
        ],
        category_gap="40%",
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="Per-item styling"))
)
styled.render_notebook()
```

## 8. Theming

Pass a built-in theme via `InitOpts(theme=...)`. Themes set the palette, background, and default text styles. Common ones: `LIGHT`, `DARK`, `WESTEROS`, `CHALK`, `ESSOS`, `MACARONS`, `ROMA`, `SHINE`, `VINTAGE`, `PURPLE_PASSION`.

------------------------------------------------------------------------

``` python
themed = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK, width="700px", height="380px"))
    .add_xaxis(months)
    .add_yaxis("A", [10, 22, 28, 23, 19, 40])
    .add_yaxis("B", [15, 18, 12, 30, 25, 20])
    .add_yaxis("C", [8, 12, 22, 14, 28, 16])
    .set_global_opts(title_opts=opts.TitleOpts(title="DARK theme"))
)
themed.render_notebook()
```

For a fully custom palette without a theme, set `color` via `InitOpts(... )` isn’t enough — use `set_colors`:

``` python
brand = (
    Bar()
    .add_xaxis(months)
    .add_yaxis("A", [10, 22, 28, 23, 19, 40])
    .add_yaxis("B", [15, 18, 12, 30, 25, 20])
    .set_colors(["#0f2130", "#2ec97e"])
    .set_global_opts(title_opts=opts.TitleOpts(title="Custom brand colours"))
)
brand.render_notebook()
```

## 9. `JsCode` — the escape hatch

The Python API can’t express *callbacks* — and ECharts uses JS functions for formatters, color logic, label content, etc. `JsCode("...")` injects a raw JS function string into the option. This is how you reach the ~10% of ECharts the typed API doesn’t cover.

Use it for: custom tooltip HTML, conditional colours, dynamic label text, axis formatters with logic.

------------------------------------------------------------------------

``` python
js_demo = (
    Bar()
    .add_xaxis(["p50", "p90", "p95", "p99"])
    .add_yaxis(
        "ms",
        [80, 140, 190, 320],
        itemstyle_opts=opts.ItemStyleOpts(
            # colour bars red if value > 200, else green
            color=JsCode(
                "function(p){ return p.value > 200 ? '#e76f51' : '#2ec97e'; }"
            )
        ),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="JsCode conditional colour"),
        tooltip_opts=opts.TooltipOpts(
            formatter=JsCode(
                "function(p){ return p.name + '<br/>' + p.value + ' ms' + "
                "(p.value > 200 ? '  slow' : '  ok'); }"
            )
        ),
    )
)
js_demo.render_notebook()
```

**Caveat:** `JsCode` strings are not validated in Python — a typo fails silently in the browser. Keep them short; if logic gets complex, that’s a signal to move to raw ECharts in JS.

## 10. Advanced gallery

### Candlestick (Kline) — financial OHLC

Data per point is `[open, close, low, high]`.

------------------------------------------------------------------------

``` python
kdata = [
    [20, 34, 10, 38], [40, 35, 30, 50], [31, 38, 33, 44],
    [38, 15, 5, 42], [25, 30, 20, 35], [30, 40, 28, 46],
]
kline = (
    Kline()
    .add_xaxis([f"d{i}" for i in range(len(kdata))])
    .add_yaxis("OHLC", kdata)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Candlestick"),
        xaxis_opts=opts.AxisOpts(is_scale=True),
        yaxis_opts=opts.AxisOpts(is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(is_show=True,
                areastyle_opts=opts.AreaStyleOpts(opacity=1))),
        datazoom_opts=[opts.DataZoomOpts(type_="inside")],
    )
)
kline.render_notebook()
```

### Heatmap

``` python
import itertools, random
random.seed(1)
hours = [f"{h}:00" for h in range(0, 24, 3)]
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
hdata = [[h, d, random.randint(0, 30)] for h, d in itertools.product(range(len(hours)), range(len(days)))]
heat = (
    HeatMap()
    .add_xaxis(hours)
    .add_yaxis("submissions", days, hdata,
               label_opts=opts.LabelOpts(is_show=True, position="inside"))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Submissions heatmap"),
        visualmap_opts=opts.VisualMapOpts(min_=0, max_=30, orient="horizontal", pos_left="center"),
    )
)
heat.render_notebook()
```

### Radar

``` python
radar = (
    Radar()
    .add_schema(schema=[
        opts.RadarIndicatorItem(name="Latency", max_=100),
        opts.RadarIndicatorItem(name="Uptime", max_=100),
        opts.RadarIndicatorItem(name="Coverage", max_=100),
        opts.RadarIndicatorItem(name="DX", max_=100),
        opts.RadarIndicatorItem(name="Docs", max_=100),
    ])
    .add("Cliniko adapter", [[82, 99, 90, 70, 60]],
         areastyle_opts=opts.AreaStyleOpts(opacity=0.2))
    .add("Nookal adapter", [[70, 95, 75, 65, 80]],
         areastyle_opts=opts.AreaStyleOpts(opacity=0.2))
    .set_global_opts(title_opts=opts.TitleOpts(title="Adapter comparison"))
)
radar.render_notebook()
```

### Gauge

``` python
gauge = (
    Gauge()
    .add("", [("SLA met", 96)], split_number=5,
         axisline_opts=opts.AxisLineOpts(
             linestyle_opts=opts.LineStyleOpts(
                 color=[(0.5, "#e76f51"), (0.8, "#f4a261"), (1, "#2ec97e")], width=20)))
    .set_global_opts(title_opts=opts.TitleOpts(title="SLA gauge"))
)
gauge.render_notebook()
```

### Funnel

``` python
funnel = (
    Funnel()
    .add("conversion",
         [("Invited", 1000), ("Opened", 720), ("Started", 540), ("Completed", 410)],
         label_opts=opts.LabelOpts(position="inside"))
    .set_global_opts(title_opts=opts.TitleOpts(title="Questionnaire funnel"))
)
funnel.render_notebook()
```

### Graph (force-directed network)

``` python
g_nodes = [
    opts.GraphNode(name="API", symbol_size=40),
    opts.GraphNode(name="Cliniko", symbol_size=25),
    opts.GraphNode(name="Nookal", symbol_size=25),
    opts.GraphNode(name="Splose", symbol_size=25),
    opts.GraphNode(name="Celery", symbol_size=20),
    opts.GraphNode(name="Postgres", symbol_size=30),
]
g_links = [
    opts.GraphLink(source="API", target="Cliniko"),
    opts.GraphLink(source="API", target="Nookal"),
    opts.GraphLink(source="API", target="Splose"),
    opts.GraphLink(source="API", target="Celery"),
    opts.GraphLink(source="Celery", target="Postgres"),
    opts.GraphLink(source="API", target="Postgres"),
]
graph = (
    Graph()
    .add("", g_nodes, g_links, repulsion=2000,
         linestyle_opts=opts.LineStyleOpts(curve=0.1))
    .set_global_opts(title_opts=opts.TitleOpts(title="Service graph"))
)
graph.render_notebook()
```

### Boxplot

``` python
raw = [
    [82, 90, 88, 95, 70, 60, 99, 85],   # Cliniko latencies
    [70, 75, 80, 65, 90, 60, 55, 72],   # Nookal
    [120, 130, 110, 140, 100, 160, 90, 125],  # Splose
]
box = Boxplot()
prepared = box.prepare_data(raw)   # computes min/Q1/median/Q3/max
box = (
    box.add_xaxis(["Cliniko", "Nookal", "Splose"])
       .add_yaxis("latency ms", prepared)
       .set_global_opts(title_opts=opts.TitleOpts(title="Latency distribution"))
)
box.render_notebook()
```

## 11. Maps / geo

`Map` colours regions by value. Built-in map names include `"china"`, `"world"`, and country names like `"australia"`. Region names must match the map’s expected labels (English for `world`/country maps). Map geometry loads from a CDN at render time, so the rendered notebook needs network access.

------------------------------------------------------------------------

``` python
aus = (
    Map()
    .add("Clinics", [
        ("Queensland", 42), ("New South Wales", 30), ("Victoria", 25),
        ("Western Australia", 12), ("South Australia", 8), ("Tasmania", 3),
        ("Northern Territory", 2), ("Australian Capital Territory", 5),
    ], "australia")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Clinics by state"),
        visualmap_opts=opts.VisualMapOpts(max_=45, is_piecewise=False),
    )
)
aus.render_notebook()
```

## 12. Composition

Four ways to combine charts:

| Tool | Use |
|----|----|
| `.overlap()` | superimpose series on the *same* coordinate system (bar+line) — shown in §5 |
| `Grid` | multiple *separate* coordinate systems on one canvas (subplots) |
| `Tab` | tabbed pages, one chart each |
| `Page` | vertically stacked dashboard of many charts in one HTML |
| `Timeline` | one chart animated across a time/category dimension with a play control |

### Grid (subplots)

------------------------------------------------------------------------

``` python
bar_g = (
    Bar()
    .add_xaxis(months)
    .add_yaxis("sends", [320, 332, 301, 334, 390, 330], label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Top: volume"),
        legend_opts=opts.LegendOpts(pos_top="2%"),
    )
)
line_g = (
    Line()
    .add_xaxis(months)
    .add_yaxis("rate %", [68, 85, 83, 70, 74, 85], is_smooth=True)
    .set_global_opts(legend_opts=opts.LegendOpts(pos_top="52%"))
)
grid = (
    Grid(init_opts=opts.InitOpts(height="500px"))
    .add(bar_g, grid_opts=opts.GridOpts(pos_bottom="58%"))
    .add(line_g, grid_opts=opts.GridOpts(pos_top="55%"))
)
grid.render_notebook()
```

### Tab

``` python
tab = Tab()
tab.add(bar, "Throughput")
tab.add(pie, "CRM split")
tab.add(heat, "Heatmap")
tab.render_notebook()
```

### Timeline

Each frame is a full chart; the widget animates between them.

``` python
tl = Timeline(init_opts=opts.InitOpts(width="700px"))
for year in [2022, 2023, 2024, 2025]:
    base = 100 + (year - 2022) * 40
    frame = (
        Bar()
        .add_xaxis(["Cliniko", "Nookal", "Splose"])
        .add_yaxis("clinics", [base, base // 2, base // 4])
        .set_global_opts(title_opts=opts.TitleOpts(title=f"Clinics, {year}"),
                         yaxis_opts=opts.AxisOpts(max_=260))
    )
    tl.add(frame, str(year))
tl.add_schema(is_auto_play=True, play_interval=1200)
tl.render_notebook()
```

## 13. Interactivity: DataZoom & VisualMap

### DataZoom

Lets users zoom/pan an axis. `type_="inside"` = scroll/drag on the chart; `type_="slider"` = a draggable bar below. Useful for dense time series.

------------------------------------------------------------------------

``` python
import math
xs = [f"t{i}" for i in range(200)]
ys = [round(50 + 30 * math.sin(i / 8) + random.uniform(-5, 5), 1) for i in range(200)]
zoomed = (
    Line()
    .add_xaxis(xs)
    .add_yaxis("metric", ys, is_symbol_show=False)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="DataZoom on a long series"),
        datazoom_opts=[
            opts.DataZoomOpts(type_="inside"),
            opts.DataZoomOpts(type_="slider", range_start=0, range_end=30),
        ],
    )
)
zoomed.render_notebook()
```

### VisualMap

Maps a data dimension to a visual channel (colour or size) continuously or piecewise. Common with heatmaps, maps, and scatter; also colours a line by value.

``` python
vm = (
    Line()
    .add_xaxis(xs)
    .add_yaxis("metric", ys, is_symbol_show=False)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="VisualMap: colour by y-value"),
        visualmap_opts=opts.VisualMapOpts(
            min_=20, max_=80, dimension=1,
            range_color=["#2ec97e", "#f4a261", "#e76f51"],
            orient="horizontal", pos_left="center", pos_bottom="0%",
        ),
    )
)
vm.render_notebook()
```

## 14. Exporting

- **Standalone HTML:** `chart.render("chart.html")` → fully self-contained page (JS from CDN by default).
- **Embeddable HTML fragment:** `chart.render_embed()` → returns an HTML string you can drop into a template.
- **Static image (PNG/SVG):** requires `snapshot-selenium` + a browser driver, or `snapshot-phantomjs`. ECharts is browser-rendered, so there’s no pure-Python image path.

``` python
chart.render("out.html")            # file
html_str = chart.render_embed()     # string

# image (needs: pip install snapshot-selenium  + chromedriver)
from snapshot_selenium import snapshot
from pyecharts.render import make_snapshot
make_snapshot(snapshot, bar.render(), "bar.png")
```

------------------------------------------------------------------------

``` python
# Demonstrate HTML export (works offline; no browser needed)
path = bar.render("/tmp/echarts_demo.html")
import os
print("Wrote", path, "-", os.path.getsize(path), "bytes")
```

    Wrote /tmp/echarts_demo.html - 8491 bytes

## 15. Bridge to ECharts in JS / React

Since you render ECharts in a React 19 SPA, the most valuable thing pyecharts gives you is **`dump_options_with_quotes()`** — the exact option object to feed `echarts.setOption()`. You can prototype a chart in Python, dump the option, and paste it into your React component.

------------------------------------------------------------------------

``` python
# Get the JS-ready option string (JsCode functions preserved correctly)
option_str = bar.dump_options_with_quotes()
print(option_str[:600], "...")
```

    {
        "animation": true,
        "animationThreshold": 2000,
        "animationDuration": 1000,
        "animationEasing": "cubicOut",
        "animationDelay": 0,
        "animationDurationUpdate": 300,
        "animationEasingUpdate": "cubicOut",
        "animationDelayUpdate": 0,
        "aria": {
            "enabled": false
        },
        "series": [
            {
                "type": "bar",
                "name": "Sends",
                "legendHoverLink": true,
                "data": [
                    320,
                    332,
                    301,
                    334,
                    390,
                    330
                ],
                "real ...

In React you’d typically use `echarts-for-react` or call the core API directly:

``` tsx
import ReactECharts from 'echarts-for-react';

const option = { /* paste/adapt the dumped option here */ };

export function ThroughputChart() {
  return <ReactECharts option={option} style={{ height: 400 }} />;
}
```

Or with the bare library and a ref:

``` tsx
import * as echarts from 'echarts';
import { useEffect, useRef } from 'react';

export function Chart({ option }: { option: echarts.EChartsOption }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const inst = echarts.init(ref.current!);
    inst.setOption(option);
    const onResize = () => inst.resize();
    window.addEventListener('resize', onResize);
    return () => { window.removeEventListener('resize', onResize); inst.dispose(); };
  }, [option]);
  return <div ref={ref} style={{ height: 400 }} />;
}
```

### When to use which

- **pyecharts**: server-rendered reports, notebooks, quick exploration, or when Python already holds the data and you want a static HTML artifact. Good for emailed/PDF dashboards.
- **ECharts directly in React**: anything interactive in your SPA. Don’t round-trip through pyecharts at runtime — have your DRF API return *data*, and build the option object in TypeScript. Use pyecharts/`dump_options` only as a **design-time** tool to discover the right option shape.

One honest caveat: pyecharts lags upstream ECharts releases, and its typed API doesn’t cover every newest option. For React, treat the official ECharts docs (`echarts.apache.org/en/option.html`) as the source of truth; pyecharts is the fast prototyping path, not the spec.

------------------------------------------------------------------------

**Recap of the whole model:** a chart is one option object → `series` + axes + global config. pyecharts builds it via chained `add_*`/`set_*_opts`; `JsCode` covers callbacks; `dump_options` reveals the JSON; composition is `overlap`/`Grid`/`Tab`/`Page`/`Timeline`; interactivity is `DataZoom`/`VisualMap`. The same option shape is exactly what `echarts.setOption()` consumes in your React app.

Back to top
