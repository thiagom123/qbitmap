from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.problems import get_problem
from pymoo.optimize import minimize
import networkx as nx
import matplotlib.pyplot as plt
'''
problem = get_problem("g1")

algorithm = GA(
    pop_size=100,
    eliminate_duplicates=True)

res = minimize(problem,
               algorithm,
               seed=1,
               verbose=False)

print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))
'''



'''graph = nx.Graph()

nodes = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
edges = [(0,1),(1,2),(1,4),(2,3),(3,5),(4,7),(5,8),
         (6,7),(7,10),(8,9),(8,11),(10,12),(11,14),
         (12,13),(12,15),(13,14),(14,16),(15,18),
         (16,19),(17,18),(18,21),(19,20),(19,22),(21,23),(22,25),
         (23,24),(24,25),(25,26)]

graph.add_nodes_from(nodes)
graph.add_edges_from(edges)

plt.figure(figsize=(6, 6))
nx.draw(graph, with_labels=True, node_color='lightblue', node_size=100, font_size=12)
plt.show()

chips = {
    '27q_device' : graph
}'''

class GraphComparator:
    def __init__(self, graph_A, graph_B):
        # Check if graph_A has more nodes than graph_B
        if graph_A.number_of_nodes() > graph_B.number_of_nodes():
            print("Error: Graph A has more nodes than Graph B.")
            return
        
        # Create mappings between nodes of graph A and graph B
        self.node_mapping = list(zip(graph_B.nodes, graph_A.nodes))
        
        print("Graphs initialized successfully.")
        print("Node Mapping:", self.node_mapping)

# Example usage:
if __name__ == "__main__":
    # Create graph A
    graph_A = nx.Graph()
    graph_A.add_nodes_from([1, 2, 3])
    
    # Create graph B
    graph_B = nx.Graph()
    graph_B.add_nodes_from([4, 5, 6, 7, 8, 10])
    
    # Initialize the class
    comparator = GraphComparator(graph_A, graph_B)
