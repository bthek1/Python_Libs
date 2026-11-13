# Altair

Interactive Plots

Author

Benedict Thekkel

``` sh
pip install altair vega_datasets
```

``` python
!pip list | grep altair
!pip list | grep vega_datasets
!pip list | grep pandas
!pip list | grep geopandas
```

    altair                        5.1.2
    geopandas                     0.14.1
    pandas                        1.5.3
    geopandas                     0.14.1

``` python
import altair as alt
import numpy as np
import pandas as pd

# Compute x^2 + y^2 across a 2D grid
x, y = np.meshgrid(range(-5, 5), range(-5, 5))
z = x ** 2 + y ** 2

# Convert this grid to columnar data expected by Altair
source = pd.DataFrame({'x': x.ravel(),
                     'y': y.ravel(),
                     'z': z.ravel()})

alt.Chart(source).mark_rect().encode(
    x='x:O',
    y='y:O',
    color='z:Q'
)
```

``` python
import altair as alt
import pandas as pd

source = pd.DataFrame(
    [
        {"a": "a1", "b": "b1", "c": "x", "p": "0.14"},
        {"a": "a1", "b": "b1", "c": "y", "p": "0.60"},
        {"a": "a1", "b": "b1", "c": "z", "p": "0.03"},
        {"a": "a1", "b": "b2", "c": "x", "p": "0.80"},
        {"a": "a1", "b": "b2", "c": "y", "p": "0.38"},
        {"a": "a1", "b": "b2", "c": "z", "p": "0.55"},
        {"a": "a1", "b": "b3", "c": "x", "p": "0.11"},
        {"a": "a1", "b": "b3", "c": "y", "p": "0.58"},
        {"a": "a1", "b": "b3", "c": "z", "p": "0.79"},
        {"a": "a2", "b": "b1", "c": "x", "p": "0.83"},
        {"a": "a2", "b": "b1", "c": "y", "p": "0.87"},
        {"a": "a2", "b": "b1", "c": "z", "p": "0.67"},
        {"a": "a2", "b": "b2", "c": "x", "p": "0.97"},
        {"a": "a2", "b": "b2", "c": "y", "p": "0.84"},
        {"a": "a2", "b": "b2", "c": "z", "p": "0.90"},
        {"a": "a2", "b": "b3", "c": "x", "p": "0.74"},
        {"a": "a2", "b": "b3", "c": "y", "p": "0.64"},
        {"a": "a2", "b": "b3", "c": "z", "p": "0.19"},
        {"a": "a3", "b": "b1", "c": "x", "p": "0.57"},
        {"a": "a3", "b": "b1", "c": "y", "p": "0.35"},
        {"a": "a3", "b": "b1", "c": "z", "p": "0.49"},
        {"a": "a3", "b": "b2", "c": "x", "p": "0.91"},
        {"a": "a3", "b": "b2", "c": "y", "p": "0.38"},
        {"a": "a3", "b": "b2", "c": "z", "p": "0.91"},
        {"a": "a3", "b": "b3", "c": "x", "p": "0.99"},
        {"a": "a3", "b": "b3", "c": "y", "p": "0.80"},
        {"a": "a3", "b": "b3", "c": "z", "p": "0.37"},
    ]
)

alt.Chart(source, width=60, height=alt.Step(8)).mark_bar().encode(
    alt.Y("c:N").axis(None),
    alt.X("p:Q").title(None).axis(format="%"),
    alt.Color("c:N").title("settings").legend(orient="bottom", titleOrient="left"),
    alt.Row("a:N").title("Factor A").header(labelAngle=0),
    alt.Column("b:N").title("Factor B"),
).interactive()
```

``` python
import altair as alt
from vega_datasets import data

source = data.stocks()

highlight = alt.selection_point(on='mouseover', fields=['symbol'], nearest=True)

base = alt.Chart(source).encode(
    x='date:T',
    y='price:Q',
    color='symbol:N'
)

points = base.mark_circle().encode(
    opacity=alt.value(0)
).add_params(
    highlight
).properties(
    width=600
)

lines = base.mark_line().encode(
    size=alt.condition(~highlight, alt.value(1), alt.value(3))
)

points + lines
```

``` python
import altair as alt
from vega_datasets import data

source = data.unemployment_across_industries.url

selection = alt.selection_point(fields=['series'], bind='legend')

alt.Chart(source).mark_area().encode(
    alt.X('yearmonth(date):T').axis(domain=False, format='%Y', tickSize=0),
    alt.Y('sum(count):Q').stack('center').axis(None),
    alt.Color('series:N').scale(scheme='category20b'),
    opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
).add_params(
    selection
)
```

``` python
import altair as alt
from vega_datasets import data

source = data.cars()

alt.Chart(source).mark_circle().encode(
    alt.X(alt.repeat("column"), type='quantitative'),
    alt.Y(alt.repeat("row"), type='quantitative'),
    color='Origin:N'
).properties(
    width=150,
    height=150
).repeat(
    row=['Horsepower', 'Acceleration', 'Miles_per_Gallon'],
    column=['Miles_per_Gallon', 'Acceleration', 'Horsepower']
).interactive()
```

