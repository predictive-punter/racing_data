def test_value(meet, race, provider):
    """The get_meet_by_race method should return the meet at which the specified race occurs"""

    assert provider.get_meet_by_race(race)['_id'] == meet['_id']
