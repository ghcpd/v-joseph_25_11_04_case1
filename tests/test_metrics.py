import datasync.metrics as metrics


def test_latency_is_float():
    value = metrics.get_latency()
    assert isinstance(value, float)
    assert value >= 0