import racing_data

from common import check_associations, check_persistence, check_providers, check_timestamps, check_types, check_updates


def test_count(races):
    """The get_races_by_meet method should return the expected number of races"""

    assert len(races) == 8


def test_meet_ids(meet, races):
    """All Race objects should contain a reference to the associated meet's database ID"""

    check_associations(races, meet)


def test_persistence(meet, provider):
    """Subsequent identical calls to get_races_by_meet should return the same Race objects"""

    check_persistence(provider.get_races_by_meet, meet)


def test_providers(races, provider):
    """All Race objects should contain a reference to the provider instance from which they were sourced"""

    check_providers(races, provider)


def test_timestamps(races):
    """All Race objects should contain timezone aware created/updated at timestamps"""

    check_timestamps(races)


def test_types(races):
    """The get_races_by_meet method should return a list of Race objects"""

    check_types(races, list, racing_data.Race)


def test_updates(future_meet, provider):
    """Subsequent identical calls to get_races_by_meet with a future meet should return the same Race objects updated"""

    check_updates(provider.get_races_by_meet, future_meet)
