import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def generate_fig_humans_vs_RNNs(df_error_rates_humans, sig_list_humans, df_error_rates_LSTM, sig_list_rnns, successive_nested):
    '''

    :param df_error_rates_humans:
    :param sig_list_humans:
    :param df_error_rates_LSTM:
    :param sig_list_rnns:
    :param successive_nested:
    :return:
    '''
    if successive_nested == 'successive':
        structures = ['embedding_mental_SR', 'embedding_mental_LR']
    elif successive_nested == 'nested':
        structures = ['objrel', 'objrel_nounpp']

    # Figure
    fig_humans, axes = plt.subplots(1, 2, figsize=(10, 5))
    hue_order = [True, False]
    palette = ['b', 'r']

    # HUMANS SR
    ax = axes[0]
    df = df_error_rates_humans.loc[
        (df_error_rates_humans['sentence_type'] == structures[0]) & (
                df_error_rates_humans['trial_type'] == 'Violation') & (
            df_error_rates_humans['violation_position'].isin(['inner', 'outer']))]
    sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects', data=df, ax=ax,
                hue_order=hue_order, palette=palette)
    add_significance(ax, successive_nested, sig_list_humans[0][0], sig_list_humans[0][1], sig_list_humans[0][2])
    ax.get_legend().set_visible(False)
    ax.set_ylim([0, 1.2])
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_xticklabels(['Embedded', 'Main'])
    ax.tick_params(labelsize=20)
    # ax.set_ylabel('Error rate', fontsize=20)
    # sns.set(font_scale=2)

    # HUMANS LR
    ax = axes[1]
    df = df_error_rates_humans.loc[
        (df_error_rates_humans['sentence_type'] == structures[1]) & (
                df_error_rates_humans['trial_type'] == 'Violation') & (
            df_error_rates_humans['violation_position'].isin(['inner', 'outer']))]
    sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects', data=df, ax=ax,
                hue_order=hue_order, palette=palette)
    ax.set_yticklabels([])
    ax.set_ylim([0, 1.2])
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_xticklabels(['Embedded', 'Main'])
    ax.tick_params(labelsize=20)
    ax.get_legend().set_visible(False)
    add_significance(ax, successive_nested, sig_list_humans[1][0], sig_list_humans[1][1], sig_list_humans[1][2])

    # LAYOUT
    # handles, labels = ax.get_legend_handles_labels()
    # fig_humans.legend(handles, ['Congruent Subjects', 'Incongruent Subjects'], loc='upper center', bbox_to_anchor=(0.5, 0.97),
    #            ncol=2, fontsize=16)
    plt.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.2)

    #
    # fig_humans.text(x=0.35, y=0.03, s='Short\nEmbedded Dependency', fontsize=16, ha='center')
    # fig_humans.text(x=0.8, y=0.03, s='Long\nEmbedded Dependency', fontsize=16, ha='center')
    fig_humans.text(x=0.03, y=0.7, s='Humans', fontsize=26, rotation=90)

    ## MODEL
    fig_model, axes = plt.subplots(1, 2, figsize=(10, 5))

    # MODEL SR
    ax = axes[0]
    df = df_error_rates_LSTM.loc[
        (df_error_rates_LSTM['sentence_type'] == structures[0]) & (
            df_error_rates_LSTM['violation_position'].isin(['inner', 'outer']))]
    sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects', data=df, ax=ax,
                hue_order=hue_order, palette=palette)
    ax.get_legend().set_visible(False)
    ax.set_xlabel('')
    ax.set_xticklabels(['Embedded', 'Main'])
    ax.tick_params(labelsize=20)
    ax.set_ylim([0, 1.2])
    ax.set_ylabel('')
    add_significance(ax, successive_nested, sig_list_rnns[0][0], sig_list_rnns[0][1], sig_list_rnns[0][2])
    # ax.set_ylabel('Error rate', fontsize=20)

    # MODEL LR
    ax = axes[1]
    df = df_error_rates_LSTM.loc[(df_error_rates_LSTM['sentence_type'] == structures[1]) & (
        df_error_rates_LSTM['violation_position'].isin(['inner', 'outer']))]
    sns.barplot(x='violation_position', y='error_rate', hue='congruent_subjects', data=df, ax=ax,
                hue_order=hue_order, palette=palette)
    ax.get_legend().set_visible(False)
    ax.set_xlabel('')
    ax.tick_params(labelsize=20)
    ax.set_xticklabels(['Embedded', 'Main'])
    ax.set_yticklabels([])
    ax.set_ylim([0, 1.2])
    ax.set_ylabel('')
    add_significance(ax, successive_nested, sig_list_rnns[1][0], sig_list_rnns[1][1], sig_list_rnns[1][2])

    # LAYOUT
    # handles, labels = ax.get_legend_handles_labels()
    plt.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.2)

    #
    # fig_model.text(x=0.35, y=0.03, s='Short\nEmbedded Dependency', fontsize=16, ha='center')
    # fig_model.text(x=0.8, y=0.03, s='Long\nEmbedded Dependency', fontsize=16, ha='center')
    fig_model.text(x=0.03, y=0.6, s='RNNs', fontsize=26, rotation=90)

    # LEGEND
    # fig_legend, ax = plt.subplots()
    # fig_model.legend(handles, ['Congruent Subjects', 'Incongruent Subjects'], loc='upper center',
    #                  bbox_to_anchor=(0.5, 0.97),
    #                  ncol=2, fontsize=16)
    import numpy as np
    fig_legend, ax = plt.subplots(figsize=(20, 2.5))
    lines = []
    lines.append(ax.plot(range(10), np.random.randn(10), color='blue', lw=6, ls='-', label='Congruent Subjects'))
    lines.append(ax.plot(range(10), np.random.randn(10), color='red', lw=6, ls='-', label='Incongruent Subjects'))


    plt.legend(loc='center', prop={'size': 45}, ncol=2)

    for _ in range(2):
        l = lines.pop(0)
        l = l.pop(0)
        l.remove()
        del l

    ax.axis('off')

    return fig_humans, fig_model, fig_legend

