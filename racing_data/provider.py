import pytz
import tzlocal

from . import Meet, Race, Runner, Horse, Jockey, Trainer, Performance


class Provider:
    """Provide managed access to racing data"""

    def __init__(self, database, scraper, local_timezone=tzlocal.get_localzone()):

        self.database = database
        self.scraper = scraper

        self.local_timezone = local_timezone

    def get_database_collection(self, entity_type):
        """Get the database collection for the specified entity type"""

        return self.database[entity_type.__name__.lower() + 's']

    def find(self, entity_type, query, property_cache):
        """Find entities of the specified type matching the specified query in the database"""

        collection = self.get_database_collection(entity_type)
        return [entity_type(self, property_cache, values) for values in collection.find(query)]

    def find_one(self, entity_type, query, property_cache):
        """Find a single entity of the specified type matching the specified query in the database"""

        collection = self.get_database_collection(entity_type)
        values = collection.find_one(query)
        if values is not None:
            return entity_type(self, property_cache, values)

    def find_or_create(self, entity_type, query, property_cache, create_method, *create_args, **create_kwargs):
        """Find or create entities of the specified type matching the specified query"""

        entities = self.find(entity_type, query, property_cache)

        must_create = len(entities) < 1
        for entity in entities:
            if entity.has_expired:
                must_create = True
                break

        if must_create:
            for created_entity in [entity_type(self, property_cache, values) for values in create_method(*create_args, **create_kwargs)]:

                for key in query:
                    created_entity[key] = query[key]

                found_entity = False

                for entity in entities:
                    if entity.is_equivalent_to(created_entity):

                        for key in created_entity:
                            if key != 'created_at':
                                entity[key] = created_entity[key]
                        self.save(entity)

                        found_entity = True
                        break

                if not found_entity:
                    self.save(created_entity)
                    entities.append(created_entity)

        return entities

    def find_or_create_one(self, entity_type, query, property_cache, expiry_date, create_method, *create_args, **create_kwargs):
        """Find or create a single entity of the specified type matching the specified query"""

        entity = self.find_one(entity_type, query, property_cache)
        if entity is None or (expiry_date is not None and entity['updated_at'] < expiry_date) or entity.has_expired:

            values = create_method(*create_args, **create_kwargs)
            if values is not None:

                for key in query:
                    values[key] = query[key]

                created_entity = entity_type(self, property_cache, values)

                if entity is None:
                    self.save(created_entity)
                    return created_entity

                else:

                    for key in created_entity:
                        if key != 'created_at':
                            entity[key] = created_entity[key]
                    self.save(entity)

        return entity
    
    def get_meets_by_date(self, date):
        """Get a list of meets occurring on the specified date"""

        try:
            date = self.local_timezone.localize(date)
        except ValueError:
            pass
        date = date.astimezone(self.scraper.SOURCE_TIMEZONE).replace(hour=0, minute=0, second=0, microsecond=0)
        date = date.astimezone(pytz.utc)

        return self.find_or_create(Meet, {'date': date}, None, self.scraper.scrape_meets, date)

    def get_meet_by_race(self, race):
        """Get the meet at which the specified race occurs"""

        return self.find_one(Meet, {'_id': race['meet_id']}, None)

    def get_races_by_meet(self, meet):
        """Get a list of races occurring at the specified meet"""

        return self.find_or_create(Race, {'meet_id': meet['_id']}, {'meet': meet}, self.scraper.scrape_races, meet)

    def get_race_by_runner(self, runner):
        """Get the race in which the specified runner competes"""

        return self.find_one(Race, {'_id': runner['race_id']}, None)

    def get_runners_by_race(self, race):
        """Get a list of runners competing in the specified race"""

        return self.find_or_create(Runner, {'race_id': race['_id']}, {'race': race}, self.scraper.scrape_runners, race)

    def get_horse_by_runner(self, runner):
        """Get the horse associated with the specified runner"""

        return self.find_or_create_one(Horse, {'url': runner['horse_url']}, None, runner.race['start_time'], self.scraper.scrape_horse, runner)

    def get_jockey_by_runner(self, runner):
        """Get the jockey associated with the specified runner"""

        return self.find_or_create_one(Jockey, {'url': runner['jockey_url']}, None, runner.race['start_time'], self.scraper.scrape_jockey, runner)

    def get_trainer_by_runner(self, runner):
        """Get the trainer associated with the specified runner"""

        return self.find_or_create_one(Trainer, {'url': runner['trainer_url']}, None, runner.race['start_time'], self.scraper.scrape_trainer, runner)

    def get_performances_by_horse(self, horse):
        """Get a list of performances for the specified horse"""

        return self.find_or_create(Performance, {'horse_url': horse['url']}, {'horse': horse}, self.scraper.scrape_performances, horse)

    def get_horse_by_performance(self, performance):
        """Get the horse associated with the specified performance"""

        return self.find_or_create_one(Horse, {'url': performance['horse_url']}, None, None, self.scraper.scrape_profile, performance['horse_url'])

    def get_performances_by_jockey(self, jockey):
        """Get a list of performances for the specified jockey"""

        return self.find(Performance, {'jockey_url': jockey['url']}, {'jockey': jockey})

    def get_jockey_by_performance(self, performance):
        """Get the jockey associated with the specified performance"""

        return self.find_or_create_one(Jockey, {'url': performance['jockey_url']}, None, None, self.scraper.scrape_profile, performance['jockey_url'])

    def save(self, entity):
        """Save the specified entity to the database"""

        collection = self.get_database_collection(entity.__class__)

        if '_id' in entity and entity['_id'] is not None:
            collection.replace_one({'_id': entity['_id']}, entity)
        else:
            entity['_id'] = collection.insert_one(entity).inserted_id
