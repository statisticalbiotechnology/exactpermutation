#/usr/bin python
import numpy as np

def significance_of_mean(a,b,num_bin = 200, data_type=np.float64): #

    # discretize
    ab = np.sort(np.concatenate((a, b), axis=None))[::-1]
    bins = np.linspace(min(ab), max(ab), num_bin)
    digitized = np.digitize(ab, bins)
    if len(a)>len(b):
        score = sum(np.digitize(b,bins))
    else:
        score = sum(np.digitize(a,bins))
    K = min(len(a),len(b))
    S = np.sum(digitized[0:K])+1
    L = len(ab)
#    NN = score_distribution(digitized,K,S,L,data_type)
    NN = score_distribution_numpy(digitized,K,S,L,data_type)
    one_side = NN[score]/2.0
    if score+1<S:
        one_side += min(np.sum(NN[score+1:]), np.sum(NN[:score]))
    p=one_side*2.0/float(np.sum(NN))
    return p,one_side,np.sum(NN)

def score_distribution(digitized,K,S,L, data_type=np.float64):
    # Initiate matrix
    # N(s,l) number of ways to reach a sum of s using k of the l first readouts
    # Calculated by iterating over the
    N = np.zeros((S,L), dtype=data_type)
    for l in range(L):
        d=digitized[l]
        N[d,l] = data_type(1)
    for k in range(1,K):
        for s in range(S-1,-1,-1):
            row_sum = data_type(0)
            for l in range(L):
                d=digitized[l]
                if l>0:
                    row_sum += N[s,l-1]
                if s+d<S:
                    N[s+d,l] = row_sum
    NN = np.sum(N,axis=1)
    return NN

def score_distribution_numpy(digitized,K,S,L, data_type=np.float64):
    # N(s,l) number of ways to reach a sum of s using k of the l first readouts
    # Calculated by iterating over the
    Nold = np.zeros((S,L), dtype=data_type)
    # Initiating (i.e. k=0 case)
    for l in range(L):
        d=digitized[l]
        Nold[d,l] = data_type(1)
    # Do each of the other picks
    for k in range(1,K):
        Nnew = np.zeros((S,L), dtype=data_type)
        C = np.zeros((S,1), dtype=data_type)
        for l in range(1,L):
            d = digitized[l]
            C +=  Nold[:,l-1:l]
            Nnew[d:S,l] = C[0:S-d,0]
        Nold = Nnew
    NN = np.sum(Nold,axis=1)
    return NN


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
    a = np.array([2.5, 3.7, 4.2])
    b = np.array([8.2, 5.3, 7.6])
#    a= rnd.normal(0.0, 1.0, 50)
#    b= rnd.normal(0.7, 1.0, 50)
    p = significance_of_mean(a,b,4)
    print(p)
    print(stat.mannwhitneyu(a,b,alternative="two-sided"))
    print(stat.ttest_ind(a, b))
