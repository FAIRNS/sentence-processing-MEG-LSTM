import argparse, os, pickle
import pandas as pd
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

parser = argparse.ArgumentParser()
parser.add_argument('--path2models', type=str, default='/neurospin/unicog/protocols/LSTMology/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/models/italian')
parser.add_argument('--model-name_template', type=str, default='italian_hidden650_batch64_dropout0.2_lr20.0_seed')
parser.add_argument('--vocabulary', default='/neurospin/unicog/protocols/LSTMology/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/models/italian/Italian_vocab.txt')
parser.add_argument('--sentences', default='/neurospin/unicog/protocols/LSTMology/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/Italian_nounpp_4000', help='Input sentences in Tal\'s format')
parser.add_argument('--ablation-results', default = 'dict_ablation_results.pkl')
parser.add_argument('--output', default = '/neurospin/unicog/protocols/LSTMology/FAIRNS/sentence-processing-MEG-LSTM/Output/top_k_', help='Path to output folder')
parser.add_argument('--top-k', default=10)
parser.add_argument('--language', default='it')
args = parser.parse_args()

if args.output: # create output folder
    os.makedirs(os.path.dirname(args.output), exist_ok=True)


def load_ablation_results(path2results):
    
    dict_ablation_results = pickle.load(open(path2results, 'rb'))
    df = {}
    df['seed'] = []
    df['unit'] = []
    df['Condition'] = []
    df['performance'] = []
    for s in dict_ablation_results.keys():
        if s != 'K':
            ss = str(int(s) + 1)
        else:
            ss = s
        for u in dict_ablation_results[s].keys():
            df['seed'].append('Model ' + ss)
            df['unit'].append(u)
            df['Condition'].append('SP')
            df['performance'].append(dict_ablation_results[s][u]['SP'])
            df['seed'].append('Model ' + ss)
            df['unit'].append(u)
            df['Condition'].append('PS')
            df['performance'].append(dict_ablation_results[s][u]['PS'])
    
    df = pd.DataFrame(df)
    df['error'] = df.apply(lambda row: 1-row['performance']['accuracy'], axis=1)
    
    return df

##########################################

df = load_ablation_results(args.ablation_results)
#print(df)
for seed in list(range(1, 20)) + ['K']:
    for condition in ['SP', 'PS']:
        #print(condition)
        df_curr_model_condition = df.loc[(df.seed==f'Model {seed}') & (df.Condition == condition)]
        df_sorted = df_curr_model_condition.sort_values(by=['error'], ascending=False)
        top_k_units = df_sorted.head(args.top_k).unit.tolist()
        for k in range(args.top_k):
            #if k==0: print(seed, k, condition, top_k_units[0], df_sorted['performance'].head(1))
            if seed == 'K':
                model_fn = f'{args.model_name_template}_{seed}.pt'
            else:
                # *** In filenames of the model the counting is from zero ***
                model_fn = f'{args.model_name_template}_{seed-1}.pt' 
            path2model = f'{args.path2models}/{model_fn}'
            units = ''
            for unit in top_k_units[:(k+1)]:
                units += f' --unit {unit}'
            output = args.output + os.path.basename(path2model)
            jobname = f'{seed}_{condition}_{k}'
            cmd = f'python /neurospin/unicog/protocols/LSTMology/FAIRNS/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/ablation-experiment.py {path2model} --input {args.sentences} --vocabulary {args.vocabulary} --output {output} {units} --lang {args.language} --do-ablation'
            cmd = f'echo {cmd} | qsub -q Nspin_long -N {jobname} -l walltime=02:00:00 -o logs/{jobname}.out -e logs/{jobname}.err'
            print(cmd)
