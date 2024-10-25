import math


class FactorialMemoization(object):

    """
    Memoizes factorials of integers up to the n argument of init.
    Provides get method to retrieve memoized factorials.
    """

    def __init__(self, n):

        """
        Stores factorials of numbers from 0 to n in list.
        """

        self.factorials = []
        self.memoized_to = n
        prev = 1

        # 0! = 1 (yeah, really)
        self.factorials.append(1)

        # Multiplying by previous factorial is much more efficient
        # than calculating each factorial individually
        for i in range(1, n + 1):
            self.factorials.append(i * prev)
            prev = self.factorials[i]

    def get(self, n):

        """
        Return factorial from list or raise ValueError if outside memoized range.
        """

        if(n < 0 or n > self.memoized_to):
            raise ValueError("Factorial requested is outside of memoized range")
        else:
            return self.factorials[n]