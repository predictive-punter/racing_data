class PerformanceList(list):
    """A performance list provides statistical analysis functionality for a list of performances"""
    
    @property
    def seconds(self):
        """Return the number of second placed performances in this list"""
        
        return self.count_results(2)

    @property
    def starts(self):
        """Return the number of starts in this performance list"""

        return len(self)

    @property
    def wins(self):
        """Return the number of winning performances in this list"""

        return self.count_results(1)

    @property
    def win_pct(self):
        """Return the percentage of winning performances in this list"""

        if self.starts > 0:
            return self.wins / self.starts

    def count_results(self, result):
        """Count the number of performances with the specified result in this list"""

        return len([performance for performance in self if performance['result'] == result])
