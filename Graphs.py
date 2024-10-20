import numpy as np
import networkx as nx

def GraphInstance(instances=0):

   
    nodesN8 = range(0,8)
    edgesN8 = [[(0, 2), (2, 4), (0, 4), (3, 5), (1, 4), (0, 5), (0, 3), (1, 2)],
               [(1,6),(2,6),(3,5),(4,6),(5,6),(2,5),(2,3),(0,1)],
               [(0,3),(1,2),(2,4),(0,6),(3,6),(0,4),(4,5),(3,5)],
               [(2,6),(1,2),(0,1),(4,5),(3,6),(2,3),(1,4),(2,5)],
               [(0,7),(2,6),(0,2),(1,5),(3,5),(4,5),(2,3),(1,6)]]
    
    GraphN8 = nx.Graph()
    GraphN8.add_nodes_from(nodesN8)
    GraphN8.add_edges_from(edgesN8[instances])

    return GraphN8
