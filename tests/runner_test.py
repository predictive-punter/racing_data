def test_horse(horse, runner):
    """The horse property should return the horse associated with the runner"""

    assert runner.horse['_id'] == horse['_id']


def test_jockey(jockey, runner):
    """The jockey property should return the jockey associated with the runner"""

    assert runner.jockey['_id'] == jockey['_id']


def test_race(race, runner):
    """The race property should return the race in which the runner competes"""

    assert runner.race['_id'] == race['_id']


def test_str(runner):
    """str(runner) should return a human readable string representation of the runner"""

    assert str(runner) == 'runner #{number} in {race}'.format(number=runner['number'], race=runner.race)


def test_trainer(trainer, runner):
    """The trainer property should return the trainer associated with the runner"""

    assert runner.trainer['_id'] == trainer['_id']
