#!/usr/bin/python3

import argparse
import fileinput

from io import TextIOWrapper
from typing import Optional

desc =  """
        Counts maximum number of different pairs of nodes so that one node is red, other
        is blue and all pairs can be connected by mutually disjunctive paths.
        If file is not specified, graph is read from standard input.
        """

parser = argparse.ArgumentParser(description=desc)
parser.add_argument("-f", "--file", default=None, type=str, help="Path to input file.")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output.")

NONE = 0    # Color for uncolored node.
RED = 1     # Color for red node.
BLUE = 2    # Color for blue node.

class Graph:
    """
    A class representing graph.

        Attributes
        ----------
            nodes: set
                nodes of graph
            neighbors: list
                contains sets of neighbors for each node of graph, indexed by node
            colors: list
                contains color of each node, indexed by node

        Methods
        -------
            count_paths():
                Counts maximum number of different pairs of nodes so that one node is red, other
                is blue and all pairs can be connected by mutually disjunctive paths.
    """

    def __init__(self, filename: Optional[str] = None):
        """
        Constructs graph by reading it from given file or standard input.

            Parameters
            ----------
                filename: Optional[str]
                    path to file describing graph or `None` if standard input should be read
        """
        with fileinput.input(files=filename) as input:
            line = input.readline().strip()
            self._M, self._R, self._B = [ int(x) for x in line.split() ]
            self.nodes = set(range(1, self._M + 2))
                # Number of nodes is `M+1`, indexing starts at 1.

            self.neighbors = self._read_neighbors(input)
            self.colors = self._read_colors(input)

        self.leaves = self._get_leaves()

    def _read_neighbors(self, input: TextIOWrapper) -> list:
        """
        Reads edges of graph and saves them as sets of neighbors.

        Each line contains one edge: two nodes it connects.

            Parameters
            ----------
                file: TextIOWrapper
                    input, from which to read edges

            Returns
            -------
                list of sets of neighbors of each node, list is indexed by nodes
        """
        neighbors = [ set() for _ in range(self._M + 2) ]

        for _ in range(self._M):
            line = input.readline().strip()
            u, v = [ int(x) for x in line.split() ]
            neighbors[u].add(v)
            neighbors[v].add(u)

        return neighbors

    def _read_colors(self, input: TextIOWrapper) -> list:
        """
        Reads colors of nodes and colors appropriate nodes.

        Red nodes are on the first line separated by space,
        blue nodes are on the second line in the same format.

            Parameters
            ----------
                file: TextIOWrapper
                    input, from which to read nodes colored red and blue


            Returns
            -------
                list of colors of nodes, list is indexed by nodes
        """
        colors = [NONE] * len(self.neighbors)
        
        line = input.readline().strip()
        red_leaves = [ int(x) for x in line.split() ]
        for leaf in red_leaves:
            colors[leaf] = RED

        line = input.readline().strip()
        blue_leaves = [ int(x) for x in line.split() ]
        for leaf in blue_leaves:
            colors[leaf] = BLUE

        return colors

    def _get_leaves(self) -> set:
        """
        Finds all leaves of graph.

            Returns
            -------
                set of leaves of graph
        """
        leaves = set([ v for v, nbrs in enumerate(self.neighbors) if len(nbrs) == 1 ])
        return leaves

    def _remove_node(self, node: int) -> None:
        """
        Removes given node from graph.

            Parameters
            ----------
                node: int
                    node to be removed from graph

            Returns
            -------
                None
        """
        for neighbor in self.neighbors[node]:
            self.neighbors[neighbor].remove(node)
            if len(self.neighbors[neighbor]) == 1:
                self.leaves.add(neighbor)

        self.neighbors[node].clear()
        self.nodes.remove(node)
        self.leaves.discard(node)

    def _path_found(self, u: int, v: int) -> bool:
        """
        Checks whether a path from red to blue node exists in graph using
        edge (`u`, `v`).

            Parameters
            ----------
                u: int
                    first node of given edge
                v: int
                    second node of given edge

            Returns
            -------
                True if path from red to blue node exists using edge (`u`, `v`)
        """
        return  self.colors[u] != NONE and \
                self.colors[v] != NONE and \
                self.colors[u] != self.colors[v]

    def _push_color(self, leaf: int, node: int) -> None:
        """
        Pushes color of leaf to its neighbor if leaf has a valid color.

            Parameters
            ----------
                leaf: int
                    leaf, whose color is to be pushed
                node: int
                    neighbor of `leaf`, this node's color will be the color of `leaf` (if `leaf` has valid color)

            Returns
            -------
                None
        """
        if self.colors[leaf] != NONE:
            self.colors[node] = self.colors[leaf]

    def count_paths(self, verbose: bool = False) -> int:
        """
        Counts maximum number of differen pairs of nodes so that one node is red, other
        is blue and all pairs can be connected by mutually disjunctive paths.

            Parameters
            ----------
                verbose: bool
                    whether to print information during each step

            Returns
            -------
                number of paths connecting maximum number of pairs

        """
        paths = 0
        while len(self.leaves) > 0:
            leaf = self.leaves.pop()
            
            if verbose:
                self._print_leaf(leaf)

            if len(self.neighbors[leaf]) == 0:
                # Leaf is isolated, just remove it and continue with next leaf.
                self._remove_node(leaf)
                
                if verbose:
                    self._print_graph()
                    self._print_paths(paths)
                continue

            neighbor = next(iter(self.neighbors[leaf]))
            self._remove_node(leaf)

            if self._path_found(leaf, neighbor):
                # There was a path found using edge (`leaf`, `neighbor`).
                paths += 1
                self._remove_node(neighbor)
            else:
                # There is not a path, push leaf's color to neighbor.
                self._push_color(leaf, neighbor)

            if verbose:
                self._print_graph()
                self._print_paths(paths)

        return paths

    def _print_leaf(self, leaf: int) -> None:
        """
        Prints message describing which leaf is being reduced.

            Parameters
            ----------
                leaf: int
                    leaf to be reduced

            Returns
            -------
                None
        """
        print(f"Reducing node {leaf}\n")

    def _print_graph(self) -> None:
        """
        Prints description of graph in the same format as input file.

            Returns
            -------
                None
        """
        M = 0
        R = []
        B = []
        edges = ""
        for u, nbrs in enumerate(self.neighbors):
            if u in self.nodes:
                if self.colors[u] == RED:
                    R.append(str(u))
                elif self.colors[u] == BLUE:
                    B.append(str(u))
            for v in nbrs:
                if v > u:
                    edges += f"{u} {v}\n"
                    M += 1
        print(f"{M} {len(R)} {len(B)}")

        if M > 0:
            print(edges[:-1])
        else:
            print("No edges")

        if len(R) > 0:
            print(" ".join(R))
        else:
            print("No red nodes")

        if len(B) > 0:
            print(" ".join(B))
        else:
            print("No blue nodes")

        print()

    def _print_paths(self, paths: int) -> None:
        """
        Prints number of paths found so far.

            Returns
            -------
                None
        """
        print(f"Number of pairs found so far: {paths}")
        print("--------------------------------------")


def main(args: argparse.Namespace):
    graph = Graph(args.file)
    print(graph.count_paths(args.verbose))
        

if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)
    main(args)