language = 'english' # english/french

base_folder = '/home/yl254115/Projects/'
base_folder = '/neurospin/unicog/protocols/intracranial/'

if language == 'english':
    script = base_folder + 'FAIRNS/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/extract-activations.py'
    model = base_folder + '/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt'
    input_data = base_folder + 'FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/RC_english_marco.txt'
    vocab = base_folder + 'FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/english_vocab.txt'
    output = base_folder + 'FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/RC_english_marco.pkl'
    eos = '"<eos>"'
    format = 'pkl'
    unk = '"<unk>"'
    lang = 'en'
    get_representations = 'lstm'
elif language == 'french':
    script = base_folder + 'FAIRNS/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/extract-activations.py'
    model = base_folder + '/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/activations/french/model2-500-2-0.5-SGD-10-tied.False-300/LSTM-corpora~frwac_random_100M_subset-500-2-0.5-SGD-10-tied.False-300/model.cpu.pt/model.cpu.pt'
    input_data = base_folder + 'FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/NP_VP_and_RC_filtered_perp.txt'
    vocab = base_folder + 'FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/activations/french/reduced-vocab.txt'
    output = base_folder + 'FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/activations/french/model2-500-2-0.5-SGD-10-tied.False-300/NP_VP_and_RC_filtered_perp'
    eos = '"</s>"'
    format = 'pkl'
    unk = '_UNK_'
    lang = 'fr'

cmd = 'python3 ' + script + ' ' + model + ' --input ' + input_data + ' --vocabulary ' + vocab + ' --output ' + output +\
                    ' --eos-separator ' + eos + ' --format ' + format + ' --use-unk' + ' --unk-token ' + unk + ' --lang ' + \
      lang + ' -g ' + get_representations + ' >extract_activation.log &'

# import os
# os.system(cmd)
print(cmd)