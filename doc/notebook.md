# Notebook for exactpermutation project

## 2019-02-19 Generated scatter plot

I tested 500 draws of 2-sample comparisons with 25 picks each from 2 normal distributions with slightly
shifted means. I tested this against my exact test, a mann-whiteney u-test and a standard t-test. The script
found in
[../src/method_scatter.py](../blob/master/src/method_scatter.py)
It seems like my exact test follows the t-test pretty well for these normal distributed data.
![alt text][scatter1]
[scatter1]: ../blob/master/doc/img/method_scatter.png "Scatter plot"



## 2019-02-18 First version
I implemented a first running prototype of the code, and checked it in as meanperm.py
