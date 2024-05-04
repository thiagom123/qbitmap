import networkx as nx

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize

from quantum_devices import QuantumDevices
from QAOAproblems import QAOAmaxcut
from QCCP import QCCP
from CustomOperators import *

graph = nx.Graph()

problem = QAOAmaxcut(graph=graph)

algorithm = GA(pop_size=100,
               sampling=QAOASampling,
               crossover = QAOAPMX,
               mutation= QAOAMutation,
               eliminate_duplicates= QAOAduplicates)

#build QCCP:
experiment = QCCP(graph,
                  problem,
                  algorithm,
                  r = 3)
