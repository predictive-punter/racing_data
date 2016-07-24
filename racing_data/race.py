from . import Entity


class Race(Entity):
    """A race represents a collection of runners competing in a single event at a meet"""

    def __str__(self):

        return 'race {number} at {meet}'.format(number=self['number'], meet=self.meet)
    
    @property
    def has_expired(self):
        """Expire races that were last updated prior to their start time"""

        return self['updated_at'] < self['start_time'] or super(Race, self).has_expired

    @property
    def meet(self):
        """Return the meet at which this race occurs"""

        return self.get_cached_property('meet', self.provider.get_meet_by_race, self)

    @property
    def runners(self):
        """Return a list of runners competing in this race"""

        return self.get_cached_property('runners', self.provider.get_runners_by_race, self)

    def is_equivalent_to(self, other_race):
        """This race is equivalent to other_race if both have the same meet_id and number"""

        return self['meet_id'] == other_race['meet_id'] and self['number'] == other_race['number']
