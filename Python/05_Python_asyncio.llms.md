# asyncio — Complete Reference

Targets Python 3.11+, with version markers where it matters. 3.11 is the meaningful floor: `TaskGroup`, `asyncio.timeout()`, and `task.uncancel()` all landed there and they change how you write correct code.

Author

Benedict Thekkel

## 1. The mental model

**Single thread, cooperative multitasking.** One OS thread runs an event loop that owns a queue of ready callbacks. Coroutines run until they hit an `await` that actually suspends, at which point they hand control back to the loop, which picks the next ready thing.

Three consequences that explain almost every asyncio bug:

1.  **`await` is the only preemption point.** Between two awaits your code is atomic. Nothing else in the loop runs. This is a genuine design tool — you often don’t need a lock, because there’s no interleaving unless you await inside the critical section.
2.  **Blocking blocks everything.** A `time.sleep(1)` or a CPU-bound loop freezes every task, every timer, every socket read in the process. There is no preemptive scheduler to rescue you.
3.  **Concurrency ≠ parallelism.** asyncio gives you thousands of concurrent IO operations on one core. It gives you zero CPU parallelism. If your bottleneck is CPU, asyncio is the wrong tool.

The right question when reaching for asyncio: *am I waiting on things, or computing things?* Waiting → asyncio. Computing → processes.

------------------------------------------------------------------------

## 2. Coroutines, tasks, futures

``` python
async def fetch(url): ...

coro = fetch(url)        # NOT running. Just an object.
result = await coro      # runs it inline — sequential, no concurrency
task = asyncio.create_task(coro)   # schedules it on the loop — concurrent
```

The distinction people get wrong: **`await` does not create concurrency.** `await a(); await b()` is strictly sequential. Concurrency requires scheduling both first.

| Type | What it is |
|----|----|
| Coroutine | The object returned by calling an `async def`. Inert until awaited or wrapped. |
| Task | A coroutine scheduled on the loop. Subclass of Future. Has a name, can be cancelled, tracks state. |
| Future | A low-level “result eventually” placeholder. You rarely create these; libraries do. |

### The fire-and-forget footgun

The event loop holds only **weak** references to tasks. A task with no strong reference elsewhere can be garbage collected mid-execution, and it just… stops. Silently.

``` python
# BROKEN — may vanish
asyncio.create_task(background_work())

# Correct
_background = set()

def spawn(coro):
    t = asyncio.create_task(coro)
    _background.add(t)
    t.add_done_callback(_background.discard)
    return t
```

Better still: use a `TaskGroup` and don’t fire-and-forget at all.

### Eager tasks (3.12+)

``` python
loop.set_task_factory(asyncio.eager_task_factory)
```

Runs the coroutine synchronously until its first real suspension instead of deferring to the next loop iteration. Meaningful win when many tasks complete without ever suspending (cache hits). Changes timing semantics subtly, so don’t enable it under a codebase that assumes deferred start.

------------------------------------------------------------------------

## 3. Running the loop

``` python
asyncio.run(main())                    # creates loop, runs, cancels stragglers, closes
asyncio.run(main(), debug=True)
```

`asyncio.Runner` (3.11+) when you need several `run` calls sharing one loop:

``` python
with asyncio.Runner() as runner:
    runner.run(setup())
    runner.run(main())
```

**Don’t use `asyncio.get_event_loop()`.** As of 3.14 it raises `RuntimeError` when there’s no current loop rather than silently creating one, and the whole event-loop-policy system is deprecated for removal in 3.16. Inside a coroutine use `asyncio.get_running_loop()`.

For uvloop or another implementation, pass a factory rather than installing a policy:

``` python
asyncio.run(main(), loop_factory=uvloop.new_event_loop)
```

> **In a notebook none of the above applies** — there is already a loop running. See §4.

------------------------------------------------------------------------

## 4. Running in Jupyter / IPython

Jupyter (IPython 7.0+, ipykernel 6+) executes every cell inside an already-running asyncio event loop. That single fact explains all the differences. The loop is a plain `_UnixSelectorEventLoop` — not tornado, not anything exotic — and it **persists across cells** for the life of the kernel.

