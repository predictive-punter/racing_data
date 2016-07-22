def test_value(horse, performance, provider):
    """The get_horse_by_performance method should return the horse associated with the specified performance"""

    assert provider.get_horse_by_performance(performance)['_id'] == horse['_id']
