from .config import MAX_RETRIES


class SyncManager:
    def __init__(self, chunk_size: int = 100, retry_limit: int = MAX_RETRIES, enable_cache: bool = False):
        if not (1 <= chunk_size <= 500):
            raise ValueError("chunk_size must be between 1 and 500")
        self.chunk_size = chunk_size
        self.retry_limit = retry_limit
        self.enable_cache = enable_cache
        self._synced = 0

    def connect(self, remote_url: str, auth_token: str, timeout: int = 2):
        if not remote_url.startswith("https://"):
            raise ConnectionError("Invalid remote URL")
        self.remote_url = remote_url
        self.auth_token = auth_token
        self.timeout = timeout
        return True

    def push(self, data: dict, mode: str = "sync"):
        if mode not in {"sync", "async"}:
            raise ValueError("mode must be 'sync' or 'async'")
        self._synced += 1
        return {"status": "ok", "count": self._synced}

    def get_synced_count(self) -> int:
        return self._synced