def test_meet(meet, race):
    """The meet property should return the meet at which the race occurs"""

    assert race.meet['_id'] == meet['_id']


def test_runners(race, runners):
    """The runners property should return the list of runners competing in the race"""

    property_ids = [runner['_id'] for runner in race.runners]
    provider_ids = [runner['_id'] for runner in runners]

    assert property_ids == provider_ids


def test_str(race):
    """str(race) should return a human readable string representation of the race"""

    assert str(race) == 'race {number} at {meet}'.format(number=race['number'], meet=race.meet)
