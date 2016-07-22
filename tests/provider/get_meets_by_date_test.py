import racing_data

from common import check_persistence, check_providers, check_timestamps, check_types, check_updates


def test_count(meets):
    """The get_meets_by_date method should return the expected number of meets"""

    assert len(meets) == 2


def test_persistence(date, provider):
    """Subsequent identical calls to get_meets_by_date should return the same Meet objects"""

    check_persistence(provider.get_meets_by_date, date)


def test_providers(meets, provider):
    """All Meet objects should contain a reference to the provider instance from which they were sourced"""

    check_providers(meets, provider)


def test_timestamps(meets):
    """All Meet objects should contain timezone aware created/updated at timestamps"""

    check_timestamps(meets)


def test_types(meets):
    """The get_meets_by_date method should return a list of Meet objects"""

    check_types(meets, list, racing_data.Meet)


def test_updates(future_date, provider):
    """Subsequent identical calls to get_meets_by_date with a future date should return the same Meet objects updated"""

    check_updates(provider.get_meets_by_date, future_date)
