import numpy as np
import random as rnd

from pymoo.core.sampling import Sampling
from pymoo.core.crossover import Crossover
from pymoo.core.mutation import Mutation
from pymoo.core.duplicate import ElementwiseDuplicateElimination

teste = False
class QAOAindividual:

    def __init__(self,ch1, ch2):
        '''
        ch1: "channel 1" containing a list of tuples that compose all edges in networkx graph and also 
              determines all ps gates for the circuit.
        ch2: "channel 2" containg another list of tuples, in witch a pair (q1,q2) are two qubits in a quantum chip
        times: Array containing the 'operation' time for each gate 
        qubitmap: Array with indexes containing the nodes from the graph and the cells containing the current machine's qubit
        '''
        self.ch1 = ch1
        self.ch2 = ch2
        self.times = None
        self.qubitmap = None

class QAOASampling(Sampling):

    def _do(self, problem, pop_size=50, **kwargs):
        

        pop = np.full((pop_size, 1), None, dtype=object)
        ps_gates = problem.ps_gates
        num_gates = len(ps_gates)
        qubit_connections = list(problem.QM.edges)

        for i in range(pop_size):
            rnd.shuffle(ps_gates)
            rnd.shuffle(qubit_connections)
            ch1 = ps_gates
            ch2 =  qubit_connections[:num_gates]
            individual = QAOAindividual(ch1, ch2)
            individual.times = problem.initial_node_times
            #individual.times = problem.node_times
            pop[i, 0] = individual
        
        return pop

class QAOAPMX(Crossover):
    def __init__(self):

        # define the crossover: number of parents and number of offsprings
        super().__init__(2, 2)

    def _do(self, problem, X, **kwargs):

        # The input of has the following shape (n_parents, n_matings, n_var)
        _, n_matings, _ = X.shape

        # The output should have the shape (n_offsprings, n_matings, n_var)
        # Because there the number of parents and offsprings are equal it keeps the shape of X
        Y = np.full_like(X, None, dtype=object)

        num_gates = len(problem.ps_gates)

        # each parent pass about half of their genes to each offspring
        n = int(num_gates/2)

        # for each mating provided
        for k in range(n_matings):

            # get the first and the second parent
            p1, p2 = X[0, k, 0], X[1, k, 0]

            # parent 1 genes
            ch1_p1 = p1.ch1
            ch2_p1 = p1.ch2
            # parent 2 genes
            ch1_p2 = p2.ch1
            ch2_p2 = p2.ch2
            if(teste):
                print("Parent 1")
                print(ch1_p1)
                print(ch2_p1)
                print("Parent 2")
                print(ch1_p2)
                print(ch2_p2)


            # offspring 1 genes
            ch1_off1 = [0] * num_gates
            ch2_off1 = [0] * num_gates
            # offspring 2 genes
            ch1_off2 = [0] * num_gates
            ch2_off2 = [0] * num_gates

            # pick which genes from each parent will be passed over to each offspring
            indexes_p1 = rnd.sample(range(num_gates), n)

            indexes_p2 = []
            for idx in indexes_p1:
                gene = ch1_p1[idx]
                corresponding_index = ch1_p2.index(gene)
                indexes_p2.append((corresponding_index))

            count_off1 = 0
            count_off2 = 0

            for i in range(num_gates):

                if i in indexes_p1: #p1 passing genes to off1
                    ch1_off1[i] = ch1_p1[i]
                    ch2_off1[i] = ch2_p1[i]
                else:
                    while count_off1 in indexes_p2:
                        count_off1 += 1
                    ch1_off1[i] = ch1_p2[count_off1]
                    ch2_off1[i] = ch2_p2[count_off1]
                    count_off1 += 1
                    
                if i in indexes_p2: #p2 passing genes to off2
                    ch1_off2[i] = ch1_p2[i]
                    ch2_off2[i] = ch2_p2[i]
                else:
                    while count_off2 in indexes_p1:
                        count_off2 += 1
                    ch1_off2[i] = ch1_p1[i]
                    ch2_off2[i] = ch2_p1[i]
                    count_off2 += 1
            
            off_1 = QAOAindividual(ch1_off1,ch2_off1)
            off_2 = QAOAindividual(ch1_off2,ch2_off2)

            # join the character list and set the output
            Y[0, k, 0], Y[1, k, 0] = off_1, off_2

        return Y
    
class QAOAMutation(Mutation):
    def __init__(self):
        super().__init__()

    def _do(self, problem, X, **kwargs):

        Y = np.full_like(X, None, dtype=object)
        num_gates = len(problem.ps_gates)
        machine_connections = problem.QM.edges
        # for each individual
        for i in range(len(X)):

            gambiarra = X[i] # Props on you for getting all the way here
            individual = gambiarra[0] # Leave my gambiarra alone
            ch1 = individual.ch1
            ch2 = individual.ch2

            # First mutation stage (mut1)
            indexes = rnd.sample(range(num_gates), 2)

            l11, l12 = ch1[indexes[0]], ch2[indexes[0]]

            ch1[indexes[0]] = ch1[indexes[1]]
            ch2[indexes[0]] = ch2[indexes[1]]
            ch1[indexes[1]] = l11
            ch2[indexes[1]]= l12
            # Second mutation stage (mut2)
            random_index = rnd.randrange(len(ch2))
            random_tuple = ch2[random_index]
            nodes_in_tuple = set(random_tuple)
            candidate_tuples = [tup for i, tup in enumerate(machine_connections) if any(node in nodes_in_tuple for node in tup)]
            new_connection = rnd.choice(candidate_tuples)
            ch2[random_index] = new_connection

            # put new mutated ind in Y
            Y[i] = QAOAindividual(ch1, ch2)

        return Y

    


class QAOADuplicateElimination(ElementwiseDuplicateElimination):

    def is_equal(self, a, b):
        return a.X[0] == b.X[0]