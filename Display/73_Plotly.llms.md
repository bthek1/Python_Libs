# Plotly

Plotly is a powerful and flexible library for creating interactive, publication-quality graphs in Jupyter Labs. It integrates seamlessly with Python and Jupyter, enabling data scientists and analysts to visualize complex datasets easily.

Author

Benedict Thekkel

## **1. Overview**

- **Plotly** is an open-source graphing library that makes interactive, publication-quality graphs.
- It is built on top of **D3.js** and **WebGL**.
- Integrates seamlessly with Jupyter Labs and supports inline rendering.
- It has two main interfaces:
  - **Plotly Express**: High-level interface for quick, concise plotting.
  - **Graph Objects**: Low-level, flexible interface for detailed customization.

------------------------------------------------------------------------

## **2. Installing Plotly for Jupyter Labs**

To get started with Plotly in Jupyter Labs, you need to install the following:

### **Install Plotly Library**

``` bash
pip install plotly
```

### **Install JupyterLab Extensions**

To render Plotly figures within JupyterLab, you need to install the following extensions:

``` bash
# JupyterLab 3.x and above (Extensions are auto-managed)
pip install jupyterlab "ipywidgets>=7.5"

# For older JupyterLab versions, you might need:
jupyter labextension install jupyterlab-plotly
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

### **Check Installation**

``` python

import plotly
print(plotly.__version__)  # Should be 5.x or above
```

Ensure you have **Plotly version 5.x or above** for the latest features.

------------------------------------------------------------------------

``` python
import plotly
print(plotly.__version__)  # Should be 5.x or above
```

    6.0.0

## **3. Importing Plotly**

``` python
import plotly.express as px
import plotly.graph_objects as go
```

- **Plotly Express (px)**: High-level, easy-to-use interface for rapid plotting.
- **Graph Objects (go)**: Low-level, flexible API for detailed customization.

------------------------------------------------------------------------

``` python
import plotly.express as px
import plotly.graph_objects as go
```

## **4. Plotly Express Basics**

### **4.1. Line Chart**

``` python
import plotly.express as px
import numpy as np
import pandas as pd

# Sample Data
x = np.linspace(0, 10, 100)
y = np.sin(x)

df = pd.DataFrame({'x': x, 'y': y})

# Line Plot
fig = px.line(df, x='x', y='y', title='Sine Wave')
fig.show()

---

### **4.2. Scatter Plot**

```python
fig = px.scatter(df, x='x', y='y', title='Scatter Plot of Sine Wave')
fig.show()
```

### **4.3. Bar Chart**

``` python
data = {'Fruits': ['Apple', 'Banana', 'Cherry', 'Date'],
        'Quantity': [10, 20, 15, 5]}

df = pd.DataFrame(data)

fig = px.bar(df, x='Fruits', y='Quantity', title='Fruit Quantity')
fig.show()
```

### **4.4. Histogram**

``` python
fig = px.histogram(df, x='Quantity', title='Histogram of Quantity')
fig.show()
```

### **4.5. Pie Chart**

``` python
fig = px.pie(df, names='Fruits', values='Quantity', title='Fruit Distribution')
fig.show()
```

------------------------------------------------------------------------

``` python
import plotly.express as px
import numpy as np
import pandas as pd
import plotly.offline as pyo
from IPython.display import HTML, display
# Sample Data
x = np.linspace(0, 10, 100)
y = np.sin(x)

df = pd.DataFrame({'x': x, 'y': y})
# Turn off the menu bar
config = {
    'displayModeBar': False  # Disable the mode bar (menu bar)
}

# Line Plot
fig = px.line(df, x='x', y='y', title='Sine Wave')
# fig.show(config=config)
fig_html = fig.to_html(full_html=False, config=config)
display(HTML(fig_html))

fig = px.scatter(df, x='x', y='y', title='Scatter Plot of Sine Wave')
# fig.show(config=config)
fig_html = fig.to_html(full_html=False, config=config)
display(HTML(fig_html))
```

``` python
data = {'Fruits': ['Apple', 'Banana', 'Cherry', 'Date'],
        'Quantity': [10, 20, 15, 5]}

df = pd.DataFrame(data)

fig = px.bar(df, x='Fruits', y='Quantity', title='Fruit Quantity')
fig_html = fig.to_html(full_html=False, config=config)
display(HTML(fig_html))


fig = px.histogram(df, x='Quantity', title='Histogram of Quantity')
fig_html = fig.to_html(full_html=False, config=config)
display(HTML(fig_html))


fig = px.pie(df, names='Fruits', values='Quantity', title='Fruit Distribution')
fig_html = fig.to_html(full_html=False, config=config)
display(HTML(fig_html))
```

## **5. Advanced Plotly Express Features**

### **5.1. Facet Plots**

``` python
df = px.data.tips()

fig = px.scatter(df, x="total_bill", y="tip", color="sex",
                 facet_col="time", facet_row="smoker",
                 title="Facet Plot of Tips")
fig.show()
```

### **5.2. Animations**

``` python
df = px.data.gapminder()

fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", 
                 animation_group="country", size="pop", color="continent",
                 hover_name="country", log_x=True, size_max=55, 
                 range_x=[100,100000], range_y=[25,90],
                 title="Gapminder Animation")
fig.show()
```

### **5.3. 3D Scatter Plot**

