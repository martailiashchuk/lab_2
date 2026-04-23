import math
import random

class LCGService:
    def __init__(self):
        self.m = 2**18 - 1
        self.a = 5**3
        self.c = 34
        self.x0 = 512

    def generate(self, count):
        sequence = []
        x = self.x0
        for _ in range(count):
            x = (self.a * x + self.c) % self.m
            sequence.append(x)
        return sequence

    def get_gcd(self, a, b):
        a, b = abs(a), abs(b)
        while b:
            a, b = b, a % b
        return a

    def cesaro_test(self, sequence):
        if len(sequence) < 2: return 0
        pairs_count = len(sequence) // 2
        coprime_count = 0
        for i in range(pairs_count):
            if self.get_gcd(sequence[i * 2], sequence[i * 2 + 1]) == 1:
                coprime_count += 1
        return coprime_count / pairs_count if pairs_count > 0 else 0

    def estimate_pi(self, probability):
        if probability <= 0: return 0
        return (6 / probability) ** 0.5

    def calculate_period(self):
        first_val = (self.a * self.x0 + self.c) % self.m
        current = first_val
        period = 1
        for _ in range(self.m + 1):
            current = (self.a * current + self.c) % self.m
            if current == first_val: return period
            period += 1
        return period

    def get_system_random_pi(self, count):
        seq = [random.randint(0, self.m) for _ in range(count)]
        return self.estimate_pi(self.cesaro_test(seq))