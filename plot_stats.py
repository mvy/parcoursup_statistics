# -*- coding: utf-8 -*-

import pandas as pnd
import matplotlib.pyplot as plt

def var(outf, inf, name):
    '''Computes variations from previous row for column name'''
    outf[name] = inf[name] - inf[name].shift(1)

def perc(outf, inf, name, ref='total'):
    outf[name + '_' + ref] = inf[name] * 100 / inf[ref]

def absolute(outf, inf, name):
    outf[name] = abs(inf[name])

def psplot(frame, columns, titles, area=False, filename=None, **kwargs):
    '''Standard plotting function

    columns: name of the columns to add on the graph.
    legend: label for each of the given columns (same order)
    area: (default false) fill the bottom part of the curves if true
    **kwargs: additional arguments for the plot function'''
    fig = plt.figure();
    if not area:
        ax = frame[columns].plot(figsize=(12, 12), **kwargs)
    else:
        ax = frame[columns].plot.area(figsize=(12, 12), **kwargs)

    legend = [titles[col] for col in columns]

    ax.legend(legend, loc="center left", bbox_to_anchor=(1, 0.5))
    ax.set_ylabel('Nombre d\'étudiants')

    bac = ['2018-06-18', '2018-06-25', '2018-07-06', '2018-07-11']
    for xc in bac:
        plt.axvline(x=xc, color='k', linestyle='--')

    if filename is not None:
        plt.savefig('last_figures/' + filename,  bbox_inches = 'tight')

    plt.close(fig)

if __name__ == '__main__':
    df = pnd.read_csv('parcoursup.csv', sep=';', header=0, index_col=0,
                      parse_dates=[0])

    # Sums all propositions columns
    df['total_prop'] = df.acc_def + df.acc_nondef + df.quit_prop

    # Sums all non propositions columns
    df['total_nonprop'] = df.wait + df.rect + df.quit_nonprop + df.all_neg

    df['total_acc_inscr']  = df.acc_def + df.acc_nondef
    df['total_quit'] = df.quit_prop + df.quit_nonprop

    # All negatives + rectorat
    df['all_neg_or_rect'] = df.rect + df.all_neg
    df['total_nonprop_inscr'] = df.all_neg_or_rect + df.wait
    df['total_dismissed'] = df.all_neg_or_rect + df.total_quit

    df['wants_better'] = df.wait + df.acc_nondef

    # Grand total
    df['total_inscr'] = df.total_acc_inscr + df.total_nonprop_inscr
    df['total'] = df.total_nonprop + df.total_prop

    # Variation frame
    vf = pnd.DataFrame(index=df.index)
    # Percent frame
    pf = pnd.DataFrame(index=df.index)
    # Absolute frame
    af = pnd.DataFrame(index=df.index)

    # Add variations
    for column in df:
        var(vf, df, column)
        perc(pf, df, column)

    for column in ['total_acc_inscr', 'total_nonprop_inscr']:
        perc(pf, df, column, 'total_inscr')

    # Computes absolutes for each columns (graph purposes)
    for column in df:
        absolute(af, vf, column)

    # Checks
    vf['all_neg_quit'] = - vf.all_neg - vf.rect

    df['wait_quit'] = vf.quit_nonprop + vf.all_neg + vf.rect

    vf['d_admitted'] = \
    - vf.wait - vf.quit_nonprop - vf.all_neg - vf.rect

    # Print the frame
    pnd.set_option('display.max_columns', None)
    print("# Input and calculated")
    print(df)
    print("# Variations")
    print(vf)
    print('# Percentages')
    print(pf)
    print('# Absolute variations')
    print(af)

    df_titles = {
            "acc_def": 'Acceptations définitives',
            "acc_nondef": 'Acceptations non définitives',
            "quit_prop": 'Quitté avec proposition',
            "wait": 'En attente',
            "rect": 'Demandes rectorat',
            "all_neg": 'Toutes négatives',
            "quit_nonprop": 'Quitté sans proposition',
            "total_prop": 'Ayant reçu au moins une proposition',
            "total_nonprop": "N'ayant reçu aucune proposition",
            "wants_better": "En attente de mieux",
            "total_acc_inscr": "Total acceptations inscrits",
            "total_nonprop_inscr": "Total sans propositions inscrits"
            }

    vf_titles = {
            "acc_def": "Variation d'acceptations définitives",
            "acc_nondef": "Variation d'acceptations non définitives",
            "wait": "Variation liste d'attente",
            "wants_better": "Variation attente de mieux",
            }

    af_titles = {
            "acc_def": "Variation absolue d'acceptations définitives",
            "acc_nondef": "Variation absolue d'acceptations non définitives",
            "wait": "Variation absolue liste d'attente",
            "wants_better": "Variation absolue attente de mieux",
            }

    # All info stacked
    psplot(df, ["acc_def", "acc_nondef", "quit_prop", "wait", "rect", 
                "all_neg", "quit_nonprop"], df_titles, area=True, stacked=True,
        filename='all_stacked.png')

    # All info not stacked
    psplot(df, ["acc_def", "acc_nondef", "quit_prop", "wait", "rect", 
                "all_neg", "quit_nonprop"], df_titles,
           filename='all_curves.png')

    # Acceptations and waiting students
    psplot(df, ["acc_def", "acc_nondef", "wait"], df_titles,
           filename='acc_wait.png')
    psplot(df, ["acc_def", "acc_nondef", "wait", "wants_better"],df_titles,
           filename='acc_wait_better.png')

    # Acceptations and waiting students (stacked)
    psplot(df, ["acc_def", "acc_nondef", "wait"], df_titles, area=True, 
           stacked=True, filename='acc_wait_stacked.png')

    # Rejections
    psplot(df, ["quit_prop", "rect", "all_neg", "quit_nonprop"], df_titles,
            filename='rejections.png')

    psplot(af, ['acc_def', 'acc_nondef', 'wait'], af_titles,
           kind='bar', filename='acc_wait_vars_bars.png')
    psplot(af, ['acc_def', 'acc_nondef', 'wait', 'wants_better'], af_titles,
           filename='acc_wait_vars.png')

    # Total prop / nonprop
    psplot(df, ['total_prop', 'total_nonprop'],df_titles,
           filename='total_propnprop.png')

    psplot(vf, ['acc_def', 'acc_nondef', 'wait', 'wants_better'], vf_titles)

    psplot(df, ['total_acc_inscr', 'total_nonprop_inscr'], df_titles)