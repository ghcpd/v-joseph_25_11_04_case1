# DataSync Library (Corrected)

`datasync` provides a simple in‑memory synchronization counter and placeholder interfaces for connecting and pushing JSON data. Current implementation is minimal and does NOT perform real network operations or caching.

---
## Installation (Local Source)
Clone or place the library locally; no PyPI package is assumed.

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt  # Only pytest and (optionally) datasync if packaged
```

---
## Quick Start

```python
from datasync import SyncManager  # Exported via __init__.py

manager = SyncManager()  # Uses defaults chunk_size=100, retry_limit=10

# Required auth_token parameter; timeout is integer seconds
manager.connect(
    remote_url="https://example.com/data",
    auth_token="my-token",
    timeout=2,
)

# Push in synchronous mode (default) then asynchronous
resp1 = manager.push({"id": 1, "value": "abc"}, mode="sync")
resp2 = manager.push({"id": 2, "value": "xyz"}, mode="async")

print("Sync completed count:", manager.get_synced_count())
print(resp2)  # {'status': 'ok', 'count': 2}
```

---
## API Reference

### SyncManager
```python
SyncManager(
    chunk_size: int = 100,
    retry_limit: int = 10,  # from config.MAX_RETRIES
    enable_cache: bool = False,
)
```
- `chunk_size`: Items per (conceptual) batch; must satisfy `1 <= chunk_size <= 500`.
- `retry_limit`: Max retries counter (currently unused beyond storage). Default sourced from `config.MAX_RETRIES`.
- `enable_cache`: Accepted but no caching implemented yet.

Raises `ValueError` if `chunk_size` outside allowed range.

### connect
```python
connect(remote_url: str, auth_token: str, timeout: int = 2) -> bool
```
- Validates only that `remote_url` starts with `https://`.
- Stores `remote_url`, `auth_token`, and `timeout`.
- Returns `True` on successful parameter acceptance.
- Raises `ConnectionError` only for invalid URL scheme.

### push
```python
push(data: dict, mode: str = "sync") -> dict
```
- `mode`: One of `"sync"` or `"async"`.
- Increments internal counter; returns `{"status": "ok", "count": <int>}`.
- Raises `ValueError` if `mode` is not one of the accepted values.

### get_synced_count
```python
get_synced_count() -> int
```
Returns number of successful `push` operations.

### metrics.get_latency
```python
from datasync import metrics
metrics.get_latency() -> float
```
Returns a placeholder latency value (`0.352` seconds).

---
## Error Handling Summary
- `ValueError`: invalid `chunk_size` range or `mode` in `push`.
- `ConnectionError`: only if `remote_url` does not start with `https://`.

---
## Roadmap / Known Gaps
- No actual network I/O; `connect` does not verify reachability.
- No caching despite `enable_cache` parameter.
- No retry logic using `retry_limit` yet.

---
## Example (Async Mode)
```python
manager.push({"id": 3}, mode="async")
```

---
## License
Internal usage example; add proper license if distributing.