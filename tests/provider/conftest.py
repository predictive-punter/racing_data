from datetime import datetime, timedelta

import cache_requests
from lxml import html
import punters_client
import pymongo
import pytest
import racing_data
import redis
import requests
import tzlocal


@pytest.fixture(scope='session', params=[datetime(2016, 2, 1), tzlocal.get_localzone().localize(datetime(2016, 2, 1))])
def date(request):

    return request.param


@pytest.fixture(scope='session')
def future_date():

    return datetime.now() + timedelta(days=1)


@pytest.fixture(scope='session')
def future_meet(future_date, provider):

    return provider.get_meets_by_date(future_date)[0]


@pytest.fixture(scope='session')
def future_race(future_meet, provider):

    return provider.get_races_by_meet(future_meet)[0]


@pytest.fixture(scope='session')
def meets(date, provider):

    return provider.get_meets_by_date(date)


@pytest.fixture(scope='session')
def meet(meets):

    for meet in meets:
        if meet['track'] == 'Kilmore':
            return meet


@pytest.fixture(scope='session')
def races(meet, provider):

    return provider.get_races_by_meet(meet)


@pytest.fixture(scope='session')
def race(races):

    for race in races:
        if race['number'] == 5:
            return race


@pytest.fixture(scope='session')
def runners(race, provider):

    return provider.get_runners_by_race(race)


@pytest.fixture(scope='session')
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
