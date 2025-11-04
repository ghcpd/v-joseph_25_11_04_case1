# DataSync Library (Corrected)

`datasync` synchronizes JSON payloads to a remote HTTPS endpoint while keeping basic retry accounting. This README reflects the current implementation in `sync.py`, `config.py`, and `metrics.py` as of 2025-11-04.

---

## Installation

At the moment the repository contains only module files and no packaging metadata, so `pip install datasync` will fail. Work with the sources directly instead:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
export PYTHONPATH="$(pwd)"  # On Windows: set PYTHONPATH=%CD%
```

Adding the repository root to `PYTHONPATH` allows the internal imports (e.g. `datasync.config`) to resolve until proper packaging is added.

---

## Quick Start

```python
from datasync.sync import SyncManager

manager = SyncManager(chunk_size=100, retry_limit=10)
manager.connect(
    remote_url="https://example.com/data",
    auth_token="super-secret-token",
    timeout=2,
)

result = manager.push({"id": 1, "value": "abc"}, mode="async")
print("Sync completed:", manager.get_synced_count())
print(result)  # {'status': 'ok', 'count': 1}
```

**Key differences from the old README**
- Initializer keyword is `chunk_size` (defaults to 100, allowed range 1–500).
- `retry_limit` defaults to `datasync.config.MAX_RETRIES` (10).
- `connect` requires an `auth_token` and defaults `timeout` to `2` seconds.
- `push` uses a string `mode` (`"sync"` or `"async"`) and returns a status dictionary.
- Use `get_synced_count()` instead of a `synced_count` attribute.

---

## API Reference

### `SyncManager(chunk_size: int = 100, retry_limit: int = 10, enable_cache: bool = False)`
- `chunk_size`: Items per batch. Values outside `1..500` raise `ValueError`.
- `retry_limit`: Maximum retries; defaults to `datasync.config.MAX_RETRIES` (10).
- `enable_cache`: Stored on the instance but no caching behavior is currently implemented.

### `connect(remote_url: str, auth_token: str, timeout: int = 2) -> bool`
- Requires an HTTPS URL; non-HTTPS values raise `ConnectionError`.
- Persists `remote_url`, `auth_token`, and `timeout` on the instance and returns `True`.
- No network I/O is performed in the current implementation; connectivity checks are limited to the URL scheme.

### `push(data: dict, mode: str = "sync") -> dict`
- Accepts `mode` values `"sync"` or `"async"`; other values raise `ValueError`.
- Increments an internal counter and returns `{"status": "ok", "count": <new_total>}`.

### `get_synced_count() -> int`
- Returns the number of successful `push` calls.

### `datasync.metrics.get_latency() -> float`
- Returns a placeholder latency `0.352` seconds.

---

## Testing

Run the bundled pytest suite (after exporting `PYTHONPATH` as shown above):

```bash
python -m pytest test_files -q
```

---

## Known Gaps

- Packaging metadata (`pyproject.toml`/`setup.cfg`) is missing. Until added, installing with `pip install datasync` will fail.
- `enable_cache` is stored but unused.
- `connect` does not validate remote availability beyond enforcing HTTPS.
```