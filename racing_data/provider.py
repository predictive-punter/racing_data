import pytz
import tzlocal

from . import Meet


class Provider:
    """Provide managed access to racing data"""

    def __init__(self, database, scraper, local_timezone=tzlocal.get_localzone()):

        self.database = database
        self.scraper = scraper

        self.local_timezone = local_timezone

    def get_database_collection(self, entity_type):
        """Get the database collection for the specified entity type"""

        return self.database[entity_type.__name__.lower() + 's']
    
    def get_meets_by_date(self, date):
        """Get a list of meets occurring on the specified date"""

        try:
            date = self.local_timezone.localize(date)
        except ValueError:
            pass
        date = date.astimezone(self.scraper.SOURCE_TIMEZONE).replace(hour=0, minute=0, second=0, microsecond=0)
        date = date.astimezone(pytz.utc)

        meets = [Meet(self, values) for values in self.get_database_collection(Meet).find({'date': date})]

        must_create = len(meets) < 1
        for meet in meets:
            if meet['updated_at'] < meet['date']:
                must_create = True
                break

        if must_create:
            for created_meet in [Meet(self, values) for values in self.scraper.scrape_meets(date)]:

                found_meet = False

                for meet in meets:
                    if meet['date'] == created_meet['date'] and meet['track'] == created_meet['track']:
                        for key in created_meet:
                            if key != 'created_at':
                                meet[key] = created_meet[key]
                        self.save(meet)
                        found_meet = True
                        break

                if not found_meet:
                    self.save(created_meet)
                    meets.append(created_meet)

        return meets

    def save(self, entity):
        """Save the specified entity to the database"""

        collection = self.get_database_collection(entity.__class__)

        if '_id' in entity and entity['_id'] is not None:
            collection.replace_one({'_id': entity['_id']}, entity)
        else:
            entity['_id'] = collection.insert_one(entity).inserted_id
