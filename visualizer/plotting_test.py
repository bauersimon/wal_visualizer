import unittest

from visualizer.plotting import hit_ratio, response_time, sliding_window


class TestHitRatio(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(0.5, hit_ratio([0, 1, 0, 1]))

    def test_empty(self):
        self.assertEqual(1.0, hit_ratio([]))

    def test_threshold(self):
        self.assertEqual(0.75, hit_ratio([0, 1, 0, 2], hit_threshold=1.0))

    def test_negative_miss(self):
        self.assertEqual(0.75, hit_ratio([0, 1, 0, -1], hit_threshold=1.0))


class TestResponseTime(unittest.TestCase):

    def test_simple(self):
        m, d = response_time([0, 1, 0, 1, 2, 1, 0, 10])
        self.assertAlmostEqual(3.00, m, delta=0.01)
        self.assertAlmostEqual(3.52, d, delta=0.01)

    def test_empty(self):
        self.assertEqual((0.0, 0.0), response_time([]))

    def test_threshold(self):
        m, d = response_time([0, 1, 0, 1, 2, 1, 0, 10], hit_threshold=1.0)
        self.assertAlmostEqual(6.00, m, delta=0.01)
        self.assertAlmostEqual(4.00, d, delta=0.01)

    def test_negative_ignore(self):
        m, d = response_time(
            [-1, 0, 1, 0, 1, 2, 1, 0, 10, -1], hit_threshold=1.0)
        self.assertAlmostEqual(6.00, m, delta=0.01)
        self.assertAlmostEqual(4.00, d, delta=0.01)


class TestSlidingWindow(unittest.TestCase):

    def test_identity(self):
        def f(x): return x[0]
        a = sliding_window([0, 1, 2, 3], [1, 3, 5, 7], f, 0, window_size=1)
        self.assertEqual([1, 3, 5, 7], a)

    def test_identity_timesteps(self):
        def f(x): return x[0] if len(x) > 0 else 0
        a = sliding_window([0, 2, 3, 4], [1, 3, 5, 7], f, 0, window_size=1)
        self.assertEqual([1, 0, 3, 5, 7], a)

    def test_addition(self):
        def f(x): return sum(x)
        a = sliding_window([0, 1, 2, 3], [1, 3, 5, 7], f, 0, window_size=3)
        self.assertEqual([4, 9, 15, 12], a)

    def test_stride(self):
        def f(x): return sum(x)
        a = sliding_window([0, 1, 2, 3, 4], [1, 3, 5, 7, 11], f, 0, window_size=3, stride=2)
        self.assertEqual([4, 15, 18], a)

    def test_argument(self):
        def f(_, override=1):
            return override
        a = sliding_window([0, 1, 2, 3], [1, 3, 5, 7], f, 0, window_size=1, override=2)
        self.assertEqual([2, 2, 2, 2], a)


if __name__ == '__main__':
    unittest.main()
