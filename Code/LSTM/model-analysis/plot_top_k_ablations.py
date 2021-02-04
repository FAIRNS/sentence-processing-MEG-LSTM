import argparse, os, pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

parser = argparse.ArgumentParser()
parser.add_argument('--path2models', type=str, default='/neurospin/unicog/protocols/LSTMology/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/models/italian')
parser.add_argument('--model-name_template', type=str, default='italian_hidden650_batch64_dropout0.2_lr20.0_seed')
parser.add_argument('--ablation-results', default = 'dict_ablation_results.pkl')
parser.add_argument('--output', default = '/neurospin/unicog/protocols/LSTMology/FAIRNS/sentence-processing-MEG-LSTM/Output/top_k_', help='Path to output folder')
parser.add_argument('--top-k', default=10)
args = parser.parse_args()


path2sentences = '../../../Data/Stimuli/nounpp_Italian_4000.info'
path2sentences_txt = '../../../Data/Stimuli/nounpp_Italian_4000.txt'

# Load ablation results and sentence metadata (info)
info = pickle.load(open(path2sentences, 'rb'))
# Find indices of the incogruent conditions
IXs = {}
IXs['SP'] = [i for (i, d) in enumerate(info) if (d['number_1'] == 'singular') and (d['number_2'] == 'plural')]
IXs['PS'] = [i for (i, d) in enumerate(info) if (d['number_1'] == 'plural') and (d['number_2'] == 'singular')]



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
print(df)

################
def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)
cmap = get_cmap(20)

results = {}
fig, ax = plt.subplots(figsize=(10,10))
for i_seed, seed in enumerate(list(range(1, 20)) + ['K']):
    results[seed] = {}
    for condition in ['SP', 'PS']:
        ls = {'SP':'-', 'PS':'--'}[condition]
        results[seed][condition] = []
        #print(condition)
        df_curr_model_condition = df.loc[(df.seed==f'Model {seed}') & (df.Condition == condition)]
        df_sorted = df_curr_model_condition.sort_values(by=['error'], ascending=False)
        top_k_units = df_sorted.head(args.top_k).unit.tolist()
        for k in range(args.top_k):
            #if k==0: print(seed, k, condition, top_k_units[0], df_sorted['performance'].head(1))
            if seed == 'K':
                color = 'grey'
                model_fn = f'{args.model_name_template}_{seed}.pt'
            else:
                color = cmap(i_seed)
                # *** In filenames of the model the counting is from zero ***
                model_fn = f'{args.model_name_template}_{seed-1}.pt' 
            path2model = f'{args.path2models}/{model_fn}'
            units = '_'.join(map(str, top_k_units[:(k+1)]))
            fn_abl_results = f'{args.output}{os.path.basename(path2model)}{units}_groupsize_1_seed_1.abl'
            # Load results
            try:
                abl_results = pickle.load(open(fn_abl_results, 'rb'))
                acc = np.sum((abl_results['log_p_targets_correct'][IXs[condition]] - abl_results['log_p_targets_wrong'][IXs[condition]]) > 0)/len(IXs[condition])
            except:
                acc = np.nan
            results[seed][condition].append(acc)
            print(f'Seed {seed} {condition} k {k}: {acc}')
        ax.plot(results[seed][condition], label=f'Model {seed} {condition}', color=color, ls=ls, lw=3)

ax.set_xlabel('Number of ablated units', fontsize=16)
ax.set_ylabel('Performance on the NA-taks', fontsize=16)
ax.set_xticks(range(args.top_k))
ax.set_xticklabels(range(1, args.top_k))
ax.xaxis.grid(True)
ax.axhline(0.5, ls='--', color='k')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.savefig('perf_top_k_ablation.png')
                    

