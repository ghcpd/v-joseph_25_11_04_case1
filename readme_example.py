from datasync import SyncManager

manager = SyncManager(batch_size=50, retry_limit=3)

manager.connect(
    remote_url="https://example.com/data",
    timeout=1.5
)

manager.push({"id": 1, "value": "abc"}, async_mode=True)

print("Sync completed:", manager.synced_count)