Everything below was run in a real kernel; the outputs are actual.

### Top-level `await` just works

``` python
import asyncio, time

async def fetch(n):
    await asyncio.sleep(0.1)
    return n * 2

result = await fetch(21)
print("top-level await ->", result)
```

    top-level await -> 42

No `async def main()` wrapper, no `asyncio.run()`. `await` at cell top level is legal in IPython even though it isn’t in a plain script.

### `asyncio.run()` fails — this is the error everyone hits

``` python
try:
    asyncio.run(fetch(1))
except RuntimeError as e:
    print("RuntimeError:", e)
```

    RuntimeError: asyncio.run() cannot be called from a running event loop
    RuntimeWarning: coroutine 'fetch' was never awaited

Note you get *two* complaints: the nesting refusal, and a never-awaited warning for the coroutine you constructed and dropped. `loop.run_until_complete()` fails the same way.

**Translation table for adapting any script example in this doc:**

| Script | Notebook cell |
|----|----|
| `asyncio.run(main())` | `await main()` |
| `asyncio.run(main(), debug=True)` | `asyncio.get_running_loop().set_debug(True)` then `await main()` |
| `loop = asyncio.new_event_loop()` | `loop = asyncio.get_running_loop()` |
| `asyncio.get_event_loop()` | `asyncio.get_running_loop()` |

### Structured concurrency works unchanged

``` python
t0 = time.perf_counter()
async with asyncio.TaskGroup() as tg:
    a = tg.create_task(fetch(1))
    b = tg.create_task(fetch(2))
print(a.result(), b.result(), f"{time.perf_counter()-t0:.2f}s")
```

    2 4 0.10s

0.10s for two 0.1s tasks — genuinely concurrent. `async with`, `async for`, and `asyncio.timeout()` are all valid at cell top level:

``` python
async def slow():
    await asyncio.sleep(0.2)
    return "ok"

try:
    async with asyncio.timeout(0.05):
        await slow()
except TimeoutError:
    print("asyncio.timeout works in a cell")
```

    asyncio.timeout works in a cell

### Background tasks survive between cells

The genuinely useful notebook-specific behaviour — the loop outlives the cell, so a spawned task keeps running while you type the next one.

``` python
# --- cell 1 ---
_bg = set()

async def ticker():
    while True:
        await asyncio.sleep(0.5)

def spawn(coro, name=None):
    t = asyncio.create_task(coro, name=name)
    _bg.add(t)                       # the weak-ref footgun from §2 applies here too
    t.add_done_callback(_bg.discard)
    return t

tick = spawn(ticker(), name="ticker")
print("spawned:", tick.get_name(), "done?", tick.done())
```

    spawned: ticker done? False

``` python
# --- cell 2, run later ---
await asyncio.sleep(1.2)
print("still alive across cells?", not tick.done())
```

    still alive across cells? True

``` python
# --- cell 3 ---
tick.cancel()
try:
    await tick
except asyncio.CancelledError:
    print("cancelled cleanly")
print([t.get_name() for t in asyncio.all_tasks()])
```

    cancelled cleanly
    ['Task-29', 'Task-30', 'Task-28']

Note that last line: **`all_tasks()` includes the kernel’s own machinery**, not just yours. Those three unnamed tasks are ipykernel’s. Name your tasks or you can’t tell them apart.

### Background exceptions are silently swallowed

The most dangerous notebook-specific behaviour:

``` python
# --- cell 1 ---
async def boom():
    await asyncio.sleep(0.1)
    raise ValueError("this failed in the background")

t = asyncio.create_task(boom())
print("spawned, cell finished")
```

    spawned, cell finished

``` python
# --- cell 2 ---
await asyncio.sleep(0.3)
print("task state:", t.done(), t.exception())
```

    task state: True this failed in the background

The `ValueError` never appeared in any cell output. It sat in the task until explicitly retrieved. In a script you’d at least get a “Task exception was never retrieved” message on the console; in a notebook it goes to the kernel log, which you’re probably not watching. **Always check `task.exception()`, or wrap background work in a try/except that prints.**

