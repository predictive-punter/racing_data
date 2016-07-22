def test_races(meet, provider):
    """The races property should return the list of races occurring at the meet"""

    property_ids = [race['_id'] for race in meet.races]
    provider_ids = [race['_id'] for race in provider.get_races_by_meet(meet)]

    assert property_ids == provider_ids
