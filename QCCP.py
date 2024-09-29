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

        '''
            This is the EA search algorithm to optimize the machine schedule.
            
            For any QAOA, a GA will optimize the time cost of all necessary
            operations in the quantum machine for each depth r.
        ''' 
        r_gates = []
        r_qubits = []
        for round in range(self.r):
            print("round ", round)
            print("current times: ", self.problem.initial_node_times) 

            self.SGr = minimize(self.problem, self.algorithm)
            

            # save partial results
            r_times = self.SGr.X[0].times # optimal times for each gate operation
            print("r_times", r_times)
            r_map = self.SGr.X[0].qubitmap # current node-qubit mapping
            r_gates.append(self.SGr.X[0].ch1) # this rounds optimal operations order
            r_qubits.append(self.SGr.X[0].ch2)

            # Update operations time and mapping for the next round
            self.problem.initial_node_times = r_times
            self.problem.initial_map = r_map

            
        print("final times: ", self.problem.initial_node_times) 
        schedule = self.create_QM_circuit()
        
        return schedule
    
    def create_QM_circuit(self): 
        schedule = "work in progress"
        return schedule

