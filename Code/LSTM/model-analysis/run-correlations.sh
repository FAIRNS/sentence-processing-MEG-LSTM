for d in diff_all pos_diff_all neg_diff_all
do
    mkdir -p ~/projects/neurospin/sentence-processing-MEG-LSTM/Output/correlation/${d}
    echo ./plot-activations.py ~/projects/neurospin/data/lstm-activations/bnc_0313_20K-LSTM650-english.pkl ~/projects/neurospin/data/parsed-corpora/bnc_0313.pkl -t correlation -g ${d} -o ~/projects/neurospin/sentence-processing-MEG-LSTM/Output/correlation/${d}
done
