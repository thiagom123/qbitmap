These files contain the results of the execution of the algorithm DBGA-X presented in the manuscript "New Coding Scheme to Compile Circuits for Quantum Approximate Optimization Algorithm by Genetic Evolution", whose authors are Lis Arufe, Riccardo Rasconi, Angelo Oddi, Ramiro Varela and Miguel A. González.

The compressed file contains directories "DBGA-X-P2" and "DBGA-X-P5", each containing the results of DBGA-X in instances considering p=2 and p=5 respectively. Inside each directory, the name of each file indicates the chip size and the instance number, and then the "1000" is the population size used. Also, in the directory "New-Instances" we give the new benchmark proposed in the paper, in particular in "QuantumHW" there are the json definition of the new quantum chips considered in the paper, i.e. those with 72 and 127 qubits, and in directories "N72" and "N127" we can find the 50 proposed instances for both chip sizes.

The first line of each results file contains a summary of the results of 10 executions of the algorithm in the corresponding instance:
-First number: the makespan of the best solution found in the 10 runs.
-Second number: in how many of the 10 runs, a solution with that makespan has been found.
-Third number: average makespan of the best solutions of the 10 runs.
-Fourth and fifth numbers: the most repeated best result in the 10 runs, and how many times it appeared (it might be the same as the best or worse solutions).
-Sixth and seventh numbers: the worst makespan obtained in the 10 runs, and in how many of the 10 runs a best result with that makespan has been found.
-Eight number: standard deviation.
-Ninth number: total time (in seconds) of all 10 runs.
-Tenth number: total number of generations of all 10 runs.
-Numbers 11 to 14: they are always 0 and can be ignored

The remaining of each file describes the best solution found in the 10 runs (i.e. a solution with a makespan equal to the first number of the first line of the file).

For each qstate (there may be 8, 21, 40, 72 or 127 depending on the chip size of the instance), there is a group of lines.

For each qstate we present the following information:
In the first line, the qstate identifier and the time in which the qstate ends all its activities. For example, "Makespan 1: 28" indicates that the qstate 1 ends all its activities at time 28.
Then, a number of lines corresponding to the number of gates in which that qstate is involved. Each line contains the following information:
1) The gate type (swap, p-s, mix)
2) The first involved qstate
3) The second involved qstate
4) Qubit in which the first involved qstate is currently located (just before the execution of the gate).
5) Qubit in which the second involved qstate is currently located (just before the execution of the gate).
6) Starting time of the gate in the schedule
7) Duration of the gate
Note: mix gates are special as there is only one qstate involved, and so in those gates 3) and 5) are omitted.

For example, the line "p-s q1: 3 q2: 5 qb1: 8 qb2: 5 init: 25  time: 3;" indicates that it is executed the gate "p-s q3 q5", and initially the qstate q3 is located in qubit 8, and the qstate q5 is located in qubit 5. The gate starts its execution at time 25 and has a duration of 3 (therefore ending at time 28).


Example file: problem_N8_i4_1000.txt (from directory "P5")

========================
76 1 78.7 81 4 81 4 2.05751 35 10236 0 0 0 0

Makespan 1: 72
SWAP q1: 2 q2: 1 qb1: 1 qb2: 2 init: 4  time: 2; 
PS q1: 1 q2: 2 qb1: 2 qb2: 1 init: 9  time: 3; 
MIX q1: 1 qb1: 2 init: 12  time: 1; 
PS q1: 1 q2: 2 qb1: 2 qb2: 1 init: 13  time: 3; 
MIX q1: 1 qb1: 2 init: 16  time: 1; 
SWAP q1: 1 q2: 4 qb1: 1 qb2: 2 init: 18  time: 2; 
PS q1: 1 q2: 2 qb1: 1 qb2: 4 init: 42  time: 3; 
MIX q1: 1 qb1: 1 init: 45  time: 1; 
PS q1: 1 q2: 2 qb1: 1 qb2: 4 init: 46  time: 3; 
MIX q1: 1 qb1: 1 init: 49  time: 1; 
PS q1: 1 q2: 2 qb1: 1 qb2: 4 init: 68  time: 3; 
MIX q1: 1 qb1: 1 init: 71  time: 1; 

Makespan 2: 76
PS q1: 2 q2: 3 qb1: 2 qb2: 3 init: 0  time: 4; 
SWAP q1: 2 q2: 1 qb1: 1 qb2: 2 init: 4  time: 2; 
PS q1: 2 q2: 6 qb1: 1 qb2: 4 init: 6  time: 3; 
PS q1: 1 q2: 2 qb1: 2 qb2: 1 init: 9  time: 3; 
MIX q1: 2 qb1: 1 init: 12  time: 1; 
PS q1: 1 q2: 2 qb1: 2 qb2: 1 init: 13  time: 3; 
SWAP q1: 2 q2: 4 qb1: 4 qb2: 1 init: 16  time: 2; 
PS q1: 2 q2: 6 qb1: 4 qb2: 6 init: 19  time: 4; 
SWAP q1: 2 q2: 6 qb1: 6 qb2: 4 init: 23  time: 2; 
SWAP q1: 2 q2: 7 qb1: 7 qb2: 6 init: 25  time: 2; 
PS q1: 2 q2: 3 qb1: 7 qb2: 8 init: 27  time: 3; 
MIX q1: 2 qb1: 7 init: 30  time: 1; 
PS q1: 2 q2: 3 qb1: 7 qb2: 8 init: 31  time: 3; 
SWAP q1: 7 q2: 2 qb1: 7 qb2: 6 init: 34  time: 2; 
PS q1: 2 q2: 6 qb1: 6 qb2: 4 init: 36  time: 4; 
SWAP q1: 2 q2: 6 qb1: 4 qb2: 6 init: 40  time: 2; 
PS q1: 1 q2: 2 qb1: 1 qb2: 4 init: 42  time: 3; 
MIX q1: 2 qb1: 4 init: 45  time: 1; 
PS q1: 1 q2: 2 qb1: 1 qb2: 4 init: 46  time: 3; 
PS q1: 2 q2: 6 qb1: 4 qb2: 6 init: 49  time: 4; 
SWAP q1: 2 q2: 6 qb1: 6 qb2: 4 init: 53  time: 2; 
SWAP q1: 2 q2: 7 qb1: 7 qb2: 6 init: 55  time: 2; 
PS q1: 2 q2: 3 qb1: 7 qb2: 8 init: 57  time: 3; 
MIX q1: 2 qb1: 7 init: 60  time: 1; 
PS q1: 2 q2: 3 qb1: 7 qb2: 8 init: 61  time: 3; 
SWAP q1: 2 q2: 7 qb1: 6 qb2: 7 init: 64  time: 2; 
SWAP q1: 2 q2: 6 qb1: 4 qb2: 6 init: 66  time: 2; 
PS q1: 1 q2: 2 qb1: 1 qb2: 4 init: 68  time: 3; 
PS q1: 2 q2: 6 qb1: 4 qb2: 6 init: 71  time: 4; 
MIX q1: 2 qb1: 4 init: 75  time: 1; 

....(it continues with the remaining qstates)....
========================