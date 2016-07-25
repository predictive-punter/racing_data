import pytest
import racing_data


@pytest.fixture(scope='module')
def performance_list(performances):

    return racing_data.PerformanceList(performances)


def count_results(performances, result):
    """Count the number of performances with the specified result"""

    return len([performance for performance in performances if performance['result'] == result])


def test_seconds(performance_list, performances):
    """The seconds property should return the number of second placed performances in the list"""

    assert performance_list.seconds == count_results(performances, 2)


def test_second_pct(performance_list, performances):
    """The second_pct property should return the percentage of second placed performances in the list"""

    assert performance_list.second_pct == performance_list.seconds / performance_list.starts


def test_starts(performance_list, performances):
    """The starts property should return the number of performances in the list"""

    assert performance_list.starts == len(performances)


def test_thirds(performance_list, performances):
    """The thirds property should return the number of third placed performances in the list"""

    assert performance_list.thirds == count_results(performances, 3)


def test_third_pct(performance_list, performances):
    """The third_pct property should return the percentage of third placed performances in the list"""

    assert performance_list.third_pct == performance_list.thirds / performance_list.starts


def test_wins(performance_list, performances):
    """The wins property should return the number of winning performances in the list"""

    assert performance_list.wins == count_results(performances, 1)


def test_win_pct(performance_list, performances):
    """The win_pct property should return the percentage of winning performances in the list"""

    assert performance_list.win_pct == performance_list.wins / performance_list.starts