### Timers and debug mode

``` python
loop = asyncio.get_running_loop()
print("loop:", type(loop).__name__, "monotonic now:", round(loop.time(), 2))

fired = []
h = loop.call_later(0.25, lambda: fired.append("settled"))
await asyncio.sleep(0.1)
h.cancel()                                    # reset the settle timer
h = loop.call_later(0.25, lambda: fired.append("settled"))
await asyncio.sleep(0.4)
print("fired:", fired)
```

    loop: _UnixSelectorEventLoop monotonic now: 45.07
    fired: ['settled']

Fires exactly once — the cancel-and-restart debounce pattern from §13 behaves identically in a notebook.

Debug mode has to be set on the existing loop rather than passed to `run`:

``` python
loop.set_debug(True)
loop.slow_callback_duration = 0.05
```

Caveat: slow-callback warnings go to the **kernel log**, not cell output. Run `jupyter lab` in a terminal you can see, or you’ll never notice them.

### `asyncio.run()` in a thread — the escape hatch

When a library insists on owning the loop (`PipelineRunner.run()`, anything doing signal handling), give it its own loop in its own thread:

``` python
import threading

def in_thread():
    asyncio.run(main())

threading.Thread(target=in_thread, daemon=True).start()
```

Verified working. The cost is that you now have two loops and objects can’t cross between them — asyncio primitives are not thread-safe, so communicate via `loop.call_soon_threadsafe` or `asyncio.run_coroutine_threadsafe` (§11).

### Do not use `nest_asyncio`

The classic advice was `nest_asyncio.apply()` to allow nested loops. It’s now a trap: the package is archived and unmaintained, it doesn’t accept the `loop_factory` parameter added in 3.12, and it’s broken outright on 3.14 (`asyncio.current_task()` among others), where it degrades into silent HTTP connection-pool failures rather than clean errors. `nest-asyncio2` is a maintained fork if you’re pinned to a library that requires it, but the correct fix is calling the async API with `await`.

### Other notes

- `%autoawait` is the IPython magic controlling this; it’s on by default for asyncio. `%autoawait trio` switches backends.
- A blocking call in a cell freezes the kernel — including your background tasks and the interrupt handler. Same rule as §10, worse consequences.
- Restarting the kernel is the only reliable way to clear orphaned tasks; half-cancelled state accumulates.
- VS Code and Colab notebooks behave identically. They’re all ipykernel.

------------------------------------------------------------------------

## 5. Structured concurrency

### TaskGroup (3.11+) — the default choice

``` python
async with asyncio.TaskGroup() as tg:
    t1 = tg.create_task(fetch(a))
    t2 = tg.create_task(fetch(b))
# both guaranteed complete here
print(t1.result(), t2.result())
```

Semantics: if any child raises, remaining children are **cancelled**, the block waits for them to finish unwinding, then raises an `ExceptionGroup`. If the body raises, same thing. Nothing escapes the block still running.

Handle with `except*`:

``` python
try:
    async with asyncio.TaskGroup() as tg:
        ...
except* ValueError as eg:
    for exc in eg.exceptions: ...
except* ConnectionError as eg:
    ...
```

### gather — legacy, with a sharp edge

``` python
results = await asyncio.gather(a(), b(), c())
results = await asyncio.gather(*coros, return_exceptions=True)  # exceptions as values
```

**The edge:** with `return_exceptions=False`, the first exception propagates to the awaiter immediately, but **the other tasks are not cancelled**. They keep running, orphaned, and if they later raise you get “Task exception was never retrieved” warnings from a task nobody owns. This is the single biggest reason to prefer `TaskGroup`.

(If `gather` *itself* is cancelled, it does cancel its children. It’s only the exception path that leaks.)

Use `gather` when you genuinely want “run all, collect all outcomes” with `return_exceptions=True`. Otherwise use `TaskGroup`.

### wait — when you need partial results

``` python
done, pending = await asyncio.wait(
    tasks, return_when=asyncio.FIRST_COMPLETED, timeout=5
)
for t in pending:
    t.cancel()
```

