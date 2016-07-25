import math

import racing_data
from racing_data.constants import BARRIER_WIDTH, HORSE_WEIGHT


def test_actual_distance(runner):
    """The actual_distance property should return the actual distance run by the horse"""

    circ_distance = straight_distance = 0
    while circ_distance + straight_distance < runner.race['distance']:

        if runner.race['distance'] - circ_distance - straight_distance < runner.race['track_straight']:
            straight_distance += runner.race['distance'] - circ_distance - straight_distance
        else:
            straight_distance += runner.race['track_straight']

        if runner.race['distance'] - circ_distance - straight_distance < runner.race['track_circ']:
            circ_distance += runner.race['distance'] - circ_distance - straight_distance
        else:
            circ_distance += runner.race['track_circ']

    actual_distance = math.sqrt((circ_distance ** 2) + ((runner['barrier'] * BARRIER_WIDTH) ** 2)) + straight_distance

    assert runner.actual_distance == actual_distance


def test_actual_weight(runner):
    """The actual_weight property should return the average racehorse weight plus the listed weight less allowances for the runner"""

    assert runner.actual_weight == HORSE_WEIGHT + runner.carrying


def test_age(runner):
    """The age property should return the horse's age as at the date of the race"""

    assert runner.age == (runner.race.meet['date'] - runner.horse['foaled']).days / 365


def test_career(runner):
    """The career property should return a PerformanceList containing all performances for the horse prior to the current race date"""

    assert isinstance(runner.career, racing_data.PerformanceList)
    assert len(runner.career) == 6


def test_carrying(runner):
    """The carrying property should return the runner's listed weight less allowances"""

    assert runner.carrying == runner['weight'] - runner['jockey_claiming']


def test_horse(horse, runner):
    """The horse property should return the horse associated with the runner"""

    assert runner.horse['_id'] == horse['_id']


def test_jockey(jockey, runner):
    """The jockey property should return the jockey associated with the runner"""

    assert runner.jockey['_id'] == jockey['_id']


def test_race(race, runner):
    """The race property should return the race in which the runner competes"""

    assert runner.race['_id'] == race['_id']


def test_result(runner):
    """The result property should return the runner's final result if the race has already been run"""

    assert runner.result == 2


def test_str(runner):
    """str(runner) should return a human readable string representation of the runner"""

    assert str(runner) == 'runner #{number} in {race}'.format(number=runner['number'], race=runner.race)


def test_trainer(trainer, runner):
    """The trainer property should return the trainer associated with the runner"""

    assert runner.trainer['_id'] == trainer['_id']
