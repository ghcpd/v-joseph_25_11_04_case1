import pytest

from datasync.config import MAX_RETRIES
from datasync.sync import SyncManager


def test_default_configuration():
    manager = SyncManager()
    assert manager.chunk_size == 100
    assert manager.retry_limit == MAX_RETRIES
    assert manager.enable_cache is False


def test_chunk_size_out_of_bounds():
    with pytest.raises(ValueError):
        SyncManager(chunk_size=0)
    with pytest.raises(ValueError):
        SyncManager(chunk_size=501)


def test_connect_requires_https_and_auth_token():
    manager = SyncManager()
    with pytest.raises(ConnectionError):
        manager.connect(remote_url="http://example.com", auth_token="token", timeout=1)

    assert manager.connect(remote_url="https://example.com", auth_token="token", timeout=4) is True
    assert manager.remote_url == "https://example.com"
    assert manager.auth_token == "token"
    assert manager.timeout == 4


def test_push_mode_validation_and_count_increment():
    manager = SyncManager()
    with pytest.raises(ValueError):
        manager.push({}, mode="invalid")

    response = manager.push({}, mode="async")
    assert response == {"status": "ok", "count": 1}
    assert manager.get_synced_count() == 1


def test_get_synced_count_matches_push_calls():
    manager = SyncManager()
    for _ in range(3):
        manager.push({}, mode="sync")
    assert manager.get_synced_count() == 3
