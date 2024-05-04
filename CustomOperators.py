import numpy as np
import random as rnd

from pymoo.core.sampling import Sampling
from pymoo.core.crossover import Crossover
from pymoo.core.mutation import Mutation

class QAOAindividual:

    def __init__(self,ch1, ch2):
        '''
        ch1: "channel 1" containing a list of tuples that compose all edges in networkx graph and also 
              determines all ps gates for the circuit.
        ch2: "channel 2" containg another list of tuples, in witch a pair (q1,q2) are two qubits in a quantum chip
        '''
        self.ch1 = ch1
        self.ch2 = ch2
        self.fitness = None

class QAOASampling(Sampling):

    def _do(self, problem, pop_size=50):

        pop = np.full((pop_size, 1), None, dtype=object)
        ps_gates = problem.ps_gates
        num_gates = len(ps_gates)
        qubit_connections = problem.QM.edges

        for i in range(pop_size):
            ch1 = rnd.shuffle(ps_gates)
            ch2 =  rnd.shuffle(qubit_connections)
            pop[i, 0] = QAOAindividual(ch1, ch2)

        return pop

class QAOAPMX(Crossover):
    def __init__(self):

        # define the crossover: number of parents and number of offsprings
        super().__init__(2, 2)

    def _do(self, problem, X, **kwargs):

        # The input of has the following shape (n_parents, n_matings, n_var)
        _, n_matings, n_var = X.shape

        # The output should have the shape (n_offsprings, n_matings, n_var)
        # Because there the number of parents and offsprings are equal it keeps the shape of X
        Y = np.full_like(X, None, dtype=object)

        num_gates = len(problem.ps_gates)
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

            # offspring 1 genes
            ch1_off1 = [0] * num_gates
            ch2_off1 = [0] * num_gates
            # offspring 2 genes
            ch1_off2 = [0] * num_gates
            ch2_off2 = [0] * num_gates

            # pick which genes from each parent will be passed over to each offspring
            indexes_p1 = rnd.sample(range(num_gates), n)
            indexes_p2 = rnd.sample(range(num_gates), n)

            for i in range(num_gates):

                if i in indexes_p1: #p1 passing genes to off1
                    ch1_off1[i] = ch1_p1
                    ch2_off1[i] = ch2_p1
                    
                if i in indexes_p2: #p2 passing genes to off2
                    ch1_off2[i] = ch1_p2
                    ch2_off2[1] = ch2_p2


            # join the character list and set the output
            Y[0, k, 0], Y[1, k, 0] = "".join(off_a), "".join(off_b)

        return Y


class MyPMX(Crossover):

    def __init__(self):

        # define the crossover: number of parents and number of offsprings
        super().__init__(2, 2)

    def _do(self, X):
        # The input has the following shape (n_parents, n_matings, n_var) -> Might change this
        _, n_matings, n_var = X.shape
        # In this case, there are 2 parents.

        num_gates = len(X[0,0,0][0])
        n = int(num_gates/2)

        for k in range(n_matings):

            # get the first and the second parent
            p1, p2 = X[0, k, 0], X[1, k, 0]

            indexes_p1 = rnd.sample(range(num_gates), n)
            indexes_p2 = rnd.sample(range(num_gates), n)

            of11 = [0] * num_gates
            of21 = [0] * num_gates
            of12 = [0] * num_gates
            of22 = [0] * num_gates

            # Fill in selected elements for p1
            for i in indexes_p1:
                if i < len(p1[0]):
                    of11[i] = p1[0][i]
                if i < len(p1[1]):
                    of12[i] = p1[1][i]

            # Fill in selected elements for p2
            for i in indexes_p2:
                if i < len(p2[0]):
                    of21[i] = p2[0][i]
                if i < len(p2[1]):
                    of22[i] = p2[1][i]

    
    
class MyMutation(Mutation):
    def __init__(self):
        super().__init__()

    def _do(self, problem, X, **kwargs):

        num_gates = len(X[0,0,0][0])

        # for each individual
        for k in range(len(X)):
            # Single mutation stage (mut1)
            indexes = rnd.sample(range(num_gates), 2)
            v1, v2 = X[0,k,indexes[0]][0], X[0,k,indexes[0]][1]
            X[0,k,indexes[0]][0] = X[0,k,indexes[1]][0]
            X[0,k,indexes[0]][1] = X[0,k,indexes[1]][1]
            X[0,k,indexes[1]][0] = v1
            X[0,k,indexes[1]][2] = v2
            
            # ch2 mutation (mut2) stage
    
#class MyDuplicateElimination()