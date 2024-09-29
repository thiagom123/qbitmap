import numpy as np
from pymoo.core.problem import ElementwiseProblem
from networkx import shortest_path
from quantum_devices import QuantumDevices


# Thiago Melo: Criar arquivo de testes
#Adicionar otimização que ele faz para portas mix -> Vou precisar adicionar um solution graph?
#before decoding: ch1: [(1, 2), (0, 1), (0, 2)] ch2: [(10, 12), (12, 15), (4, 7)] deu pau aqui

time_ps=3
time_swap = 2
time_mix=1

teste = True

class QAOAmaxcut(ElementwiseProblem):
    def __init__(self, graph, hardware_graph, initial_qubitmap = None, initial_node_times = None):

        self.ps_gates = list(graph.edges)
        if(graph.number_of_nodes() == 0):
            raise ValueError("Graph with zero nodes")
        if initial_node_times == None:
            self.initial_node_times = np.zeros(graph.number_of_nodes())
        else:
            self.initial_node_times = initial_node_times
        #self.node_times = self.initial_node_times

        self.num_gates = len(list(graph.edges))
        #self.op_times = op_times

        #self.devices = QuantumDevices()
        #self.QM = self.devices[hardware]
        if(hardware_graph.number_of_nodes()==0):
            raise ValueError("Hardware with zero qubits")
        self.QM = hardware_graph
        self.num_qubits = self.QM.number_of_nodes()

        #Check if choosen device is qualified
        if graph.number_of_nodes() > self.num_qubits:
            raise ValueError("Job requires more qubits than available by choosen device.")

        # Creates initial mapping None or picks current map if available
        if initial_qubitmap == None:
            self.initial_map = list(range(graph.number_of_nodes()))
            # map index is graph node, map value is hardware qubit
        else: self.initial_map = initial_qubitmap
        #self.qubitmap = self.initial_map

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
        #resetar qubit map e node time
        #qubitmap = individual.qubitmap
        #node_times = individual.node_times
        qubitmap = self.initial_map
        node_times = self.initial_node_times
        if(teste): print('before decoding:', individual.times, self.initial_node_times)
        qubitmap, node_times = self.decoding(ch1, ch2, qubitmap, node_times)
        #print('after decoding:', self.node_time)
        fitness = max(node_times)
        individual.times = node_times
        individual.qubitmap = qubitmap

        X[0] = individual
        out["F"] = fitness
    

    def decoding(self, ch1, ch2, qubitmap=None, node_times=None):
        '''
        Decodes the chromossomes ch1, ch2 
        ch1: List of duples
        ch2: List of duples
        '''
        if(node_times is None):
            node_times = self.initial_node_times
        if(qubitmap is None):
            qubitmap = self.initial_map
        mix_gates = list(range(len(node_times)))
        #No lugar de last_gates, poderia até salvar todos os gates
        last_gates = ['0' for x in range(len(node_times))]
        if teste: print("Decoding")
        if teste: print(last_gates)
        for k in range(self.num_gates):
            n_i, n_j = ch1[k][0], ch1[k][1]
            q_k, q_l = ch2[k][0], ch2[k][1]
            q_ni, q_nj = qubitmap[n_i], qubitmap[n_j]
            path_i, path_j = self._calculate_minimal_paths(q_ni, q_nj, q_k, q_l)
            d_ni, d_nj = path_i[-1], path_j[-1]
            while (q_ni!=d_ni) or (q_nj!=d_nj):
                q, q1 = self._next_qubits(path_i, path_j, q_ni, q_nj)
                if [q, q1] != [q_ni, q_nj] and [q, q1] != [q_nj, q_ni]:
                    if(q1 in qubitmap):
                        self._add_swaps2(q, q1,qubitmap, node_times, last_gates)
                        if teste: print(last_gates)
                    else:
                        self._add_swaps1(q, q1, qubitmap, node_times, last_gates)
                        if teste: print(last_gates)
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
            self._add_ps(n_i, n_j, node_times, last_gates)
            mix_gates = self._add_mix_new(mix_gates, ch1, k, node_times, last_gates)
            if teste: print(last_gates)       
        
        if teste: print("node times", node_times)
        return qubitmap, node_times
        
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
    
    def _add_swaps1(self, q, q1, qubitmap, node_times, last_gates):
        '''
        Add the swaps. Only the qubit q is occupied by a node.
        '''
        n = qubitmap.index(q)
        qubitmap[n] = q1
        node_times[n] += time_swap
        #print("SWAP", n)
        #print("times", node_times)
        last_gates[n]='swap'
        return
    
    def _change_mix_swap(self, a, b, node_times, last_gates):
        '''
        Verify if we should change the order of the swap and mix gate
        '''
        if(last_gates[a] == 'mix' and node_times[b] < node_times[a] - time_mix ):
            node_times[a] = node_times[a] + time_swap
            node_times[b] = node_times[a] - time_mix
            last_gates[a] = 'mix'
            last_gates[b] = 'swap'
            return True
        else:
            return False

    def _add_swaps2(self, q, q1, qubitmap, node_times, last_gates):
        '''
        Add the swaps. Both qubits q and q1 are occupied by a node.
        '''
        n = qubitmap.index(q)
        n1 = qubitmap.index(q1)
        #Swap qubits
        qubitmap[n] = q1
        qubitmap[n1] = q
        #Add time on nodes
        aux1 = self._change_mix_swap(n, n1, node_times, last_gates)
        aux2 = self._change_mix_swap(n1, n, node_times, last_gates)
        if(aux1 is False and aux2 is False):
            max_time = max(node_times[n], node_times[n1])
            node_times[n1] = max_time+time_swap
            node_times[n] = max_time+time_swap
            last_gates[n1] = 'swap'
            last_gates[n] = 'swap'
        #print("SWAP", n, n1)
        #print("times", node_times)
        
        return


    
    def _add_ps(self, n, n1, node_times, last_gates):
        '''
        Add a p-s gate to both qubits
        '''
        max_time=max(node_times[n], node_times[n1])
        node_times[n1] = max_time+time_ps
        node_times[n] = max_time+time_ps
        last_gates[n1] = 'ps'
        last_gates[n] = 'ps'
        #print("P-S", n, n1)
        #print("times", node_times)
        return
    
    #def _add_mix(self):
        #print(self.node_time)
    #    node_times = [x+time_mix for x in node_times]
        #self.last_gate = ['mix' for x in self.last_gate]
    #    return
    
    def _add_mix_new(self, mix_gates, ch1, k, node_times, last_gates):
        '''
        Add a mix gate to all qubits that no longer require p-s gates
        '''
        #print(self.node_time)
        mix_gates_copy = mix_gates.copy()
        ps_gates = ch1[k+1:]
        #print("next ps", ps_gates)
        #print("next mix", mix_gates)
        for n in mix_gates_copy:
            #remove = True
            if all(t[0]!=n and t[1]!=n for t in ps_gates):
                #for i in range(k+1, len(ch1)):
                #    for j in range(2):
                #        if n==ch1[i][j]:
                #            remove = False
                #if(remove):
                node_times[n] += time_mix
                last_gates[n] = 'mix'
                mix_gates.remove(n)
                #print("mix ", n)
                #print(node_times)
                #print("remain ", mix_gates)
            #else:
            #    print("not yet ", n)
        #self.last_gate = ['mix' for x in self.last_gate]
        
        return mix_gates
 
