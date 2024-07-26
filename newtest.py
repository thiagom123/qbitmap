from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.problems import get_problem
from pymoo.optimize import minimize

from QAOAproblems import QAOAmaxcut
from CustomOperators import MySampling, MyPMX

problem = QAOAmaxcut

algorithm = GA(
    pop_size= 10,
    sampling= MySampling,
    crossover=MyPMX
)

res = minimize(problem,
               algorithm,
               seed=1,
               verbose=False)

## ACHO QUE PODEMOS DELETAR ESSE ARQUIVO