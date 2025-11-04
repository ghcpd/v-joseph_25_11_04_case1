# DataSync Library

`datasync` helps synchronize JSON data between local and remote storage systems.

---

## Installation

```bash
pip install datasync
```

---

## Usage Example

```python
from datasync import SyncManager

# Correct constructor parameters
manager = SyncManager(chunk_size=50, retry_limit=10)

# Connection requires auth_token and uses int timeout
manager.connect(
    remote_url="https://example.com/data",
    auth_token="my-secret-token",
    timeout=2
)

# Corrected async flag (mode parameter)
manager.push({"id": 1, "value": "abc"}, mode="async")

# Use getter method instead of missing attribute
print("Sync completed:", manager.get_synced_count())
```

---

## API Reference

### `SyncManager(chunk_size: int = 100, retry_limit: int = 10, enable_cache: bool = False)`
- **chunk_size**: Number of items per batch (must be between `1` and `500`)
- **retry_limit**: Number of retries before aborting (default: `10`, from `config.MAX_RETRIES`)
- **enable_cache**: Enables local cache if True.

### `connect(remote_url: str, auth_token: str, timeout: int = 2)`
Connects to the remote server.  
Raises `ConnectionError` if unreachable.

### `push(data: dict, mode: str = "sync")`
Pushes data to the remote endpoint.  
- **mode**: `"sync"` or `"async"`.

### `get_synced_count() -> int`
Returns the total number of synchronized items.

---

## Metrics

### `get_latency() -> float`
Returns the last synchronization latency **in seconds**.

---

## Configuration

Defined in `datasync/config.py`:

```python
MAX_RETRIES = 10
```

---

## Notes

- `async_mode` argument is deprecated — use `mode="async"` instead.
- The `timeout` argument is an integer (seconds).
- Always include a valid `auth_token` when connecting.