Takes **Tasks, not coroutines** (passing coroutines was removed in 3.11+). Never cancels anything for you — cleaning up `pending` is your job.

### as_completed — results in finishing order

``` python
for coro in asyncio.as_completed(tasks):
    result = await coro
```

------------------------------------------------------------------------

## 6. Cancellation

The subject worth understanding deeply, because it’s where most real-world async bugs live.

### Mechanics

`task.cancel()` **requests** cancellation. It schedules a `CancelledError` to be thrown into the coroutine at its next suspension point. It does not stop anything immediately, and a task doing CPU work with no awaits cannot be cancelled at all.

``` python
task.cancel()
try:
    await task
except asyncio.CancelledError:
    pass
```

Cancellation isn’t complete until you await the task. `cancel()` returning doesn’t mean it’s done.

### CancelledError is a BaseException

Since 3.8. This is deliberate and load-bearing:

``` python
try:
    await something()
except Exception:      # does NOT catch CancelledError — correct
    log.exception("failed")
```

If you catch it explicitly, **you must re-raise it** unless you’re deliberately absorbing the cancellation:

``` python
try:
    await work()
except asyncio.CancelledError:
    await cleanup()
    raise            # ← non-negotiable
```

Swallowing it makes the task un-cancellable, breaks `TaskGroup` and `timeout()` nesting, and produces hangs on shutdown that are miserable to debug.

### Cleanup during cancellation

`finally` runs, but awaiting inside it is dangerous — the task is already being cancelled, so a second cancellation can interrupt your cleanup:

``` python
try:
    await work()
finally:
    await asyncio.shield(close_connection())   # survives the cancellation
```

Keep cleanup short and non-blocking where you can.

### shield

``` python
result = await asyncio.shield(critical_write())
```

Protects the *inner* operation. If the outer scope is cancelled, `shield` raises `CancelledError` to the caller but the inner coroutine **keeps running to completion** — orphaned unless you kept a reference. Common misunderstanding: shield does not make the caller wait.

### uncancel (3.11+)

`task.uncancel()` and `task.cancelling()` exist so nested cancellation scopes can tell “I was cancelled by my own timeout” from “someone upstream cancelled me.” `TaskGroup` and `asyncio.timeout()` use them internally. You mostly won’t call them directly, but knowing why they exist explains why nested timeouts work correctly in 3.11+ and were broken before.

------------------------------------------------------------------------

## 7. Timeouts

``` python
async with asyncio.timeout(5):          # 3.11+, preferred
    await work()

async with asyncio.timeout_at(loop.time() + 5):
    await work()
```

Raises `TimeoutError` (builtin; `asyncio.TimeoutError` is an alias since 3.11). The context manager form composes and nests correctly, and can be rescheduled mid-flight via the returned handle.

``` python
async with asyncio.timeout(5) as cm:
    await first_part()
    cm.reschedule(loop.time() + 10)
    await second_part()
```

The older `asyncio.wait_for(coro, timeout)` still works and is fine for a single call.

------------------------------------------------------------------------

## 8. Synchronization primitives

`Lock`, `Event`, `Condition`, `Semaphore`, `BoundedSemaphore`, `Barrier` (3.11+). All asyncio-specific — **not thread-safe**, don’t share them with threads.

``` python
sem = asyncio.Semaphore(10)          # cap concurrency

async def fetch_one(url):
    async with sem:
        return await client.get(url)
```

None of them take a timeout argument. Compose with `asyncio.timeout()`:

``` python
async with asyncio.timeout(1):
    async with lock:
        ...
```

**You need a lock less often than you think** — see the atomicity-between-awaits point in §1. You need one only when a critical section contains an `await`.

------------------------------------------------------------------------

## 9. Queues

`Queue`, `LifoQueue`, `PriorityQueue`. The standard producer/consumer plumbing, and the natural way to build backpressure.

