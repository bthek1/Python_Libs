# Abstract Syntax Trees (AST) in Python

The `ast` module lets you parse, inspect, and transform Python source code as a tree structure. Here’s everything you need to know.

Author

Benedict Thekkel

## What is an AST?

When Python parses source code, it converts it into a tree of nodes — each representing a syntactic construct (expressions, statements, function definitions, etc.). The `ast` module gives you access to this tree.

``` python
import ast

tree = ast.parse("x = 1 + 2")
print(ast.dump(tree, indent=2))
```

------------------------------------------------------------------------

## Core Concepts

**Node types** fall into a few categories:

- **Statements** — `Assign`, `If`, `For`, `FunctionDef`, `ClassDef`, `Return`, `Import`, …
- **Expressions** — `BinOp`, `Call`, `Name`, `Constant`, `Attribute`, `Subscript`, …
- **Operators** — `Add`, `Sub`, `Mult`, `Eq`, `Lt`, `And`, `Or`, …
- **Root** — `Module`, `Expression`, `Interactive`

Every node has positional fields (`lineno`, `col_offset`, `end_lineno`, `end_col_offset`) and typed child fields.

------------------------------------------------------------------------

### Parsing

``` python
import ast

# Parse a module (default)
tree = ast.parse("x = 1 + 2")

# Parse a single expression
tree = ast.parse("1 + 2", mode="eval")

# Parse an interactive statement
tree = ast.parse("x = 1", mode="single")
```

------------------------------------------------------------------------

### Inspecting Nodes

``` python
tree = ast.parse("x = 1 + 2")

# Pretty-print the tree
print(ast.dump(tree, indent=2))

# Walk all nodes
for node in ast.walk(tree):
    print(type(node).__name__)

# Check node type
assign = tree.body[0]
print(isinstance(assign, ast.Assign))  # True

# Access fields
print(assign.targets[0].id)   # 'x'
print(assign.value.left)      # Constant(value=1)
```

------------------------------------------------------------------------

### NodeVisitor — read-only traversal

Subclass `ast.NodeVisitor` and define `visit_<NodeType>` methods. Call `generic_visit` to recurse into children.

``` python
class FunctionCollector(ast.NodeVisitor):
    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        self.generic_visit(node)  # recurse into nested functions

tree = ast.parse(open("myfile.py").read())
collector = FunctionCollector()
collector.visit(tree)
print(collector.functions)
```

------------------------------------------------------------------------

### NodeTransformer — mutating the tree

Subclass `ast.NodeTransformer` to modify or replace nodes. Return the (modified) node, a new node, or `None` to delete it.

``` python
class PowerRewriter(ast.NodeTransformer):
    """Replace x ** 2 with x * x"""
    def visit_BinOp(self, node):
        self.generic_visit(node)
        if (
            isinstance(node.op, ast.Pow)
            and isinstance(node.right, ast.Constant)
            and node.right.value == 2
        ):
            return ast.BinOp(
                left=node.left,
                op=ast.Mult(),
                right=node.left,
            )
        return node

tree = ast.parse("y = x ** 2")
new_tree = PowerRewriter().visit(tree)
ast.fix_missing_locations(new_tree)
print(ast.unparse(new_tree))  # y = x * x
```

------------------------------------------------------------------------

### Key Utility Functions

| Function | Purpose |
|----|----|
| `ast.parse(src)` | Source string → AST |
| `ast.dump(node, indent=2)` | AST → readable string |
| `ast.unparse(node)` | AST → source string (3.9+) |
| `ast.walk(node)` | Iterator over all descendant nodes |
| `ast.fix_missing_locations(tree)` | Fill in missing line numbers after transforms |
| `ast.get_docstring(node)` | Extract docstring from func/class/module |
| `ast.literal_eval(s)` | Safely evaluate a literal expression string |
| `ast.copy_location(new, old)` | Copy line info from one node to another |

------------------------------------------------------------------------

### Compiling and executing a modified tree

``` python
tree = ast.parse("x = 1 + 2")
# ... transform ...
ast.fix_missing_locations(tree)

code = compile(tree, filename="<ast>", mode="exec")
exec(code)
```

------------------------------------------------------------------------

## Common Patterns

**Find all imports:**

``` python
class ImportFinder(ast.NodeVisitor):
    def visit_Import(self, node):
        for alias in node.names:
            print(alias.name)

    def visit_ImportFrom(self, node):
        print(f"from {node.module} import ...")
```

**Count function calls:**

``` python
calls = sum(1 for n in ast.walk(tree) if isinstance(n, ast.Call))
```

**Check for a specific variable name:**

``` python
names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
```

**Safe eval of a config dict:**

``` python
value = ast.literal_eval("{'key': [1, 2, 3]}")  # no exec, fully safe
```

------------------------------------------------------------------------

## Real-world use cases

- **Linters** (flake8, pylint) — detect style/logic issues
- **Type checkers** (mypy, pyright) — type inference and checking
- **Code formatters** (black, autopep8) — parse → normalize → unparse
- **Import sorters** (isort) — reorder import statements
- **Security scanners** (bandit) — find dangerous patterns
- **Macro/DSL systems** — rewrite syntax before execution
- **Coverage tools** — instrument code by injecting tracking calls
- **Refactoring tools** — rename symbols, extract methods

------------------------------------------------------------------------

## Gotchas

- `ast.unparse()` is only available in **Python 3.9+**; use `astor` or `astunparse` for older versions.
- After manually constructing or modifying nodes, always call `ast.fix_missing_locations(tree)` before compiling — missing `lineno`/`col_offset` will raise a `ValueError`.
- `ast.literal_eval` only handles literals (strings, numbers, tuples, lists, dicts, booleans, `None`) — it will raise `ValueError` for anything else.
- The AST structure changes between Python versions (e.g. `ast.Num`, `ast.Str` were deprecated in 3.8 in favour of `ast.Constant`).

------------------------------------------------------------------------

Back to top
