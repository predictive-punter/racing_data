def test_get_cached_property(races):
    """The get_cached_property method should not return stale data"""

    assert [runner['_id'] for runner in races[0].runners] != [runner['_id'] for runner in races[1].runners]
