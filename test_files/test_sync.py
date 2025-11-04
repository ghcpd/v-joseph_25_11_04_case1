from datasync.config import MAX_RETRIES
from datasync.metrics import get_latency
from datasync.sync import SyncManager
import pytest


def test_default_configuration_matches_constants():
    manager = SyncManager()
    assert manager.chunk_size == 100
    assert manager.retry_limit == MAX_RETRIES
    assert manager.enable_cache is False


def test_chunk_size_validation():
    with pytest.raises(ValueError):
        SyncManager(chunk_size=0)
    with pytest.raises(ValueError):
        SyncManager(chunk_size=600)


def test_connect_requires_https_and_auth_token():
    manager = SyncManager()
    with pytest.raises(ConnectionError):
        manager.connect(remote_url="http://example.com", auth_token="token")

    result = manager.connect(remote_url="https://example.com", auth_token="token", timeout=3)
    assert result is True
    assert manager.remote_url == "https://example.com"
    assert manager.auth_token == "token"
    assert manager.timeout == 3


def test_push_mode_and_count_tracking():
    manager = SyncManager()
    response = manager.push({"id": 1}, mode="sync")
    assert response == {"status": "ok", "count": 1}
    assert manager.get_synced_count() == 1

    response_async = manager.push({"id": 2}, mode="async")
    assert response_async == {"status": "ok", "count": 2}
    assert manager.get_synced_count() == 2

    with pytest.raises(ValueError):
        manager.push({"id": 3}, mode="invalid")


def test_latency_metric_is_float():
    value = get_latency()
    assert isinstance(value, float)
    assert value >= 0
