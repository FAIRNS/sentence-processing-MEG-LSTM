for d in diff_all pos_diff_all neg_diff_all
do
    mkdir -p ~/projects/neurospin/sentence-processing-MEG-LSTM/Output/correlation-${d}
    echo ./plot-activations.py ~/projects/neurospin/data/lstm-activations/bnc_0313_SNPVP_20K-LSTM650-english.pkl ~/projects/neurospin/data/parsed-corpora/bnc_0313_SNPVP_20K.pkl -t correlation -g ${d} -o ~/projects/neurospin/sentence-processing-MEG-LSTM/Output/correlation-${d} --decorrelate sentence-length
done
for d in diff_all pos_diff_all neg_diff_all
do
    mkdir -p ~/projects/neurospin/sentence-processing-MEG-LSTM/Output/correlation-diffact-${d}
    echo ./plot-activations.py ~/projects/neurospin/data/lstm-activations/bnc_0313_SNPVP_20K-LSTM650-english.pkl ~/projects/neurospin/data/parsed-corpora/bnc_0313_SNPVP_20K.pkl -t correlation -g ${d} -o ~/projects/neurospin/sentence-processing-MEG-LSTM/Output/correlation-diffact-${d} --decorrelate sentence-length
done
