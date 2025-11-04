"""
Demonstration that corrected README examples work correctly
This file validates that all code examples from corrected_readme.md execute successfully
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sync import SyncManager
from metrics import get_latency


def test_basic_usage_example():
    """Test the basic usage example from corrected README"""
    print("\n=== Testing Basic Usage Example ===")
    
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
    
    assert manager.get_synced_count() == 1
    assert result["status"] == "ok"
    print("✓ Basic usage example works!")


def test_syncmanager_initialization():
    """Test SyncManager initialization example"""
    print("\n=== Testing SyncManager Initialization ===")
    
    manager = SyncManager(chunk_size=100, retry_limit=5, enable_cache=True)
    
    assert manager.chunk_size == 100
    assert manager.retry_limit == 5
    assert manager.enable_cache is True
    print("✓ SyncManager initialization works!")


def test_connect_example():
    """Test connect method example"""
    print("\n=== Testing Connect Method ===")
    
    manager = SyncManager()
    result = manager.connect(
        remote_url="https://example.com/data",
        auth_token="abc123token",
        timeout=3
    )
    
    assert result is True
    assert manager.remote_url == "https://example.com/data"
    assert manager.auth_token == "abc123token"
    assert manager.timeout == 3
    print("✓ Connect method works!")


def test_push_examples():
    """Test push method examples"""
    print("\n=== Testing Push Method ===")
    
    manager = SyncManager()
    manager.connect("https://example.com/data", "token")
    
    # Synchronous mode (default)
    result = manager.push({"id": 1, "value": "abc"}, mode="sync")
    assert result["status"] == "ok"
    assert result["count"] == 1
    
    # Asynchronous mode
    result = manager.push({"id": 2, "value": "def"}, mode="async")
    assert result["status"] == "ok"
    assert result["count"] == 2
    
    print("✓ Push method works!")


def test_get_synced_count_example():
    """Test get_synced_count example"""
    print("\n=== Testing get_synced_count Method ===")
    
    manager = SyncManager()
    manager.connect("https://example.com/data", "token")
    manager.push({"id": 1}, mode="sync")
    
    count = manager.get_synced_count()
    print(f"Total synced: {count}")
    
    assert count == 1
    assert isinstance(count, int)
    print("✓ get_synced_count method works!")


def test_complete_working_example():
    """Test the complete working example from corrected README"""
    print("\n=== Testing Complete Working Example ===")
    
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
        raise

    # Push data in async mode
    data_items = [
        {"id": 1, "value": "first"},
        {"id": 2, "value": "second"},
        {"id": 3, "value": "third"}
    ]

    for item in data_items:
        result = manager.push(item, mode="async")
        print(f"Pushed item {item['id']}: {result}")
        assert result["status"] == "ok"

    # Get sync statistics
    total_synced = manager.get_synced_count()
    latency = get_latency()

    print(f"\nSummary:")
    print(f"Total items synced: {total_synced}")
    print(f"Last sync latency: {latency}s")
    
    assert total_synced == 3
    assert latency == 0.352
    print("✓ Complete working example works!")


def test_error_handling():
    """Test error handling examples"""
    print("\n=== Testing Error Handling ===")
    
    # Test invalid chunk_size
    try:
        manager = SyncManager(chunk_size=501)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"✓ Caught expected error for invalid chunk_size: {e}")
    
    # Test invalid URL
    try:
        manager = SyncManager()
        manager.connect("http://insecure.com", "token")
        assert False, "Should have raised ConnectionError"
    except ConnectionError as e:
        print(f"✓ Caught expected error for invalid URL: {e}")
    
    # Test invalid mode
    try:
        manager = SyncManager()
        manager.connect("https://example.com", "token")
        manager.push({"id": 1}, mode="invalid")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"✓ Caught expected error for invalid mode: {e}")
    
    print("✓ Error handling works correctly!")


if __name__ == "__main__":
    print("=" * 60)
    print("CORRECTED README EXAMPLES - VALIDATION TEST")
    print("=" * 60)
    
    test_basic_usage_example()
    test_syncmanager_initialization()
    test_connect_example()
    test_push_examples()
    test_get_synced_count_example()
    test_complete_working_example()
    test_error_handling()
    
    print("\n" + "=" * 60)
    print("ALL CORRECTED README EXAMPLES WORK SUCCESSFULLY!")
    print("=" * 60)
