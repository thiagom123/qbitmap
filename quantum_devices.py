import networkx as nx


def QuantumDevices():
    IBM_27q = nx.Graph()
    IBM_127q = nx.Graph()
    IBM_133q = nx.Graph()

    nodes = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
    edges = [(0,1),(1,2),(1,4),(2,3),(3,5),(4,7),(5,8),
            (6,7),(7,10),(8,9),(8,11),(10,12),(11,14),
            (12,13),(12,15),(13,14),(14,16),(15,18),
            (16,19),(17,18),(18,21),(19,20),(19,22),(21,23),(22,25),
            (23,24),(24,25),(25,26)]

    IBM_27q.add_nodes_from(nodes)
    IBM_27q.add_edges_from(edges)

    chips = {
        'IBM27q' : IBM_27q
    }

    return chips