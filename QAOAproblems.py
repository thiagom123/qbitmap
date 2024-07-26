import numpy as np
from pymoo.core.problem import ElementwiseProblem
from networkx import shortest_path
from quantum_devices import QuantumDevices


# Thiago Melo: Criar arquivo de testes
#Adicionar otimização que ele faz para portas mix -> Vou precisar adicionar um solution graph?
#before decoding: ch1: [(1, 2), (0, 1), (0, 2)] ch2: [(10, 12), (12, 15), (4, 7)] deu pau aqui

class QAOAmaxcut(ElementwiseProblem):
    def __init__(self, graph, hardware = 'IBM27q',  op_times = [1, 2, 3, 4], initial_qubitmap = None, initial_node_times = None):

        self.ps_gates = list(graph.edges)
        if initial_node_times == None:
            self.initial_node_times = np.zeros(graph.number_of_nodes())
        else:
            self.initial_node_times = initial_node_times
        self.node_times = self.initial_node_times

        self.num_gates = len(self.ps_gates)
        self.op_times = op_times

        self.devices = QuantumDevices()
        self.QM = self.devices[hardware]
        self.num_qubits = self.QM.number_of_nodes()

        #Check if choosen device is qualified
        if graph.number_of_nodes() > self.num_qubits:
            print("Error: Job requires more qubits than available by choosen device.")

        # Creates initial mapping None or picks current map if available
        if initial_qubitmap == None:
            self.initial_map = list(range(graph.number_of_nodes()))
            # map index is graph node, map value is hardware qubit
        else: self.initial_map = initial_qubitmap
        self.qubitmap = self.initial_map

        super().__init__(n_var=1, # graph.number_of_nodes()
                         n_obj=1, n_constr=0,
                         xl=0,
                         xu=graph.number_of_nodes()-1,
                         elementwise_evaluation=True)

    def _evaluate(self, X, out):
        '''
        ch1: List of duples elements of Chromossome 1
        ch2: List of duples elements of Chromossome 1
        '''
        individual = X[0]
        ch1 = individual.ch1
        ch2 = individual.ch2
        #times = individual.times
        #resetar qubit map e node time
        self.qubitmap = self.initial_map
        self.node_times = self.initial_node_times
        #print('before decoding: ch1:', ch1, 'ch2:', ch2, 'node times:', self.node_time)
        self.decoding(ch1, ch2)
        #print('after decoding:', self.node_time)
        fitness = max(self.node_times)
        individual.times = self.node_times
        individual.qubitmap = self.qubitmap

        out["F"] = fitness
    

    def decoding(self, ch1, ch2):
        '''
        Decodes the chromossomes ch1, ch2 
        ch1: List of duples
        ch2: List of duples
        '''
        for k in range(self.num_gates):
            n_i, n_j = ch1[k][0], ch1[k][1]
            q_k, q_l = ch2[k][0], ch2[k][1]
            q_ni, q_nj = self.qubitmap[n_i], self.qubitmap[n_j]
            path_i, path_j = self._calculate_minimal_paths(q_ni, q_nj, q_k, q_l)
            d_ni, d_nj = path_i[-1], path_j[-1]
            while (q_ni!=d_ni) or (q_nj!=d_nj):
                q, q1 = self._next_qubits(path_i, path_j, q_ni, q_nj)
                if [q, q1] != [q_ni, q_nj] and [q, q1] != [q_nj, q_ni]:
                    if(q1 in self.qubitmap):
                        self._add_swaps2(q, q1)
                    else:
                        self._add_swaps1(q, q1)
                    if q == q_ni:
                        q_ni = q1
                    elif q == q_nj:
                        q_nj = q1
                else:
                    #swap in 𝑝𝑎𝑡ℎ1 and 𝑝𝑎𝑡ℎ2 the subpaths from the current qubits
                    if(q1 in path_i and q1 in path_j):
                        path_i, path_j = self._swap_paths(path_i, path_j, q1)
                    else:
                        path_i, path_j = self._swap_paths(path_i, path_j, q)
                    #update final destinations
                    d_ni, d_nj = path_i[-1], path_j[-1]
            self._add_ps(n_i, n_j)
        self._add_mix()        
            
        return
        
    def _calculate_minimal_paths(self, q_ni, q_nj, q_k, q_l):
        '''
        Determine the minimal path from {q_ni, q_nj}
        to {q_k, q_l}
        q_ni, q_nj: Current qubits
        q_k, q_l: Destination qubits
        '''
        path_a1 = shortest_path(self.QM, q_ni, q_k)
        path_b1 = shortest_path(self.QM, q_nj, q_l)
        path_a2 = shortest_path(self.QM, q_ni, q_l)
        path_b2 = shortest_path(self.QM, q_nj, q_k)

        if(len(path_a1) + len(path_b1) <= len(path_a2) + len(path_b2)):
            return path_a1, path_b1
        else:
            return path_a2, path_b2
        
    def _next_qubits(self, path_i, path_j, q_ni, q_nj):
        '''
        Get the sucessors of the elements in a list, if possible
        '''
        if(path_i.index(q_ni)+1<len(path_i)):
            succ_i = path_i[path_i.index(q_ni)+1]
        else:
            succ_i = q_ni
        if(path_j.index(q_nj)+1<len(path_j)):
            succ_j = path_j[path_j.index(q_nj)+1]
        else:
            succ_j = q_nj
        #if [n_qi, succ_i]!=[n_qi, n_qj]:
        if succ_i!= q_ni and succ_i!=q_nj:
            q, q1 = q_ni, succ_i
        #elif [n_qj, succ_j]!=[n_qj, n_qi]:
        elif succ_j!= q_nj and succ_j!=q_ni:
            q, q1 = q_nj, succ_j
        else:
            #print("XXX")
            q, q1 = q_ni, q_nj

        return q, q1
        
    def _swap_paths(self, path_i, path_j, q_intersect):
        '''
        Swap subpaths of the current paths
        path_i, path_j: Current paths
        q_intersect: Qubit of intersection
        '''
        if(path_i.index(q_intersect)+1<len(path_i)):
            sub_pathi = path_i[path_i.index(q_intersect)+1:]
        else:
            sub_pathi=[]
        if(path_j.index(q_intersect)+1<len(path_j)):
            sub_pathj = path_j[path_j.index(q_intersect)+1:]
        else:
            sub_pathj=[]
        path_i = path_i[:path_i.index(q_intersect)+1]+sub_pathj
        path_j = path_j[:path_j.index(q_intersect)+1]+sub_pathi

        return path_i, path_j
    
    def _add_swaps1(self, q, q1):
        '''
        Add the swaps. Only the qubit q is occupied by a node.
        '''
        n = self.qubitmap.index(q)
        self.qubitmap[n] = q1
        self.node_times[n] += self.op_times[1]
        return

    def _add_swaps2(self, q, q1):
        '''
        Add the swaps. Both qubits q and q1 are occupied by a node.
        '''
        n = self.qubitmap.index(q)
        n1 = self.qubitmap.index(q1)
        #Swap qubits
        self.qubitmap[n] = q1
        self.qubitmap[n1] = q
        #Add time on nodes
        max_time=max(self.node_times[n], self.node_times[n1])
        self.node_times[n1] = max_time+self.op_times[1]
        self.node_times[n] = max_time+self.op_times[1]
        #print("nodes", n, n1)
        #print("times", self.node_time[n])
        #self.last_gate[n1] = 'swap'
        #self.last_gate[n] = 'swap'
        return


    
    def _add_ps(self, n, n1):
        max_time=max(self.node_times[n], self.node_times[n1])
        self.node_times[n1] = max_time+self.op_times[2]
        self.node_times[n] = max_time+self.op_times[2]
        #self.last_gate[n1] = 'ps'
        #self.last_gate[n] = 'ps'
        #print("nodes", n, n1)
        #print("times", self.node_time[n])
        return
    
    def _add_mix(self):
        #print(self.node_time)
        self.node_times = [x+self.op_times[0] for x in self.node_times]
        #self.last_gate = ['mix' for x in self.last_gate]
        return
 
