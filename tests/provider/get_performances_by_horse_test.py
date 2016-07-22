import racing_data

from common import check_persistence, check_providers, check_timestamps, check_types


def test_count(performances):
    """The get_performances_by_horse method should return the expected number of performances"""

    assert len(performances) >= 11


def test_persistence(horse, provider):
    """Subsequent identical calls to get_performances_by_horse should return the same Performance objects"""

    check_persistence(provider.get_performances_by_horse, horse)


def test_providers(performances, provider):
    """All Performance objects should contain a reference to the provider instance from which they were sourced"""

    check_providers(performances, provider)


def test_timestamps(performances):
    """All Performance objects should contain timezone aware created/updated at timestamps"""

    check_timestamps(performances)


def test_types(performances):
    """The get_performances_by_horse method should return a list of Performance objects"""

    check_types(performances, list, racing_data.Performance)


def test_updates(future_runner, provider):
    """Subsequent identical calls to get_performances_by_horse with a future horse should return the same Performance objects updated"""

    old_horse = provider.get_horse_by_runner(future_runner)
    old_performances = provider.get_performances_by_horse(old_horse)

    new_horse = provider.get_horse_by_runner(future_runner)
    new_performances = provider.get_performances_by_horse(new_horse)

    for new_performance in new_performances:

        found_performance = None
        for old_performance in old_performances:
            if old_performance['_id'] == new_performance['_id']:
                found_performance = old_performance
                break

        assert new_performance['updated_at'] > found_performance['updated_at']
