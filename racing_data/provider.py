import pytz
import tzlocal

from . import Meet, Race, Runner


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
    
    def get_meets_by_date(self, date):
        """Get a list of meets occurring on the specified date"""

        try:
            date = self.local_timezone.localize(date)
        except ValueError:
            pass
        date = date.astimezone(self.scraper.SOURCE_TIMEZONE).replace(hour=0, minute=0, second=0, microsecond=0)
        date = date.astimezone(pytz.utc)

        return self.find_or_create(Meet, {'date': date}, None, self.scraper.scrape_meets, date)

    def get_races_by_meet(self, meet):
        """Get a list of races occurring at the specified meet"""

        return self.find_or_create(Race, {'meet_id': meet['_id']}, {'meet': meet}, self.scraper.scrape_races, meet)

    def get_race_by_runner(self, runner):
        """Get the race in which the specified runner competes"""

        return self.find_one(Race, {'_id': runner['race_id']}, None)

    def get_runners_by_race(self, race):
        """Get a list of runners competing in the specified race"""

        return self.find_or_create(Runner, {'race_id': race['_id']}, {'race': race}, self.scraper.scrape_runners, race)

    def save(self, entity):
        """Save the specified entity to the database"""

        collection = self.get_database_collection(entity.__class__)

        if '_id' in entity and entity['_id'] is not None:
            collection.replace_one({'_id': entity['_id']}, entity)
        else:
            entity['_id'] = collection.insert_one(entity).inserted_id
