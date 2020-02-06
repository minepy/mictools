##    Copyright 2017 MICtools Developers <davide.albanese@gmail.com>

##    This file is part of MICtools.
##
##    MICtools is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    MICtools is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.

##    You should have received a copy of the GNU General Public License
##    along with MICtools. If not, see <http://www.gnu.org/licenses/>.


import sys

import numpy as np
import pandas as pd

import minepy
import mictools.utils
from mictools import NULL_HIST_RES


def compute_null_oneclass(X, Y=None, rowwise=False, B=9, c=5, nperm=250000, seed=0):

    mictools.utils.check_data(X, Y=Y)

    bins = np.linspace(0, 1, NULL_HIST_RES+1)
    hist = np.zeros(NULL_HIST_RES, dtype=np.int64)
    rs = np.random.RandomState(seed)
    mine = minepy.MINE(alpha=B, c=c, est="mic_e")

    Xa = X.values
    if Y is None:
        idx = np.arange(Xa.shape[0])
        Ya, max_idx_rowwise = None, None
    else:
        Ya = Y.values
        if rowwise:
            max_idx_rowwise = min(Xa.shape[0], Ya.shape[0])
            idx = None

    for n in range(nperm):
        if Y is None:
            i, j = rs.choice(idx, size=2, replace=False)
            x, y = Xa[i], rs.permutation(Xa[j])     
        else:
            if rowwise:
                i = j = rs.randint(max_idx_rowwise)
            else:
                i, j = rs.randint(Xa.shape[0]), rs.randint(Ya.shape[0])

            x, y = Xa[i], rs.permutation(Ya[j])

        mine.compute_score(x, y)
        tic = mine.tic(norm=True)
        hist_idx = min(np.digitize([tic], bins)[0]-1, NULL_HIST_RES-1)
        hist[hist_idx] += 1

    # right-tailed area
    hist_cum = np.cumsum(hist[::-1])[::-1]

    index = pd.MultiIndex.from_arrays([bins[:-1], bins[1:]],
                                      names=('BinStart', 'BinEnd'))
    hist_df = pd.DataFrame({"NullCount": hist, 
                            "NullCountCum": hist_cum},
                            index=index,
                            columns=["NullCount", "NullCountCum"])

    return hist_df


def compute_null(X, labels=None, Y=None, rowwise=False, B=9, c=5, nperm=250000,
                 seed=0):

    mictools.utils.check_data(X, labels=labels, Y=Y)

    if labels is None:
        labels = pd.Series('None', index=X.columns)

    clss = sorted(labels.unique())
    null_dist_list = []
    for cl in clss:
        keep = (cl == labels)
        X_cl = X.loc[:, keep]
        
        if Y is None:
            Y_cl = None
        else:
            Y_cl = Y.loc[:, keep]
            
        null_dist_cl = compute_null_oneclass(
            X_cl, Y_cl, rowwise=rowwise, B=B, c=c, nperm=nperm, seed=seed)

        null_dist_list.append(null_dist_cl)

    null_dist = pd.concat(null_dist_list, axis=0, keys=clss, names=["Class"])

    return null_dist


def null_cmd(xvars_fn, output_fn, labels_fn=None, target=None, yvars_fn=None,
             rowwise=False, nperm=250000, seed=0, grid=9, clumps=5):

    X, labels, Y = mictools.utils.read_data(xvars_fn, labels_fn, target,
                                            yvars_fn)    

    sys.stdout.write("X: {} variables\n".format(X.shape[0]))

    if not Y is None:
        sys.stdout.write("Y: {} variables\n".format(Y.shape[0]))
    
    sys.stdout.write("Samples per class:\n")
    if not labels is None:
        for cl in sorted(labels.unique()):
            sys.stdout.write("* {}: {:d}\n".format(cl, (cl == labels).sum()))
    else:
        sys.stdout.write("* None: {:d}\n".format(X.shape[1]))

    null_dist = compute_null(X=X,
                             labels=labels, 
                             Y=Y, 
                             rowwise=rowwise,
                             B=grid, 
                             c=clumps,
                             nperm=nperm,
                             seed=seed)
    
    null_dist.to_csv(output_fn, sep='\t', float_format="%.6f")


def mergenull_cmd(null_fns, output_fn):
    null_dist = pd.read_csv(null_fns[0], sep='\t', index_col=[0, 1, 2])
    
    for null_fn in null_fns[1:]:
        null_dist_tmp = pd.read_csv(null_fn, sep='\t', index_col=[0, 1, 2])
        null_dist += null_dist_tmp

    null_dist.to_csv(output_fn, sep='\t')
