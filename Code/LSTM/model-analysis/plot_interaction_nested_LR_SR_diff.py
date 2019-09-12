import matplotlib.pyplot as plt
import numpy as np

# ------------------------------
# ---    ITALIAN     -----------
# ------------------------------
perf_objrel_nounpp_SSS = 1.00
perf_objrel_nounpp_SSP = 0.99
perf_objrel_nounpp_SPS = 0.04
perf_objrel_nounpp_SPP = 0.12
perf_objrel_nounpp_PSS = 0.21
perf_objrel_nounpp_PSP = 0.04
perf_objrel_nounpp_PPS = 0.98
perf_objrel_nounpp_PPP = 1.00


diff_objrel_nounpp_SXS = perf_objrel_nounpp_SSS - perf_objrel_nounpp_SPS
diff_objrel_nounpp_PXP = perf_objrel_nounpp_PPP - perf_objrel_nounpp_PSP

diff_objrel_nounpp = np.mean([diff_objrel_nounpp_SXS, diff_objrel_nounpp_PXP])

perf_objrel_SS = 1.00
perf_objrel_SP = 0.53
perf_objrel_PS = 0.64
perf_objrel_PP = 1.00

diff_objrel_nounpp_SX = perf_objrel_SS - perf_objrel_SP
diff_objrel_nounpp_PX = perf_objrel_PP - perf_objrel_PS
diff_objrel = np.mean([diff_objrel_nounpp_SX, diff_objrel_nounpp_PX])

print(diff_objrel_nounpp, diff_objrel)

perf_embedding_mental_LR_SSS = 1.00
perf_embedding_mental_LR_SSP = 0.98
perf_embedding_mental_LR_SPS = 0.92
perf_embedding_mental_LR_SPP = 0.99
perf_embedding_mental_LR_PSS = 1.00
perf_embedding_mental_LR_PSP = 0.99
perf_embedding_mental_LR_PPS = 0.93
perf_embedding_mental_LR_PPP = 0.99

diff_embedding_mental_LR_SXS = perf_embedding_mental_LR_SSS - perf_embedding_mental_LR_SPS
diff_embedding_mental_LR_PXP = perf_embedding_mental_LR_PPP - perf_embedding_mental_LR_PSP

diff_embedding_mental_LR = np.mean([diff_embedding_mental_LR_SXS, diff_embedding_mental_LR_PXP])

perf_embedding_mental_SR_SS = 1.00
perf_embedding_mental_SR_SP = 0.99
perf_embedding_mental_SR_PS = 1.00
perf_embedding_mental_SR_PP = 0.99

diff_embedding_mental_SR_SX = perf_embedding_mental_SR_SS - perf_embedding_mental_SR_SP
diff_embedding_mental_SR_PX = perf_embedding_mental_SR_PP - perf_embedding_mental_SR_PS
diff_embedding_mental_SR = np.mean([diff_embedding_mental_SR_SX, diff_embedding_mental_SR_PX])

print(diff_embedding_mental_LR, diff_embedding_mental_SR)

# ------------------------------
# ---    Plot     -----------
# ------------------------------


fig, ax = plt.subplots(figsize=(20, 10))
ax.plot((diff_embedding_mental_SR, diff_embedding_mental_LR), marker='^', markersize=10, ls='-', color='c', lw=2, label='Succesive dependecies')
ax.plot((diff_objrel, diff_objrel_nounpp), marker='D', markersize=10, ls='--', color='r', lw=2, label='Nested dependecies')
ax.set_xticks((0,1))
ax.set_xticklabels(('Short-range', 'Long-range'), fontsize=26)
ax.tick_params(axis='y', which='major', labelsize=14)
ax.set_xlim((-0.2, 1.2))
ax.set_ylim((0, 1))
# ax.set_xlabel('LR-mechanism is free/occupied', fontsize=30, labelpad=16)
ax.set_ylabel('Error rate on V2', fontsize=30)
ax.axhline(0.5, ls=':', color='k', label='Chance')
ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=20)
ax.set_title('Italian', fontsize=30)
plt.subplots_adjust(right=0.8)
plt.savefig('../../../Figures/interaction_error_Italian_nested_SR_LR.png')


fig, ax = plt.subplots(figsize=(20, 10))
ax.plot((Italina_SR_successive, Italina_LR_successive), marker='^', markersize=10, ls='-', color='c', lw=2, label='Succesive LRs')
ax.plot((Italina_SR_nested, Italina_LR_nested), marker='D', markersize=10, ls='--', color='r', lw=2, label='Nested LRs')
ax.set_xticks((0,1))
ax.set_xticklabels(('w/o attractor', 'with attractor'), fontsize=26)
ax.tick_params(axis='y', which='major', labelsize=14)
ax.set_xlim((-0.2, 1.2))
ax.set_ylim((0, 1))
# ax.set_xlabel('Whether the LR-mechanism is free or occupied', fontsize=30, labelpad=16)
ax.set_ylabel('Model accuracy on V2', fontsize=30)
ax.axhline(0.5, ls=':', color='k', label='Chance')
ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=20)
ax.set_title('Italian', fontsize=30)
plt.subplots_adjust(right=0.8)
plt.savefig('../../../Figures/interaction_Italian_nested_SR_LR_transpose.png')


