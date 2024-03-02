from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize

class QCCP:
    '''
    QCCP: Quantum Circuit Compilation Problem - QAOA

    Generalized for any QAOA problem

    INPUT
    hamiltonian: PS gates in one layer (might need MIX gates as well)
    QM = Quantum Hardware
    w = measured weights for the quantum machine
    r: (int) rounds/layers

    '''
    def __init__(self, hamiltonian, QM, w, r=1):
        self.qm = QM
        self.circuit = hamiltonian
        self.w = w
        self.r = r

        '''
        self.num_qubits = 
        if (# qubits em QM) < (num_qubits):
         error: hamiltoniana tem mais qubits que o chip escolhido, escolher outro hardware
        '''

        #self.qbitmap = assign_qubits()
        #self.problem = generate_pymoo_problem()
    
    def generate_pymoo_problem(self):
        '''
        This will set the problem on pymoo format, (decoding scheme goes here?)
        '''

        return problem
    
    def assign_qubits(self):
        # Do initial assignment of QM qubits for the hamiltonian
    
    def get_machine_schedule(self, algorithm = GA):
        for i in range(self.r):
            self.SGr = minimize(self.problem, algorithm)
        
        return schedule

