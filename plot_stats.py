# -*- coding: utf-8 -*-

import pandas as pnd
import matplotlib.pyplot as plt

def var(df, name):
    '''Computes variations from previous row for column name'''
    df['D_' + name] = df[name] - df[name].shift(1)

def perc(df, name):
    df['p_' + name] = df[name] * 100 / df['total']

def absolute(df, name):
    df['abs_' + name] = abs(df[name])

def psplot(columns, area=False, filename=None, **kwargs):
    '''Standard plotting function

    columns: name of the columns to add on the graph.
    legend: label for each of the given columns (same order)
    area: (default false) fill the bottom part of the curves if true
    **kwargs: additional arguments for the plot function'''
    fig = plt.figure();
    if not area:
        ax = df[columns].plot(figsize=(12, 12), **kwargs)
    else:
        ax = df[columns].plot.area(figsize=(12, 12), **kwargs)

    legend = [titles[col] for col in columns]

    ax.legend(legend, loc="center left", bbox_to_anchor=(1, 0.5))
    ax.set_ylabel('Nombre d\'étudiants')

    bac = ['2018-06-18', '2018-06-25', '2018-07-06', '2018-07-11']
    for xc in bac:
        plt.axvline(x=xc, color='k', linestyle='--')

    if filename is not None:
        plt.savefig('last_figures/' + filename,  bbox_inches = 'tight')

if __name__ == '__main__':
    df = pnd.read_csv('parcoursup.csv', sep=';', header=0, index_col=0,
                      parse_dates=[0])

    # Sums all propositions columns
    df['total_prop'] = df.acc_def + df.acc_nondef + df.quit_prop

    # Sums all non propositions columns
    df['total_nonprop'] = df.wait + df.rect + df.quit_nonprop + df.all_neg

    df['total_quit'] = df.quit_prop + df.quit_nonprop

    # All negatives + rectorat
    df['all_neg_or_rect'] = df.rect + df.all_neg

    df['total_dismissed'] = df.all_neg_or_rect + df.total_quit

    df['wants_better'] = df.wait + df.acc_nondef

    # Grand total
    df['total'] = df.total_nonprop + df.total_prop

    # Add variations
    for column in df:
        var(df, column)
        perc(df, column)

    # Computes absolutes for each columns (graph purposes)
    for column in df:
        absolute(df, column)

    # Checks
    df['d_all_neg_quit'] = - df.D_all_neg - df.D_rect

    df['d_wait_quit'] = df.D_quit_nonprop + df.D_all_neg + df.D_rect

    df['d_admitted'] = \
    - df.D_wait - df.D_quit_nonprop - df.D_all_neg - df.D_rect

    # Print the frame
    pnd.set_option('display.max_columns', None)
    print(df)

    titles = {
            "acc_def": 'Acceptations définitives',
            "acc_nondef": 'Acceptations non définitives',
            "quit_prop": 'Quitté avec proposition',
            "wait": 'En attente',
            "rect": 'Demandes rectorat',
            "all_neg": 'Toutes négatives',
            "quit_nonprop": 'Quitté sans proposition',
            "total_prop": 'Ayant reçu au moins une proposition',
            "total_nonprop": "N'ayant reçu aucune proposition",
            "abs_D_acc_def": "Variation absolue d'acceptations définitives",
            "abs_D_acc_nondef": "Variation absolue d'acceptations non définitives",
            "abs_D_wait": "Variation absolue liste d'attente",
            "lpf_D_acc_def": "EWMA variation d'acceptations définitives",
            "abs_D_wants_better": "Variation absolue attente de mieux",
            "wants_better": "En attente de mieux",
            }

    # All info stacked
    psplot(["acc_def", "acc_nondef", "quit_prop", "wait", "rect", "all_neg",
            "quit_nonprop"], area=True, stacked=True,
        filename='all_stacked.png')

    # All info not stacked
    psplot(["acc_def", "acc_nondef", "quit_prop", "wait", "rect", "all_neg",
            "quit_nonprop"], filename='all_curves.png')

    # Acceptations and waiting students
    psplot(["acc_def", "acc_nondef", "wait"],
           filename='acc_wait.png')
    psplot(["acc_def", "acc_nondef", "wait", "wants_better"],
           filename='acc_wait_better.png')

    # Acceptations and waiting students (stacked)
    psplot(["acc_def", "acc_nondef", "wait"], area=True, stacked=True,
            filename='acc_wait_stacked.png')

    # Rejections
    psplot(["quit_prop", "rect", "all_neg", "quit_nonprop"],
            filename='rejections.png')

    psplot(['abs_D_acc_def', 'abs_D_acc_nondef', 'abs_D_wait'],
           kind='bar', filename='acc_wait_vars_bars.png')
    psplot(['abs_D_acc_def', 'abs_D_acc_nondef', 'abs_D_wait',
            'abs_D_wants_better'],
           filename='acc_wait_vars.png')

    # Total prop / nonprop
    psplot(['total_prop', 'total_nonprop'],
           filename='total_propnprop.png')