# ------------------------------
# ---    English     -----------
# ------------------------------
perf_objrel_nounpp_SSS = 0.95
perf_objrel_nounpp_SSP = 0.74
perf_objrel_nounpp_SPS = 0.47
perf_objrel_nounpp_SPP = 0.79
perf_objrel_nounpp_PSS = 0.75
perf_objrel_nounpp_PSP = 0.34
perf_objrel_nounpp_PPS = 0.80
perf_objrel_nounpp_PPP = 0.92

perf_objrel_SS = 0.98
perf_objrel_SP = 0.99
perf_objrel_PS = 0.79
perf_objrel_PP = 1.00

perf_embedding_mental_LR_SSS = 0.93
perf_embedding_mental_LR_SSP = 0.61
perf_embedding_mental_LR_SPS = 0.89
perf_embedding_mental_LR_SPP = 0.99
perf_embedding_mental_LR_PSS = 1.93
perf_embedding_mental_LR_PSP = 0.61
perf_embedding_mental_LR_PPS = 0.89
perf_embedding_mental_LR_PPP = 0.99


perf_embedding_mental_SR_SS = 0.96
perf_embedding_mental_SR_SP = 1.00
perf_embedding_mental_SR_PS = 0.97
perf_embedding_mental_SR_PP = 1.00

English_SR_nested = (perf_objrel_PS + perf_objrel_SP)/2
English_SR_successive = (perf_embedding_mental_SR_SP + perf_embedding_mental_SR_PS)/2
English_LR_nested = (perf_objrel_nounpp_SP + perf_objrel_nounpp_PS)/2
English_LR_successive = (perf_embedding_mental_LR_SPS + perf_embedding_mental_LR_PSP)/2

# ------------------------------
# ---    Plot     -----------
# ------------------------------


fig, ax = plt.subplots(figsize=(20, 10))
ax.plot((English_SR_successive, English_SR_nested), marker='^', markersize=10, ls='-', color='c', lw=2, label='w/o attractor')
ax.plot((English_LR_successive, English_LR_nested), marker='D', markersize=10, ls='--', color='r', lw=2, label='with attractor')
ax.set_xticks((0,1))
ax.set_xticklabels(('Successive (free)', 'Nested (occupied)'), fontsize=26)
ax.tick_params(axis='y', which='major', labelsize=14)
ax.set_xlim((-0.2, 1.2))
ax.set_ylim((0, 1))
ax.set_xlabel('LR-mechanism is free/occupied', fontsize=30, labelpad=16)
ax.set_ylabel('Model accuracy on V2', fontsize=30)
ax.axhline(0.5, ls=':', color='k', label='Chance')
ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=20)
ax.set_title('English', fontsize=30)
plt.subplots_adjust(right=0.8)
plt.savefig('../../../Figures/interaction_English_nested_SR_LR.png')


fig, ax = plt.subplots(figsize=(20, 10))
ax.plot((English_SR_successive, English_LR_successive), marker='^', markersize=10, ls='-', color='c', lw=2, label='Succesive LRs')
ax.plot((English_SR_nested, English_LR_nested), marker='D', markersize=10, ls='--', color='r', lw=2, label='Nested LRs')
ax.set_xticks((0,1))
ax.set_xticklabels(('w/o attractor', 'with attractor'), fontsize=26)
ax.tick_params(axis='y', which='major', labelsize=14)
ax.set_xlim((-0.2, 1.2))
ax.set_ylim((0, 1))
# ax.set_xlabel('LR-mechanism is free/occupied', fontsize=30, labelpad=16)
ax.set_ylabel('Model accuracy on V2', fontsize=30)
ax.axhline(0.5, ls=':', color='k', label='Chance')
ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=20)
ax.set_title('English', fontsize=30)
plt.subplots_adjust(right=0.8)
plt.savefig('../../../Figures/interaction_English_nested_SR_LR_transpose.png')




# fig, ax = plt.subplots(figsize=(20, 10))
# ax.plot([], marker='^', markersize=10, ls='-', color='c', lw=2, label='Short-range')
# ax.plot([], marker='D', markersize=10, ls='--', color='r', lw=2, label='Long-range')
# ax.set_xticks((0,1))
# ax.set_xticklabels(('Successive (free)', 'Nested (occupied)'), fontsize=26)
# ax.tick_params(axis='y', which='major', labelsize=14)
# ax.set_xlim((-0.2, 1.2))
# ax.set_xlabel('Whether the LR-mechanism is free or occupied', fontsize=30, labelpad=16)
# ax.set_ylabel('Model accuracy on V2', fontsize=30)
# ax.axhline(0.5, ls=':', color='k', label='Chance')
# ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=20)
# plt.subplots_adjust(right=0.85)
# plt.savefig('../../../Figures/interaction_Italian_nested_SR_LR_humans.png')
