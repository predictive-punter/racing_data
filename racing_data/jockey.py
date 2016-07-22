from . import Entity


class Jockey(Entity):
    """A jockey represents the person riding a runner"""
    
    @property
    def performances(self):
        """Return a list of performances associated with this jockey"""

        return self.get_cached_property('performances', self.provider.get_performances_by_jockey, self)
