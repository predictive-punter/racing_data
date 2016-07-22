def test_horse(performance, horse):
    """The horse property should return the horse associated with the performance"""

    assert performance.horse['_id'] == horse['_id']


def test_jockey(performance, jockey):
    """The jockey property should return the jockey associated with the performance"""

    assert performance.jockey['_id'] == jockey['_id']
