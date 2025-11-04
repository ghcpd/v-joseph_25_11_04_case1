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

manager = SyncManager(batch_size=50, retry_limit=3)

manager.connect(
    remote_url="https://example.com/data",
    timeout=1.5
)

manager.push({"id": 1, "value": "abc"}, async_mode=True)

print("Sync completed:", manager.synced_count)
```

---

## API Reference

### `SyncManager(batch_size: int = 50, retry_limit: int = 3, enable_cache: bool = False)`
- **batch_size**: Number of items per batch (must be between `10` and `100`)
- **retry_limit**: Number of retries before aborting
- **enable_cache**: Enables local cache if True

### `connect(remote_url: str, timeout: float = 1.5)`
Connects to remote server.  
Raises `ConnectionError` if unreachable.

### `push(data: dict, async_mode: bool = True)`
Pushes data to the remote endpoint asynchronously.

---
