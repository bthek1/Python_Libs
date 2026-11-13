# SQLAlchemy

Here’s a compact-but-complete engineer’s guide to SQLAlchemy (v2.x mindset), with code you can lift into real projects.

Author

Benedict Thekkel

## What SQLAlchemy Is (and Isn’t)

- **Two layers**

  1.  **Core**: SQL expression language + dialects + connection/transaction APIs.
  2.  **ORM**: Maps Python classes ↔︎ tables, manages identity map & unit-of-work via `Session`.

- **Batteries for SQL, not a DB**: You still pick Postgres/MySQL/SQLite/etc. SQLAlchemy gives you *portable* SQL and well-designed state management.

------------------------------------------------------------------------

## Core vs ORM (when to use which)

| Use case | Prefer |
|----|----|
| Hand-tuned SQL, ETL, admin scripts, DDL | **Core** |
| App domain models, relations, change tracking, identity map | **ORM** |
| Hybrid: complex read SQL + mapped writes | Both (Core selects, ORM for stateful writes) |

------------------------------------------------------------------------

## Quickstart – the modern (2.x) style

### 1) Define tables & models (Declarative)

``` python
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase): pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    posts: Mapped[list["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    author: Mapped[User] = relationship(back_populates="posts")
```

### 2) Engine & schema

``` python
from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg://user:pass@localhost/dbname", echo=False)

# Create tables (dev/test use; prod uses Alembic)
Base.metadata.create_all(engine)
```

### 3) Sessions & basic CRUD

``` python
from sqlalchemy.orm import Session

with Session(engine, expire_on_commit=False) as session:
    alice = User(email="alice@example.com")
    alice.posts.append(Post(title="Hello!"))
    session.add(alice)
    session.commit()

    # Query (2.x style)
    from sqlalchemy import select
    q = select(User).where(User.email == "alice@example.com")
    row = session.execute(q).scalar_one()
```

------------------------------------------------------------------------

## Querying (2.x patterns)

``` python
from sqlalchemy import select, func

# Filter + order + limit
stmt = (
    select(Post.title, func.count(Post.id).label("n"))
    .group_by(Post.title)
    .order_by(func.count(Post.id).desc())
    .limit(10)
)
rows = session.execute(stmt).all()

# Join + load related efficiently
from sqlalchemy.orm import joinedload, selectinload
stmt = select(User).options(selectinload(User.posts))  # great for 1-to-many
users = session.execute(stmt).scalars().all()
```

**Loading strategies**

- `selectinload`: many small SELECTs; excellent for 1-to-many fan-out (avoids big cartesian explosions).
- `joinedload`: single JOIN; good for 1-to-1 or small 1-to-many.
- Default lazy loading can cause **N+1**; prefer explicit `.options(...)`.

------------------------------------------------------------------------

## Transactions: do them right

``` python
with engine.begin() as conn:           # Core transaction
    conn.execute(...)

with Session(engine) as session:       # ORM unit-of-work
    with session.begin():              # commit/rollback handled
        session.add(obj)
        # multiple operations…
```

- Prefer `with session.begin()` blocks for atomic writes.
- `expire_on_commit=False` keeps objects usable after commit (common web pattern).

------------------------------------------------------------------------

## AsyncIO support

``` python
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

async_engine = create_async_engine("postgresql+asyncpg://user:pass@/dbname")
AsyncSession = async_sessionmaker(async_engine, expire_on_commit=False)

async def run():
    async with AsyncSession() as s:
        from sqlalchemy import select
        res = await s.execute(select(User).where(User.email.like("%@example.com")))
        users = res.scalars().all()

asyncio.run(run())
```

- Async is great for high-latency I/O workloads (APIs, microservices).
- ORM patterns are nearly identical, just `await` connection/session ops.

------------------------------------------------------------------------

## Migrations with Alembic (the standard)

1.  `alembic init migrations`
2.  Set `sqlalchemy.url` in `alembic.ini`.
3.  `alembic revision --autogenerate -m "add post table"`
4.  `alembic upgrade head`

**Tips**

- Keep metadata import in `env.py` pointing to your `Base.metadata`.
- Review autogen diffs (types, constraints, server defaults) before applying.
- For multi-DB setups, create envs or programmatic configs.

------------------------------------------------------------------------

## Relationships & Cascades (cheat sheet)

``` python
relationship(
    back_populates="...",
    cascade="save-update, merge, delete, delete-orphan",
    passive_deletes=True,        # pair with ON DELETE in FK for DB-side deletes
    lazy="selectin"               # sane default for 1-to-many
)
```

