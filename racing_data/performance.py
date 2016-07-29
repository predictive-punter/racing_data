import math

from . import Entity
from .constants import BARRIER_WIDTH, HORSE_WEIGHT, METRES_PER_LENGTH


class Performance(Entity):
    """A performance represents the result of a completed run for a horse/jockey"""

    def __str__(self):

        return 'performance for {horse} at {track} on {date:%Y-%m-%d}'.format(horse=self.horse, track=self['track'], date=self['date'].astimezone(self.provider.local_timezone))

    @property
    def actual_distance(self):
        """Return the actual distance run by the horse in the winning time"""

        if self['distance'] is not None:
            return math.sqrt((self['distance'] ** 2) + ((self['barrier'] * BARRIER_WIDTH) ** 2)) - (self['lengths'] * METRES_PER_LENGTH)

    @property
    def actual_weight(self):
        """Return the total combined weight of the horse and jockey"""

        if self['carried'] is None:
            if self['weight'] is None:
                return HORSE_WEIGHT
            else:
                return self['weight'] + HORSE_WEIGHT
        else:
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
    def momentum(self):
        """Return the average momentum of the horse/jockey during this performance"""

        if self.speed is not None:
            return self.actual_weight * self.speed

    @property
    def previous_performance(self):
        """Return the previous performance for the horse"""

        def get_previous_performance():
            previous_performances = [performance for performance in self.horse.performances if performance['date'] < self['date']]
            if len(previous_performances) > 0:
                return sorted(previous_performances, key=lambda p: p['date'], reverse=True)[0]

        return self.get_cached_property('previous_performance', get_previous_performance)

    @property
    def profit(self):
        """Return the profit earned on a win bet for this performance"""

        profit = -1.00
        if self['result'] == 1:
            if self['starting_price'] is None:
                profit = 0.00
            else:
                profit += self['starting_price']

        return profit

    @property
    def speed(self):
        """Return the average speed of the horse/jockey for this performance"""

        if self.actual_distance is not None and self['winning_time'] is not None:
            return self.actual_distance / self['winning_time']

    @property
    def spell(self):
        """Return the number of days since the horse's previous performance"""

        if self.previous_performance is not None:
            return (self['date'] - self.previous_performance['date']).days

    @property
    def up(self):
        """Return the number of runs, including this one, since a spell of 90 days or more"""

        if self.spell is None or self.spell >= 90:
            return 1
        elif self.previous_performance is None:
            return 1
        else:
            return self.previous_performance.up + 1

    def is_equivalent_to(self, other_performance):
        """This performance is equivalent to other_performance if both have the same horse_url, track and date"""

        return self['date'] == other_performance['date'] and self['horse_url'] == other_performance['horse_url'] and self['track'] == other_performance['track']
