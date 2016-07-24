def test_str(trainer):
    """str(trainer) should return a human readable string representation of the trainer"""

    assert str(trainer) == 'trainer {name}'.format(name=trainer['name'])