``` python
q = asyncio.Queue(maxsize=100)     # maxsize is your backpressure

async def producer():
    await q.put(item)              # blocks when full ← this is the point

async def consumer():
    while True:
        item = await q.get()
        try:
            await handle(item)
        finally:
            q.task_done()

await q.join()                     # wait until all items processed
```

An unbounded queue is a memory leak waiting for a slow consumer. Set `maxsize`.

`Queue.shutdown()` + `QueueShutDown` (3.13+) gives clean consumer termination without sentinel values.

------------------------------------------------------------------------

## 10. Never block the loop

``` python
# Blocking IO → thread
result = await asyncio.to_thread(requests.get, url)          # 3.9+

# CPU-bound → process
loop = asyncio.get_running_loop()
with ProcessPoolExecutor() as pool:
    result = await loop.run_in_executor(pool, heavy_compute, data)
```

`asyncio.to_thread` uses the default thread pool and propagates contextvars. For CPU work it’s useless — the GIL means threads don’t help — so use processes.

**Detecting it:** debug mode logs any callback taking longer than `loop.slow_callback_duration` (default 0.1s).

``` python
asyncio.run(main(), debug=True)
# or PYTHONASYNCIODEBUG=1
```

Turn this on in development. It finds accidental blocking that you will otherwise ship.

The usual offenders: `time.sleep`, `requests`, `psycopg2`, `boto3`, PIL/OpenCV, `json.loads` on very large payloads, model inference, regex catastrophic backtracking.

------------------------------------------------------------------------

## 11. Bridging sync and async

| Direction | Tool |
|----|----|
| async → sync function | `await asyncio.to_thread(fn, *args)` |
| other thread → loop (callback) | `loop.call_soon_threadsafe(fn, *args)` |
| other thread → loop (coroutine) | `asyncio.run_coroutine_threadsafe(coro, loop)` → `concurrent.futures.Future` |
| sync → async (Django world) | `asgiref.sync.async_to_sync(coro_fn)(...)` |
| async → sync (Django world) | `asgiref.sync.sync_to_async(fn)(...)` |

`call_soon_threadsafe` is the *only* loop method safe to call from another thread. Calling anything else cross-thread is a race, even when it appears to work.

------------------------------------------------------------------------

## 12. Async iteration, context managers, generators

``` python
class Stream:
    def __aiter__(self): return self
    async def __anext__(self):
        chunk = await self.read()
        if not chunk: raise StopAsyncIteration
        return chunk

async for chunk in Stream(): ...
```

``` python
from contextlib import asynccontextmanager

@asynccontextmanager
async def connection():
    conn = await connect()
    try:
        yield conn
    finally:
        await conn.close()
```

**Async generator finalization is a real hazard.** If you break out of an `async for` early, the generator’s `finally` may not run until GC. Use `aclosing`:

``` python
from contextlib import aclosing

async with aclosing(agen()) as it:
    async for x in it:
        if done: break          # finally now runs deterministically
```

`asyncio.run()` calls `loop.shutdown_asyncgens()` for you; hand-rolled loops must do it themselves.

------------------------------------------------------------------------

## 13. Timers and time

``` python
loop = asyncio.get_running_loop()
handle = loop.call_later(0.25, callback)     # returns TimerHandle
handle.cancel()

loop.call_at(loop.time() + 0.25, callback)
loop.call_soon(callback)
```

**`loop.time()` is monotonic**, not wall-clock. It is unaffected by NTP steps and clock changes, which is exactly what you want for timers, and it means you must never compare it against `time.time()`.

Two ways to build a settle/debounce timer, and the choice matters:

``` python
# A: callback-based — no task, cancel is synchronous and immediate
self._timer = loop.call_later(0.25, self._on_settle)
# to reset:
self._timer.cancel()
self._timer = loop.call_later(0.25, self._on_settle)

# B: task-based — can await, cancel is cooperative
async def _settle():
    await asyncio.sleep(0.25)
    await self._on_settle()          # can await; A cannot

self._task and self._task.cancel()
self._task = asyncio.create_task(_settle())
```

