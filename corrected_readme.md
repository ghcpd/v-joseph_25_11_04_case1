# DataSync Library

`datasync` helps synchronize JSON data between local and remote storage systems.

---

## Installation

Create and activate a virtual environment, then install the package in editable mode along with test requirements:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

---

## Quick Start

```python
from datasync.sync import SyncManager

manager = SyncManager(chunk_size=100, retry_limit=10)

manager.connect(
    remote_url="https://example.com/data",
    auth_token="secret-token",
    timeout=2,
)

manager.push({"id": 1, "value": "abc"}, mode="async")

print("Sync completed:", manager.get_synced_count())
```

---

## API Reference

### `SyncManager(chunk_size: int = 100, retry_limit: int = 10, enable_cache: bool = False)`
- **chunk_size**: Number of items processed per batch. Must be between `1` and `500` (inclusive).
- **retry_limit**: Maximum number of retries before aborting. Default is `datasync.config.MAX_RETRIES` (`10`).
- **enable_cache**: Enables a local cache when set to `True` (feature stub).

### `connect(remote_url: str, auth_token: str, timeout: int = 2) -> bool`
Establishes a connection to the remote server. The URL must use HTTPS; otherwise a `ConnectionError` is raised. Returns `True` on success.

### `push(data: dict, mode: str = "sync") -> dict`
Pushes payloads to the remote endpoint. `mode` must be either `"sync"` or `"async"`. Returns a dict containing the status and cumulative synced count.

### `get_synced_count() -> int`
Returns the number of records pushed during the current session.

---

## Metrics

### `datasync.metrics.get_latency() -> float`
Returns the most recent sync latency in seconds.

---

## Running Tests

```bash
pytest
```
