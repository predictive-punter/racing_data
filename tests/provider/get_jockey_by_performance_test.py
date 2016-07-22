def test_value(jockey, performance, provider):
    """The get_jockey_by_performance method should return the jockey associated with the specified performance"""

    assert provider.get_jockey_by_performance(performance)['_id'] == jockey['_id']
