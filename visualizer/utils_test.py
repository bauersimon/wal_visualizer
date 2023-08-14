import unittest

from visualizer.utils import compute_latency, merge_indices


class TestMergeIndices(unittest.TestCase):

    def test_simple(self):
        self.assertEqual([5], merge_indices([0, 2, 4, 5, 6, 8], [1, 3, 5, 7, 9]))


class TestLatency(unittest.TestCase):

    def test_empty(self):
        self.assertEqual([], compute_latency([], []))

    def test_simple(self):
        self.assertEqual([0, 1, 4], compute_latency([1, 3, 5], [1, 4, 9]))

    def test_no_responses_end(self):
        self.assertEqual([0, 1, -1, -1], compute_latency([1, 3, 7, 8], [1, 4]))

    def test_no_requests_end(self):
        self.assertEqual([0, 1], compute_latency([1, 3], [1, 4, 7, 9]))

    def test_no_response_middle(self):
        self.assertEqual([0, 1, -1, 1], compute_latency([1, 3, 7, 8], [1, 4, 9]))

    def test_duplicated_response(self):
        self.assertEqual([0, 1, 1], compute_latency([1, 3, 8], [1, 4, 7, 9]))

    def test_complex(self):
        self.assertEqual([0, 2, -1, 3, -1], compute_latency([1, 3, 8, 10, 15], [1, 2, 5, 13]))


if __name__ == '__main__':
    unittest.main()