- **`delete-orphan`** only on the parent side of a one-to-many.
- Set **`nullable=False`** on FKs when the child must always have a parent.
- Add **`index=True`** to FKs used in joins.

------------------------------------------------------------------------

## Performance Playbook

- **Pick the right loader** (`selectinload` vs `joinedload`).
- **Batch writes** with `session.bulk_save_objects` (ORM) or **Core** `execute(many=True)`; measure correctness vs speed (bulk APIs skip some ORM events).
- **Pagination**: use keyset (a.k.a. “seek”) pagination with `WHERE (created_at, id) > (...) ORDER BY created_at, id LIMIT n` for large tables.
- **Profiling**: set `echo=True` in dev; or use `sqlalchemy.engine` logging + `EXPLAIN ANALYZE` in Postgres.
- **Avoid N+1**: always declare loader options for list views.
- **Connection pool**: tune `pool_size`, `max_overflow`, `pool_recycle` for your DB and workload.

------------------------------------------------------------------------

## Typing, Dataclasses, and Pydantic

- Use **PEP-484 typed mappings** (`Mapped[T]`, `mapped_column`) for editor help & safety.
- For API schemas, prefer **Pydantic** models at the boundary; map ORM ↔︎ DTOs explicitly (don’t bleed ORM into transport).
- With FastAPI, return Pydantic models; load ORM entities *inside* request handlers.

------------------------------------------------------------------------

## Patterns for Web Apps

### Session scoping

- **FastAPI**: provide a session per request (dependency) and close it.
- **Django** (DRF) alongside SQLAlchemy: keep SQLAlchemy session separate from Django ORM; use middleware or per-view dependency.

------------------------------------------------------------------------

### Repositories (optional)

- Wrap DB access in small “repo” classes to decouple domain from ORM. Good for large codebases/testing.

------------------------------------------------------------------------

## Testing

- Use **SQLite :memory:** for fast unit tests (be careful with PostgreSQL-specific features).
- For integration tests, spin up a **temp Postgres** (Docker) + transactional rollbacks.
- Use **`session.begin_nested()`** and savepoint rollbacks per test to avoid re-creating schema.
- Factory libraries (e.g., `factory_boy`) help generate related graphs.

------------------------------------------------------------------------

## Advanced SQL with Core (portable power)

``` python
from sqlalchemy import Table, Column, Integer, String, MetaData, select, text
meta = MetaData()
t = Table("thing", meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), index=True),
)
with engine.connect() as conn:
    conn.execute(text("SET LOCAL statement_timeout = 2000"))       # Postgres hint
    rows = conn.execute(select(t.c.id, t.c.name).where(t.c.name.ilike("%foo%"))).all()
```

- **Window functions** (`func.row_number().over(...)`), **CTEs** (`stmt.cte()`), **UNION/INTERSECT**, **array/json** types via dialects.

------------------------------------------------------------------------

## Postgres-specific goodies

``` python
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
class Event(Base):
    __tablename__ = "event"
    id: Mapped[int] = mapped_column(primary_key=True)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String))
    payload: Mapped[dict] = mapped_column(JSONB)

# Indexes / constraints
from sqlalchemy import Index, func
Index("ix_event_gin_payload", Event.payload, postgresql_using="gin")

# Upserts
from sqlalchemy.dialects.postgresql import insert
stmt = insert(User).values(email="x@x.com").on_conflict_do_nothing(index_elements=[User.email])
session.execute(stmt)
```

------------------------------------------------------------------------

## Concurrency & Locks (pragmatic notes)

- Use `SELECT ... FOR UPDATE` with ORM:

  ``` python
  from sqlalchemy import select
  u = session.execute(
      select(User).where(User.id==uid).with_for_update()
  ).scalar_one()
  ```

- Prefer **app-level idempotency** (unique keys) to avoid duplicate writes.

- Use **advisory locks** (Postgres) for coarse critical sections.

------------------------------------------------------------------------

## Common Pitfalls (and fixes)

- **N+1 queries** → always set loader options for list endpoints.
- **Stale objects after commit** → `expire_on_commit=False` (but remember to refresh when needed).
- **Implicit flush surprises** → `autoflush=True` is default; call `session.flush()` where order matters, or disable via context manager temporarily.
- **Leaking sessions** → always `with Session(...) as s:` or ensure FastAPI dependency closes sessions.
- **Over-eager cascades** → review `cascade=` rules; be explicit with deletes.

