import numpy as np
from pymoo.core.problem import Problem
from networkx import shortest_path



#Pendencias: Thiago Melo: - ch1 precisa ser uma lista simples?
# Thiago Melo: Como representar ch1 d ch2 no x
# Thiago Melo: Verificar se estamos pegando solucoes de rounds anteriores: Sim, através do current_time(?)
# Thiago Melo: Mudar variaveis q e n -> nodo n qubit q (feito)
# Thiago Melo: Criar arquivo de testes
#Adicionar otimização que ele faz para portas mix -> Vou precisar adicionar um solution graph?
# Analisar se precisamos retornar um solution graph ou não
#Código está funcionando, mas apenas para um Quantum hardware sem pesos
#Podemos colocar o pesos no próprios hardware_graph?
#Adicionar otimização

class QAOAmaxcut(Problem):
    def __init__(self, num_gates, qubitmap, hardware_graph, current_time, op_times = [1, 2, 3, 4], w = 0):

        #Lista de 
        self.map = qubitmap
        self.w = w
        self.QM = hardware_graph
        self.node_time = current_time
        self.op_times = op_times
        self.last_gate = np.zeros(len(self.node_time))
        super().__init__(n_var=num_gates, n_obj=1, n_constr=0, xl=0, xu=num_gates-1, elementwise_evaluation=True)


    def _evaluate(self, ch1, ch2, out):
        '''
        ch1: List of elements of Chromossome 1
        ch2: List of elements of Chromossome 1
        '''
        self.decoding(ch1, ch2)
        #fitness = self.makespan(ch1, ch2)
        fitness = max(self.node_time)
        out["F"] = fitness
    
    def makespan(self):

        return fit

    def decoding(self, ch1, ch2):
        '''
        Gets ch1(x), ch2, w and more to evaluate
        ch1: List of duples
        ch2: List of duples
        '''
        num_gates = self.n_var
        for k in range(num_gates):
            n_i, n_j = ch1[k][0], ch1[k][1]
            q_k, q_l = ch2[k][0], ch2[k][1]
            #pegar o qubit atual dos qstates
            q_ni, q_nj = self.map[n_i], self.map[n_j]
            path_i, path_j = self._calculate_minimal_paths(q_ni, q_nj, q_k, q_l)
            d_ni, d_nj = path_i[-1], path_j[-1]

            while (q_ni!=d_ni) or (q_nj!=d_nj):
                #q, q1 = q_ni, q_nj
                q, q1 = self._next_qubits(path_i, path_j, q_ni, q_nj);
                if [q, q1] != [q_ni, q_nj] and [q, q1] != [q_nj, q_ni]:
                    print("add_swaps",n_i, n_j, q, q1)
                    self._add_swaps(self.map.index(q), self.map.index(q1), q, q1)
                    #O avanço aqui está bugado
                    if q == q_ni:
                        q_ni = q1
                    elif q == q_nj:
                        q_nj = q1
                else:
                    #swap in 𝑝𝑎𝑡ℎ1 and 𝑝𝑎𝑡ℎ2 the subpaths from the current qubits
                    print("swap paths")
                    path_i, path_j = self._swap_paths(path_i, path_j, q)
            print("add ps", n_i, n_j)
            self._add_ps(n_i, n_j)
        print("add mix")
        self._add_mix()        
            
        return
        
    def _calculate_minimal_paths(self, q_ni, q_nj, n_k, n_l):
        #checar argumentos
        path_a1 = shortest_path(self.QM, q_ni, n_k)
        path_b1 = shortest_path(self.QM, q_nj, n_l)
        path_a2 = shortest_path(self.QM, q_ni, n_l)
        path_b2 = shortest_path(self.QM, q_nj, n_k)

        if(len(path_a1) + len(path_b1) <= len(path_a2) + len(path_b2)):
            return path_a1, path_b1
        else:
            return path_a2, path_b2
        
    def _next_qubits(self, path_i, path_j, q_ni, q_nj):
        '''
        Get the sucessors of the elements in a list, if possible
        '''
        #Acho que tem forma melhor
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
            q, q1 = q_ni, q_nj

        return q, q1
        
    def _swap_paths(self, path_i, path_j, n):
        sub_pathi = path_i[path_i.index(n):]
        sub_pathj = path_j[path_j.index(n):]
        path_i = path_i[:path_i.index(n)]+sub_pathj
        path_j = path_j[:path_j.index(n)]+sub_pathi

        return path_i, path_j
    
    def _add_swaps(self, n, n1, q, q1):
        #Swap qubits
        self.map[n] = q1
        self.map[n1] = q
        #Add time on nodes
        max_time=max(self.node_time[n], self.node_time[n1])
        self.node_time[n1] = max_time+self.op_times[1]
        self.node_time[n] = max_time+self.op_times[1]
        print("nodes", n, n1)
        print("times", self.node_time[n])
        self.last_gate[n1] = 1
        self.last_gate[n] = 1
        return


    
    def _add_ps(self, n, n1):
        max_time=max(self.node_time[n], self.node_time[n1])
        self.node_time[n1] = max_time+self.op_times[2]
        self.node_time[n] = max_time+self.op_times[2]
        self.last_gate[n1] = 2
        self.last_gate[n] = 2
        print("nodes", n, n1)
        print("times", self.node_time[n])
        return
    
    def _add_mix(self):
        print(self.node_time)
        self.node_time = [x+self.op_times[0] for x in self.node_time]
        self.last_gate = [3 for x in self.last_gate]
        return
 
