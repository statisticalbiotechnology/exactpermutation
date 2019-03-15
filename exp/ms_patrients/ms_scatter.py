import pandas as pd
import numpy as np
import numpy.random as rnd
import scipy.stats as stat
import seaborn as sns
import matplotlib.pyplot as plt
import sys
sys.path.append("../../src/")

from scatter_plots import *

ms_data = pd.read_csv("stat_eig_df_tab_delim.csv",  delimiter="\t")
scatter_from_df(ms_data,'_H_0','_M_0','ms_',200)
