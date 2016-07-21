from . import Meet


class Provider:
    """Provide managed access to racing data"""

    def __init__(self, scraper):

        self.scraper = scraper
    
    def get_meets_by_date(self, date):
        """Get a list of meets occurring on the specified date"""

        meets = [Meet(values) for values in self.scraper.scrape_meets(date)]
        return meets
