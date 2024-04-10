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

    def _do(self, pop):


    
    
class MyMutation(Mutation):
    
class MyDuplicateElimination()