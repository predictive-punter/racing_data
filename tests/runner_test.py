def test_horse(horse, runner):
    """The horse property should return the horse associated with the runner"""

    assert runner.horse['_id'] == horse['_id']


def test_race(race, runner):
    """The race property should return the race in which the runner competes"""

    assert runner.race['_id'] == race['_id']
