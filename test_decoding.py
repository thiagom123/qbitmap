from unittest import TestCase
from QAOAproblems import QAOAmaxcut
import numpy as np


class TestDecoding(TestCase):
    def test_shortest_path(self, hardware_graph, n_qi, n_qj, n_k, n_l):
        max_cut = QAOAmaxcut()