Use A when the action is synchronous and you want cancellation to be instantaneous and race-free. Use B when the settle action needs to await. B’s cancellation is *requested*, not immediate — if `_on_settle` already started, cancelling won’t unwind it until its next await point, which is a real race in turn-taking code.

`asyncio.sleep(0)` yields to the loop without delay. Useful for letting queued work drain, and in tests for forcing a scheduling point.

------------------------------------------------------------------------

## 14. Networking and subprocesses

High-level streams:

``` python
reader, writer = await asyncio.open_connection(host, port)
writer.write(data)
await writer.drain()               # respects backpressure — don't skip this
data = await reader.readline()
writer.close()
await writer.wait_closed()

server = await asyncio.start_server(handle_client, host, port)
async with server:
    await server.serve_forever()
```

Subprocesses:

``` python
proc = await asyncio.create_subprocess_exec(
    "ffmpeg", "-i", "in.wav", "out.mp3",
    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
)
stdout, stderr = await proc.communicate()
```

Below streams sit **transports and protocols** — the callback-based layer. You’ll only touch it writing a protocol implementation; it’s what aiohttp and the WebRTC libraries are built on.

------------------------------------------------------------------------

## 15. Debugging and introspection

``` python
asyncio.current_task()
asyncio.all_tasks()                            # everything alive right now
task = asyncio.create_task(coro, name="settle-timer")   # always name tasks
task.get_coro(), task.get_stack(), task.print_stack()
```

Naming tasks costs nothing and turns “Task-47 was destroyed but it is pending” into an actionable message.

**3.14 introspection** — genuinely new capability:

``` bash
python -m asyncio ps <pid>
python -m asyncio pstree <pid>     # full await call graph of a running process
```

Attaches to a live process without stopping it and shows you what’s awaiting what. This is the answer to “production is hung and I don’t know where.” (Needs `sudo` on macOS.)

3.14 also rewrote task bookkeeping as a per-thread linked list — 10–20% faster on benchmarks, less memory — and made event loops thread-safe under free-threaded builds, so multiple loops can run in parallel across threads.

**Warnings worth knowing:** - `RuntimeWarning: coroutine 'x' was never awaited` — you called an async function and dropped the result. - `Task was destroyed but it is pending!` — the fire-and-forget GC bug from §2, or shutdown without draining. - `Task exception was never retrieved` — usually the `gather` leak from §5.

------------------------------------------------------------------------

## 16. Testing

``` python
# pyproject.toml / pytest.ini
[tool.pytest.ini_options]
asyncio_mode = "auto"        # every async test just works, no decorator
```

Strict mode requires `@pytest.mark.asyncio` on each test; auto mode doesn’t. Auto is less ceremony and worth it unless you’re mixing sync/async frameworks.

Standard library alternative: `unittest.IsolatedAsyncioTestCase`.

**The real problem is time.** Tests that `await asyncio.sleep(0.25)` to let a timer fire are slow and flaky under CI load. Three options, in order of preference:

1.  **Inject the clock and the delays.** Make the settle interval a constructor parameter; use 5ms in tests. Fastest and most honest.
2.  **Assert on order and causality, not timestamps.** “The cancel happened before the utterance was emitted” is a stable assertion; “it took 250±20ms” is not.
3.  **Actually run in real time.** Slow but tests the genuine scheduling behaviour. Defensible for a small suite where the timing *is* the thing under test — just know you’re buying wall-clock seconds and some CI flakiness.

`await asyncio.sleep(0)` to force a scheduling point is the cheapest way to let pending tasks make progress deterministically.

Mock async functions with `unittest.mock.AsyncMock` (auto-selected by `patch` for async targets since 3.8).

------------------------------------------------------------------------

## 17. Django / ASGI notes

Given a Django + DRF codebase, the practical shape:

``` python
async def my_view(request):
    obj = await Model.objects.aget(pk=1)
    count = await Model.objects.acount()
    async for row in Model.objects.filter(...):
        ...
```

