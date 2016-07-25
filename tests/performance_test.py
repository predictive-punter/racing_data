import math

import tzlocal

from racing_data.constants import BARRIER_WIDTH, HORSE_WEIGHT, METRES_PER_LENGTH


def test_actual_distance(performance):
    """The actual_distance property should return the actual distance run by the horse in the winning time"""

    expected_value = math.sqrt((performance['distance'] ** 2) + ((performance['barrier'] * BARRIER_WIDTH) ** 2)) - (performance['lengths'] * METRES_PER_LENGTH)

    assert performance.actual_distance == expected_value


def test_actual_weight(performance):
    """The actual_weight property should return the total weight of the horse and jockey"""

    expected_value = performance['carried'] + HORSE_WEIGHT

    assert performance.actual_weight == expected_value


def test_horse(performance, horse):
    """The horse property should return the horse associated with the performance"""

    assert performance.horse['_id'] == horse['_id']


def test_jockey(performance, jockey):
    """The jockey property should return the jockey associated with the performance"""

    assert performance.jockey['_id'] == jockey['_id']


def test_momentum(performance):
    """The momentum property should return the average momentum for the horse/jockey during the performance"""

    expected_value = performance.actual_weight * performance.speed

    assert performance.momentum == expected_value


def test_profit(performance):
    """The profit property should return the profit earned on a win bet for the performance"""

    expected_value = -1.0
    if performance['result'] == 1:
        expected_value += performance['starting_price']

    assert performance.profit == expected_value


def test_speed(performance):
    """The speed property should returned the average speed of the horse/jockey during the performance"""

    expected_value = performance.actual_distance / performance['winning_time']

    assert performance.speed == expected_value


def test_spell(performance):
    """The spell property should return the number of days since the horse's previous performance"""

    assert performance.spell == 11


def test_str(performance):
    """str(performance) should return a human readable string representation of the performance"""

    assert str(performance) == 'performance for {horse} at {track} on {date:%Y-%m-%d}'.format(horse=performance.horse, track=performance['track'], date=performance['date'].astimezone(tzlocal.get_localzone()))


def test_up(performance):
    """The up property should return the number of runs for the horse, including this one, since a spell of 90 days or more"""

    assert performance.up == 3
