import pandas as pd
import numpy as np
import numpy.random as rnd
import scipy.stats as stat
import seaborn as sns
import matplotlib.pyplot as plt
import sys
sys.path.append("../../src/")

from meanperm import *
from pathlib import Path

result_file = Path("pvals.pkl")
if not result_file.exists():
    tcga_data = pd.read_csv("eig_stat_tcga.csv",  delimiter="\t")
    df = pd.DataFrame(columns=['exact', 'mwu', 'ttest'])

    tn_cols = [col for col in tcga_data.columns if '_T_' in col]
    o_cols = [col for col in tcga_data.columns if '_R_' in col]

    for index, row in tcga_data.iterrows():
        a = np.array(row[tn_cols],dtype='float64')
        b = np.array(row[o_cols],dtype='float64')
        p1 = significance_of_mean(a,b,100)[0]
        p2 = stat.mannwhitneyu(a,b,alternative="two-sided")[1]
        p3 = stat.ttest_ind(a, b)[1]
        print(p1,p2,p3)
        df.loc[index] = [p1,p2,p3]

    df.to_pickle(result_file)
else:
    df = pd.read_pickle(result_file)

sns.set(style="whitegrid")
sns.set_context("talk")
# Draw a scatter plot while assigning point colors and sizes to different
# variables in the dataset
g = sns.pairplot(df,plot_kws={"s": 3})
sns.despine()
g.savefig("tcga_3meth_calibration.png")
plt.show()

f, ax = plt.subplots(figsize=(7, 7))
ax.set(xscale="log", yscale="log")
sns.regplot("exact", "ttest", df, ax=ax, fit_reg=False, scatter_kws={"s": 3})
ax.plot([min(df["exact"]),min(df["exact"])], [max(df["exact"]),max(df["exact"])], 'k-', linewidth=2)
sns.despine()
f.savefig("tcga_loglog_calibration.png")
plt.show()



#f, ax = plt.subplots(figsize=(6.5, 6.5))
#sns.despine(f, left=True, bottom=True)
#sns.scatterplot(x="ttest", y="exact",
#                linewidth=0,
#                data=df, ax=ax)
