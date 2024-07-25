import networkx as nx

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize

from quantum_devices import QuantumDevices
from QAOAproblems import QAOAmaxcut
from QCCP import QCCP
from CustomOperators import *

graph = nx.Graph()
nodes = [0, 1, 2, 3, 4, 5]
edges = [(0, 1), (1, 2), (2, 0), (5,0), (4,5), (3,5), (1,3)]
graph.add_nodes_from(nodes)
graph.add_edges_from(edges)

problem = QAOAmaxcut(graph=graph)

algorithm = GA(pop_size=50,
               sampling=QAOASampling(),
               crossover = QAOAPMX(),
               mutation= QAOAMutation(),
               eliminate_duplicates= QAOADuplicateElimination())

#build QCCP:
experiment = QCCP(graph,
                  problem,
                  algorithm,
                  r = 3)

schedule = experiment.get_machine_schedule()