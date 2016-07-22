===========
racing_data
===========


This project aims to provide horse racing data management and analysis services in Python.


.. image:: https://travis-ci.org/justjasongreen/racing_data.svg?branch=master
    :target: https://travis-ci.org/justjasongreen/racing_data
    :alt: Build Status
.. image:: https://coveralls.io/repos/github/justjasongreen/racing_data/badge.svg?branch=master
    :target: https://coveralls.io/github/justjasongreen/racing_data?branch=master
    :alt: Coverage Status
.. image:: https://landscape.io/github/justjasongreen/racing_data/master/landscape.svg?style=flat
    :target: https://landscape.io/github/justjasongreen/racing_data/master
    :alt: Code Health


************
Installation
************


Prior to using racing_data, the package must be installed in your current Python environment. In most cases, an automated installation via PyPI and pip will suffice, as follows::

    pip install racing_data

If you would prefer to gain access to new (unstable) features via a pre-release version of the package, specify the 'pre' option when calling pip, as follows::

    pip install --pre racing_data

To gain access to bleeding edge developments, the package can be installed from a source distribution. To do so, you will need to clone the git repository and execute the setup.py script from the root directory of the source tree, as follows::

    git clone https://github.com/justjasongreen/racing_data.git
    cd racing_data
    python setup.py install

If you would prefer to install the package as a symlink to the source distribution (for development purposes), execute the setup.py script with the 'develop' option instead, as follows::

    python setup.py develop


***********
Basic Usage
***********


To access the functionality described below, you must first create an instance of the racing_data.Provider class. To do so, you will need to provide a compatible web scraper and a database connection. The web scraper can be any object that implements the punters_client.Scraper API, support calls such as the following::

    meets = scraper.scrape_meets(date)
    races = scraper.scrape_races(meet)
    runners = scraper.scrape_runners(race)
    horse = scraper.scrape_horse(runner)
    jockey = scraper.scrape_jockey(runner)
    trainer = scraper.scrape_trainer(runner)
    performances = scraper.scrape_performances(horse)

The database connection can be any object that implements the pymongo.Database API, supporting calls such as the following::

    documents = database[collection_name].find(query)
    document['_id'] = database[collection_name].insert_one(document).inserted_id
    database[collection_name].replace_one({'_id': document['_id']}, document)

racing_data has only been tested with punters_client.Scraper as the web scraper and pymongo.Database as the database connection. To set up the required dependencies in your own project using the same packages, execute the following code in your Python interpreter::

    >>> import pymongo
    >>> database_uri = 'mongodb://localhost:27017/racing_data'
    >>> database_client = pymongo.MongoClient(database_uri)
    >>> database = database_client.get_default_database()
    >>> import cache_requests
    >>> http_client = cache_requests.Session()
    >>> from lxml import html
    >>> html_parser = html.fromstring
    >>> import punters_client
    >>> scraper = punters_client.Scraper(http_client, html_parser)

With these dependencies in place, you can now create an instance of the racing_data.Provider class as follows::

    >>> import racing_data
    >>> provider = racing_data.Provider(database, scraper)

The provider instance can now be used to scrape, store and access a range of racing data, as illustrated in the following sections...


Getting Meets
=============

Meets represent a collection of races occurring at a given track on a given date. To get a list of meets occurring on a given date, execute the following code in your Python interpreter::

    >>> from datetime import datetime
    >>> date = datetime(2016, 2, 1)
    >>> meets = provider.get_meets_by_date(date)

The get_meets_by_date method will return a list of Meet objects. Meet objects are derived from Python's built-in dict type, so a meet's details can be accessed as follows::

    >>> meet = meets[index]
    >>> track = meet['track']


Getting Races
=============

Races represent a collection of runners competing in a single event at a meet. To get a list of races occurring at a given meet, execute the following code in your Python interpreter (where meet is an existing Meet object obtained via the provider.get_meets_by_date method)::

    >>> races = meet.races

The meet.races property will return a list of Race objects. Race objects are derived from Python's built-in dict type, so a race's details can be accessed as follows::

    >>> race = races[index]
    >>> number = race['number']

In addition to the dictionary values, Race objects also provide a 'meet' property that can be used to get the meet at which the race occurs::

    >>> meet = race.meet


Getting Runners
===============

Runners represent a single combination of horse, jockey and trainer competing in a race. To get a list of runners competing in a given race, execute the following code in your Python interpreter (where race is an existing Race object obtained via the Meet.races property)::

    >>> runners = race.runners

The race.runners property will return a list of Runner objects. Runner objects are derived from Python's built-in dict type, so a runner's details can be accessed as follows::

    >>> runner = runners[index]
    >>> number = runner['number']

In addition to the dictionary values, Runner objects also provide a 'race' property that can be used to get the race in which the runner occurs::

    >>> race = runner.race


Getting Horses, Jockeys and Trainers
====================================

To get the horse, jockey or trainer associated with a given runner, execute the following code in your Python interpreter (where runner is an existing Runner object obtained via the Race.runners property)::

    >>> horse = runner.horse
    >>> jockey = runner.jockey
    >>> trainer = runner.trainer

The runner.horse, runner.jockey and runner.trainer properties will return Horse, Jockey and Trainer objects respectively. Horse, Jockey and Trainer objects are derived from Python's built-in dict type, so a horse/jockey/trainer's details can be accessed as follows::

    >>> name = horse['name']
    >>> name = jockey['name']
    >>> name = trainer['name']


Getting Performances
====================

Performances represent the results of completed runs by horses and jockeys. To get a list of performances for a given horse, execute the following code in your Python interpreter (where horse is an existing Horse object obtained via the Runner.horse property)::

    >>> performances = horse.performances

The horse.performances property will return a list of Performance objects. Performance objects are derived from Python's built-in dict type, so a performance's details can be accessed as follows::

    >>> performance = performances[index]
    >>> result = performance['result']

In addition to the dictionary values, Performance objects also provide 'horse' and 'jockey' properties that can be used to get the horse/jockey associated with the performance::

    >>> horse = performance.horse
    >>> jockey = performance.jockey

NOTE: Jockey objects also provide a 'performances' property that can be used to access a list of performances associated with that jockey. Unlike the Horse.performances property though, the Jockey.performances property will not scrape the web in search of relevant data. Instead, the Jockey.performances property will only return relevant performances that already exist in the database. This is due to the vast number of past performances associated with any given jockey, and the inherent difficulty in scraping such a vast amount of data in a timely fashion from most data providers.


***********************
Development and Testing
***********************


The source distribution includes a test suite based on pytest. To ensure compatibility with all supported versions of Python, it is recommended that the test suite be run via tox.

To install all development and test requirements into your current Python environment, execute the following command from the root directory of the source tree::

    pip install -e .[dev,test]

To run the test suite included in the source distribution, execute the tox command from the root directory of the source tree as follows::

    tox
