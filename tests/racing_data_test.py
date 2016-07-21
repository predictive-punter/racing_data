import racing_data
import setuptools_scm


def test_version():
    """racing_data.__version__ should return the correct version string"""

    assert racing_data.__version__ == setuptools_scm.get_version()
