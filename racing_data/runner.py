import math

from . import Entity
from .constants import *


class Runner(Entity):
    """A runner represents a single combination of horse, jockey and trainer competing in a race"""

    def __str__(self):

        return 'runner #{number} in {race}'.format(number=self['number'], race=self.race)

    @property
    def actual_distance(self):
        """Return the race distance adjusted for this runner's barrier and the race's track circ/straight values"""

        circ_distance = straight_distance = 0
        while circ_distance + straight_distance < self.race['distance']:

            if self.race['distance'] - circ_distance - straight_distance < self.race['track_straight']:
                straight_distance += self.race['distance'] - circ_distance - straight_distance
            else:
                straight_distance += self.race['track_straight']

            if self.race['distance'] - circ_distance - straight_distance < self.race['track_circ']:
                circ_distance += self.race['distance'] - circ_distance - straight_distance
            else:
                circ_distance += self.race['track_circ']

        return math.sqrt((circ_distance ** 2) + ((self['barrier'] * BARRIER_WIDTH) ** 2)) + straight_distance

    @property
    def actual_weight(self):
        """Return the average racehorse weight plus the listed weight less allowances for this runner"""

        return HORSE_WEIGHT + self.carrying

    @property
    def age(self):
        """Return the horse's age as at the date of the race"""

        if 'foaled' in self.horse:
            return (self.race.meet['date'] - self.horse['foaled']).days / 365

    @property
    def carrying(self):
        """Return this runner's listed weight less allowances"""

        return self['weight'] - self['jockey_claiming']

    @property
    def current_performance(self):
        """Return the performance associated with this runner if the race has already been run"""

        def get_current_performance():
            for performance in self.horse.performances:
                if performance['date'] == self.race.meet['date'] and performance['track'] == self.race.meet['track']:
                    return performance

        return self.get_cached_property('current_performance', get_current_performance)
    
    @property
    def has_expired(self):
        """Expire runners that were last updated prior to the start time of the associated race"""

        return self['updated_at'] < self.race['start_time'] or super(Runner, self).has_expired

    @property
    def horse(self):
        """Return the horse associated with this runner"""

        return self.get_cached_property('horse', self.provider.get_horse_by_runner, self)

    @property
    def jockey(self):
        """Return the jockey associated with this runner"""

        return self.get_cached_property('jockey', self.provider.get_jockey_by_runner, self)

    @property
    def race(self):
        """Return the race in which this runner is competing"""

        return self.get_cached_property('race', self.provider.get_race_by_runner, self)

    @property
    def result(self):
        """Return the final result for this runner if the race has already been run"""
        
        if self.current_performance is not None:
            return self.current_performance['result']

    @property
    def trainer(self):
        """Return the trainer associated with this runner"""

        return self.get_cached_property('trainer', self.provider.get_trainer_by_runner, self)

    def is_equivalent_to(self, other_runner):
        """This runner is equivalent to other_runner if both have the same race_id and number"""

        return self['race_id'] == other_runner['race_id'] and self['number'] == other_runner['number']
