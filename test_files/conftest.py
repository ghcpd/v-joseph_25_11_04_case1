"""
Pytest configuration and fixtures for datasync tests
"""
import pytest
import sys
from pathlib import Path

# Ensure parent directory is in path for all tests
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sync_manager():
    """Fixture that provides a fresh SyncManager instance"""
    from sync import SyncManager
    return SyncManager()


@pytest.fixture
def connected_manager():
    """Fixture that provides a connected SyncManager instance"""
    from sync import SyncManager
    manager = SyncManager()
    manager.connect(
        remote_url="https://test.example.com/api",
        auth_token="test_token_fixture",
        timeout=2
    )
    return manager


@pytest.fixture
def custom_manager():
    """Fixture that provides a customized SyncManager instance"""
    from sync import SyncManager
    return SyncManager(
        chunk_size=50,
        retry_limit=5,
        enable_cache=True
    )