- ORM async methods are `a`-prefixed: `aget`, `acreate`, `aupdate`, `afirst`, `acount`, `aexists`, `abulk_create`.
- **`SynchronousOnlyOperation`** is what you get calling sync ORM from async context. Wrap with `sync_to_async(fn, thread_sensitive=True)` — thread-sensitive matters because Django’s connection handling and transactions are thread-local.
- The async ORM is currently an async *interface* over a sync core; the database driver work still happens in a thread. It removes the `SynchronousOnlyOperation` friction, not the thread hop.
- Middleware must be marked async-capable or Django inserts sync/async adaptation on every request — measurable overhead.
- Deploy under uvicorn/hypercorn/daphne, not gunicorn-wsgi, or none of this does anything.

Honest assessment: Django’s async story is good enough for calling external APIs concurrently inside a view. It is not a reason to rewrite a working sync codebase.

------------------------------------------------------------------------

## 18. Ecosystem

| Need | Library |
|----|----|
| Faster loop | `uvloop` (2–4× on socket-heavy workloads) |
| HTTP client | `httpx`, `aiohttp` |
| Postgres | `asyncpg` (fast) or `psycopg` 3 (async support, more familiar) |
| Redis | `redis.asyncio` |
| Files | `aiofiles` (a thread-pool wrapper, not real async IO) |
| Backend-agnostic async | `anyio` — write once, run on asyncio or trio |
| Structured concurrency done right | `trio` — where TaskGroup’s design came from |

`anyio` is worth knowing about even if you stay on asyncio: its cancel scopes and task groups are a cleaner API than the stdlib’s, and it’s what FastAPI uses underneath.

------------------------------------------------------------------------

## 19. Consolidated gotchas

1.  **`await a(); await b()` is sequential.** Concurrency requires `create_task` or a TaskGroup.
2.  **Fire-and-forget tasks get garbage collected.** Hold a reference.
3.  **`gather` doesn’t cancel siblings on exception.** Use `TaskGroup`.
4.  **`except Exception` doesn’t catch `CancelledError`.** By design.
5.  **Catching `CancelledError` without re-raising** breaks cancellation everywhere upstream.
6.  **`task.cancel()` is a request.** Await the task to know it’s finished.
7.  **`shield` doesn’t make the caller wait** for the shielded operation.
8.  **One blocking call freezes the whole process.** Debug mode finds them.
9.  **Unbounded queues are memory leaks.** Set `maxsize`.
10. **asyncio primitives are not thread-safe.** Only `call_soon_threadsafe` crosses threads.
11. **`loop.time()` is monotonic**, never comparable to `time.time()`.
12. **Async generators need `aclosing`** if you break out early.
13. **CPU-bound work doesn’t belong here.** Threads don’t help; use processes.
14. **`get_event_loop()` is effectively gone** — `RuntimeError` in 3.14, policies removed in 3.16.
15. **`asyncio.run()` fails in notebooks.** Use bare `await`; don’t reach for `nest_asyncio`.
16. **Notebook background-task exceptions are silent.** Check `task.exception()`.

------------------------------------------------------------------------

## 20. Version cheat sheet

| Version | Added |
|----|----|
| 3.8 | `CancelledError` becomes `BaseException`; `AsyncMock` |
| 3.9 | `asyncio.to_thread` |
| 3.11 | **`TaskGroup`**, **`asyncio.timeout()`**, `Barrier`, `Runner`, `task.uncancel()`, `TimeoutError` unified with builtin |
| 3.12 | Eager task factory; `wait` no longer accepts coroutines |
| 3.13 | `Queue.shutdown()` / `QueueShutDown` |
| 3.14 | `get_event_loop()` raises without a loop; policies deprecated; child watchers removed; `python -m asyncio pstree`; 10–20% faster; free-threading support |
| 3.16 | (planned) event loop policy system removed |

------------------------------------------------------------------------

## 21. If you only remember five things

1.  `await` is the only place another task can run — that’s both the constraint and the tool.
2.  Use `TaskGroup`, not `gather`.
3.  `CancelledError` is a `BaseException`; catch it only to clean up, then re-raise.
4.  Never block the loop; `to_thread` for IO, processes for CPU.
5.  Bound your queues and name your tasks.

------------------------------------------------------------------------

Back to top
