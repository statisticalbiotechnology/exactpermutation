import pandas as pd
import numpy as np
import numpy.random as rnd
import scipy.stats as stat
import seaborn as sns
import matplotlib.pyplot as plt
import sys
sys.path.append("../../src/")

from scatter_plots import *

cll_data = pd.read_csv("eig_stat_cll.csv",  delimiter="\t")
scatter_from_df(cll_data,'_n_0','_y_0','cll_',200)

