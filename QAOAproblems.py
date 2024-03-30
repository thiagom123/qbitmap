import numpy as np
from pymoo.core.problem import Problem
from networkx import shortest_path



#Pendencias: Thiago Melo: - ch1 precisa ser uma lista simples?
# Thiago Melo: Como representar ch1 d ch2 no x
# Thiago Melo: Verificar se estamos pegando solucoes de rounds anteriores
# Thiago Melo: Mudar variaveis q e n
# Thiago Melo: Criar arquivo de testes

class QAOAmaxcut(Problem):
    def __init__(self, num_gates, qubitmap, hardware_graph, qubit_time, op_times = [1, 2, 3, 4], w = 0):

        #Lista de 
        self.map = qubitmap
        self.w = w
        self.QM = hardware_graph
        self.qubit_time = qubit_time
        self.op_times = op_times
        super().__init__(n_var=num_gates, n_obj=1, n_constr=0, xl=0, xu=num_gates-1, elementwise_evaluation=True)


    def _evaluate(self, x, out):
        '''
        x: Matrix containin ch1 only
        '''
        fitness = self.makespan()
        out["F"] = fitness
    
    def makespan():
        return fit

    def decoding(self, ch1, ch2, SG):
        '''
        Gets ch1(x), ch2, w and more to evaluate
        ch1: List of duples
        ch2: List of duples
        '''
        #Ver questão da continuidade dos rounds
        SGr=SG
        num_gates = self.n_var
        #Mudar notação, trocar q pelo n
        for k in num_gates:
            q_i, q_j = ch1[k][0], ch1[k][1]
            n_k, n_l = ch2[k][0], ch2[k][1]
            #pegar o qubit atual dos qstates
            n_qi, n_qj = self.map[q_i], self.map[q_j]
            path_i, path_j = self._calculate_minimal_paths(n_qi, n_qj, n_k, n_l)
            d_qi, d_qj = path_i[-1], path_j[-1]

            while (n_qi!=d_qi) or (n_qj!=d_qj):
                #n, n1 = n_qi, n_qj
                n, n1 = self._next_qubits(path_i, path_j, n_qi, n_qj);
                if [n, n1] != [n_qi, n_qj] and [n, n1] != [n_qj, n_qi]:
                    self._add_swaps(n, n1)
                    n = n1
                else:
                    #swap in 𝑝𝑎𝑡ℎ1 and 𝑝𝑎𝑡ℎ2 the subpaths from the current qubits
                    self._swap_paths(path_i, path_j, n)

            self._add_ps(n_k, n_l)
        self._add_mix()        
            
        return SGr
        
    def _calculate_minimal_paths(self, n_qi, n_qj, n_k, n_l):
        #checar argumentos
        path_a1 = shortest_path(n_qi, n_k, self.QM)
        path_b1 = shortest_path(n_qj, n_l, self.QM)
        path_a2 = shortest_path(n_qi, n_l, self.QM)
        path_b2 = shortest_path(n_qj, n_k, self.QM)

        if(len(path_a1) + len(path_b1) <= len(path_a2) + len(path_b2)):
            return path_a1, path_b1
        else:
            return path_a2, path_b2
        
    def _next_qubits(self, path_i, path_j, n_qi, n_qj):
        '''
        Get the sucessors of the elements in a list, if possible
        '''
        #Acho que tem forma melhor
        if(path_i.index(n_qi)+1<len(path_i)):
            succ_i = path_i[path_i.index(n_qi)+1]
        if(path_j.index(n_qj)+1<len(path_j)):
            succ_j = path_j[path_j.index(n_qj)+1]
        #if [n_qi, succ_i]!=[n_qi, n_qj]:
        if succ_i!=n_qj:
            n, n1 = n_qi, succ_i
        #elif [n_qj, succ_j]!=[n_qj, n_qi]:
        elif succ_j!=n_qi:
            n, n1 = n_qj, succ_j
        else:
            n, n1 = n_qi, n_qj

        return n, n1
        
    def _swap_paths(self, path_i, path_j, n):
        sub_pathi = path_i[path_i.index(n):]
        sub_pathj = path_j[path_j.index(n):]
        path_i = path_i[:path_i.index(n)]+sub_pathj
        path_j = path_j[:path_j.index(n)]+sub_pathi

        return path_i, path_j
    
    def _add_swaps(self, n, n1):
        #Swap qubits
        aux = self.map[n]
        self.map[n] = self.map[n1]
        self.map[n1] = aux
        #Add time on nodes
        max_time=max(self.qubit_time[n], self.qubit_time[n1])
        self.qubit_time[n1] = max_time+self.op_times[1]
        self.qubit_time[n] = max_time+self.op_times[1]

    
    def _add_ps(self, n, n1):
        max_time=max(self.qubit_time[n], self.qubit_time[n1])
        self.qubit_time[n1] = max_time+self.op_times[2]
        self.qubit_time[n] = max_time+self.op_times[2]
    
    def _add_mix(self):
        self.qubit_time = [x+self.op_times[0] for x in self.qubit_time]
 
