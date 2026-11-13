import unittest

from src.analysis import estimate, read_values


class AnalysisTests(unittest.TestCase):
    def test_known_mean(self):
        values = read_values(b"valor\n2\n4\n6\n8\n10\n")
        result = estimate(values, seed=42, resamples=1000)
        self.assertEqual(result["mean"], 7.0)
        self.assertEqual(result["n"], 5)
        self.assertLess(result["lower"], result["mean"])
        self.assertGreater(result["upper"], result["mean"])

    def test_constant_data(self):
        result = estimate([4, 4], seed=42, resamples=100)
        self.assertEqual(result, {"n": 2, "mean": 4, "lower": 4, "upper": 4})

    def test_same_seed_repeats_metrics(self):
        values = [2, 4, 6, 8, 10]
        self.assertEqual(estimate(values, 42, 1000), estimate(values, 42, 1000))

    def test_invalid_data(self):
        for data in (b"otra\n1\n2", b'valor\n""\n2', b"valor\nnan\n2",
                     b"valor\n11\n2", b"valor\n1,2\n3", b"valor\n1"):
            with self.subTest(data=data), self.assertRaises(ValueError):
                read_values(data)
