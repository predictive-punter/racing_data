def test_performances(horse, performances):
    """The performances property should return the list of performances associated with the horse"""

    property_ids = [performance['_id'] for performance in horse.performances]
    provider_ids = [performance['_id'] for performance in performances]

    assert property_ids == provider_ids
