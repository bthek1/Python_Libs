# Latexify examples

This notebook provides several examples to use `latexify`.

Author

Benedict Thekkel

See also the [official documentation](https://github.com/google/latexify_py/blob/documentation/docs/index.md) for more details.

If you have any questions, please ask it in the [issue tracker](https://github.com/google/latexify_py/issues).

## Install `latexify`

## Import `latexify` into your code

``` python
import math  # Optional
import numpy as np  # Optional
import latexify

latexify.__version__
```

    '0.4.2'

## Examples

``` python
@latexify.function
def solve(a, b, c):
  return (-b + math.sqrt(b**2 - 4*a*c)) / (2*a)

print(solve(1, 4, 3))  # Invoking the function works as expected.
print(solve)  # Printing the function shows the underlying LaTeX source.
solve  # Displays the expression.

# Writes the underlying LaTeX source into a file.
with open("compiled.tex", "w") as fp:
  print(solve, file=fp)
```

    -1.0
    \mathrm{solve}(a, b, c) = \frac{-b + \sqrt{ b^{2} - 4 a c }}{2 a}

``` python
# latexify.expression works similarly, but does not output the signature.
@latexify.expression
def solve(a, b, c):
  return (-b + math.sqrt(b**2 - 4*a*c)) / (2*a)

solve
```

$$\displaystyle \frac{-b + \sqrt{ b^{2} - 4 a c }}{2 a}$$

``` python
# latexify.get_latex obtains the underlying LaTeX expression directly.
def solve(a, b, c):
  return (-b + math.sqrt(b**2 - 4*a*c)) / (2*a)

latexify.get_latex(solve)
```

    '\\mathrm{solve}(a, b, c) = \\frac{-b + \\sqrt{ b^{2} - 4 a c }}{2 a}'

``` python
@latexify.function
def sinc(x):
  if x == 0:
    return 1
  else:
    return math.sin(x) / x

sinc
```

$$\displaystyle \mathrm{sinc}(x) = \left\{ \begin{array}{ll} 1, & \mathrm{if} \ x = 0 \\ \frac{\sin x}{x}, & \mathrm{otherwise} \end{array} \right.$$

``` python
# Elif or nested else-if are unrolled.
@latexify.function
def fib(x):
  if x == 0:
    return 0
  elif x == 1:
    return 1
  else:
    return fib(x-1) + fib(x-2)

fib
```

$$\displaystyle \mathrm{fib}(x) = \left\{ \begin{array}{ll} 0, & \mathrm{if} \ x = 0 \\ 1, & \mathrm{if} \ x = 1 \\ \mathrm{fib} \mathopen{}\left( x - 1 \mathclose{}\right) + \mathrm{fib} \mathopen{}\left( x - 2 \mathclose{}\right), & \mathrm{otherwise} \end{array} \right.$$

``` python
# Some math symbols are converted automatically.
@latexify.function(use_math_symbols=True)
def greek(alpha, beta, gamma, Omega):
  return alpha * beta + math.gamma(gamma) + Omega

greek
```

$$\displaystyle \mathrm{greek}(\alpha, \beta, \gamma, \Omega) = \alpha \beta + \Gamma \mathopen{}\left( \gamma \mathclose{}\right) + \Omega$$

``` python
# Function names, arguments, variables can be replaced.
identifiers = {
    "my_function": "f",
    "my_inner_function": "g",
    "my_argument": "x",
}

@latexify.function(identifiers=identifiers)
def my_function(my_argument):
    return my_inner_function(my_argument)

my_function
```

$$\displaystyle f(x) = g \mathopen{}\left( x \mathclose{}\right)$$

``` python
# Assignments can be reduced into one expression.
@latexify.function(reduce_assignments=True)
def f(a, b, c):
    discriminant = b**2 - 4 * a * c
    numerator = -b + math.sqrt(discriminant)
    denominator = 2 * a
    return numerator / denominator

f
```

$$\displaystyle f(a, b, c) = \frac{-b + \sqrt{ b^{2} - 4 a c }}{2 a}$$

``` python
# Matrix support.
@latexify.function(reduce_assignments=True, use_math_symbols=True)
def transform(x, y, a, b, theta, s, t):
  cos_t = math.cos(theta)
  sin_t = math.sin(theta)
  scale = np.array([[a, 0, 0], [0, b, 0], [0, 0, 1]])
  rotate = np.array([[cos_t, -sin_t, 0], [sin_t, cos_t, 0], [0, 0, 1]])
  move = np.array([[1, 0, s], [0, 1, t], [0, 0, 1]])
  return move @ rotate @ scale @ np.array([[x], [y], [1]])

transform
```

$$\displaystyle \mathrm{transform}(x, y, a, b, \theta, s, t) = \begin{bmatrix} 1 & 0 & s \\ 0 & 1 & t \\ 0 & 0 & 1 \end{bmatrix} \cdot \begin{bmatrix} \cos \theta & -\sin \theta & 0 \\ \sin \theta & \cos \theta & 0 \\ 0 & 0 & 1 \end{bmatrix} \cdot \begin{bmatrix} a & 0 & 0 \\ 0 & b & 0 \\ 0 & 0 & 1 \end{bmatrix} \cdot \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$

``` python
# latexify.algorithmic generates an algorithmic environment instead of an equation.
@latexify.algorithmic
def fib(x):
  if x == 0:
    return 0
  elif x == 1:
    return 1
  else:
    return fib(x-1) + fib(x-2)

fib
```

\$ $$\begin{array}{l} \mathbf{function} \ \mathrm{fib}(x) \\ \hspace{1em} \mathbf{if} \ x = 0 \\ \hspace{2em} \mathbf{return} \ 0 \\ \hspace{1em} \mathbf{else} \\ \hspace{2em} \mathbf{if} \ x = 1 \\ \hspace{3em} \mathbf{return} \ 1 \\ \hspace{2em} \mathbf{else} \\ \hspace{3em} \mathbf{return} \ \mathrm{fib} \mathopen{}\left( x - 1 \mathclose{}\right) + \mathrm{fib} \mathopen{}\left( x - 2 \mathclose{}\right) \\ \hspace{2em} \mathbf{end \ if} \\ \hspace{1em} \mathbf{end \ if} \\ \mathbf{end \ function} \end{array}$$

\$

``` python
# Another example: latexify.algorithmic supports usual control flows.
@latexify.algorithmic
def collatz(x):
  n = 0
  while x > 1:
    n = n + 1
    if x % 2 == 0:
      x = x // 2
    else:
      x = 3 * x + 1
  return n

collatz
```

\$ $$\begin{array}{l} \mathbf{function} \ \mathrm{collatz}(x) \\ \hspace{1em} n \gets 0 \\ \hspace{1em} \mathbf{while} \ x > 1 \\ \hspace{2em} n \gets n + 1 \\ \hspace{2em} \mathbf{if} \ x \mathbin{\%} 2 = 0 \\ \hspace{3em} x \gets \left\lfloor\frac{x}{2}\right\rfloor \\ \hspace{2em} \mathbf{else} \\ \hspace{3em} x \gets 3 x + 1 \\ \hspace{2em} \mathbf{end \ if} \\ \hspace{1em} \mathbf{end \ while} \\ \hspace{1em} \mathbf{return} \ n \\ \mathbf{end \ function} \end{array}$$

\$

Back to top
