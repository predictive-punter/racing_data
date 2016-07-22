def test_race(race, runner):
    """The race property should return the race in which the runner competes"""

    assert runner.race['_id'] == race['_id']
