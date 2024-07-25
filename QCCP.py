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
                #opt_f =self.SGr.F
                r_times = self.SGr.X[0].times
                r_map = self.SGr.X[0].qubitmap
                r_gates = self.SGr.X[0].ch1


                # sketch
                #opt_total = opt_total + opt_f
                #opt_circuit = self.makespan(r_times)
                #current_time =  extract from opt_circuit
                # update current time in problem
                #self.problem.current_time = current_time
                schedule = 0
            else:
                self.problem.initial_node_time = r_times
                self.problem.initial_map = r_map
                self.SGr = minimize(problem=self.problem, algorithm=self.algorithm)   
                r_times = self.SGr.X[0].times    

            print("current times: ", r_times) 
        #One more function here to compile a working machine schedule for IBM machine or Qiskit
        
        return schedule

