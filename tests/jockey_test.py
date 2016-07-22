def test_performances(jockey, performances, provider):
    """The performances property should return the list of performances associated with the jockey"""

    property_ids = [performance['_id'] for performance in jockey.performances]
    provider_ids = [performance['_id'] for performance in provider.get_performances_by_jockey(jockey)]

    assert property_ids == provider_ids