``` python
import altair as alt
from vega_datasets import data

source = data.seattle_weather.url

step = 20
overlap = 1

alt.Chart(source, height=step).transform_timeunit(
    Month='month(date)'
).transform_joinaggregate(
    mean_temp='mean(temp_max)', groupby=['Month']
).transform_bin(
    ['bin_max', 'bin_min'], 'temp_max'
).transform_aggregate(
    value='count()', groupby=['Month', 'mean_temp', 'bin_min', 'bin_max']
).transform_impute(
    impute='value', groupby=['Month', 'mean_temp'], key='bin_min', value=0
).mark_area(
    interpolate='monotone',
    fillOpacity=0.8,
    stroke='lightgray',
    strokeWidth=0.5
).encode(
    alt.X('bin_min:Q')
        .bin('binned')
        .title('Maximum Daily Temperature (C)'),
    alt.Y('value:Q')
        .axis(None)
        .scale(range=[step, -step * overlap]),
    alt.Fill('mean_temp:Q')
        .legend(None)
        .scale(domain=[30, 5], scheme='redyellowblue')
).facet(
    row=alt.Row('Month:T')
        .title(None)
        .header(labelAngle=0, labelAlign='left', format='%B')
).properties(
    title='Seattle Weather',
    bounds='flush'
).configure_facet(
    spacing=0
).configure_view(
    stroke=None
).configure_title(
    anchor='end'
)
```

``` python
import altair as alt
from vega_datasets import data

source = data.seattle_weather()

alt.Chart(source, title="Daily Max Temperatures (C) in Seattle, WA").mark_rect().encode(
    alt.X("date(date):O").title("Day").axis(format="%e", labelAngle=0),
    alt.Y("month(date):O").title("Month"),
    alt.Color("max(temp_max)").title(None),
    tooltip=[
        alt.Tooltip("monthdate(date)", title="Date"),
        alt.Tooltip("max(temp_max)", title="Max Temp"),
    ],
).configure_view(
    step=13,
    strokeWidth=0
).configure_axis(
    domain=False
)
```

``` python
import altair as alt
from vega_datasets import data

states = alt.topo_feature(data.us_10m.url, 'states')
source = data.income.url

alt.Chart(source).mark_geoshape().encode(
    shape='geo:G',
    color='pct:Q',
    tooltip=['name:N', 'pct:Q'],
    facet=alt.Facet('group:N', columns=2),
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(data=states, key='id'),
    as_='geo'
).properties(
    width=300,
    height=175,
).project(
    type='albersUsa'
)
```

``` python
import altair as alt
from vega_datasets import data
import geopandas as gpd

# load data
gdf_quakies = gpd.read_file(data.earthquakes.url, driver="GeoJSON")
gdf_world = gpd.read_file(data.world_110m.url, driver="TopoJSON")

# defintion for interactive brush
brush = alt.selection_interval(
    encodings=["longitude"],
    empty=False,
    value={"longitude": [-50, -110]}
)

# world disk
sphere = alt.Chart(alt.sphere()).mark_geoshape(
    fill="transparent", stroke="lightgray", strokeWidth=1
)

# countries as shapes
world = alt.Chart(gdf_world).mark_geoshape(
    fill="lightgray", stroke="white", strokeWidth=0.1
)

# earthquakes as dots on map
quakes = alt.Chart(gdf_quakies).transform_calculate(
    lon="datum.geometry.coordinates[0]",
    lat="datum.geometry.coordinates[1]",
).mark_circle(opacity=0.35, tooltip=True).encode(
    longitude="lon:Q",
    latitude="lat:Q",
    color=alt.condition(brush, alt.value("goldenrod"), alt.value("steelblue")),
    size=alt.Size("mag:Q").scale(type="pow", range=[1, 1000], domain=[0, 7], exponent=4),
).add_params(brush)

# combine layers for the map
left_map = alt.layer(sphere, world, quakes).project(type="mercator")

# histogram of binned earthquakes
bars = alt.Chart(gdf_quakies).mark_bar().encode(
    x=alt.X("mag:Q").bin(extent=[0,7]),
    y="count(mag):Q",
    color=alt.value("steelblue")
)

# filtered earthquakes
bars_overlay = bars.encode(color=alt.value("goldenrod")).transform_filter(brush)

# combine layers for histogram
right_bars = alt.layer(bars, bars_overlay)

# vertical concatenate map and bars
left_map | right_bars
```

