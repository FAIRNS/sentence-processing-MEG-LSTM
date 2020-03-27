import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# from functions import plotting


##################################
### LOAD RESULTS TO DATA FRAME ###
##################################
fn = 'SC_OR_and_OR_OR.csv'
df = pd.read_csv(fn, dtype={'accuracy':float})

# FIX/ADD STUFF
df['error_rate'] =  df.apply(lambda row: 1-row['accuracy'], axis=1)
df['verb_position'] =  df.apply(lambda row: row['sentence_type'].split('_')[-1], axis=1)
df['sentence_type'] =  df.apply(lambda row: row['sentence_type'][0:5], axis=1)
df['condition'] =  df.apply(lambda row: row['condition'].strip(), axis=1)
def is_congruent_subjects(row):
    if (row['condition'][0:2]=='SS') | (row['condition'][0:2]=='PP'):
        return True
    else:
        return False
df['congruent_subjects'] =  df.apply(lambda row: is_congruent_subjects(row), axis=1)

# FILTER
# df = df.loc[(df['congruent_subjects']==True)]
print(df)
# PLOT
fig, ax = plt.subplots()
sns.barplot(x='verb_position', y='error_rate', hue='sentence_type', data=df, ax=ax)#, hue_order=hue_order, palette=palette)
ax.set_xlabel('')
ax.set_ylabel('Error Rate')
ax.set_xticklabels(['Outer Verb', 'Middle Verb', 'Inner Verb'])
plt.show()