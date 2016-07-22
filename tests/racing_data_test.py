import racing_data


def test_version():
    """racing_data.__version__ should return the correct version string"""

    assert racing_data.__version__ == '1.0.0a1'
