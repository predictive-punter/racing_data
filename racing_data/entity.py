from datetime import datetime

import pytz


class Entity(dict):
    """Common functionality for racing entities"""
    
    def __init__(self, provider, *args, **kwargs):

        super(Entity, self).__init__(*args, **kwargs)

        self.provider = provider

        if not 'created_at' in self:
            self['created_at'] = self['updated_at'] = datetime.now(pytz.utc)

        for key in self:
            if isinstance(self[key], datetime):
                try:
                    self[key] = pytz.utc.localize(self[key])
                except ValueError:
                    pass

    @property
    def has_expired(self):
        """Expire entities sourced from an incompatible scraper version"""

        return not self.provider.scraper.is_compatible_with(self['scraper_version'])

    def is_equivalent_to(self, other_entity):
        """This entity is equivalent to other_entity if both are equal"""

        return self == other_entity
