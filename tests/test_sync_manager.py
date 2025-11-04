import datasync
import pytest


def test_init_defaults():
    m = datasync.SyncManager()
    assert m.chunk_size == 100
    assert m.retry_limit == 10
    assert m.enable_cache is False


def test_invalid_chunk_size_low():
    with pytest.raises(ValueError):
        datasync.SyncManager(chunk_size=0)


def test_invalid_chunk_size_high():
    with pytest.raises(ValueError):
        datasync.SyncManager(chunk_size=501)


def test_connect_requires_auth_token():
    m = datasync.SyncManager()
    ok = m.connect(remote_url="https://example.com", auth_token="token123")
    assert ok is True
    assert m.remote_url == "https://example.com"
    assert m.auth_token == "token123"


def test_connect_invalid_url_scheme():
    m = datasync.SyncManager()
    with pytest.raises(ConnectionError):
        m.connect(remote_url="http://insecure.example.com", auth_token="token123")


def test_push_and_count_sync_async():
    m = datasync.SyncManager()
    r1 = m.push({"id": 1}, mode="sync")
    assert r1["count"] == 1 and r1["status"] == "ok"
    r2 = m.push({"id": 2}, mode="async")
    assert r2["count"] == 2 and r2["status"] == "ok"
    assert m.get_synced_count() == 2


def test_push_invalid_mode():
    m = datasync.SyncManager()
    with pytest.raises(ValueError):
        m.push({}, mode="invalid")


def test_get_synced_count_accessor():
    m = datasync.SyncManager()
    m.push({"id": 1})
    assert m.get_synced_count() == 1