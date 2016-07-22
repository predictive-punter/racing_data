import racing_data

from common import check_timestamps


def test_persistence(horse, runner, provider):
    """Subsequent identical calls to get_horse_by_runner should return the same Horse object"""

    assert provider.get_horse_by_runner(runner)['_id'] == horse['_id']


def test_provider(horse, provider):
    """All Horse objects should contain a reference to the provider instance from which they were sourced"""

    assert horse.provider == provider


def test_timestamps(horse):
    """All Horse objects should contain timezone aware created/updated at timestamps"""

    check_timestamps(horse)


def test_types(horse):
    """The get_horse_by_runner method should return a Horse object"""

    assert isinstance(horse, racing_data.Horse)


def test_updates(future_horse, future_runner, provider):
    """Subsequent identical calls to get_horse_by_runner with a future runner should return the same Horse object updated"""

    new_horse = provider.get_horse_by_runner(future_runner)

    assert new_horse['_id'] == future_horse['_id']
    assert new_horse['updated_at'] > future_horse['updated_at']
