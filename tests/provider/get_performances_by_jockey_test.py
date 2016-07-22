def test_count(jockey, provider):
    """The get_performances_by_jockey method should return the expected number of performances"""

    assert len(provider.get_performances_by_jockey(jockey)) >= 1