------------------------------------------------------------------------

## Alembic Gotchas

- Column type changes may need **server_default** adjustments & data migrations.
- Enum changes in Postgres require `ALTER TYPE` (write revision manually).
- Renames: use `op.alter_column(..., new_column_name=...)`, and keep ORM property name aligned.

------------------------------------------------------------------------

## Choosing the right abstraction

- **Small service, API-only, heavy I/O** → ORM + async session, or Core if you prefer SQL control.
- **Large domain model, rich relations** → ORM with explicit loader strategies and clear aggregate boundaries.
- **Analytics/ETL** → Core for READs + bulk COPY; ORM optional for simple stateful writes.

------------------------------------------------------------------------

## Mini “starter template” (sync)

    yourapp/
      db.py          # engine, SessionLocal, Base
      models.py      # declarative models
      schema.py      # Pydantic DTOs (if using FastAPI)
      repo/          # optional repositories
      services/      # business logic (or “use cases”)
      api/           # FastAPI/Django views
      migrations/    # Alembic
    tests/

**db.py**

``` python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

class Base(DeclarativeBase): pass

engine = create_engine("postgresql+psycopg://user:pass@localhost/app", future=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False)

def get_session():
    with SessionLocal() as s:
        yield s
```

------------------------------------------------------------------------

``` python
# db_async_nb.py  (just paste in a notebook cell)
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

DATABASE_URL = "postgresql+asyncpg://ben:secret@localhost:5433/mydb"

engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    connect_args={"server_settings": {"search_path": "api,public"}},
)

async def get_table_info(schema: str = "api"):
    async with engine.begin() as conn:
        result = await conn.execute(text("""
            SELECT 
                table_name,
                column_name,
                ordinal_position,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_schema = :schema
            ORDER BY table_name, ordinal_position
        """), {"schema": schema})
        return [dict(r) for r in result.mappings().all()]
```

``` python
import pandas as pd

rows = await get_table_info("api")   # <-- key change: use await, not asyncio.run
df = pd.DataFrame(rows)
df
```

|  | table_name | column_name | ordinal_position | data_type | is_nullable | column_default |
|----|----|----|----|----|----|----|
| 0 | iotawatt | timestamp | 1 | timestamp with time zone | NO | None |
| 1 | iotawatt | device | 2 | text | NO | None |
| 2 | iotawatt | sensor | 3 | text | NO | None |
| 3 | iotawatt | power | 4 | double precision | YES | None |
| 4 | iotawatt | pf | 5 | double precision | YES | None |
| 5 | iotawatt | current | 6 | double precision | YES | None |
| 6 | iotawatt | v | 7 | double precision | YES | None |

``` python
from sqlalchemy import text

async def get_constraints(schema: str = "api"):
    async with engine.begin() as conn:
        res = await conn.execute(text("""
            SELECT
              tc.table_name,
              tc.constraint_type,
              kcu.column_name,
              ccu.table_name AS foreign_table,
              ccu.column_name AS foreign_column
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
             AND tc.table_schema = kcu.table_schema
            LEFT JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
             AND ccu.table_schema = tc.table_schema
            WHERE tc.table_schema = :schema
            ORDER BY tc.table_name, tc.constraint_type
        """), {"schema": schema})
        return [dict(r) for r in res.mappings().all()]

constraints_df = pd.DataFrame(await get_constraints("api"))
constraints_df
```

|     |
|-----|

``` python
async def get_index_ddl(schema: str = "api"):
    async with engine.begin() as conn:
        res = await conn.execute(text("""
            SELECT n.nspname  AS schema,
                   c.relname  AS table,
                   i.relname  AS index,
                   pg_get_indexdef(ix.indexrelid) AS definition,
                   ix.indisunique AS is_unique
            FROM pg_index ix
            JOIN pg_class i  ON i.oid = ix.indexrelid
            JOIN pg_class c  ON c.oid = ix.indrelid
            JOIN pg_namespace n ON n.oid = c.relnamespace
            WHERE n.nspname = :schema
            ORDER BY c.relname, i.relname
        """), {"schema": schema})
        return [dict(r) for r in res.mappings().all()]

indexes_df = pd.DataFrame(await get_index_ddl("api"))
indexes_df
```

|  | schema | table | index | definition | is_unique |
|----|----|----|----|----|----|
| 0 | api | iotawatt | iotawatt_timestamp_idx | CREATE INDEX iotawatt_timestamp_idx ON api.iot... | False |

Back to top
