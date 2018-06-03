# -*- coding: utf-8 -*-

import pandas as pnd
import matplotlib.pyplot as plt

def var(df, name):
    '''Computes variations from previous row for column name'''
    df['D_' + name] = df[name] - df[name].shift(1)

def perc(df, name):
    df['p_' + name] = df[name] * 100 / df['total']

def psplot(columns, legend, area=False, **kwargs):
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
    ax.legend(legend, loc="center left", bbox_to_anchor=(1, 0.5))
    ax.set_ylabel('Nombre d\'étudiants')

if __name__ == '__main__':
    df = pnd.read_csv('parcoursup.csv', sep=';', header=0, index_col=0,
                      parse_dates=[0])

    # Sums all propositions columns
    df['total_prop'] = \
    df.acc_def + df.acc_nondef + df.quit_prop

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

    # Checks
    df['d_all_neg_quit'] = - df.D_all_neg - df.D_rect

    df['d_wait_quit'] = df.D_quit_nonprop + df.D_all_neg + df.D_rect

    df['d_admitted'] = \
    - df.D_wait - df.D_quit_nonprop - df.D_all_neg - df.D_rect

    # Print the frame
    pnd.set_option('display.max_columns', None)
    print(df)

    # All info stacked
    psplot(["acc_def", "acc_nondef", "quit_prop", "wait", "rect", "all_neg",
            "quit_nonprop"],
           ['Acceptations définitives', 'Acceptations non définitives',
            'Quitté avec proposition', 'En attente', 'Demandes rectorat',
            'Toutes négatives', 'Quitté sans proposition'], area=True,
            stacked=True)

    # All info not stacked
    psplot(["acc_def", "acc_nondef", "quit_prop", "wait", "rect", "all_neg",
            "quit_nonprop"],
           ['Acceptations définitives', 'Acceptations non définitives',
            'Quitté avec proposition', 'En attente', 'Demandes rectorat',
            'Toutes négatives', 'Quitté sans proposition'])

    # Acceptations and waiting students
    psplot(["acc_def", "acc_nondef", "wait"],
           ['Acceptations définitives', 'Acceptations non définitives',
             'En attente'])

    # Acceptations and waiting students (stacked)
    psplot(["acc_def", "acc_nondef", "wait"],
           ['Acceptations définitives', 'Acceptations non définitives',
             'En attente'], area=True, stacked=True)

    # Rejections
    psplot(["quit_prop", "rect", "all_neg", "quit_nonprop"],
           ['Quitté avec proposition','Demandes rectorat',
            'Toutes négatives', 'Quitté sans proposition'])
