# Ruff Rule Categories — Purpose & Reason\*\*

Ruff organizes linting rules into *families* (prefix codes like `F`, `E`, `W`, `N`, `B`, etc.). Here is the full high-level list.

Author

Benedict Thekkel

## 1. **Pyflakes (`F`)**

**Purpose:** Catch syntax errors, unused variables, undefined names. **Reason:** Prevents runtime crashes and dead code.

**Examples**

- `F401` — unused import
- `F821` — undefined variable
- `F841` — assigned but unused variable

------------------------------------------------------------------------

## 2. **pycodestyle (`E`, `W`)**

**Purpose:** Enforce PEP 8 style and whitespace rules. **Reason:** Improves consistency/reliability across teams.

**Examples**

- `E501` — line too long
- `E302` — expected 2 blank lines
- `W291` — trailing whitespace

------------------------------------------------------------------------

## 3. **Pep8-naming (`N`)**

**Purpose:** Ensure correct naming conventions. **Reason:** Makes code predictable.

**Examples**

- `N802` — function name should be lowercase
- `N803` — argument name should be lowercase
- `N806` — variable in function should be lowercase

------------------------------------------------------------------------

## 4. **pyupgrade (`UP`)**

**Purpose:** Modernize code to newer Python syntax. **Reason:** Removes legacy patterns and ensures performance.

**Examples**

- rewrite `dict()` → `{}`
- rewrite `.format()` → f-string
- replace old `typing.X` with built-in types (Python 3.9+)

------------------------------------------------------------------------

## 5. **Flake8-bugbear (`B`)**

**Purpose:** Prevent common logic bugs. **Reason:** Catches subtle issues that tests often miss.

**Examples**

- `B006` — mutable default arguments
- `B007` — loop variable overwritten
- `B008` — function call in default argument

------------------------------------------------------------------------

## 6. **Flake8-comprehensions (`C4`)**

**Purpose:** Improve comprehensions. **Reason:** Cleaner, faster, more Pythonic code.

**Examples**

- `C401` — unnecessary list/dict/set comprehension
- `C402` — unnecessary dict comprehension

------------------------------------------------------------------------

## 7. **isort (`I`)**

**Purpose:** Sort imports automatically. **Reason:** Prevents merge conflicts and keeps imports consistent.

Examples:

- `I001` — imports not sorted

------------------------------------------------------------------------

## 8. **mccabe (`C90`)**

**Purpose:** Check cyclomatic complexity. **Reason:** Flags overly complex functions → refactor opportunities.

Example:

- `C901` — function too complex

------------------------------------------------------------------------

## 9. **Pylint rules (`PL`)**

**Purpose:** High-level code smell detection. **Reason:** Improves maintainability.

Examples:

- `PLR2004` — magic values
- `PLR0913` — too many arguments

------------------------------------------------------------------------

## 10. **Bandit (`S`)**

**Purpose:** Security linting. **Reason:** Prevents real-world vulnerabilities.

Examples:

- `S102` — use of `exec`
- `S307` — suspicious use of `eval`
- `S501` — insecure `requests` call without verify

------------------------------------------------------------------------

## 11. **Flake8-boolean-trap (`FBT`)**

**Purpose:** Avoid boolean default arguments. **Reason:** They hide poor API design.

Examples:

- `FBT001` — boolean default in function

------------------------------------------------------------------------

## 12. **Flake8-datetimez (`DTZ`)**

**Purpose:** Enforce timezone-aware datetimes. **Reason:** Prevents timezone bugs (critical for Django).

Examples:

- `DTZ003` — `datetime.now()` used without timezone

------------------------------------------------------------------------

## 13. **Flake8-erase (`ERA`)**

**Purpose:** Remove commented-out code blocks. **Reason:** Prevents stale code, improves readability.

Example:

- `ERA001` — commented-out code detected

------------------------------------------------------------------------

## 14. **Flake8-unused-arguments (`ARG`)**

**Purpose:** Find unused function parameters. **Reason:** Often indicates dead code or refactoring leftovers.

Example:

- `ARG001` — unused function argument

------------------------------------------------------------------------

## 15. **Flake8-print (`T20`)**

**Purpose:** Detect print statements. **Reason:** Prevents debug prints from leaking into prod.

Example:

- `T201` — `print()` found

------------------------------------------------------------------------

## 16. **Flake8-self (`SLF`)**

