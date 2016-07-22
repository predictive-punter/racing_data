def test_meet(meet, race):
    """The meet property should return the meet at which the race occurs"""

    assert race.meet['_id'] == meet['_id']
