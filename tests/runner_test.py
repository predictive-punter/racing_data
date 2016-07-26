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


def test_at_distance(runner):
    """The at_distance property should return a PerformanceList containing all prior performances within 100m of the current race"""

    assert isinstance(runner.at_distance, racing_data.PerformanceList)
    assert len(runner.at_distance) == 3


def test_at_distance_on_track(runner):
    """The at_distance_on_track property should return a PerformanceList containing all prior performances for the horse on the same track and within 100m of the current race"""

    assert isinstance(runner.at_distance_on_track, racing_data.PerformanceList)
    assert len(runner.at_distance_on_track) == 0


def test_at_up(runner):
    """The at_up property should return a PerformanceList containing all prior performances with the same UP number as the current run"""

    assert isinstance(runner.at_up, racing_data.PerformanceList)
    assert len(runner.at_up) == 1


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


def test_last_10(runner):
    """The last_10 property should return a PerformanceList containing the last 10 prior performances for the horse"""

    assert isinstance(runner.last_10, racing_data.PerformanceList)
    assert len(runner.last_10) == 6


def test_last_12_months(runner):
    """The last_12_months property should return a PerformanceList containing all prior performances for the horse in the last 12 months"""

    assert isinstance(runner.last_12_months, racing_data.PerformanceList)
    assert len(runner.last_12_months) == 6


def test_on_firm(runner):
    """The on_firm property should return a PerformanceList containing all prior performances for the horse on FIRM tracks"""

    assert isinstance(runner.on_firm, racing_data.PerformanceList)
    assert len(runner.on_firm) == 0


def test_on_good(runner):
    """The on_good property should return a PerformanceList containing all prior performances for the horse on GOOD tracks"""

    assert isinstance(runner.on_good, racing_data.PerformanceList)
    assert len(runner.on_good) == 4


def test_on_heavy(runner):
    """The on_heavy property should return a PerformanceList containing all prior performances for the horse on HEAVY tracks"""

    assert isinstance(runner.on_heavy, racing_data.PerformanceList)
    assert len(runner.on_heavy) == 1


def test_on_soft(runner):
    """The on_soft property should return a PerformanceList containing all prior performances for the horse on SOFT tracks"""

    assert isinstance(runner.on_soft, racing_data.PerformanceList)
    assert len(runner.on_soft) == 1


def test_on_synthetic(runner):
    """The on_synthetic property should return a PerformanceList containing all prior performances for the horse on SYNTHETIC tracks"""

    assert isinstance(runner.on_synthetic, racing_data.PerformanceList)
    assert len(runner.on_synthetic) == 0


def test_on_track(runner):
    """The on_track property should return a PerformanceList containing all prior performances for the horse on the current track"""

    assert isinstance(runner.on_track, racing_data.PerformanceList)
    assert len(runner.on_track) == 0


def test_on_turf(runner):
    """The on_turf property should return a PerformanceList containing all prior performances for the horse on turf tracks"""

    assert isinstance(runner.on_track, racing_data.PerformanceList)
    assert len(runner.on_turf) == 6


def test_race(race, runner):
    """The race property should return the race in which the runner competes"""

    assert runner.race['_id'] == race['_id']


def test_result(runner):
    """The result property should return the runner's final result if the race has already been run"""

    assert runner.result == 2


def test_since_rest(runner):
    """The since_rest property should return a PerformanceList containing all prior performances for the horse since its last spell of 90 days or more"""

    assert isinstance(runner.since_rest, racing_data.PerformanceList)
    assert len(runner.since_rest) == 2


def test_spell(runner):
    """The spell property should return the number of days since the horse's previous race"""

    assert runner.spell == 11


def test_starting_price(runner):
    """The starting_price property should return the runner's starting price if the race has already been run"""

    assert runner.starting_price == 4.00


def test_str(runner):
    """str(runner) should return a human readable string representation of the runner"""

    assert str(runner) == 'runner #{number} in {race}'.format(number=runner['number'], race=runner.race)


def test_trainer(trainer, runner):
    """The trainer property should return the trainer associated with the runner"""

    assert runner.trainer['_id'] == trainer['_id']


def test_up(runner):
    """The up property should return the number of races run by the horse, including this one, since its last spell of 90 days or more"""

    assert runner.up == 3


def test_with_jockey(runner):
    """The with_jockey property should return a PerformanceList containing all prior performances for the horse with the same jockey"""

    assert isinstance(runner.with_jockey, racing_data.PerformanceList)
    assert len(runner.with_jockey) == 1
