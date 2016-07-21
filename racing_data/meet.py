from datetime import datetime

import pytz


class Meet(dict):
    """A meet represents a collection of races occurring at a given track on a given date"""
    
    def __init__(self, provider, *args, **kwargs):

        super(Meet, self).__init__(*args, **kwargs)

        self.provider = provider

        if not 'created_at' in self:
            self['created_at'] = self['updated_at'] = datetime.now(pytz.utc)
