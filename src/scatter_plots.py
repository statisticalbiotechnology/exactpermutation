import pandas as pd
import numpy as np
import numpy.random as rnd
import scipy.stats as stat
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from meanperm import *
from pathlib import Path

result_df = pd.DataFrame(columns=['exact', 'mwu', 'ttest'])
rix = 0
def log_result(result):
    # result_list is modified only by the main process, not the pool workers.
    global result_df
    global rix
    result_df.loc[rix] = result
    rix += 1

def p_value_calc(a,b,dig_res):
    p1 = significance_of_mean(a,b,dig_res)[0]
    p2 = stat.mannwhitneyu(a,b,alternative="two-sided")[1]
    p3 = stat.ttest_ind(a, b)[1]
    print([p1,p2,p3])
    return [p1,p2,p3]

# Generic Thread pool code from https://gist.github.com/heavywatal/d05a8c8a9c38ab5c895464b1d64c224f
import multiprocessing
import multiprocessing.pool as mpp
def mpp_tp(call,tasks,lg_result):
    with mpp.ThreadPool(multiprocessing.cpu_count()-1) as pool:
        results = [pool.apply_async(call, args=tpl, callback=lg_result) for tpl in tasks]
        pool.close()
        pool.join()
#        for async_result in results:
#            try:
#                lg_result(async_result.get())
#            except ValueError as e:
#                print(e)

def _core_async(data,a_pattern,b_pattern,prefix,dig_res):
        a_cols = [col for col in data.columns if a_pattern in col]
        b_cols = [col for col in data.columns if b_pattern in col]

        tasks =[]
        for index, row in data.iterrows():
            a = np.array(row[a_cols],dtype='float64')
            b = np.array(row[b_cols],dtype='float64')
            tasks.append((a,b,dig_res,))
        mpp_tp(p_value_calc,tasks,log_result)

def _core(data,a_pattern,b_pattern,prefix,dig_res):
        a_cols = [col for col in data.columns if a_pattern in col]
        b_cols = [col for col in data.columns if b_pattern in col]
        for index, row in data.iterrows():
            a = np.array(row[a_cols],dtype='float64')
            b = np.array(row[b_cols],dtype='float64')
            ps = p_value_calc(a,b,dig_res)
            log_result(ps)


def scatter_from_df(data,a_pattern,b_pattern,prefix="my_",dig_res=200,pkl_file="pvals.pkl",threaded=True):
    global result_df
    result_file = Path(pkl_file)
    if not result_file.exists():
        if threaded:
            _core_async(data,a_pattern,b_pattern,prefix,dig_res)
        else:
            _core(data,a_pattern,b_pattern,prefix,dig_res)
        result_df.to_pickle(result_file)
    else:
        result_df = pd.read_pickle(result_file)

    sns.set(style="white")
    sns.set_context("talk")
    g = sns.pairplot(result_df,plot_kws={"s": 3})
    sns.despine()
    g.savefig(prefix+"3meth_calibration.png")
    plt.show()

    low = min(result_df["exact"])
    hi = max(result_df["exact"])
    f, ax = plt.subplots(figsize=(7, 7))
    ax.set(xscale="log", yscale="log")
    g=sns.regplot("exact", "ttest", result_df, ax=ax, fit_reg=False, scatter_kws={"s": 3})
    g.plot([low,hi], [low,hi], 'k-', linewidth=1)
    sns.despine()
    f.savefig(prefix+"loglog_calibration.png")
    plt.show()
