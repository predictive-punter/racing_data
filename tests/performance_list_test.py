import pytest
import racing_data


@pytest.fixture(scope='module')
def performance_list(performances):

    return racing_data.PerformanceList(performances)


def test_starts(performance_list, performances):
    """The starts property should return the number of performances in the list"""

    assert performance_list.starts == len(performances)
