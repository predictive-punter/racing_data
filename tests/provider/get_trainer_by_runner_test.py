import racing_data

from common import check_timestamps


def test_persistence(trainer, runner, provider):
    """Subsequent identical calls to get_trainer_by_runner should return the same Trainer object"""

    assert provider.get_trainer_by_runner(runner)['_id'] == trainer['_id']


def test_provider(trainer, provider):
    """All Trainer objects should contain a reference to the provider instance from which they were sourced"""

    assert trainer.provider == provider


def test_timestamps(trainer):
    """All Trainer objects should contain timezone aware created/updated at timestamps"""

    check_timestamps(trainer)


def test_types(trainer):
    """The get_trainer_by_runner method should return a Trainer object"""

    assert isinstance(trainer, racing_data.Trainer)


def test_updates(future_trainer, future_runner, provider):
    """Subsequent identical calls to get_trainer_by_runner with a future runner should return the same Trainer object updated"""

    new_trainer = provider.get_trainer_by_runner(future_runner)

    assert new_trainer['_id'] == future_trainer['_id']
    assert new_trainer['updated_at'] > future_trainer['updated_at']
