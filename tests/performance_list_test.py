import pytest
import racing_data


@pytest.fixture(scope='module')
def performance_list(performances):

    return racing_data.PerformanceList(performances)


def test_starts(performance_list, performances):
    """The starts property should return the number of performances in the list"""

    assert performance_list.starts == len(performances)


def test_wins(performance_list, performances):
    """The wins property should return the number of winning performances in the list"""

    assert performance_list.wins == len([performance for performance in performances if performance['result'] == 1])
