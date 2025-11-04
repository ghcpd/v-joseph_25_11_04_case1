# DataSync Library (Corrected Documentation)

## Overview
The in-repository `datasync` modules provide a lightweight manager for batching
data uploads and reporting simple metrics. The library currently consists of:

- `config.py` – houses configuration constants (`MAX_RETRIES = 10`).
- `sync.py` – exposes the `SyncManager` class for connecting to a remote HTTPS
  endpoint and pushing payloads.
- `metrics.py` – contains helper telemetry such as `get_latency()`.

> **Note**: The project has not yet been packaged for PyPI. Import paths in the
> examples assume you run from the repository root (or add it to
> `PYTHONPATH`) so that `datasync.*` resolves to these local modules.

---

## Environment Setup

1. Create and activate a virtual environment (example with the bundled `.venv`
   name):
   ```bash
   python -m venv .venv
   # Linux/macOS
   source .venv/bin/activate
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   ```
2. Install tooling and test dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. (Optional) export the project root so the `datasync` package can be imported
   directly:
   ```bash
   # Linux/macOS
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   # Windows PowerShell
   $env:PYTHONPATH = (Get-Location).Path + ';' + $env:PYTHONPATH
   ```

You can run the helper script `setup.sh` from POSIX shells to automate steps 1–2
on Unix-like environments.

---

## Quick Start Example

```python
from datasync.config import MAX_RETRIES
from datasync.sync import SyncManager

manager = SyncManager(chunk_size=100, retry_limit=MAX_RETRIES, enable_cache=False)

manager.connect(
    remote_url="https://example.com/data",
    auth_token="my-api-token",
    timeout=2,
)

result = manager.push({"id": 1, "value": "abc"}, mode="async")
print("Push result:", result)
print("Sync completed:", manager.get_synced_count())
```

Running the above snippet from the repository root succeeds and prints:

```
Push result: {'status': 'ok', 'count': 1}
Sync completed: 1
```

---

## API Reference (Current Implementation)

### `SyncManager(chunk_size: int = 100, retry_limit: int = 10, enable_cache: bool = False)`
- **chunk_size** – Number of records per push batch. Must satisfy `1 <= chunk_size <= 500`.
- **retry_limit** – Maximum retry attempts before aborting. Defaults to
  `datasync.config.MAX_RETRIES` (`10`).
- **enable_cache** – Enables the optional local cache flag (currently unused in
  core logic).

### `connect(remote_url: str, auth_token: str, timeout: int = 2) -> bool`
- Requires an HTTPS URL; otherwise a `ConnectionError` is raised.
- Stores the remote URL, auth token, and timeout on the manager and returns
  `True` on success.

### `push(data: dict, mode: str = "sync") -> dict`
- Accepts `mode` values of either `"sync"` or `"async"`; any other value raises
  `ValueError`.
- Each successful push increments the internal counter and returns a status
  dictionary shaped like `{"status": "ok", "count": <int>}`.

### `get_synced_count() -> int`
- Convenience accessor exposing the cumulative number of successful pushes.

### `datasync.metrics.get_latency() -> float`
- Returns the most recently recorded latency in seconds (static value `0.352`
  in the current stub implementation).

---

## Testing

Pytest-based regression tests live in `test_files/`. Execute them from the
repository root:

```bash
pytest test_files
```

The helper script `run_tests.sh` wraps the same command.

---

## Change Log / Known Gaps

- Packaging metadata is not yet provided; `pip install datasync` resolves to an
  unrelated third-party project.
- `enable_cache` is reserved for future enhancements and currently has no effect.
- Error handling for network outages is limited to scheme validation and does
  not perform real network checks.
