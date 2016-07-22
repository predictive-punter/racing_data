from . import Entity


class Race(Entity):
    """A race represents a collection of runners competing in a single event at a meet"""
    
    @property
    def has_expired(self):
        """Expire races that were last updated prior to their start time"""

        return self['updated_at'] < self['start_time'] or super(Race, self).has_expired

    def is_equivalent_to(self, other_race):
        """This race is equivalent to other_race if both have the same meet_id and number"""

        return self['meet_id'] == other_race['meet_id'] and self['number'] == other_race['number']
