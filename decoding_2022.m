function SGr = decoding_2022(P, QM, ch1, ch2, SG, w)
    SGr = SG;
    n = length(ch1);
    for k = 1:n
        q_i = ch1(k, 1);
        q_j = ch1(k, 2);
        n_k = ch2(k, 1);
        n_l = ch2(k, 2);
        n_qi = SGr.current_qubit(q_i);
        n_qj = SGr.current_qubit(q_j);
        path_i = MinimalPath(n_qi, n_k, QM);
        path_j = MinimalPath(n_qj, n_l, QM);
        while (n_qi ~= n_k) || (n_qj ~= n_l)
            n = n_qi;
            n1 = n_qj;
            succ_i = Sucessor(n_qi, path_i);
            succ_j = Sucessor(n_qj, path_j);
            if ~isequal([n_qi, succ_i], [n_qi, n_qj])
                n = n_qi;
                n1 = succ_i;
            elseif ~isequal([n_qi, succ_j], [n_qj, n_qi])
                n = n_qj;
                n1 = succ_j;
            end
            if ~isequal([n, n1], [n_qi, n_qj])
                SGr = add_swap(SGr, n, n1);
                n = n1;
            else
                sub_pathi = path_i(find(path_i == n):end);
                sub_pathj = path_j(find(path_j == n):end);
                path_i = [path_i(1:find(path_i == n)-1), sub_pathj];
                path_j = [path_j(1:find(path_j == n)-1), sub_pathi];
            end
        end
        SGr = add_ps(SGr, n_k, n_l);
    end
    SGr = add_mix(SGr);
end


