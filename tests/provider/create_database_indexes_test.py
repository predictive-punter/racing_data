import racing_data


def test_indexes(provider):
    """The provider should create all necessary database indexes during initialisation"""

    expected_indexes = {
        racing_data.Meet:           [
            [('date', 1)]
        ],
        racing_data.Race:           [
            [('meet_id', 1)]
        ],
        racing_data.Runner:         [
            [('race_id', 1)]
        ],
        racing_data.Horse:          [
            [('url', 1)]
        ],
        racing_data.Jockey:         [
            [('url', 1)]
        ],
        racing_data.Trainer:        [
            [('url', 1)]
        ],
        racing_data.Performance:    [
            [('horse_url', 1)],
            [('jockey_url', 1)]
        ]
    }

    for entity_type in expected_indexes:
        collection = provider.get_database_collection(entity_type)
        index_keys = [index['key'] for index in collection.index_information().values()]
        for expected_index in expected_indexes[entity_type]:
            assert expected_index in index_keys
