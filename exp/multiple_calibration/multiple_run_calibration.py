import pandas as pd
import sys
sys.path.append("../../src/")

from calibration_test import *

def repeated_calibration_test(repeat,dist,num_features,num_individuals):
    my_dfs = []
    for _ in range(repeat):
        my_dfs.append(calibration_test(dist,num_features,num_individuals))
    return pd.concat(my_dfs, ignore_index=True)

if __name__ == "__main__":

    df = repeated_calibration_test(20,beta_dist_2_5,1000,40)
    my_scatter_plot(df,"repeated_beta_2_5_loglog.png")
    df = repeated_calibration_test(20,beta_dist_05_05,1000,40)
    my_scatter_plot(df,"repeated_beta_05_05_loglog.png")
