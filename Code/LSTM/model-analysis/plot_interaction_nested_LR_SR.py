import matplotlib.pyplot as plt


# ------------------------------
# ---    ITALIAN     -----------
# ------------------------------
perf_objrel_nounpp_SP = 0.04
perf_objrel_nounpp_PS = 0.04

perf_objrel_PS = 0.64
perf_objrel_SP = 0.53

perf_embedding_mental_LR_SPS = 0.92
perf_embedding_mental_LR_PSP = 0.99

perf_embedding_mental_SR_SP = 0.986
perf_embedding_mental_SR_PS = 0.99

Italina_SR_nested = (perf_objrel_PS + perf_objrel_SP)/2
Italina_SR_successive = (perf_embedding_mental_SR_SP + perf_embedding_mental_SR_PS)/2
Italina_LR_nested = (perf_objrel_nounpp_SP + perf_objrel_nounpp_PS)/2
Italina_LR_successive = (perf_embedding_mental_LR_SPS + perf_embedding_mental_LR_PSP)/2

# ------------------------------
# ---    Plot     -----------
# ------------------------------


fig, ax = plt.subplots(figsize=(20, 10))
ax.plot((Italina_SR_successive, Italina_SR_nested), marker='^', markersize=10, ls='-', color='c', lw=2, label='w/o attractor')
ax.plot((Italina_LR_successive, Italina_LR_nested), marker='D', markersize=10, ls='--', color='r', lw=2, label='with attractor')
ax.set_xticks((0,1))
ax.set_xticklabels(('Successive (free)', 'Nested (occupied)'), fontsize=26)
ax.tick_params(axis='y', which='major', labelsize=14)
ax.set_xlim((-0.2, 1.2))
ax.set_ylim((0, 1))
ax.set_xlabel('LR-mechanism is free/occupied', fontsize=30, labelpad=16)
ax.set_ylabel('Model accuracy on V2', fontsize=30)
ax.axhline(0.5, ls=':', color='k', label='Chance')
ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=20)
ax.set_title('Italian', fontsize=30)
plt.subplots_adjust(right=0.8)
plt.savefig('../../../Figures/interaction_Italian_nested_SR_LR.png')


fig, ax = plt.subplots(figsize=(20, 10))
ax.plot((Italina_SR_successive, Italina_LR_successive), marker='^', markersize=10, ls='-', color='c', lw=2, label='Succesive depend')
ax.plot((Italina_SR_nested, Italina_LR_nested), marker='D', markersize=10, ls='--', color='r', lw=2, label='Nested depend')
ax.set_xticks((0,1))
ax.set_xticklabels(('short-range', 'long-range'), fontsize=26)
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
perf_objrel_nounpp_SP = 0.29
perf_objrel_nounpp_PS = 0.19

perf_objrel_PS = 0.79
perf_objrel_SP = 0.99

perf_embedding_mental_LR_SPS = 0.88
perf_embedding_mental_LR_PSP = 0.53

perf_embedding_mental_SR_SP = 1.00
perf_embedding_mental_SR_PS = 0.97

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
ax.plot((English_SR_successive, English_LR_successive), marker='^', markersize=10, ls='-', color='c', lw=2, label='Succesive depend')
ax.plot((English_SR_nested, English_LR_nested), marker='D', markersize=10, ls='--', color='r', lw=2, label='Nested depend')
ax.set_xticks((0,1))
ax.set_xticklabels(('short-range', 'long-range'), fontsize=26)
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
