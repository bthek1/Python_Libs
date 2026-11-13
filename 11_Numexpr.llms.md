# Numexpr

**NumExpr** is a fast numerical expression evaluator for NumPy. It speeds up mathematical computations by using multithreading and efficient evaluation techniques, making it ideal for large datasets or complex numerical expressions.

Author

Benedict Thekkel

## **1. What is NumExpr?**

- **NumExpr** is a Python library for evaluating numerical expressions faster than pure Python or NumPy.
- It compiles expressions into bytecode and evaluates them efficiently using vectorized operations and multi-threading.

------------------------------------------------------------------------

## **2. Key Features**

1.  **Fast Execution**:
    - Evaluates expressions more quickly than NumPy for large arrays by avoiding intermediate arrays.
2.  **Multithreading**:
    - Uses multiple CPU cores for faster computations.
3.  **Memory Efficient**:
    - Minimizes memory usage by not creating temporary arrays for intermediate results.
4.  **NumPy Integration**:
    - Works seamlessly with NumPy arrays.

------------------------------------------------------------------------

## **3. Installation**

To install NumExpr, use pip:

``` bash
pip install numexpr
```

------------------------------------------------------------------------

## **4. Basic Usage**

To evaluate a mathematical expression:

``` python
import numexpr as ne

# Define a NumPy array
import numpy as np
a = np.arange(1e6)

# Evaluate an expression
result = ne.evaluate("a ** 2 + 3 * a - 5")
```

- **`ne.evaluate()`** takes a string expression and evaluates it.
- It supports standard mathematical operations (`+`, `-`, `*`, `/`, `**`) and functions (e.g., `sin`, `cos`, `log`).

------------------------------------------------------------------------

``` python
import numexpr as ne

# Define a NumPy array
import numpy as np
a = np.arange(1e6)

# Evaluate an expression
result = ne.evaluate("a ** 2 + 3 * a - 5")
a, result
```

    (array([0.00000e+00, 1.00000e+00, 2.00000e+00, ..., 9.99997e+05,
            9.99998e+05, 9.99999e+05], shape=(1000000,)),
     array([-5.000000e+00, -1.000000e+00,  5.000000e+00, ...,  9.999970e+11,
             9.999990e+11,  1.000001e+12], shape=(1000000,)))

## **5. Supported Operations**

### A) **Arithmetic Operators**

| Operator | Description    |
|----------|----------------|
| `+`      | Addition       |
| `-`      | Subtraction    |
| `*`      | Multiplication |
| `/`      | Division       |
| `**`     | Power          |
| `%`      | Modulus        |

Example:

``` python
ne.evaluate("2 * a + 3")
```

### B) **Relational and Logical Operators**

| Operator | Description           |
|----------|-----------------------|
| `<`      | Less than             |
| `>`      | Greater than          |
| `<=`     | Less than or equal    |
| `>=`     | Greater than or equal |
| `==`     | Equal                 |
| `!=`     | Not equal             |
| `&`      | Logical AND           |
| `|`      | Logical OR            |

Example:

``` python
ne.evaluate("(a > 0.5) & (a < 0.8)")
```

### C) **Mathematical Functions**

| Function                     | Description                         |
|------------------------------|-------------------------------------|
| `sin`, `cos`, `tan`          | Trigonometric functions             |
| `arcsin`, `arccos`, `arctan` | Inverse trigonometric functions     |
| `log`, `log10`, `exp`        | Logarithm and exponential functions |
| `sqrt`                       | Square root                         |
| `abs`                        | Absolute value                      |
| `where`                      | Conditional function                |

Example:

``` python
ne.evaluate("sqrt(a) + log(a)")
```

------------------------------------------------------------------------

## **6. Multithreading**

NumExpr automatically uses multiple threads for parallel computation.

### Adjusting the Number of Threads

You can control the number of threads:

``` python
import numexpr as ne

# Set the number of threads
ne.set_num_threads(4)

# Get the current thread count
print(ne.nthreads)
```

------------------------------------------------------------------------

## **7. Benefits Over NumPy**

| Feature                 | NumPy                | NumExpr                  |
|-------------------------|----------------------|--------------------------|
| **Intermediate Arrays** | Created              | Avoided                  |
| **Performance**         | Single-threaded      | Multithreaded            |
| **Memory Usage**        | Higher (temp arrays) | Lower (in-place)         |
| **Syntax**              | Standard Python      | String-based expressions |

------------------------------------------------------------------------

## **8. Error Handling**

If there’s an issue with your expression, NumExpr will raise an error. Always validate your inputs to ensure compatibility.

Example:

``` python
try:
    result = ne.evaluate("a ** 2 + invalid_function(a)")
except Exception as e:
    print(f"Error: {e}")
```

------------------------------------------------------------------------

## **9. When to Use NumExpr?**

1.  **Large Datasets**: Works best when processing large arrays.
2.  **Complex Expressions**: Reduces the overhead of creating temporary arrays.
3.  **Performance-Critical Applications**: Offers significant speed-ups over NumPy for heavy computations.

------------------------------------------------------------------------

## **10. Benchmarks**

### Comparing NumPy and NumExpr:

``` python
import numpy as np
import numexpr as ne
import time

a = np.random.rand(1_000_000)

# Using NumPy
start = time.time()
result_numpy = a**2 + 3*a - 5
end = time.time()
print("NumPy Time:", end - start)

# Using NumExpr
start = time.time()
result_numexpr = ne.evaluate("a**2 + 3*a - 5")
end = time.time()
print("NumExpr Time:", end - start)
```

Output (example):

    NumPy Time: 0.015
    NumExpr Time: 0.008

------------------------------------------------------------------------

## **11. Limitations**

1.  **String-based Syntax**:
    - Expressions must be written as strings, which may feel less natural than Python’s native syntax.
2.  **Unsupported Functions**:
    - Only supports a subset of NumPy functions.
    - Custom Python functions cannot be used directly in expressions.
3.  **Not for Small Arrays**:
    - Overhead may negate performance benefits for small datasets.
4.  **No GPU Support**:
    - NumExpr is CPU-bound and does not leverage GPUs.

------------------------------------------------------------------------

## **12. Advanced Usage**

### A) Conditional Expressions

Use `where` to perform conditional operations:

``` python
ne.evaluate("where(a > 0.5, a, 0)")
```

### B) Broadcasting

NumExpr supports broadcasting, similar to NumPy:

``` python
b = np.arange(1, 1e6 + 1)
ne.evaluate("a + b")
```

### C) Chained Operations

You can chain multiple operations in a single expression:

``` python
ne.evaluate("(a ** 2 + b) / (a + 1)")
```

------------------------------------------------------------------------

## **13. Common Use Cases**

1.  **Financial Calculations**:
    - Fast evaluation of complex mathematical models.
2.  **Data Science and Machine Learning**:
    - Preprocessing and transforming large datasets.
3.  **Simulations**:
    - Efficiently evaluating mathematical models for physical systems.
4.  **Scientific Computing**:
    - Speeding up computationally intensive numerical workflows.

------------------------------------------------------------------------

## **14. Alternatives to NumExpr**

1.  **Numba**: Just-In-Time (JIT) compilation for Python, offering similar speed-ups.
2.  **CuPy**: GPU-based acceleration for NumPy-like operations.
3.  **SciPy**: Offers advanced numerical computing but lacks NumExpr’s speed for expressions.

------------------------------------------------------------------------

Back to top
