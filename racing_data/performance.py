from . import Entity


class Performance(Entity):
    """A performance represents the result of a completed run for a horse/jockey"""

    def __str__(self):

        return 'performance for {horse} at {track} on {date:%Y-%m-%d}'.format(horse=self.horse, track=self['track'], date=self['date'].astimezone(self.provider.local_timezone))
    
    @property
    def has_expired(self):
        """Expire runners that were last updated prior to the start time of the associated race"""

        return self['updated_at'] < self.horse['updated_at'] or super(Performance, self).has_expired

    @property
    def horse(self):
        """Return the horse associated with this performance"""

        return self.get_cached_property('horse', self.provider.get_horse_by_performance, self)

    @property
    def jockey(self):
        """Return the jockey associated with this performance"""

        return self.get_cached_property('jockey', self.provider.get_jockey_by_performance, self)

    def is_equivalent_to(self, other_performance):
        """This performance is equivalent to other_performance if both have the same horse_url, track and date"""

        return self['date'] == other_performance['date'] and self['horse_url'] == other_performance['horse_url'] and self['track'] == other_performance['track']
