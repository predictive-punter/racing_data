def test_horse(performance, horse):
    """The horse property should return the horse associated with the performance"""

    assert performance.horse['_id'] == horse['_id']
