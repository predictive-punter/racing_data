from . import Entity


class Meet(Entity):
    """A meet represents a collection of races occurring at a given track on a given date"""

    def __str__(self):

        return '{track} on {date:%Y-%m-%d}'.format(track=self['track'], date=self['date'].astimezone(self.provider.local_timezone))
    
    @property
    def has_expired(self):
        """Expire meets that were last updated prior to their actual date"""

        return self['updated_at'] < self['date'] or super(Meet, self).has_expired

    @property
    def races(self):
        """Return a list of races occurring at this meet"""

        return self.get_cached_property('races', self.provider.get_races_by_meet, self)

    def is_equivalent_to(self, other_meet):
        """This meet is equivalent to other_meet if both have the same date and track"""

        return self['date'] == other_meet['date'] and self['track'] == other_meet['track']
