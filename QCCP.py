from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize
import networkx as nx
from quantum_devices import QuantumDevices
from QAOAproblems import QAOAmaxcut

class QCCP:
    '''
    QCCP: Quantum Circuit Compilation Problem - QAOA

    Generalized for any QAOA problem
    '''

    def __init__(self, graph, QM = 'IBM27q', r = 1, w = 0):
        '''
        graph: networkx Graph
        QM: (str = 'IBM27q', ...) Quantum Hardware to perform the job
        r: (int) rounds/layers
        w: Current connection weights measured on the quantum device
        '''

        self.graph = graph
        self.ps_gates = graph.edges
        self.permutation_dim = graph.number_of_edges()

        self.devices = QuantumDevices()
        self.hardware = self.devices(QM)
        
        self.r = r
        self.w = w

        if self.graph.num_nodes > self.hardware.number_of_nodes():
            print("Error: Job requires more qubits than available by choosen device.")
        
        # Assign problem nodes to hardware qubits
        #self.qubitmap = list(zip(self.graph.nodes, self.hardware.nodes)) # Usar lista simples
        self.qubitmap = range(len(self.hardware.nodes))
    
    def get_machine_schedule(self, algorithm = 'GA', problem = QAOAmaxcut):

        if chosen_algorithm == "GA":
            algorithm = GA(pop_size=11,
                  sampling=MySampling(),
                  crossover=MyCrossover(),
                  mutation=MyMutation(),
                  eliminate_duplicates=MyDuplicateElimination()
                )

        # This is the EA search algorithm to optimize the machine schedule
        for i in range(self.r):
            self.SGr = minimize(problem, algorithm) # This should also return updated qubitmap

            #SG = SG + SGr
        
        #One more function here to compile a working machine schedule for IBM machine or Qiskit
        
        return schedule

