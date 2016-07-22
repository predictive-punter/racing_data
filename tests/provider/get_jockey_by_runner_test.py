import racing_data

from common import check_timestamps


def test_persistence(jockey, runner, provider):
    """Subsequent identical calls to get_jockey_by_runner should return the same Jockey object"""

    assert provider.get_jockey_by_runner(runner)['_id'] == jockey['_id']


def test_provider(jockey, provider):
    """All Jockey objects should contain a reference to the provider instance from which they were sourced"""

    assert jockey.provider == provider


def test_timestamps(jockey):
    """All Jockey objects should contain timezone aware created/updated at timestamps"""

    check_timestamps(jockey)


def test_types(jockey):
    """The get_jockey_by_runner method should return a Jockey object"""

    assert isinstance(jockey, racing_data.Jockey)


def test_updates(future_jockey, future_runner, provider):
    """Subsequent identical calls to get_jockey_by_runner with a future runner should return the same Jockey object updated"""

    new_jockey = provider.get_jockey_by_runner(future_runner)

    assert new_jockey['_id'] == future_jockey['_id']
    assert new_jockey['updated_at'] > future_jockey['updated_at']
