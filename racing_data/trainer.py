from . import Entity


class Trainer(Entity):
    """A trainer represents the person/people responsible for training a runner"""
    
    def __str__(self):

        return 'trainer {name}'.format(name=self['name'])
