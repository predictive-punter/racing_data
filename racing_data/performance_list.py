class PerformanceList(list):
    """A performance list provides statistical analysis functionality for a list of performances"""

    @property
    def earnings(self):
        """Return the total prize money for the performances in this list"""

        prize_monies = [performance['prize_money'] for performance in self if performance['prize_money'] is not None]
        if len(prize_monies) > 0:
            return sum(prize_monies)
        else:
            return 0.00

    @property
    def earnings_potential(self):
        """Return the total prize money as a percentage of the total prize pools for the performances in this list"""

        prize_pools = [performance['prize_pool'] for performance in self if performance['prize_pool'] is not None]
        if len(prize_pools) > 0:
            return self.calculate_percentage(self.earnings, sum(prize_pools))

    @property
    def fourths(self):
        """Return the number of fourth placed performances in this list"""

        return self.count_results(4)

    @property
    def fourth_pct(self):
        """Return the percentage of fourth placed performances in this list"""

        return self.calculate_percentage(self.fourths)

    @property
    def momentums(self):
        """Return a tuple containing the minimum, maximum and average momentums for the performances in this list"""

        momentums = [performance.momentum for performance in self if performance.momentum is not None]

        return (min(momentums), max(momentums), sum(momentums) / len(momentums)) if len(momentums) > 0 else (None, None, None)

    @property
    def places(self):
        """Return the number of first, second and third placed performances in this list"""

        return self.wins + self.seconds + self.thirds

    @property
    def place_pct(self):
        """Return the percentage of first, second and third placed performances in this list"""

        return self.calculate_percentage(self.places)

    @property
    def result_potential(self):
        """Return 1 - the sum of all results / the sum of all starters for the performances in this list"""

        results = [performance['result'] for performance in self if performance['result'] is not None]
        if len(results) > 0:

            starters = [performance['starters'] for performance in self if performance['starters'] is not None]
            if len(starters) > 0:

                pct = self.calculate_percentage(sum(results), sum(starters))
                if pct is not None:

                    return 1.0 - pct

    @property
    def roi(self):
        """Return the total profits divided by the number of starts in this list"""

        profits = [performance.profit for performance in self]

        if len(profits) > 0:
            return self.calculate_percentage(sum(profits))

    @property
    def seconds(self):
        """Return the number of second placed performances in this list"""

        return self.count_results(2)

    @property
    def second_pct(self):
        """Return the percentage of second placed performances in this list"""

        return self.calculate_percentage(self.seconds)

    @property
    def starting_prices(self):
        """Return a tuple containing the minimum, maximum and average starting prices for the performances in this list"""

        starting_prices = [performance['starting_price'] for performance in self if performance['starting_price'] is not None]

        return (min(starting_prices), max(starting_prices), sum(starting_prices) / len(starting_prices)) if len(starting_prices) > 0 else (None, None, None)

    @property
    def starts(self):
        """Return the number of starts in this performance list"""

        return len(self)

    @property
    def thirds(self):
        """Return the number of third placed performances in this list"""

        return self.count_results(3)

    @property
    def third_pct(self):
        """Return the percentage of third placed performances in this list"""

        return self.calculate_percentage(self.thirds)

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
