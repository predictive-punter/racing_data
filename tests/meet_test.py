def test_races(meet, races):
    """The races property should return the list of races occurring at the meet"""

    property_ids = [race['_id'] for race in meet.races]
    provider_ids = [race['_id'] for race in races]

    assert property_ids == provider_ids
