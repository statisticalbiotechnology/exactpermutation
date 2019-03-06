import pandas as pd
import numpy as np
import numpy.random as rnd
import scipy.stats as stat
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from meanperm import *
from pathlib import Path

def scatter_from_df(data,a_pattern,b_pattern,prefix="my_",dig_res=200,pkl_file="pvals.pkl"):
    result_file = Path(pkl_file)
    if not result_file.exists():
        df = pd.DataFrame(columns=['exact', 'mwu', 'ttest'])

        a_cols = [col for col in data.columns if a_pattern in col]
        b_cols = [col for col in data.columns if b_pattern in col]

        for index, row in data.iterrows():
            a = np.array(row[a_cols],dtype='float64')
            b = np.array(row[b_cols],dtype='float64')
            p1 = significance_of_mean(a,b,dig_res)[0]
            p2 = stat.mannwhitneyu(a,b,alternative="two-sided")[1]
            p3 = stat.ttest_ind(a, b)[1]
            print(p1,p2,p3)
            df.loc[index] = [p1,p2,p3]

        df.to_pickle(result_file)
    else:
        df = pd.read_pickle(result_file)

    sns.set(style="white")
    sns.set_context("talk")
    g = sns.pairplot(df,plot_kws={"s": 3})
    sns.despine()
    g.savefig(prefix+"3meth_calibration.png")
    plt.show()

    low = min(df["exact"])
    hi = max(df["exact"])
    f, ax = plt.subplots(figsize=(7, 7))
    ax.set(xscale="log", yscale="log")
    g=sns.regplot("exact", "ttest", df, ax=ax, fit_reg=False, scatter_kws={"s": 3})
    g.plot([low,hi], [low,hi], 'k-', linewidth=1)
    sns.despine()
    f.savefig(prefix+"loglog_calibration.png")
    plt.show()



