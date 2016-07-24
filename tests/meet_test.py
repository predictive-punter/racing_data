import tzlocal


def test_races(meet, races):
    """The races property should return the list of races occurring at the meet"""

    property_ids = [race['_id'] for race in meet.races]
    provider_ids = [race['_id'] for race in races]

    assert property_ids == provider_ids


def test_str(meet):
    """str(meet) should return a human readable string representation of meet"""

    assert str(meet) == '{track} on {date:%Y-%m-%d}'.format(track=meet['track'], date=meet['date'].astimezone(tzlocal.get_localzone()))
