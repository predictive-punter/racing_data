def test_value(race, runner, provider):
    """The get_race_by_runner method should return the race in which the specified runner competes"""

    assert provider.get_race_by_runner(runner)['_id'] == race['_id']
