from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize
import networkx as nx
from quantum_devices import QuantumDevices
from QAOAproblems import QAOAmaxcut

class QCCP:
    '''
    QCCP: Quantum Circuit Compilation Problem - QAOA

    Generalized for any QAOA problem

        graph: (networkx Graph)
        problem: (pymoo ElementWiseProblem)
        algorithm: (pymoo Algorithm)
        r: (int) rounds/layers
        w: Current connection weights measured on the quantum device (NOT IN USE)
        run: (bool) automatically runs QCCP instance and saves a QM schedule
    '''

    def __init__(self, graph, problem, algorithm, r = 1, w = 0, run = False):

        # Incorporate declared variables
        self.graph = graph
        self.problem = problem
        self.algorithm = algorithm
        self.r = r
        self.w = w

        if run == True:
            self.schedule = self.get_machine_schedule()
    
    def get_machine_schedule(self):

        # This is the EA search algorithm to optimize the machine schedule
        for i in range(self.r):
            if i==0:
                self.SGr = minimize(self.problem, self.algorithm)
            else:
                self.SGr = minimize(problem=self.SGr.problem, algorithm= self.algorithm)        
        #One more function here to compile a working machine schedule for IBM machine or Qiskit
        
        return schedule

