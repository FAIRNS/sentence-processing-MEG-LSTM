import matplotlib.pyplot as plt

sentence = 'The girl/girls with blue eyes often goes'.split()

# define series values
sing_input = [0]*len(sentence)
sing_input[1] = 1
pl_input = [0]*len(sentence)
forget = [1] * len(sentence)
forget[0] = 0
forget[1] = 0


plt.figure(figsize=(9,4))
plt.plot(pl_input, ls='--', lw=4, label='The girls $i_t \\tilde{C}_t$', color='C1')
plt.plot(sing_input, ls='--', lw=4, label='The girl $i_t \\tilde{C}_t$', color='C0')
plt.plot(forget, ls=':', lw=4, label='The girl/girls $f_t$', color='C2')
plt.xticks(ticks=range(len(sentence)), labels=sentence, fontsize=18)
plt.legend(fontsize=18)
plt.savefig('lstm-cartoon.png', dpi=100)
