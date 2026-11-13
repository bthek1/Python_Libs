# Bokeh

[Bokeh](https://docs.bokeh.org/en/latest/#)

Author

Benedict Thekkel

    pip install bokeh

``` python
pip list | grep bokeh
```

    bokeh                     3.6.3
    Note: you may need to restart the kernel to use updated packages.

## Initialize bokeh for Notebook

``` python
from bokeh.io import output_notebook
```

``` python
output_notebook()
```

Loading BokehJS ...

## Simple line graph

``` python
from bokeh.plotting import figure, show

# prepare some data
x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]

# create a new plot with a title and axis labels
p = figure(title="Simple line example", x_axis_label='x', y_axis_label='y')


# add a line renderer with legend and line thickness to the plot
p.line(x, y, legend_label="Temp.", line_width=2)

# show the results
show(p)
```

## Multiple Line graphs

``` python
from bokeh.plotting import figure, show

# prepare some data
x = [1, 2, 3, 4, 5]
y1 = [6, 7, 2, 4, 5]
y2 = [2, 3, 4, 5, 6]
y3 = [4, 5, 5, 7, 2]

# create a new plot with a title and axis labels
p = figure(title="Multiple line example", x_axis_label="x", y_axis_label="y")

# add multiple renderers
p.line(x, y1, legend_label="Temp.", color="blue", line_width=2)
p.line(x, y2, legend_label="Rate", color="red", line_width=2)
p.line(x, y3, legend_label="Objects", color="green", line_width=2)

# show the results
show(p)
```

``` python
from bokeh.plotting import figure, output_file, save

# prepare some data
x = [1, 2, 3, 4, 5]
y = [4, 5, 5, 7, 2]

# set output to static HTML file
output_file(filename="custom_filename.html", title="Static HTML file")

# create a new plot with a specific size
p = figure(sizing_mode="stretch_width", max_width=500, height=250)

# add a scatter renderer
p.scatter(x, y, fill_color="red", size=15)

# save the results to a file
save(p)
```

    '/home/ben/BENEDICT_Only/Benedict_Projects/Benedict_ML/MLtools/nbs/custom_filename.html'

## Multiple types

``` python
from bokeh.plotting import figure, show

# prepare some data
x = [1, 2, 3, 4, 5]
y1 = [6, 7, 2, 4, 5]
y2 = [2, 3, 4, 5, 6]
y3 = [4, 5, 5, 7, 2]

# create a new plot with a title and axis labels
p = figure(title="Multiple glyphs example", x_axis_label="x", y_axis_label="y")

# add multiple renderers
p.line(x, y1, legend_label="Temp.", color="blue", line_width=2)
p.vbar(x=x, top=y2, legend_label="Rate", width=0.5, bottom=0, color="red")
p.scatter(x, y3, legend_label="Objects", color="yellow", size=12)

# show the results
show(p)
```

## Legends, text and annotations

``` python
import random
from bokeh.io import curdoc
from bokeh.models import BoxAnnotation
from bokeh.plotting import figure, show
# apply theme to current document
curdoc().theme = "dark_minimal"

# generate some data (1-50 for x, random values for y)
x = list(range(0, 51))
y = random.sample(range(0, 100), 51)

# create new plot
p = figure(title="Box annotation example")

# add line renderer
line = p.line(x, y, line_color="#000000", line_width=2)

# add box annotations
low_box = BoxAnnotation(top=20, fill_alpha=0.2, fill_color="#F0E442")
mid_box = BoxAnnotation(bottom=20, top=80, fill_alpha=0.2, fill_color="#009E73")
high_box = BoxAnnotation(bottom=80, fill_alpha=0.2, fill_color="#F0E442")

# add boxes to existing figure
p.add_layout(low_box)
p.add_layout(mid_box)
p.add_layout(high_box)

# show the results
show(p)
```

``` python
import random
from datetime import UTC, datetime, timedelta

from bokeh.models import DatetimeTickFormatter, NumeralTickFormatter
from bokeh.plotting import figure, show

# generate list of dates (today's date in subsequent weeks)
dates = [(datetime.now(UTC) + timedelta(day * 7)) for day in range(0, 26)]

# generate 25 random data points
y = random.sample(range(0, 100), 26)

# create new plot
p = figure(
    title="datetime axis example",
    x_axis_type="datetime",
    sizing_mode="stretch_width",
    max_width=500,
    height=250,
)

# add renderers
p.scatter(dates, y, size=8)
p.line(dates, y, color="navy", line_width=1)

# format axes ticks
p.yaxis[0].formatter = NumeralTickFormatter(format="$0.00")
p.xaxis[0].formatter = DatetimeTickFormatter(months="%b %Y")

# show the results
show(p)
```

## Vectorizing colors and sizes

``` python
import numpy as np

from bokeh.plotting import figure, show

# generate some data
N = 1000
x = np.random.random(size=N) * 100
y = np.random.random(size=N) * 100

# generate radii and colors based on data
radii = y / 100 * 2
colors = [f"#{255:02x}{int((value * 255) / 100):02x}{255:02x}" for value in y]

# create a new plot with a specific size
p = figure(
    title="Vectorized colors and radii example",
    sizing_mode="stretch_width",
    max_width=500,
    height=250,
)

# add circle renderer
p.circle(
    x,
    y,
    radius=radii,
    fill_color=colors,
    fill_alpha=0.6,
    line_color="lightgrey",
)

# show the results
show(p)
```

## Combining plots

``` python
from bokeh.layouts import row
from bokeh.plotting import figure, show

# prepare some data
x = list(range(11))
y0 = x
y1 = [10 - i for i in x]
y2 = [abs(i - 5) for i in x]

# create three plots with one renderer each
s1 = figure(width=250, height=250, background_fill_color="#fafafa")
s1.scatter(x, y0, marker="circle", size=12, color="#53777a", alpha=0.8)

s2 = figure(width=250, height=250, background_fill_color="#fafafa")
s2.scatter(x, y1, marker="triangle", size=12, color="#c02942", alpha=0.8)

s3 = figure(width=250, height=250, background_fill_color="#fafafa")
s3.scatter(x, y2, marker="square", size=12, color="#d95b43", alpha=0.8)

# put the results in a row that automatically adjusts
# to the browser window's width
show(row(children=[s1, s2, s3], sizing_mode="scale_width"))
```

## Using widgets

``` python
from bokeh.layouts import layout
from bokeh.models import Div, RangeSlider, Spinner
from bokeh.plotting import figure, show

# prepare some data
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [4, 5, 5, 7, 2, 6, 4, 9, 1, 3]

# create plot with circle glyphs
p = figure(x_range=(1, 9), width=500, height=250)
points = p.scatter(x=x, y=y, size=30, fill_color="#21a7df")

# set up textarea (div)
div = Div(
    text="""
          <p>Select the circle's size using this control element:</p>
          """,
    width=200,
    height=30,
)

# set up spinner
spinner = Spinner(
    title="Circle size",
    low=0,
    high=60,
    step=5,
    value=points.glyph.size,
    width=200,
)
spinner.js_link("value", points.glyph, "size")

# set up RangeSlider
range_slider = RangeSlider(
    title="Adjust x-axis range",
    start=0,
    end=10,
    step=1,
    value=(p.x_range.start, p.x_range.end),
)
range_slider.js_link("value", p.x_range, "start", attr_selector=0)
range_slider.js_link("value", p.x_range, "end", attr_selector=1)

# create layout
layout = layout(
    [
        [div, spinner],
        [range_slider],
        [p],
    ],
)

# show result
show(layout)
```

## Example

``` python
from math import pi

import pandas as pd

from bokeh.palettes import Category20c
from bokeh.plotting import figure, show
from bokeh.transform import cumsum

x = {
    'United States': 157,
    'United Kingdom': 93,
    'Japan': 89,
    'China': 63,
    'Germany': 44,
    'India': 42,
    'Italy': 40,
    'Australia': 35,
    'Brazil': 32,
    'France': 31,
    'Taiwan': 31,
    'Spain': 29,
}

data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'country'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = Category20c[len(x)]

p = figure(height=350, title="Pie Chart", toolbar_location=None,
           tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

p.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='country', source=data)

p.axis.axis_label = None
p.axis.visible = False
p.grid.grid_line_color = None

show(p)
```

``` python
import bokeh
```

``` python
bokeh.sampledata.download()
```

    Using data directory: /home/ben/.bokeh/data
    Skipping 'CGM.csv' (checksum match)
    Skipping 'US_Counties.zip' (checksum match)
    Skipping 'us_cities.json' (checksum match)
    Skipping 'unemployment09.csv' (checksum match)
    Skipping 'AAPL.csv' (checksum match)
    Skipping 'FB.csv' (checksum match)
    Skipping 'GOOG.csv' (checksum match)
    Skipping 'IBM.csv' (checksum match)
    Skipping 'MSFT.csv' (checksum match)
    Skipping 'WPP2012_SA_DB03_POPULATION_QUINQUENNIAL.zip' (checksum match)
    Skipping 'gapminder_fertility.csv' (checksum match)
    Skipping 'gapminder_population.csv' (checksum match)
    Skipping 'gapminder_life_expectancy.csv' (checksum match)
    Skipping 'gapminder_regions.csv' (checksum match)
    Skipping 'world_cities.zip' (checksum match)
    Skipping 'airports.json' (checksum match)
    Skipping 'movies.db.zip' (checksum match)
    Skipping 'airports.csv' (checksum match)
    Skipping 'routes.csv' (checksum match)
    Skipping 'haarcascade_frontalface_default.xml' (checksum match)
    Skipping 'SampleSuperstore.csv.zip' (checksum match)
    Skipping 'emissions.csv' (checksum match)
    Skipping 'titanic_all.csv' (checksum match)

``` python
import pandas as pd

from bokeh.palettes import Spectral4
from bokeh.plotting import figure, show
from bokeh.sampledata.stocks import AAPL, GOOG, IBM, MSFT

p = figure(width=800, height=250, x_axis_type="datetime")
p.title.text = 'Click on legend entries to hide the corresponding lines'

for data, name, color in zip([AAPL, IBM, MSFT, GOOG], ["AAPL", "IBM", "MSFT", "GOOG"], Spectral4):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    p.line(df['date'], df['close'], line_width=2, color=color, alpha=0.8, legend_label=name)

p.legend.location = "top_left"
p.legend.click_policy="mute"

show(p)
```

Back to top
