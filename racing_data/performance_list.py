class PerformanceList(list):
    """A performance list provides statistical analysis functionality for a list of performances"""
    
    @property
    def seconds(self):
        """Return the number of second placed performances in this list"""
        
        return self.count_results(2)

    @property
    def second_pct(self):
        """Return the percentage of second placed performances in this list"""
        
        return self.calculate_percentage(self.seconds)

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

        return self.calculate_percentage(self.wins)

    def calculate_percentage(self, numerator, denominator=None, divide_by_zero=None):
        """Return numerator / denominator, or divide_by_zero if denominator is 0"""

        if denominator is None:
            denominator = self.starts

        if denominator == 0:
            return divide_by_zero
        else:
            return numerator / denominator

    def count_results(self, result):
        """Count the number of performances with the specified result in this list"""

        return len([performance for performance in self if performance['result'] == result])
