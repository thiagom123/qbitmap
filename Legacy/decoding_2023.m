function SGr = decoding_2023(QM, ch1, ch2, SG, w)
    SGr = SG;
    n = length(ch1);

    for k = 1:n
        q_i = ch1(k, 1);
        q_j = ch1(k, 2);
        [swaps, dq] = SelectSwaps(SGr, ch1(k, :), ch2(k, :), QM);
        for sw = 1:length(swaps)
            SGr = add_swaps(SGr, swaps(sw, 1), swaps(sw, 2));
        end
        SGr = add_ps(SGr, dq(1), dq(2));
    end
    SGr = add_mix(SGr);
end



function SGr = SelectSwaps(SGr, ps, X, QM)
    qi = ps(1);
    qj = ps(2);
    [paths, dist_ij] = ShortestPaths(QM, qi, qj);
    if X >= 0 && X < 1
        z = floor(X * dist_ij) + 1;
        for i = 1:dist_ij
            if i < dist_ij - z
                path = ChoosePath(paths, 'start', SGr);
                SGr = add_swaps(SGr, path(i), path(i+1));
            else
                path = ChoosePath(paths, 'end', SGr);
                SGr = add_swaps(SGr, path(dist_ij - i), path(dist_ij - i - 1));
            end
        end
    end
    
    if X == -1
        for i = 1:dist_ij
            n_1 = paths(i);
            n_2 = paths(dist_ij - i);
        end
    end
end