``` python
fig = px.scatter_3d(df, x='gdpPercap', y='lifeExp', z='pop', 
                    color='continent', size='pop', 
                    hover_name='country', log_x=True, 
                    title="3D Scatter Plot of Gapminder Data")
fig.show()
```

### **5.4. Geographic Plots**

``` python
fig = px.choropleth(df, locations="iso_alpha",
                    color="lifeExp",
                    hover_name="country",
                    animation_frame="year",
                    title="World Life Expectancy Over Time")
fig.show()
```

------------------------------------------------------------------------

``` python
df = px.data.tips()

fig = px.scatter(df, x="total_bill", y="tip", color="sex",
                 facet_col="time", facet_row="smoker",
                 title="Facet Plot of Tips")
fig.show()

df = px.data.gapminder()

fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", 
                 animation_group="country", size="pop", color="continent",
                 hover_name="country", log_x=True, size_max=55, 
                 range_x=[100,10000], range_y=[25,90],
                 title="Gapminder Animation")
fig.show()
```

## **6. Plotly Graph Objects (Advanced Customization)**

### **6.1. Line Chart**

``` python
fig = go.Figure()

fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Sine Wave'))
fig.update_layout(title='Sine Wave', xaxis_title='X', yaxis_title='Y')
fig.show()
```

### **6.2. Subplots**

``` python
from plotly.subplots import make_subplots

fig = make_subplots(rows=2, cols=2)

fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Line Plot'), row=1, col=1)
fig.add_trace(go.Scatter(x=x, y=np.cos(x), mode='markers', name='Scatter Plot'), row=1, col=2)
fig.add_trace(go.Bar(x=['A', 'B', 'C'], y=[5, 10, 15], name='Bar Chart'), row=2, col=1)
fig.add_trace(go.Pie(labels=['Apple', 'Banana', 'Cherry'], values=[10, 20, 30], name='Pie Chart'), row=2, col=2)

fig.update_layout(title='Multiple Plots')
fig.show()
```

### **6.3. Annotations and Shapes**

``` python
fig.update_layout(
    annotations=[dict(x=2, y=0, xref="x", yref="y", text="Annotation",
                      showarrow=True, arrowhead=2)],
    shapes=[dict(type="line", x0=2, y0=-1, x1=2, y1=1, 
                 line=dict(color="RoyalBlue", width=2))]
)
fig.show()
```

------------------------------------------------------------------------

``` python
fig = go.Figure()

fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Sine Wave'))
fig.update_layout(title='Sine Wave', xaxis_title='X', yaxis_title='Y')
fig.show()

from plotly.subplots import make_subplots

fig = make_subplots(rows=2, cols=2)

fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Line Plot'), row=1, col=1)
fig.add_trace(go.Scatter(x=x, y=np.cos(x), mode='markers', name='Scatter Plot'), row=1, col=2)
fig.add_trace(go.Bar(x=['A', 'B', 'C'], y=[5, 10, 15], name='Bar Chart'), row=2, col=1)
# fig.add_trace(go.Pie(labels=['Apple', 'Banana', 'Cherry'], values=[10, 20, 30], name='Pie Chart'), row=2, col=2)

fig.update_layout(title='Multiple Plots')
fig.show()

fig.update_layout(
    annotations=[dict(x=2, y=0, xref="x", yref="y", text="Annotation",
                      showarrow=True, arrowhead=2)],
    shapes=[dict(type="line", x0=2, y0=-1, x1=2, y1=1, 
                 line=dict(color="RoyalBlue", width=2))]
)
fig.show()
```

## **7. Saving and Exporting**

### **7.1. Static Images**

``` python
fig.write_image("plot.png")   # PNG format
fig.write_image("plot.pdf")   # PDF format
```

**Dependencies**:

``` bash
pip install -U kaleido  # Required for static image export
```

### **7.2. Interactive HTML**

``` python
fig.write_html("plot.html", auto_open=True)
```

------------------------------------------------------------------------

## **8. Integration with Jupyter Widgets**

``` python
import ipywidgets as widgets

def update_plot(change):
    new_data = np.sin(x + change['new'])
    fig = px.line(x=x, y=new_data, title='Interactive Sine Wave')
    fig.show()

slider = widgets.FloatSlider(value=0, min=0, max=10, step=0.1, description='Phase')
slider.observe(update_plot, names='value')
display(slider)
```

------------------------------------------------------------------------

## **9. Best Practices and Tips**

- **Use Plotly Express** for quick prototyping and rapid visualization.
- **Use Graph Objects** for advanced customizations and complex layouts.
- **Optimize Performance**:
  - Use `scattergl` for large datasets (WebGL acceleration).
  - Reduce DOM size by limiting data points or using aggregation.
- **JupyterLab Integration**:
  - Ensure JupyterLab extensions are up to date for optimal rendering.
  - Use `fig.show(renderer='notebook')` for inline rendering in some cases.

------------------------------------------------------------------------

## **10. Common Issues and Solutions**

### **10.1. Graphs Not Displaying in Jupyter Lab**

- Ensure JupyterLab extensions are installed and updated.
- Clear browser cache or try a different browser.
- Use `%matplotlib inline` to avoid conflicts with Matplotlib.

### **10.2. Exporting as Static Images Not Working**

- Install `kaleido` for image exporting:

  ``` bash
  pip install -U kaleido
  ```

### **10.3. Performance Lag with Large Datasets**

- Use `scattergl` for WebGL acceleration.
- Consider down-sampling or aggregating data.

------------------------------------------------------------------------

Back to top
