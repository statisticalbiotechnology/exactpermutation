import pandas as pd
import numpy as np
import numpy.random as rnd
import scipy.stats as stat
import seaborn as sns
import matplotlib.pyplot as plt
import sys
sys.path.append("../../src/")

from meanperm import *

ms_data = pd.read_csv("stat_eig_df_tab_delim.csv",  delimiter="\t")
df = pd.DataFrame(columns=['Exact', 'mwu', 't-test', 'ANOVA'])

healthy_cols = [col for col in ms_data.columns if '_H_0' in col]
ms_cols = [col for col in ms_data.columns if '_M_0' in col]

number_of_tests = 500
sample_size = 25

for index, row in ms_data.iterrows():
    a = np.array(row[healthy_cols],dtype='float64')
    b = np.array(row[ms_cols],dtype='float64')
    p1 = significance_of_mean(a,b,200)[0]
    p2 = stat.mannwhitneyu(a,b,alternative="two-sided")[1]
    p3 = stat.ttest_ind(a, b)[1]
    p4 = float(row["C(Status)_p"])
    print(p1,p2,p3,p4)
    df.loc[index] = [p1,p2,p3,p4]

sns.set(style="whitegrid")
# Draw a scatter plot while assigning point colors and sizes to different
# variables in the dataset
g = sns.pairplot(df)
g.savefig("4meth_calibration.png")
plt.show()

f, ax = plt.subplots(figsize=(7, 7))
ax.set(xscale="log", yscale="log")
sns.regplot("Exact", "ANOVA", df, ax=ax, fit_reg=False, scatter_kws={"s": 100})
ax.set_xlabel('Exact $p$ value')
ax.set_ylabel('ANOVA $p$ value')
f.savefig("loglog_anova_calibration.png")
plt.show()



#f, ax = plt.subplots(figsize=(6.5, 6.5))
#sns.despine(f, left=True, bottom=True)
#sns.scatterplot(x="ttest", y="exact",
#                linewidth=0,
#                data=df, ax=ax)
