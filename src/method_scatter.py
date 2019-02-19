import pandas as pd
import numpy.random as rnd
import scipy.stats as stat
from meanperm import *
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame(columns=['exact', 'mwu', 'ttest'])

number_of_tests = 500
sample_size = 25

for ix in range(number_of_tests):
    a= rnd.normal(0.0, 1.0, sample_size)
    b= rnd.normal(0.5, 1.0, sample_size)
    p1 = significance_of_mean(a,b)[0]
    p2 = stat.mannwhitneyu(a,b,alternative="two-sided")[1]
    p3 = stat.ttest_ind(a, b)[1]
    print(p1,p2,p3)
    df.loc[ix] = [p1,p2,p3]

sns.set(style="whitegrid")
# Draw a scatter plot while assigning point colors and sizes to different
# variables in the dataset
g = sns.pairplot(df)
g.savefig("method_scatter.png")
plt.show()

#f, ax = plt.subplots(figsize=(6.5, 6.5))
#sns.despine(f, left=True, bottom=True)
#sns.scatterplot(x="ttest", y="exact",
#                linewidth=0,
#                data=df, ax=ax)
