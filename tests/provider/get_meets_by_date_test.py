from datetime import datetime

import cache_requests
from lxml import html
import punters_client
import pymongo
import pytest
import pytz
import racing_data
import redis
import requests
import tzlocal


@pytest.fixture(scope='module', params=[datetime(2016, 2, 1), tzlocal.get_localzone().localize(datetime(2016, 2, 1))])
def date(request):

    return request.param


@pytest.fixture(scope='module')
def meets(date, provider):

    return provider.get_meets_by_date(date)


@pytest.fixture(scope='module')
def provider():

    database_uri = 'mongodb://localhost:27017/racing_data_test'
    database_name = database_uri.split('/')[-1]
    database_client = pymongo.MongoClient(database_uri)
    database_client.drop_database(database_name)
    database = database_client.get_default_database()

    http_client = None
    try:
        http_client = cache_requests.Session(connection=redis.fromurl('redis://localhost:6379/racing_data_test'))
    except BaseException:
        try:
            http_client = cache_requests.Session()
        except BaseException:
            http_client = requests.Session()

    html_parser = html.fromstring

    scraper = punters_client.Scraper(http_client, html_parser)

    return racing_data.Provider(database, scraper)


def test_count(meets):
    """The get_meets_by_date method should return the expected number of meets"""

    assert len(meets) == 2


def test_persistence(date, meets, provider):
    """Subsequent identical calls to get_meets_by_date should return the same Meet objects"""

    old_ids = [meet['_id'] for meet in meets]
    new_ids = [meet['_id'] for meet in provider.get_meets_by_date(date)]

    assert old_ids == new_ids


def test_providers(meets, provider):
    """All Meet objects should contain a reference to the provider instance from which they were sourced"""

    for meet in meets:
        assert meet.provider == provider


def test_timestamps(meets):
    """All Meet objects should contain timezone aware created/updated at timestamps"""

    for meet in meets:
        for key in ('created_at', 'updated_at'):
            assert meet[key].tzinfo == pytz.utc


def test_types(meets):
    """The get_meets_by_date method should return a list of Meet objects"""

    assert isinstance(meets, list)
    for meet in meets:
        assert isinstance(meet, racing_data.Meet)
