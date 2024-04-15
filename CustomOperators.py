import numpy as np
import random as rnd

from pymoo.core.sampling import Sampling
from pymoo.core.crossover import Crossover
from pymoo.core.mutation import Mutation

class MySampling(Sampling):

    def _do(self, gates, qubit_connections, pop_size=50):
        '''
        gates: list of tuples indicating PS-gates as graph edges
        '''
        pop = np.zeros(pop_size,2)
        num_gates, _ = np.shape(gates)

        for i in range(pop_size):
            pop[i,0] = rnd.shuffle(gates)
            pop[i,1] = rnd.sample(qubit_connections, num_gates)

        return pop
    
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

            Y[0,k,0], Y[1,k,0] = 

                






    
    
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
    
class MyDuplicateElimination()