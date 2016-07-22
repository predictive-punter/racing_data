from . import Entity


class Horse(Entity):
    """A horse represents the equine component of a runner"""

    @property
    def performances(self):
        """Return a list of performances associated with this horse"""

        return self.get_cached_property('performances', self.provider.get_performances_by_horse, self)
