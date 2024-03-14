import numpy as np
from pymoo.core.problem import Problem


class QAOAmaxcut(Problem):
    def __init__(self, num_gates, qubitmap, w = 0):

        self.map = qubitmap
        self.w = w
        super().__init__(n_var=num_gates, n_obj=1, n_constr=0, xl=0, xu=num_gates-1, elementwise_evaluation=True)


    def _evaluate(self, x, out):
        '''
        x: Matrix containin ch1 only
        '''
        fitness = self.makespan()
        out["F"] = fitness

    def decoding():
        '''
        Gets ch1(x), ch2, w and more to evaluate
        '''
        return SGr
    
    def makespan():
        return fit