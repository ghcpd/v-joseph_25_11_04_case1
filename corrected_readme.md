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
from sync import SyncManager

manager = SyncManager(chunk_size=50, retry_limit=3)

manager.connect(
    remote_url="https://example.com/data",
    auth_token="your_auth_token_here",
    timeout=2
)

result = manager.push({"id": 1, "value": "abc"}, mode="async")

print("Sync completed:", manager.get_synced_count())
print("Push result:", result)
```

---

## API Reference

### `SyncManager(chunk_size: int = 100, retry_limit: int = 10, enable_cache: bool = False)`

Creates a new SyncManager instance.

**Parameters:**
- **chunk_size** (int, default=100): Number of items per batch. Must be between `1` and `500`.
- **retry_limit** (int, default=10): Number of retries before aborting. Default value is imported from `config.MAX_RETRIES`.
- **enable_cache** (bool, default=False): Enables local cache if True.

**Raises:**
- `ValueError`: If chunk_size is not between 1 and 500.

**Example:**
```python
manager = SyncManager(chunk_size=100, retry_limit=5, enable_cache=True)
```

---

### `connect(remote_url: str, auth_token: str, timeout: int = 2)`

Connects to remote server with authentication.

**Parameters:**
- **remote_url** (str): The remote server URL. Must start with `https://`.
- **auth_token** (str): Authentication token for the remote server (required).
- **timeout** (int, default=2): Connection timeout in seconds.

**Returns:**
- `bool`: Returns `True` on successful connection.

**Raises:**
- `ConnectionError`: If the remote URL is invalid (doesn't start with `https://`).

**Example:**
```python
manager.connect(
    remote_url="https://example.com/data",
    auth_token="abc123token",
    timeout=3
)
```

---

### `push(data: dict, mode: str = "sync")`

Pushes data to the remote endpoint.

**Parameters:**
- **data** (dict): The data dictionary to push to the remote server.
- **mode** (str, default="sync"): Synchronization mode. Must be either `"sync"` or `"async"`.

**Returns:**
- `dict`: A dictionary with the following keys:
  - `status` (str): Status of the operation (e.g., "ok")
  - `count` (int): Total number of items synced so far

**Raises:**
- `ValueError`: If mode is not "sync" or "async".

**Example:**
```python
# Synchronous mode (default)
result = manager.push({"id": 1, "value": "abc"}, mode="sync")

# Asynchronous mode
result = manager.push({"id": 2, "value": "def"}, mode="async")

print(result)  # {'status': 'ok', 'count': 2}
```

---

### `get_synced_count() -> int`

Returns the total number of items that have been synced.

**Returns:**
- `int`: The count of synced items.

**Example:**
```python
count = manager.get_synced_count()
print(f"Total synced: {count}")
```

---

## Additional Modules

### `config.py`

Contains configuration constants:
- **MAX_RETRIES** (int): Default maximum retry attempts (value: 10)

### `metrics.py`

Provides performance metrics:
- **get_latency()**: Returns the last sync latency in seconds (float).

---

## Complete Working Example

```python
from sync import SyncManager
from metrics import get_latency

# Initialize with custom settings
manager = SyncManager(
    chunk_size=50,
    retry_limit=5,
    enable_cache=True
)

# Connect to remote server
try:
    manager.connect(
        remote_url="https://api.example.com/sync",
        auth_token="your_secure_token",
        timeout=3
    )
    print("Connected successfully!")
except ConnectionError as e:
    print(f"Connection failed: {e}")
    exit(1)

# Push data in async mode
data_items = [
    {"id": 1, "value": "first"},
    {"id": 2, "value": "second"},
    {"id": 3, "value": "third"}
]

for item in data_items:
    result = manager.push(item, mode="async")
    print(f"Pushed item {item['id']}: {result}")

# Get sync statistics
total_synced = manager.get_synced_count()
latency = get_latency()

print(f"\nSummary:")
print(f"Total items synced: {total_synced}")
print(f"Last sync latency: {latency}s")
```

---

## Error Handling

The library raises the following exceptions:

- **ValueError**: 
  - When `chunk_size` is outside the range [1, 500]
  - When `mode` parameter in `push()` is not "sync" or "async"

- **ConnectionError**: 
  - When `remote_url` doesn't start with "https://"

Always wrap connection attempts in try-except blocks for production use.

---