``` python
import altair as alt
import pandas as pd
import numpy as np

np.random.seed(0)

n_objects = 20
n_times = 50

# Create one (x, y) pair of metadata per object
locations = pd.DataFrame({
    'id': range(n_objects),
    'x': np.random.randn(n_objects),
    'y': np.random.randn(n_objects)
})

# Create a 50-element time-series for each object
timeseries = pd.DataFrame(np.random.randn(n_times, n_objects).cumsum(0),
                          columns=locations['id'],
                          index=pd.RangeIndex(0, n_times, name='time'))

# Melt the wide-form timeseries into a long-form view
timeseries = timeseries.reset_index().melt('time')

# Merge the (x, y) metadata into the long-form view
timeseries['id'] = timeseries['id'].astype(int)  # make merge not complain
data = pd.merge(timeseries, locations, on='id')

# Data is prepared, now make a chart

selector = alt.selection_point(fields=['id'])

base = alt.Chart(data).properties(
    width=250,
    height=250
).add_params(selector)

points = base.mark_point(filled=True, size=200).encode(
    x='mean(x)',
    y='mean(y)',
    color=alt.condition(selector, 'id:O', alt.value('lightgray'), legend=None),
)

timeseries = base.mark_line().encode(
    x='time',
    y=alt.Y('value').scale(domain=(-15, 15)),
    color=alt.Color('id:O').legend(None)
).transform_filter(
    selector
)

points | timeseries
```

``` python
import altair as alt
import vega_datasets

alt.Chart(
    vega_datasets.data.barley.url,
    title='Barley Yield comparison between 1932 and 1931'
).mark_trail().encode(
    alt.X('year:O').title(None),
    alt.Y('variety:N').title('Variety'),
    alt.Size('yield:Q')
        .scale(range=[0, 12])
        .legend(values=[20, 60])
        .title('Barley Yield (bushels/acre)'),
    alt.Color('delta:Q')
        .scale(domainMid=0)
        .title('Yield Delta (%)'),
    alt.Tooltip(['year:O', 'yield:Q']),
    alt.Column('site:N').title('Site')
).transform_pivot(
    "year",
    value="yield",
    groupby=["variety", "site"]
).transform_fold(
    ["1931", "1932"],
    as_=["year", "yield"]
).transform_calculate(
    calculate="datum['1932'] - datum['1931']",
    as_="delta"
).configure_legend(
    orient='bottom',
    direction='horizontal'
).configure_view(
    stroke=None
)
```

``` python
import altair as alt
from vega_datasets import data

source = data.disasters.url

alt.Chart(source).transform_filter(
    alt.datum.Entity != 'All natural disasters'
).mark_circle(
    opacity=0.8,
    stroke='black',
    strokeWidth=1,
    strokeOpacity=0.4
).encode(
    alt.X('Year:T')
        .title(None)
        .scale(domain=['1899','2018']),
    alt.Y('Entity:N')
        .title(None)
        .sort(field="Deaths", op="sum", order='descending'),
    alt.Size('Deaths:Q')
        .scale(range=[0, 2500])
        .title('Deaths')
        .legend(clipHeight=30, format='s'),
    alt.Color('Entity:N').legend(None),
    tooltip=[
        "Entity:N",
        alt.Tooltip("Year:T", format='%Y'),
        alt.Tooltip("Deaths:Q", format='~s')
    ],
).properties(
    width=450,
    height=320,
    title=alt.Title(
        text="Global Deaths from Natural Disasters (1900-2017)",
        subtitle="The size of the bubble represents the total death count per year, by type of disaster",
        anchor='start'
    )
).configure_axisY(
    domain=False,
    ticks=False,
    offset=10
).configure_axisX(
    grid=False,
).configure_view(
    stroke=None
)
```

``` python
import altair as alt
from vega_datasets import data

source = data.seattle_weather()

color = alt.Color('weather:N').scale(
    domain=['sun', 'fog', 'drizzle', 'rain', 'snow'],
    range=['#e7ba52', '#a7a7a7', '#aec7e8', '#1f77b4', '#9467bd']
)

# We create two selections:
# - a brush that is active on the top panel
# - a multi-click that is active on the bottom panel
brush = alt.selection_interval(encodings=['x'])
click = alt.selection_point(encodings=['color'])

# Top panel is scatter plot of temperature vs time
points = alt.Chart().mark_point().encode(
    alt.X('monthdate(date):T').title('Date'),
    alt.Y('temp_max:Q')
        .title('Maximum Daily Temperature (C)')
        .scale(domain=[-5, 40]),
    alt.Size('precipitation:Q').scale(range=[5, 200]),
    color=alt.condition(brush, color, alt.value('lightgray')),
).properties(
    width=550,
    height=300
).add_params(
    brush
).transform_filter(
    click
)

# Bottom panel is a bar chart of weather type
bars = alt.Chart().mark_bar().encode(
    x='count()',
    y='weather:N',
    color=alt.condition(click, color, alt.value('lightgray')),
).transform_filter(
    brush
).properties(
    width=550,
).add_params(
    click
)

alt.vconcat(
    points,
    bars,
    data=source,
    title="Seattle Weather: 2012-2015"
)
```

Back to top
