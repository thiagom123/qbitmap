#SGr seria o subgrafo que resolve o problema para o round r.
#Ele salva o current qubit de cada qstate, além do current depth
#Tem metodos para adicionar mix, swaps e p-s



def decoding_2022(P, QM, ch1, ch2, SG, w):
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
        #pegar os q's e n's
        q_i = ch1[k][0]
        q_j = ch1[k][1]
        n_k = ch2[k][0]
        n_l = ch2[k][1]
        #pegar o qubit atual dos qstates
        n_qi = SGr.qubitmap[q_i]
        n_qj = SGr.qubitmap[q_j]
        #pair of minimal paths from {𝑛(𝑞𝑖), 𝑛(𝑞𝑗)} to {𝑛𝑘, 𝑛𝑙} in 𝑄𝑀 
        # Talvez tenha um problema aqui, que é nessa diferença entre o d(q_i) pro n_k
        # Tem que analisar como vai ser calculado o minimal path
        path_i = MinimalPath(n_qi, n_k, QM)
        path_j = MinimalPath(n_qj, n_l, QM)
        while (n_qi!=n_k) or (n_qj!=n_l):
            n, n1 = n_qi, n_qj
            #(𝑛, 𝑛′) ← (𝑛(𝑞𝑖), 𝑠𝑢𝑐𝑐(𝑛(𝑞𝑖)) or (𝑛(𝑞𝑗), 𝑠𝑢𝑐𝑐(𝑛(𝑞𝑗)) if possible such
            #that {𝑛, 𝑛′} ≠ {𝑛(𝑞𝑖), 𝑛(𝑞𝑗)};
            #Tem que rever essa condicional aqui, talvez tenha que ser conjunto?
            #Sucessor é apenas sucessor em uma lista
            succ_i = Sucessor(n_qi, path_i)
            succ_j = Sucessor(n_qj, path_j)
            if [n_qi, succ_i]!=[n_qi, n_qj]:
                n, n1 = n_qi, succ_i
            elif [n_qj, succ_j]!=[n_qj, n_qi]:
                n, n1 = n_qj, succ_j
            #if {𝑛, 𝑛′} ≠ {𝑛(𝑞𝑖), 𝑛(𝑞𝑗)} then
            #insert a 𝑠𝑤𝑎𝑝 gate on qubits {𝑛, 𝑛′} and update 𝑠𝑔𝑟;
            #𝑛 ← 𝑛′; // advance in 𝑝𝑎𝑡ℎ1 or in 𝑝𝑎𝑡ℎ2
            #Ajeitar condicional
            if [n, n1] != [n_qi, n_qj]:
                SGr.add_swap(n, n1)
                n = n1
            else:
                #swap in 𝑝𝑎𝑡ℎ1 and 𝑝𝑎𝑡ℎ2 the subpaths from the current qubits
                #𝑛 and 𝑛′ to their destination qubits, so that the new paths
                #become 𝑛, 𝑛′ ⇝ 𝑛𝑏 and 𝑛′ ⇝ 𝑛𝑎 if the old paths were 𝑛, 𝑛′ ⇝ 𝑛𝑎
                #and 𝑛′ ⇝ 𝑛𝑏 respectively;
                #TEM QUE VERIFICAR O CÓDIGO
                sub_pathi = path_i[path_i.index(n):]
                sub_pathj = path_j[path_j.index(n):]
                path_i = path_i[:path_i.index(n)]+sub_pathj
                path_j = path_j[:path_j.index(n)]+sub_pathi
                
        #insert a p-s gate on qubits {𝑛𝑘, 𝑛𝑙} (where qstates {𝑞𝑖, 𝑞𝑗} are nowhold) and update 𝑠𝑔𝑟;
        SGr.add_ps(n_k, n_l)
    #insert mix in all qubits holding a qstate
    SGr.add_mix()
    return SGr


## DECODING de 2023

def ShortestPaths(G, a, b):
    '''
    Return all the shortest paths
    '''
    return []



def SelectSwaps(SGr, ps, X, QM):
    qi = ps[0]
    qj = ps[1]
    #path é uma lista de listas
    paths, dist_ij = ShortestPaths(QM, qi, qj)
    if X>=0 and X<1:
        #Meeting POint
        z = floor(X*dist_ij)+1
        #making distij−z moves from n(qi) towards n(qj)
        #z −1 moves from n(qj) towards n(qi).
        for i in range(dist_ij):
            if(i<dist_ij-z):
                #move n(qi) towards n(qj)
                path = ChoosePath(paths, "start", SGr)
                SGr.add_swaps(path[i], path[i+1])
            else:
                #n(qj) towards n(qi)
                path = ChoosePath(paths, "end", SGr)
                SGr.add_swaps(path[dist_ij-i], path[dist_ij-i-1])

    if X==-1:
        #EST
        for i in range(dist_ij):
            n_1 = paths[i]
            n_2 = paths[dist_ij-i]

    return 

def decoding_2023(QM, ch1, ch2, SG, w):
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
        #pegar o qubit atual dos qstates
        q_i = ch1[k][0]
        q_j = ch1[k][1]
        swaps, [dq_i, dq_j] = Select_Swaps(SGr, ch1[k], ch2[k], QM)
        for sw in swaps:
            SGr.add_swaps(sw[0], sw[1])
            #update current positions
        #insert gate p-s(qi, qj) on qubits d(qi), d(qj) in sgr
        SGr.add_ps(dq_i, dq_j)
    SGr.add_mix()


    return SGr


