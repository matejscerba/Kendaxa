#!/usr/bin/python3

import unittest

from main import Graph
from main import NONE, RED, BLUE

class AlgorithmTest(unittest.TestCase):

    def test_read_neighbors(self):
        graph = Graph('data_cases/case_01.in')
        neighbors = [
            set([]),
            set([2]),
            set([1, 3, 4]),
            set([2]),
            set([2, 5]),
            set([7, 6, 4]),
            set([5]),
            set([5])
        ]
        self.assertListEqual(graph.neighbors, neighbors)

    def test_read_colors(self):
        graph = Graph('data_cases/case_01.in')
        colors = [NONE, RED, NONE, RED, NONE, NONE, BLUE, BLUE]
        self.assertListEqual(graph.colors, colors)

    def test_get_leaves(self):
        graph = Graph('data_cases/case_01.in')
        leaves = set([1, 3, 6, 7])
        self.assertSetEqual(graph._get_leaves(), leaves)

        graph = Graph('data_cases/case_03.in')
        leaves = set([1, 2, 7, 8, 11, 12, 16, 17, 18])
        self.assertSetEqual(graph._get_leaves(), leaves)

    def test_remove_node(self):
        graph = Graph('data_cases/case_01.in')
        graph._remove_node(1)
        vertices = set([2, 3, 4, 5, 6, 7])
        leaves = set([3, 6, 7])
        neighbors = set([3, 4])
        self.assertSetEqual(graph.nodes, vertices)
        self.assertSetEqual(graph.leaves, leaves)
        self.assertSetEqual(graph.neighbors[2], neighbors)

        graph._remove_node(3)
        vertices = set([2, 4, 5, 6, 7])
        leaves = set([2, 6, 7])
        neighbors = set([4])
        self.assertSetEqual(graph.nodes, vertices)
        self.assertSetEqual(graph.leaves, leaves)
        self.assertSetEqual(graph.neighbors[2], neighbors)

        graph._remove_node(5)
        vertices = set([2, 4, 6, 7])
        leaves = set([2, 4, 6, 7])
        neighbors = [
            set([2]),
            set(),
            set()
            ]
        self.assertSetEqual(graph.nodes, vertices)
        self.assertSetEqual(graph.leaves, leaves)
        self.assertListEqual([graph.neighbors[4], graph.neighbors[6], graph.neighbors[7]], neighbors)

    def test_cases(self):
        for i in range(1, 11):
            file = "data_cases/case_{:02d}.in".format(i)
            graph = Graph(file)
            with open("data_cases/case_{:02d}.out".format(i), "r") as f:
                line = f.readline().strip()
                correct = int(line)
            self.assertEqual(graph.count_paths(), correct)

def main():
    unittest.main()        

if __name__ == "__main__":
    main()