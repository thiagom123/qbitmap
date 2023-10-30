def decoding_2022(P, QM, ch1, ch2, SG, w, current_q):
    '''
    P: Problem instance with P rounds
    QM: (Graph/Matrix) Quantum Hardware
    ch1: ps(q_i, q_j) (Lista de duplas indicando as portas)
    ch2: {n_k, n_l} (Lista de duplas indicando os qubits do hardware)
    SG: Solução parcial do round anterior
    w: lista de pesos das portas (Talvez fique separado)
    '''
    SGr=SG
    n = len(ch1)
    #for each p-s(q_i, q_j) in ch1
    for k in n:
        q_i = ch1[k][0]
        q_j = ch1[k][1]
        n_k = ch2[k][0]
        n_l = ch2[k][1]
        n_qi = current_q[q_i]
        n_qj = current_q[q_j]  
        path_i = MinimalPath(q_i, n_k, QM)
        path_j = MinimalPath(q_j, n_l, QM)
        while (n_qi!=n_k) or (n_qj!=n_l):
            n, n1 = n_qi, n_qj
            if [n_qi, Sucessor(n_qi, path_i)]!=[n_qi, n_qj]:
                n, n1 = n_qi, Sucessor(n_qi, path_i)
            elif [n_qi, Sucessor(n_qj, path_j)]!=[n_qj, n_qi]:
                n, n1 = n_qj, Sucessor(n_qj, path_j)
            
    
       
       while ()


    return SGr, current_q


def SelectSwaps(sg, ps, X):
    qi = ps[0]
    qj = ps[1]
    if X>=0 and X<1:
        #Meeting POint

    if X==-1:
        #EST
    return 

def decoding_2023(P, QM, ch1, ch2, SG, w):
    '''
    P: Problem instance with P rounds
    QM: (Graph/Matrix) Quantum Hardware
    ch1: ps(q_i, q_j) (Lista de duplas indicando as portas)
    ch2: {n_k, n_l} (Lista de duplas indicando os qubits do hardware)
    SG: Solução parcial do round anterior
    w: lista de pesos das portas (Talvez fique separado)
    '''
    SGr=SG
    n = len(ch1)
    for k in n:
        swaps = Select_Swaps
    for sw in swaps:
        #insert swap gate in SGr
    #insert gate p-s(qi, qj) on qubits d(qi), d(qj) in sgr
    


    return SGr


