#/usr/bin python
import numpy as np

def significance_of_mean(a,b,num_bin = 50, data_type=np.float64): #

    # discretize
    ab = np.sort(np.concatenate((a, b), axis=None))[::-1]
    bins = np.linspace(min(ab), max(ab), num_bin)
    digitized = np.digitize(ab, bins)
    K = min(len(a),len(b))
    S = np.sum(digitized[0:K])+1
    if len(a)>len(b):
        score = sum(np.digitize(b,bins))
    else:
        score = sum(np.digitize(a,bins))
    L = len(ab)
#    print(digitized)
#    print(K,S,L,score)
    N = np.zeros((S,L), dtype=data_type)
    for l in range(L):
        b=digitized[l]
        N[b,l] = np.uint64(1)
    for k in range(1,K):
#        print(np.sum(N,axis=1))
#        print(N)
        for s in range(S-1,-1,-1):
            row_sum = data_type(0)
            for l in range(L):
                b=digitized[l]
                if l>0:
                    row_sum += N[s,l-1]
                if s+b<S:
#                    print(s,b,l,row_sum)
                    N[s+b,l] = row_sum
    NN = np.sum(N,axis=1)
#    print(NN)
#    print(np.sum(NN))
    one_side = NN[score]/2.0
    if score+1<S:
        one_side += min(np.sum(NN[score+1:]), np.sum(NN[:score]))
    p=one_side*2.0/float(np.sum(NN))
    return p,one_side,np.sum(NN)

if __name__ == "__main__":
    import argparse
    import sys
    import pandas as pd
    import numpy.random as rnd
    import scipy.stats as stat
#    parser = argparse.ArgumentParser(description='Calculates statistics for network enrichment of pathways.')
#    parser.add_argument('networkfile', type=argparse.FileType('r'),
#        help='Filename of Network file')
#    parser.add_argument('pathwayfile', type=argparse.FileType('r'),
#        help='Filename of Pathway file')
#    parser.add_argument('querygenesfile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,help='Filename of File with query genes. If omitted the gene names will be read from STDIN')
#    parser.add_argument('-s','--singlepathway', metavar='PATHWAY',default='',help='The examined pathway. If omitted, all pathways in the pathway file will be tested.')
#    parser.add_argument('-n','--networktreshold', default=0.7, metavar='float', type=float)

#    args = parser.parse_args()

#    a = np.array([2.5, 3.7, 4.2,5.0,4.0,2.9,3.2])
#    b = np.array([8.2, 5.3, 7.6,6.3,6.2,5.2,8.7])
    a= rnd.normal(0.0, 1.0, 50)
    b= rnd.normal(0.7, 1.0, 50)
    p = significance_of_mean(a,b)
    print(p)
    print(stat.mannwhitneyu(a,b,alternative="two-sided"))
    print(stat.ttest_ind(a, b))
