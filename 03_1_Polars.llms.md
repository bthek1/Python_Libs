# Polars

Polars

Author

Benedict Thekkel

## 🛠️ 1. Installation

``` bash
pip install polars[all] jupyterlab
```

------------------------------------------------------------------------

## 📦 2. Basic Usage in Jupyter

``` python
import polars as pl

# Read CSV
df = pl.read_csv("data.csv")

# Show head
df.head()

# Select and filter
df.select(["col1", "col2"]).filter(pl.col("col1") > 10)
```

------------------------------------------------------------------------

## ⚙️ 3. Eager vs Lazy Mode

| Mode                | Description                                 |
|---------------------|---------------------------------------------|
| **Eager** (default) | Executes immediately (like Pandas)          |
| **Lazy**            | Builds a computation graph and optimizes it |

``` python

# Lazy version
ldf = pl.read_csv("data.csv").lazy()
result = ldf.filter(pl.col("price") > 100).select(["item", "price"]).collect()
```

------------------------------------------------------------------------

## 🧠 4. Advanced Polars Features

### 📊 A. Custom Expressions

``` python
df.with_columns([
    (pl.col("price") * 0.1).alias("tax"),
    pl.col("name").str.to_uppercase()
])
```

### 📈 B. GroupBy + Aggregations

``` python
df.groupby("category").agg([
    pl.col("price").mean().alias("avg_price"),
    pl.count().alias("count")
])
```

### 🔁 C. Join Operations

``` python
df1.join(df2, on="id", how="inner")
```

| Join Type        | Description                     |
|------------------|---------------------------------|
| `inner`          | Only matching rows              |
| `left` / `outer` | Keep left/all rows              |
| `semi` / `anti`  | Exists / doesn’t exist in right |

### D. Window Functions

``` python

df.sort("timestamp").with_columns([
   pl.col("price").rolling_mean(window_size=3).over("category")
])
```

> Useful for moving averages, cumulative stats, and rankings.

### 🧪 E. Pivot and Melt

``` python

# Pivot
df.pivot(values="value", index="date", columns="category", aggregate_fn="sum")

# Melt (unpivot)
df.melt(id_vars="date", value_vars=["sales_a", "sales_b"])
```

------------------------------------------------------------------------

## 📁 5. Read/Write Support

| Format    | Method                                |
|-----------|---------------------------------------|
| CSV       | `pl.read_csv`, `df.write_csv`         |
| Parquet   | `pl.read_parquet`, `df.write_parquet` |
| JSON      | `pl.read_json`, `df.write_json`       |
| IPC/Arrow | `pl.read_ipc`, `df.write_ipc`         |

------------------------------------------------------------------------

## 🎯 6. Interoperability

### 🔁 Convert between Polars ↔︎ Pandas

``` python
import pandas as pd

df_pl = pl.DataFrame(pd_df)       # from pandas
pd_df = df_pl.to_pandas()         # to pandas
```

### 📊 Plotting

Polars doesn’t support plotting directly — convert to Pandas:

``` python

import matplotlib.pyplot as plt

df_pl.to_pandas().plot(x="date", y="sales")
plt.show()
```

------------------------------------------------------------------------

## ⚡ 7. Performance Tuning Tips

- Use lazy evaluation for large workflows
- Minimize `.collect()` calls
- Prefer `pl.struct()` for group-wise operations
- Use `categorical` or `integer` types for joins
- Combine `.filter().select().groupby()` in a lazy pipeline

------------------------------------------------------------------------

## 🔬 8. Debugging & Inspection in Jupyter

``` python
# Schema inspection
df.schema

# Data types
df.dtypes

# Lazy query plan (before execution)
ldf.describe_plan()
```

------------------------------------------------------------------------

## 📦 9. Streaming & Chunked Data (Advanced)

``` python

for chunk in pl.read_csv("big.csv", chunk_size=100_000):
    process(chunk)
```

Useful for real-time or out-of-core processing.

------------------------------------------------------------------------

## 🧩 10. Plugins & Ecosystem Integration

| Tool                 | Integration                                |
|----------------------|--------------------------------------------|
| **DuckDB**           | Direct querying via `pl.read_database()`   |
| **Arrow**            | Native backend format; fast interop        |
| **SQL (via DuckDB)** | `duckdb.query("SELECT ...").pl()`          |
| **Machine Learning** | Use `.to_pandas()` or convert to `numpy()` |

------------------------------------------------------------------------

## 📈 11. Benchmarking Example

``` python
import time
df = pl.read_csv("big.csv")

start = time.time()
df.groupby("category").agg(pl.col("price").mean())
print("Elapsed:", time.time() - start)
```

------------------------------------------------------------------------

## 📚 12. Cheat Sheet Summary

| Operation         | Code                                        |
|-------------------|---------------------------------------------|
| Filter            | `df.filter(pl.col("x") > 5)`                |
| Select            | `df.select(["a", "b"])`                     |
| GroupBy + Mean    | `df.groupby("cat").agg(pl.col("x").mean())` |
| Join              | `df1.join(df2, on="id")`                    |
| Convert to Pandas | `df.to_pandas()`                            |
| Lazy collect      | `ldf.collect()`                             |
| Sort              | `df.sort("x", descending=True)`             |
| Window fn         | `pl.col("val").cum_sum().over("group")`     |

------------------------------------------------------------------------

Back to top
