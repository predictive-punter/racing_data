import math

from . import Entity
from .constants import *


class Performance(Entity):
    """A performance represents the result of a completed run for a horse/jockey"""

    def __str__(self):

        return 'performance for {horse} at {track} on {date:%Y-%m-%d}'.format(horse=self.horse, track=self['track'], date=self['date'].astimezone(self.provider.local_timezone))

    @property
    def actual_distance(self):
        """Return the actual distance run by the horse in the winning time"""

        return math.sqrt((self['distance'] ** 2) + ((self['barrier'] * BARRIER_WIDTH) ** 2)) - (self['lengths'] * METRES_PER_LENGTH)

    @property
    def actual_weight(self):
        """Return the total combined weight of the horse and jockey"""

        return self['carried'] + HORSE_WEIGHT
    
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

    @property
    def profit(self):
        """Return the profit earned on a win bet for this performance"""

        profit = -1.00
        if self['result'] == 1:
            profit += self['starting_price']

        return profit

    @property
    def speed(self):
        """Return the average speed of the horse for this performance"""

        return self.actual_distance / self['winning_time']

    def is_equivalent_to(self, other_performance):
        """This performance is equivalent to other_performance if both have the same horse_url, track and date"""

        return self['date'] == other_performance['date'] and self['horse_url'] == other_performance['horse_url'] and self['track'] == other_performance['track']
