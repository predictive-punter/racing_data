class Meet(dict):
    """A meet represents a collection of races occurring at a given track on a given date"""
    
    def __init__(self, provider, *args, **kwargs):

        super(Meet, self).__init__(*args, **kwargs)

        self.provider = provider
