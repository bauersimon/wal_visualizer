import unittest

from visualizer.utils import compute_latency, merge_indices


class TestMergeIndices(unittest.TestCase):

    def test_simple(self):
        self.assertEqual([5], merge_indices([0, 2, 4, 5, 6, 8], [1, 3, 5, 7, 9]))


class TestLatency(unittest.TestCase):

    def test_empty(self):
        self.assertEqual([], compute_latency([], []))

    def test_simple(self):
        self.assertEqual([1, 2, 4], compute_latency([1, 3, 5], [2, 5, 9]))

    def test_no_responses_end(self):
        self.assertEqual([1, 1, -1, -1], compute_latency([1, 3, 7, 8], [2, 4]))

    def test_no_requests_end(self):
        self.assertEqual([1, 1], compute_latency([1, 3], [2, 4, 7, 9]))

    def test_no_response_middle(self):
        self.assertEqual([1, 1, -1, 1], compute_latency([1, 3, 7, 8], [2, 4, 9]))

    def test_duplicated_response(self):
        self.assertEqual([1, 1, 1], compute_latency([1, 3, 8], [2, 4, 7, 9]))

    def test_complex(self):
        self.assertEqual([1, 2, -1, 3, -1], compute_latency([1, 3, 8, 10, 15], [1, 2, 5, 13]))

    def test_increased_shortest_path(self):
        self.assertEqual([-1, 2, -1, 3, -1], compute_latency([1, 3, 8, 10, 15], [1, 2, 5, 13], shortest_path=2))


if __name__ == '__main__':
    unittest.main()
