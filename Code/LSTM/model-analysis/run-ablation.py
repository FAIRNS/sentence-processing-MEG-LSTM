# Paths
script = "$HOME/projects/neurospin/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/ablation-experiment.py"
model = "/checkpoint/germank/neurospin/data/trained-english-models/hidden650_batch128_dropout0.2_lr20.0.pt"
agreement_data = "$HOME/projects/neurospin/sentence-processing-MEG-LSTM/Data/agreement-data/best_model.tab"
vocab = "$HOME/projects/neurospin/data/trained-english-models/vocab.txt"
output = "$HOME/projects/neurospin/shared-data/ablation/ablation_results_killing_unit_"
eos = '"<eos>"'
format = 'pkl'
unit_to_kill_from = 776
unit_to_kill_to = 777

for seed in range(1):
    g = 1 # group size of units to kill in including random ones

    cmd = "$HOME/.conda/envs/localconda/bin/python " + script + ' ' + model + ' --input ' + agreement_data + ' --vocabulary ' + vocab + ' --output ' + output +\
                        ' --eos-separator ' + eos + ' --format ' + format + ' -uf ' + str(unit_to_kill_from) + ' -ut ' + str(unit_to_kill_to) + ' -g '\
          + str(g) + ' -s ' + str(seed) + ' --cuda'
    print(cmd)
