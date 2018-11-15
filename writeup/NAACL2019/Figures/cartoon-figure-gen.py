import matplotlib.pyplot as plt
plt.rc('text', usetex=False)
plt.rc('font', family='serif')

sentence = 'The \\textbf{boy(s)} near the \\underline{car(s)} \\textbf{greet(s)}'.split()

# nouns and verb positions
N1=1
N2=4
V=5
off = .1
SS_off= off+off/2
SP_off = off/2
PS_off= -off/2
PP_off = -off-off/2


# define series values
SS_sugg = [0 + SS_off]*len(sentence)
SS_sugg[N1] = 1 + SS_off
SS_sugg[N2] = 1 + SS_off
PS_sugg = [0 + PS_off]*len(sentence)
PS_sugg[N1] = -1 + PS_off
PS_sugg[N2] = 1 + PS_off
SP_sugg = [0 + SP_off]*len(sentence)
SP_sugg[N1] = 1 + SP_off
SP_sugg[N2] = -1 + SP_off
PP_sugg = [0 + PP_off]*len(sentence)
PP_sugg[N1] = -1 + PP_off
PP_sugg[N2] = -1 + PP_off

SS_input = [0 + SS_off]*len(sentence)
SS_input[N1] = 1 + SS_off
SS_input[N2] = 0 + SS_off
PS_input = [0 + PS_off]*len(sentence)
PS_input[N1] = 1 + PS_off
PS_input[N2] = 0 + PS_off
SP_input = [0 + SP_off]*len(sentence)
SP_input[N1] = 1 + SP_off
SP_input[N2] = 0 + SP_off
PP_input = [0 + PP_off]*len(sentence)
PP_input[N1] = 1 + PP_off
PP_input[N2] = 0 + PP_off

SS_forget = [1 + SS_off]*len(sentence)
SS_forget[N1] = 0 + SS_off
SS_forget[N1-1] = 0 + SS_off
PS_forget = [1 + PS_off]*len(sentence)
PS_forget[N1] = 0 + PS_off
PS_forget[N1-1] = 0 + PS_off
SP_forget = [1 + SP_off]*len(sentence)
SP_forget[N1] = 0 + SP_off
SP_forget[N1-1] = 0 + SP_off
PP_forget = [1 + PP_off]*len(sentence)
PP_forget[N1] = 0 + PP_off
PP_forget[N1-1] = 0 + PP_off


SS_cell = [1 + SS_off]*len(sentence)
SS_cell[N1] = 0 + SS_off
SS_cell[N1-1] = 0 + SS_off
PS_cell = [-1 + PS_off]*len(sentence)
PS_cell[N1] = 0 + PS_off
PS_cell[N1-1] = 0 + PS_off
SP_cell = [1 + SP_off]*len(sentence)
SP_cell[N1] = 0 + SP_off
SP_cell[N1-1] = 0 + SP_off
PP_cell = [-1 + PP_off]*len(sentence)
PP_cell[N1] = 0 + PP_off
PP_cell[N1-1] = 0 + PP_off


plt.figure(figsize=(10,10))
fig, (sugg_ax, input_ax, forget_ax, cell_ax) = plt.subplots(4, 1) # two plots in a single column
sugg_ax.plot(PP_sugg, ls='-', lw=2, label=r'\textbf{Plural}-\underline{Plural}', color='blue')
sugg_ax.plot(SS_sugg, ls='-', lw=2, label=r'\textbf{Singular}-\underline{Singular}', color='red')
sugg_ax.plot(PS_sugg, ls=':', lw=3, label=r'\textbf{Plural}-\underline{Singular}', color='blue')
sugg_ax.plot(SP_sugg, ls=':', lw=3, label=r'\textbf{Singular}-\underline{Plural}', color='red')
sugg_ax.set_ylabel("Suggestion")
sugg_ax.set_xticks([])

input_ax.plot(PP_input, ls='-', lw=2, color='blue')
input_ax.plot(SS_input, ls='-', lw=2, color='red')
input_ax.plot(PS_input, ls=':', lw=3, color='blue')
input_ax.plot(SP_input, ls=':', lw=3, color='red')
input_ax.set_ylabel("Input", labelpad=12)
input_ax.set_xticks([])

forget_ax.plot(PP_forget, ls='-', lw=2, color='blue')
forget_ax.plot(SS_forget, ls='-', lw=2, color='red')
forget_ax.plot(PS_forget, ls=':', lw=3, color='blue')
forget_ax.plot(SP_forget, ls=':', lw=3, color='red')
forget_ax.set_ylabel("Forget", labelpad=12)
forget_ax.set_xticks([])

cell_ax.plot(PP_cell, ls='-', lw=2, color='blue')
cell_ax.plot(SS_cell, ls='-', lw=2, color='red')
cell_ax.plot(PS_cell, ls=':', lw=3, color='blue')
cell_ax.plot(SP_cell, ls=':', lw=3, color='red')
cell_ax.set_ylabel("Cell")
#forget_ax.set_xticks([])
#plt.plot(forget, ls=':', lw=4, label='The girl/girls $f_t$', color='C2')
plt.xticks(ticks=range(len(sentence)), labels=sentence, fontsize=14, rotation=0)
handles, labels = sugg_ax.get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', ncol=2)
fig.savefig('unit-timeseries-cartoon.png')
