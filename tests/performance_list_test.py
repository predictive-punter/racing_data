import pytest
import racing_data


@pytest.fixture(scope='module')
def performance_list(performances):

    return racing_data.PerformanceList(performances)


def count_results(performances, result):
    """Count the number of performances with the specified result"""

    return len([performance for performance in performances if performance['result'] == result])


def test_earnings(performance_list, performances):
    """The earnings property should return the total prize money for the performances in the list"""

    assert performance_list.earnings == sum([performance['prize_money'] for performance in performances])


def test_earnings_potential(performance_list, performances):
    """The earnings_potential property should return the earnings / the total prize pools for the performances in the list"""

    assert performance_list.earnings_potential == performance_list.earnings / sum([performance['prize_pool'] for performance in performances])


def test_fourths(performance_list, performances):
    """The fourths property should return the number of fourth placed performances in the list"""

    assert performance_list.fourths == count_results(performances, 4)


def test_fourth_pct(performance_list, performances):
    """The fourth_pct property should return the percentage of fourth placed performances in the list"""

    assert performance_list.fourth_pct == performance_list.fourths / performance_list.starts


def test_momentums(performance_list, performances):
    """The momentums property should return a tuple containing the minimum, maximum and average momentums for the performances in the list"""

    momentums = [performance.momentum for performance in performances]

    assert performance_list.momentums == (min(momentums), max(momentums), sum(momentums) / len(momentums))


def test_places(performance_list, performances):
    """The places property should return the number of first, second and third placed performances in the list"""

    assert performance_list.places == performance_list.wins + performance_list.seconds + performance_list.thirds


def test_place_pct(performance_list, performances):
    """The place_pct property should return the percentage of first, second and third placed performances in the list"""

    assert performance_list.place_pct == performance_list.places / performance_list.starts


def test_result_potential(performance_list, performances):
    """The result_potential property should return 1 - the sum of all results / the sum of all starters for the performances in the list"""

    results = [performance['result'] for performance in performances]
    starters = [performance['starters'] for performance in performances]

    assert performance_list.result_potential == 1.0 - (sum(results) / sum(starters))


def test_roi(performance_list, performances):
    """The roi property should return the total profits divided by number of starts for the performances in the list"""

    profits = [performance.profit for performance in performances]

    assert performance_list.roi == sum(profits) / performance_list.starts


def test_seconds(performance_list, performances):
    """The seconds property should return the number of second placed performances in the list"""

    assert performance_list.seconds == count_results(performances, 2)


def test_second_pct(performance_list, performances):
    """The second_pct property should return the percentage of second placed performances in the list"""

    assert performance_list.second_pct == performance_list.seconds / performance_list.starts


def test_starting_prices(performance_list, performances):
    """The starting_prices property should return a tuple of the minimum, maximum and average starting prices for the performances in the list"""

    starting_prices = [performance['starting_price'] for performance in performances if performance['starting_price'] is not None]

    assert performance_list.starting_prices == (min(starting_prices), max(starting_prices), sum(starting_prices) / len(starting_prices))


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
