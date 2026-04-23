import unittest
from backend.lcg_service import LCGService

class TestCesaro(unittest.TestCase):

    def setUp(self):
        self.service = LCGService()

    def test_known_coprime_sequence(self):
        """Тест на послідовності, де всі пари взаємно прості (GCD=1)"""
        sequence = [2, 3, 5, 7]
        prob = self.service.cesaro_test(sequence)
        result = self.service.estimate_pi(prob)
        self.assertAlmostEqual(result, 2.4494897, places=6)

    def test_non_coprime_sequence(self):
        """Тест на послідовності, де немає взаємно простих пар"""
        sequence = [2, 4, 6, 8]
        prob = self.service.cesaro_test(sequence)
        result = self.service.estimate_pi(prob)
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()