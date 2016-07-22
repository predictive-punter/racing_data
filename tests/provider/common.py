import pytz


def check_associations(collection, association):
    """All items in collection should contain a reference to the association's database ID"""

    for item in collection:
        assert item[association.__class__.__name__.lower() + '_id'] == association['_id']


def check_persistence(target, *target_args, **target_kwargs):
    """Subsequent identical calls to target should return the same objects"""

    old_ids = [entity['_id'] for entity in target(*target_args, **target_kwargs)]
    new_ids = [entity['_id'] for entity in target(*target_args, **target_kwargs)]

    assert old_ids == new_ids


def check_providers(collection, provider):
    """All items in collection should contain a reference to the provider instance from which they were sourced"""

    for item in collection:
        assert item.provider == provider


def check_timestamps(target):
    """All items in collection should contain timezone aware created/updated at timestamps"""

    if isinstance(target, list):

        for item in target:
            for key in ('created_at', 'updated_at'):
                assert item[key].tzinfo == pytz.utc

    else:

        for key in ('created_at', 'updated_at'):
            assert target[key].tzinfo == pytz.utc


def check_types(collection, collection_type, item_type):
    """Assert that the collection and all items within it are of the correct type"""

    assert isinstance(collection, collection_type)
    for item in collection:
        assert isinstance(item, item_type)


def check_updates(target, *target_args, **target_kwargs):
    """Subsequent identical calls to target should return the same objects updated"""

    old_items = target(*target_args, **target_kwargs)
    new_items = target(*target_args, **target_kwargs)

    for new_item in new_items:

        found_item = None
        for old_item in old_items:
            if old_item['_id'] == new_item['_id']:
                found_item = old_item
                break

        assert new_item['updated_at'] > found_item['updated_at']
