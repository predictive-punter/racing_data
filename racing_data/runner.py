from datetime import timedelta
import math

from . import Entity, PerformanceList
from .constants import ALTERNATIVE_TRACK_NAMES, BARRIER_WIDTH, HORSE_WEIGHT


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
    def at_distance(self):
        """Return a PerformanceList containing all prior performances for the horse within 100m of the current race distance"""

        def generate_at_distance():
            return PerformanceList([performance for performance in self.career if self.race['distance'] - 100 < performance['distance'] < self.race['distance'] + 100])

        return self.get_cached_property('at_distance', generate_at_distance)

    @property
    def at_distance_on_track(self):
        """Return a PerformanceList containing all prior performances for the horse within 100m of the current race distance and on the same track"""

        def generate_at_distance_on_track():
            return PerformanceList([performance for performance in self.at_distance if performance in self.on_track])

        return self.get_cached_property('at_distance_on_track', generate_at_distance_on_track)

    @property
    def at_up(self):
        """Return a PerformanceList containing all prior performances for the horse with the same UP number as the current run"""

        def generate_at_up():
            return PerformanceList([performance for performance in self.career if performance.up == self.up])

        return self.get_cached_property('at_up', generate_at_up)

    @property
    def career(self):
        """Return a PerformanceList containing all performances for the horse prior to the current race date"""

        def generate_career():
            return PerformanceList(sorted([performance for performance in self.horse.performances if performance['date'] < self.race.meet['date']], key=lambda p: p['date'], reverse=True))

        return self.get_cached_property('career', generate_career)

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
    def last_10(self):
        """Return a PerformanceList containing the last 10 prior performances for the horse"""

        def generate_last_10():
            performance_list = PerformanceList()
            for performance in self.career:
                if len(performance_list) < 10:
                    performance_list.append(performance)
                else:
                    break
            return performance_list

        return self.get_cached_property('last_10', generate_last_10)

    @property
    def last_12_months(self):
        """Return a PerformanceList containing all prior performances for the horse in the last 12 months"""

        def generate_last_12_months():
            return PerformanceList([performance for performance in self.career if performance['date'] >= self.race.meet['date'] - timedelta(days=365)])

        return self.get_cached_property('last_12_months', generate_last_12_months)

    @property
    def on_firm(self):
        """Return a PerformanceList containing all prior performances for the horse on FIRM tracks"""

        return self.get_cached_property('on_firm', self.get_performance_list_on_track_condition, 'FIRM')

    @property
    def on_good(self):
        """Return a PerformanceList containing all prior performances for the horse on GOOD tracks"""

        return self.get_cached_property('on_good', self.get_performance_list_on_track_condition, 'GOOD')

    @property
    def on_heavy(self):
        """Return a PerformanceList containing all prior performances for the horse on HEAVY tracks"""

        return self.get_cached_property('on_heavy', self.get_performance_list_on_track_condition, 'HEAVY')

    @property
    def on_soft(self):
        """Return a PerformanceList containing all prior performances for the horse on SOFT tracks"""

        return self.get_cached_property('on_soft', self.get_performance_list_on_track_condition, 'SOFT')

    @property
    def on_synthetic(self):
        """Return a PerformanceList containing all prior performances for the horse on SYNTHETIC tracks"""

        return self.get_cached_property('on_synthetic', self.get_performance_list_on_track_condition, 'SYNTHETIC')

    @property
    def on_track(self):
        """Return a PerformanceList containing all prior performances for the horse on the current track"""

        def get_track_names():
            for track_names in ALTERNATIVE_TRACK_NAMES:
                if self.race.meet['track'] in track_names:
                    return track_names
            return [self.race.meet['track']]

        def generate_on_track():
            return PerformanceList([performance for performance in self.career if performance['track'] in get_track_names()])

        return self.get_cached_property('on_track', generate_on_track)

    @property
    def on_turf(self):
        """Return a PerformanceList containing all prior performances for the horse on turf tracks"""

        def generate_on_turf():
            return PerformanceList([performance for performance in self.career if performance['track_condition'] is not None and 'SYNTHETIC' not in performance['track_condition']])

        return self.get_cached_property('on_turf', generate_on_turf)

    @property
    def previous_performance(self):
        """Return the previous performance for the horse"""

        if len(self.career) > 0:
            return self.career[0]

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
    def since_rest(self):
        """Return a PerformanceList containing all prior performances for the horse since its last spell of 90 days or more"""

        def generate_since_rest():
            performances = []
            if self.spell is not None and self.spell < 90:
                for performance in self.career:
                    performances.append(performance)
                    if performance.spell >= 90:
                        break
            return PerformanceList(performances)

        return self.get_cached_property('since_rest', generate_since_rest)

    @property
    def spell(self):
        """Return the number of days since the horse's last run"""

        if self.previous_performance is not None:
            return (self.race.meet['date'] - self.previous_performance['date']).days

    @property
    def starting_price(self):
        """Return the starting price for this runner if the race has already been run"""

        if self.current_performance is not None:
            return self.current_performance['starting_price']

    @property
    def trainer(self):
        """Return the trainer associated with this runner"""

        return self.get_cached_property('trainer', self.provider.get_trainer_by_runner, self)

    @property
    def up(self):
        """Return the number of races run by the horse, including this one, since its last spell of 90 days or more"""

        if self.spell >= 90:
            return 1
        else:
            if self.previous_performance is None:
                return 1
            else:
                return self.previous_performance.up + 1

    @property
    def with_jockey(self):
        """Return a PerformanceList containing all prior performances for the horse with the same jockey"""

        def generate_with_jockey():
            return PerformanceList([performance for performance in self.career if performance['jockey_url'] == self['jockey_url']])

        return self.get_cached_property('with_jockey', generate_with_jockey)

    def get_performance_list_on_track_condition(self, track_condition):
        """Return a PerformanceList containing all prior past performances for the horse on the specified track condition"""

        return PerformanceList([performance for performance in self.career if performance['track_condition'] is not None and track_condition.upper() in performance['track_condition']])

    def is_equivalent_to(self, other_runner):
        """This runner is equivalent to other_runner if both have the same race_id and number"""

        return self['race_id'] == other_runner['race_id'] and self['number'] == other_runner['number']
