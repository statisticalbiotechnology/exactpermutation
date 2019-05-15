#!/usr/bin/env python3
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from meanperm import *
import multiprocessing
import concurrent.futures as cf
import numpy.random as rnd

def beta_dist_2_5(num_examples):
    return [rnd.beta(2.0,5.0) for _ in range(num_examples)]

def beta_dist_2_10(num_examples):
    return [rnd.beta(2.0,10.0) for _ in range(num_examples)]

def beta_dist_05_05(num_examples):
    return [rnd.beta(.5,.5) for _ in range(num_examples)]

def p_value_calc(args):
    a,b = args
    p=significance_of_mean(a,b)[0]
    return p

def calibration_series_generator(distribution,num_tests,num_examples):
    for _ in range(num_tests):
        a_sample = distribution(num_examples)
        b_sample = distribution(num_examples)
        yield ([a_sample,b_sample])

def calibration_test(distribution,num_tests,num_examples):
    with cf.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()-1) as pool:
        p_list = list(pool.map(p_value_calc, calibration_series_generator(distribution,num_tests,num_examples)))
#    p_list = list(map(p_value_calc, calibration_series_generator(distribution,num_tests,num_examples) ))
    p_list.sort()
    p_arr = np.array(p_list)
    offset = 1.0/float(num_tests)
    ideal_arr = np.linspace(offset,1.0-offset,num_tests)
    return pd.DataFrame({'Observed p-value':p_arr,'Theoretical p-value':ideal_arr})

def my_scatter_plot(df,save_name):
    sns.set(style="white")
    sns.set_context("talk")

    low = min(df["Theoretical p-value"])
    hi = max(df["Theoretical p-value"])
    f, ax = plt.subplots(figsize=(7, 7))
    ax.set(xscale="log", yscale="log")
    g=sns.regplot(x='Theoretical p-value', y ='Observed p-value', data=df,  ax=ax, fit_reg=False, scatter_kws={"s": 5})
    # sns.lmplot(x='Theoretical p-value', y ='Observed p-value', fit_reg=False, data = df, scatter_kws={"marker": "D",  "s": 10})
    # sns.relplot(x='Theoretical p-value', y ='Observed p-value', data = df)
    g.plot([low,hi], [low,hi], 'k-', linewidth=.5)
    sns.despine()
    f.savefig(save_name)

if __name__ == "__main__":
    df = calibration_test(beta_dist_2_5,1000,40)
    my_scatter_plot(df,"beta_2_5_loglog.png")
    df = calibration_test(beta_dist_05_05,1000,40)
    my_scatter_plot(df,"beta_05_05_loglog.png")
