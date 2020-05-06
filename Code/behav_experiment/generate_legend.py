# LEGEND
import matplotlib.pyplot as plt
import numpy as np
fig_legend_weights, ax = plt.subplots(figsize=(6, 3))
lines = []
lines.append(ax.scatter(range(1), np.random.randn(1), color='k', marker='.', s=500, label='Singular'))
lines.append(ax.scatter(range(1), np.random.randn(1), color='k', marker='_', s=500, label='Plural'))


plt.legend(loc='center', prop={'size': 45})
for _ in range(2):
     l = lines.pop(0)
     # l = l.pop(0)
     l.remove()
     del l

ax.axis('off')
plt.savefig('../../Figures/legend_weights_number.png')
plt.close()

fig_legend_weights, ax = plt.subplots(figsize=(6, 3))
lines = []
lines.append(ax.scatter(range(1), np.random.randn(1), color='k', marker='.', s=500, label='Masculine'))
lines.append(ax.scatter(range(1), np.random.randn(1), color='k', marker='_', s=500, label='Feminine'))


plt.legend(loc='center', prop={'size': 45})
for _ in range(2):
     l = lines.pop(0)
     # l = l.pop(0)
     l.remove()
     del l

ax.axis('off')
plt.savefig('../../Figures/legend_weights_gender.png')
plt.close()