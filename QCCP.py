from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize
import networkx as nx
from quantum_devices import QuantumDevices
from QAOAjob import QAOAjob

class QCCP:
    '''
    QCCP: Quantum Circuit Compilation Problem - QAOA

    Generalized for any QAOA problem
    '''
    
    def __init__(self, Job, QM = 'IBM27q', w = 0):
        '''
        job_list: Object containing the graph, list of jobs for the machine, the problem, and more
        QM: (str = 'IBM27q', ...) Quantum Hardware to perform the job
        w: Current connection weights measured on the quantum device
        r: (int) rounds/layers
        '''
        self.job = Job.job_list 
        self.qubits = Job.num_of_qubits
        self.graph = Job.graph
        self.num_nodes = self.graph.number_of_nodes()
        self.num_edges = self.graph.number_of_edges()

        self.devices = QuantumDevices()
        self.hardware = self.devices(QM)
        
        self.w = w

        if self.num_nodes > self.hardware.number_of_nodes():
            print("Error: Job requires more qubits than available by choosen device.")
        
        # Assign problem nodes to hardware qubits
        self.qubitmap = list(zip(self.graph.nodes, self.hardware.nodes)) # Pode ser melhor usar outro método
    
    def get_machine_schedule(self, algorithm = GA):

        # This is the EA search algorithm to optimize the machine schedule
        for i in range(self.r):
            self.SGr = minimize(self.problem, algorithm)
        
        return schedule

