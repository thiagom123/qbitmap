import networkx as nx

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize

from quantum_devices import QuantumDevices
from QAOAproblems import QAOAmaxcut
from QCCP import QCCP
from CustomOperators import *
from Graphs import GraphInstance
import matplotlib.pyplot as plt

'''graph = nx.Graph()
nodes = [0, 1, 2, 3, 4, 5]
edges = [(0, 1), (1, 2), (2, 0), (5,0), (4,5), (3,5), (1,3)]
graph.add_nodes_from(nodes)
graph.add_edges_from(edges)'''

graph = GraphInstance(instances=0)
#nx.draw(graph, with_labels=True, node_color = 'orange')
#plt.show()

hardware = 'IBM27q'
devices = QuantumDevices()
hardware_graph = devices[hardware]

problem = QAOAmaxcut(graph=graph, hardware_graph=hardware_graph)

algorithm = GA(pop_size=400,
               sampling=QAOASampling(),
               crossover = QAOAPMX(),
               mutation= QAOAMutation(),
               eliminate_duplicates= QAOADuplicateElimination())

#build QCCP:
experiment = QCCP(graph,
                  problem,
                  algorithm,
                  r = 2,
                  n_gen_stale=200)

schedule = experiment.get_machine_schedule()

print(f'final schedule: {schedule}')