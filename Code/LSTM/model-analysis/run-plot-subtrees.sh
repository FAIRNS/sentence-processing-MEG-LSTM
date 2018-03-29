for fn in ADJP_3t_100 ADVP_3t_100 ADXP_3t_100 all_3t_100
do
    echo python ./plot-activations.py ~/projects/neurospin/data/subtrees/${fn}.activations.pkl \
        ~/projects/neurospin/data/subtrees/${fn}.pkl -t categories -g pattern \
        -o ~/projects/neurospin/sentence-processing-MEG-LSTM/Figures/subtrees/${fn} \
        --lock-vectors tree-pos
done

