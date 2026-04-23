import secrets
import math


class LCGService:
    def __init__(self, a=6364136223846793005, c=1, m=2 ** 64, seed=None):
        self.a = a
        self.c = c
        self.m = m
        self.state = seed if seed is not None else secrets.randbelow(self.m)

    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

    def generate(self, count):
        return [self.next() for _ in range(count)]

    def get_period(self, max_iter=1000000):
        first_val = self.state
        period = 0
        current = first_val

        for _ in range(max_iter):
            current = (self.a * current + self.c) % self.m
            period += 1
            if current == first_val:
                return period
        return period

    def cesaro_test(self, seq):
        count = 0
        pairs = 0
        for i in range(0, len(seq) - 1, 2):
            pairs += 1
            if math.gcd(seq[i], seq[i + 1]) == 1:
                count += 1
        return count / pairs if pairs > 0 else 0

    def estimate_pi(self, probability):
        if probability == 0:
            return 0
        return math.sqrt(6 / probability)

    def get_system_random_pi(self, count):
        seq = [secrets.randbelow(self.m + 1) for _ in range(count)]
        return self.estimate_pi(self.cesaro_test(seq))
