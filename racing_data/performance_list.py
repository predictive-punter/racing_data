class PerformanceList(list):
    """A performance list provides statistical analysis functionality for a list of performances"""
    
    @property
    def starts(self):
        """Return the number of starts in this performance list"""

        return len(self)

    @property
    def wins(self):
        """Return the number of winning performances in this list"""

        return len([performance for performance in self if performance['result'] == 1])

    @property
    def win_pct(self):
        """Return the percentage of winning performances in this list"""

        if self.starts > 0:
            return self.wins / self.starts
