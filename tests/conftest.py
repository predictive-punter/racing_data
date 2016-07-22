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
def future_runner(future_race, provider):

    return provider.get_runners_by_race(future_race)[0]


@pytest.fixture(scope='session')
def future_horse(future_runner, provider):

    return provider.get_horse_by_runner(future_runner)


@pytest.fixture(scope='session')
def future_jockey(future_runner, provider):

    return provider.get_jockey_by_runner(future_runner)


@pytest.fixture(scope='session')
def future_trainer(future_runner, provider):

    return provider.get_trainer_by_runner(future_runner)


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
def runner(runners):

    for runner in runners:
        if runner['number'] == 1:
            return runner


@pytest.fixture(scope='session')
def horse(runner, provider):

    return provider.get_horse_by_runner(runner)


@pytest.fixture(scope='session')
def jockey(runner, provider):

    return provider.get_jockey_by_runner(runner)


@pytest.fixture(scope='session')
def trainer(runner, provider):

    return provider.get_trainer_by_runner(runner)


@pytest.fixture(scope='session')
def performances(horse, provider):

    return provider.get_performances_by_horse(horse)


@pytest.fixture(scope='session')
def performance(meet, performances):

    for performance in performances:
        if performance['date'] == meet['date'] and performance['track'] == meet['track']:
            return performance


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