def add_significance(ax, successive_nested, text_interaction, text_embedded, text_main, delta_y=0.05, pad_y_interaction=0.2, pad_y=0.1):
    bar_widths = [patch.get_width() for patch in ax.patches]
    bar_heights = [patch.get_height() for patch in ax.patches]
    if successive_nested == 'nested':
        # significance of interaction
        x1, x2 = 0, 1
        y, col = max(bar_heights) + pad_y_interaction, 'k'
        ax.plot([x1, x1, x2, x2], [y, y + delta_y, y + delta_y, y], lw=1.5, c=col)
        ax.text((x1 + x2) * .5, y + delta_y, text_interaction, ha='center', va='bottom', color=col)

        # significance of embedded
        x1, x2 = 1 - bar_widths[1] / 2, 1 + bar_widths[3] / 2
        y, col = max((bar_heights[1], bar_heights[3])) + pad_y, 'k'
        ax.plot([x1, x1, x2, x2], [y, y + delta_y, y + delta_y, y], lw=1.5, c=col)
        ax.text((x1 + x2) * .5, y + delta_y, text_embedded, ha='center', va='bottom', color=col)

        # significance of main
        x1, x2 = -bar_widths[0] / 2, bar_widths[0] / 2
        y, col = max((bar_heights[2], bar_heights[2])) + pad_y, 'k'
        ax.plot([x1, x1, x2, x2], [y, y + delta_y, y + delta_y, y], lw=1.5, c=col)
        ax.text((x1 + x2) * .5, y + delta_y, text_main, ha='center', va='bottom', color=col)
    if successive_nested == 'successive':
        # significance of embedded
        x1, x2 = - bar_widths[0] / 2, bar_widths[1] / 2
        y, col = max((bar_heights[0], bar_heights[1])) + pad_y, 'k'
        ax.plot([x1, x1, x2, x2], [y, y + delta_y, y + delta_y, y], lw=1.5, c=col)
        ax.text((x1 + x2) * .5, y + delta_y, text_embedded, ha='center', va='bottom', color=col)


def generate_scatter_incongruent_subjects_V1_vs_V2(df, sentence_type):
    X1 = df.loc[(df['sentence_type'] == sentence_type) & (df['violation_position'] == 'inner') & (df['congruent_subjects'] == False)&(df['trial_type'] == 'Violation')]
    X1 = X1.groupby('subject', as_index=False).mean()
    X2 = df.loc[(df['sentence_type'] == sentence_type) & (df['violation_position'] == 'outer') & (df['congruent_subjects'] == False)&(df['trial_type'] == 'Violation')]
    X2 = X2.groupby('subject', as_index=False).mean()

    fig, ax = plt.subplots(figsize=[10,10])
    ax.scatter(X1['error_rate'].values, X2['error_rate'].values, c=X1['subject'].values)
    ax.plot(np.mean(X1.values[:, 1]), np.mean(X2.values[:, 1]), 'ro')
    ax.set_xlabel('Error-Rate Embedded Verb', fontsize=24)
    ax.set_ylabel('Error-Rate Main Verb', fontsize=24)
    ax.set_title(sentence_type, fontsize=24)
    ax.plot([0, 1], [0, 1], 'k-', alpha=0.75, zorder=0)
    ax.set_aspect('equal')
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    # plt.show()
    return fig, ax
    # ax = sns.scatterplot(x="total_bill", y="tip", hue="time", style="time", data=tips)