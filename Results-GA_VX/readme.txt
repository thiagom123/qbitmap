These files contain the results of the execution of the algorithm GA-VX presented in the manuscript "Solving Quantum Circuit Compilation Problem variants through Genetic Algorithms", whose authors are Lis Arufe, Riccardo Rasconi, Angelo Oddi, Ramiro Varela and Miguel A. González.

The compressed file contains directories "QCCP", "QCCPV", "QCCPX" and "QCCPVX", each containing the results of GA-VX in the four problem variants considered in the paper. Inside each directory, the name of each file indicates the chip size and the instance number, and then the "1000" is the population size used. Also, in the directory "New-Instances" we give the instances with 72 and 127 qubits, in particular in "QuantumHW" there are the json definition of the quantum chips, and in directories "N72" and "N127" we can find the 50 instances for each of those chip sizes.

The first line of each results file contains a summary of the results of 10 executions of the algorithm in the corresponding instance:
-First number: the makespan of the best solution found in the 10 runs.
-Second number: average makespan of the best solutions of the 10 runs.
-Third number: the worst makespan obtained, as best solution, in the 10 runs.
-Fourth number: standard deviation.
-Fifth number: total time (in seconds) of all 10 runs.
-Sixth number: total number of generations of all 10 runs.

The remaining of each file describes the best solution found in the 10 runs (i.e. a solution with a makespan equal to the first number of the first line of the file).

For each qstate (there may be 8, 21, 40, 72 or 127 depending on the chip size of the instance), there is a group of lines.

For each qstate we present the following information:
In the first line, the qstate identifier and the time in which the qstate ends all its activities. For example, "Makespan 1: 28" indicates that the qstate 1 ends all its activities at time 28. Then, a line indicating in which qubit that qstate starts at the beginning of the schedule (for example "Starts in 5"). Then, a number of lines corresponding to the number of gates in which that qstate is involved. Each line contains the following information:
1) The gate type (SWAP, PS, MIX)
2) The first involved qstate
3) The second involved qstate
4) Qubit in which the first involved qstate is currently located (just before the execution of the gate).
5) Qubit in which the second involved qstate is currently located (just before the execution of the gate).
6) Starting time of the gate in the schedule
7) Duration of the gate
Note: mix gates are special as there is only one qstate involved, and so in those gates 3) and 5) are omitted.

For example, the line "PS q1: 3 q2: 5 qb1: 8 qb2: 5 init: 25  time: 3;" indicates that it is executed the gate "p-s q3 q5", and initially the qstate q3 is located in qubit 8, and the qstate q5 is located in qubit 5. The gate starts its execution at time 25 and has a duration of 3 (therefore ending at time 28).


Example file: problem_N8_i10_1000.txt (from directory "QCCPVX")

========================
22 22.6 24 0.699206 61 8541

Makespan 1: 18
Starts in 2
PS q1: 1 q2: 2 qb1: 2 qb2: 1 init: 0  time: 3; 
SWAP q1: 4 q2: 1 qb1: 3 qb2: 2 init: 7  time: 2; 
SWAP q1: 1 q2: 3 qb1: 3 qb2: 5 init: 12  time: 2; 
PS q1: 1 q2: 7 qb1: 5 qb2: 8 init: 14  time: 3; 
MIX q1: 1 qb1: 5 init: 17  time: 1; 

Makespan 2: 21
Starts in 1
PS q1: 1 q2: 2 qb1: 2 qb2: 1 init: 0  time: 3; 
PS q1: 2 q2: 6 qb1: 1 qb2: 4 init: 4  time: 3; 
PS q1: 2 q2: 4 qb1: 1 qb2: 2 init: 9  time: 3; 
PS q1: 2 q2: 8 qb1: 1 qb2: 4 init: 12  time: 3; 
PS q1: 2 q2: 5 qb1: 1 qb2: 4 init: 17  time: 3; 
MIX q1: 2 qb1: 1 init: 20  time: 1; 

Makespan 3: 14
Starts in 5
SWAP q1: 1 q2: 3 qb1: 3 qb2: 5 init: 12  time: 2; 

....(it continues with the remaining qstates)....
========================