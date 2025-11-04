import importlib
import pathlib
import sys
import types

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

datasync_pkg = types.ModuleType("datasync")
datasync_pkg.__path__ = [str(ROOT)]
sys.modules.setdefault("datasync", datasync_pkg)

config_mod = importlib.import_module("config")
sys.modules.setdefault("datasync.config", config_mod)

sync_mod = importlib.import_module("sync")
sys.modules.setdefault("datasync.sync", sync_mod)

SyncManager = sync_mod.SyncManager


def test_chunk_size_must_be_within_bounds():
    with pytest.raises(ValueError):
        SyncManager(chunk_size=0)
    with pytest.raises(ValueError):
        SyncManager(chunk_size=501)


def test_connect_requires_https_and_auth_token():
    manager = SyncManager()
    with pytest.raises(ConnectionError):
        manager.connect("http://example.com", auth_token="token")

    assert manager.connect("https://example.com", auth_token="secret") is True
    assert manager.remote_url == "https://example.com"
    assert manager.auth_token == "secret"
    assert manager.timeout == 2


def test_push_accumulates_synced_count():
    manager = SyncManager()

    result = manager.push({"id": 1}, mode="sync")
    assert result == {"status": "ok", "count": 1}

    with pytest.raises(ValueError):
        manager.push({"id": 2}, mode="invalid")

    manager.push({"id": 3}, mode="async")
    assert manager.get_synced_count() == 2
