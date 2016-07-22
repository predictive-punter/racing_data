import racing_data

from common import check_associations, check_persistence, check_providers, check_timestamps, check_types, check_updates


def test_count(runners):
    """The get_runners_by_race method should return the expected number of runners"""

    assert len(runners) == 10


def test_race_ids(race, runners):
    """All Runner objects should contain a reference to the associated race's database ID"""

    check_associations(runners, race)


def test_persistence(race, provider):
    """Subsequent identical calls to get_runners_by_race should return the same Runner objects"""

    check_persistence(provider.get_runners_by_race, race)


def test_providers(runners, provider):
    """All Runner objects should contain a reference to the provider instance from which they were sourced"""

    check_providers(runners, provider)


def test_timestamps(runners):
    """All Runner objects should contain timezone aware created/updated at timestamps"""

    check_timestamps(runners)


def test_types(runners):
    """The get_runners_by_race method should return a list of Runner objects"""

    check_types(runners, list, racing_data.Runner)


def test_updates(future_race, provider):
    """Subsequent identical calls to get_runners_by_race with a future race should return the same Runner objects updated"""

    check_updates(provider.get_runners_by_race, future_race)