**Purpose:** Prevent private attribute access. **Reason:** Encourages proper encapsulation.

Example:

- `SLF001` — accessing `_private` attribute

------------------------------------------------------------------------

## 17. **Flake8-type-checking (`TC`)**

**Purpose:** Move heavy imports under `TYPE_CHECKING`. **Reason:** Faster runtime & avoids circular imports.

Example:

- `TC001` — move import into type-checking block

------------------------------------------------------------------------

## 18. **Flake8-ellipsis (`PLE`)**

**Purpose:** Validate correct use of `...`. **Reason:** Avoids odd “placeholder” errors.

Example:

- misuse of bare ellipsis

------------------------------------------------------------------------

## 19. **Tryceratops (`TRY`)**

**Purpose:** Improve error handling. **Reason:** Prevents try/except anti-patterns.

Examples:

- `TRY002` — raise without from
- `TRY003` — too broad exception clause

------------------------------------------------------------------------

## 20. **Ruff-specific rules (`RUF`)**

**Purpose:** Ruff’s own logic checks. **Reason:** Improves performance and sanity of code.

Examples:

- `RUF100` — unused `noqa` tag
- `RUF200` — ambiguous unicode character

------------------------------------------------------------------------

## 21. **Django rules (`DJ`)**

*(Only if Django plugin enabled)* **Purpose:** Enforce Django best practices. **Reason:** Prevent ORM bugs and bad patterns.

Examples:

- avoiding raw SQL
- warning about `null=True` on `CharField`

------------------------------------------------------------------------

## 22. **Django security (`DJ S`)**

**Purpose:** Catch common Django security issues. **Reason:** Prevents XSS, CSRF, password handling issues.

------------------------------------------------------------------------

## 23. **Pandas rules (PD)** *(new)*

**Purpose:** Detect inefficient Pandas operations. **Reason:** Prevent memory/time blowouts.

Examples:

- iterating rows unnecessarily
- chained indexing

------------------------------------------------------------------------

## 24. **Async rules (`ASYNC`)**

**Purpose:** Catch misuse of async/await. **Reason:** Ensures correct concurrency behavior.

Example:

- blocking calls inside async functions

------------------------------------------------------------------------

## 25. **Typing rules (`TYP`)**

**Purpose:** Improve annotations. **Reason:** Cleaner type hints → fewer mypy/pydantic errors.

Examples:

- unnecessary `Optional`
- improper `Union[...]` usage

------------------------------------------------------------------------

## 26. **Formatter rules (Ruff Formatter)**

**Purpose:** Replace Black. **Reason:** Fastest Python formatter (2–5× faster).

Examples:

- consistent string quotes
- consistent docstring formatting

------------------------------------------------------------------------

## ✔ Summary Table

| Category              | Prefix | Purpose                        |
|-----------------------|--------|--------------------------------|
| Pyflakes              | `F`    | Syntax / unused checks         |
| pycodestyle           | `E/W`  | PEP 8 rules                    |
| pep8-naming           | `N`    | Naming rules                   |
| pyupgrade             | `UP`   | Modern Python                  |
| Flake8-bugbear        | `B`    | Logic bugs                     |
| Flake8-comprehensions | `C4`   | Comprehension improvements     |
| isort                 | `I`    | Import sorting                 |
| mccabe                | `C90`  | Complexity                     |
| Pylint subset         | `PL`   | Code smells                    |
| Bandit                | `S`    | Security                       |
| Boolean trap          | `FBT`  | Boolean argument API issues    |
| Datetimez             | `DTZ`  | TZ-safe datetimes              |
| Erase                 | `ERA`  | Remove commented code          |
| Unused arguments      | `ARG`  | Unused parameters              |
| Print statements      | `T20`  | Remove debug prints            |
| Self rules            | `SLF`  | Accessing private attrs        |
| Type-checking         | `TC`   | Move imports                   |
| Tryceratops           | `TRY`  | Better try/except patterns     |
| Ruff-specific         | `RUF`  | Internal checks                |
| Django                | `DJ`   | Django practices               |
| Pandas                | `PD`   | Pandas correctness/performance |

------------------------------------------------------------------------

If you want, I can also generate:

✅ A recommended **Ruff configuration** for your Django/DRF/pytest codebase ✅ A full `ruff.toml` template ✅ A diagram showing how rule categories overlap ✅ A priority list (rules to enable first, optional ones, strict mode)

------------------------------------------------------------------------

Back to top
