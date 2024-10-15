These files contain the results of the execution of the algorithm DBGA presented in the manuscript "Quantum Circuit Compilation by Genetic Algorithm for Quantum Approximate Optimization Algorithm applied to MaxCut Problem", whose authors are Lis Arufe, Miguel A. González, Angelo Oddi, Riccardo Rasconi and Ramiro Varela.

The compressed file contains several directories, each containing the results of DBGA of one of the Tables of the manuscript (Tables 2, 3, 4, 5 and 6). Inside each directory, the name of each file indicates the chip size and the instance number. Also, in the directory "Table 6" there are the json definition of the adapted instances used in that Table.

The first line of each results file contains a summary of the results of 10 executions of the algorithm in the corresponding instance:
-First number: the makespan of the best solution found in the 10 runs.
-Second number: in how many of the 10 runs, a solution with that makespan has been found.
-Third number: average makespan of the best solutions of the 10 runs.
-Fourth and fifth numbers: the most repeated best result in the 10 runs, and how many times it appeared (it might be the same as the best or worse solutions).
-Sixth and seventh numbers: the worst makespan obtained in the 10 runs, and in how many of the 10 runs a best result with that makespan has been found.
-Eight number: standard deviation.
-Ninth number: total time (in seconds) of all 10 runs.
-Number 10: total time (in seconds) of all 10 runs optimizing only the first compilation pass (the execution is divided in two rounds, as it is a decomposition-based algorithm).
-Number 11: total number of generations from all runs.
-Number 12: total number of generations from all runs optimizing only the first compilation pass (the execution is divided in two rounds, as it is a decomposition-based algorithm).
-Number 13: it is always 0.

The remaining of each file describes the best solution found in the 10 runs (i.e. a solution with a makespan equal to the first number of the first line of the file).

For each qstate (there may be 8, 21 or 40, depending on the chip size of the instance), there is a group of lines.

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
Note: mix gates are special as there is only one qstate involved. In those gates 3) is always zero, and 5) is always equal to 4).

For example, the line "p-s q1: 3 q2: 5 qb1: 8 qb2: 5 init: 25  time: 3;" indicates that it is executed the gate "p-s q3 q5", and initially the qstate q3 is located in qubit 8, and the qstate q5 is located in qubit 5. The gate starts its execution at time 25 and has a duration of 3 (therefore ending at time 28).


Example file: problem_N8_i4.txt (from directory "Table 2")

========================
32 1 33.1 33 7 34 2 0.567646 52 23 16304 8001 0

Makespan 1: 28
swap q1: 2 q2: 1 qb1: 2 qb2: 1 init: 4  time: 2; 
p-s q1: 1 q2: 2 qb1: 2 qb2: 1 init: 9  time: 3; 
mix q1: 1 q2: 0 qb1: 2 qb2: 2 init: 12  time: 1; 
p-s q1: 1 q2: 2 qb1: 2 qb2: 1 init: 13  time: 3; 
mix q1: 1 q2: 0 qb1: 2 qb2: 2 init: 16  time: 1; 
swap q1: 2 q2: 1 qb1: 1 qb2: 2 init: 21  time: 2; 
swap q1: 5 q2: 1 qb1: 2 qb2: 1 init: 26  time: 2; 

Makespan 2: 32
p-s q1: 2 q2: 3 qb1: 2 qb2: 3 init: 0  time: 4; 
swap q1: 2 q2: 1 qb1: 2 qb2: 1 init: 4  time: 2; 
p-s q1: 2 q2: 6 qb1: 1 qb2: 4 init: 6  time: 3; 
p-s q1: 1 q2: 2 qb1: 2 qb2: 1 init: 9  time: 3; 
mix q1: 2 q2: 0 qb1: 1 qb2: 1 init: 12  time: 1; 
p-s q1: 1 q2: 2 qb1: 2 qb2: 1 init: 13  time: 3; 
p-s q1: 2 q2: 6 qb1: 1 qb2: 4 init: 18  time: 3; 
swap q1: 2 q2: 1 qb1: 1 qb2: 2 init: 21  time: 2; 
swap q1: 2 q2: 5 qb1: 2 qb2: 3 init: 24  time: 2; 
p-s q1: 2 q2: 3 qb1: 3 qb2: 5 init: 27  time: 4; 
mix q1: 2 q2: 0 qb1: 3 qb2: 3 init: 31  time: 1; 

....(it continues with the remaining qstates)....
========================