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
import os
import os.path
import csv

import numpy as np
import pandas as pd
import scipy.stats

import minepy
import mictools.utils


NPOINTS_BINS = [1,    25,   50,   250,   500, 1000, 2500, 5000, 10000, 40000]
ALPHAS =       [0.85, 0.80, 0.75, 0.70, 0.65, 0.6,  0.55, 0.5,  0.45,  0.4]


def compute_alpha(npoints):
    if npoints < 1:
        raise ValueError("the number of points must be >=1")

    return ALPHAS[np.digitize([npoints], NPOINTS_BINS)[0] - 1]


def compute_strength(X, pval, output_fn, labels=None, Y=None, t=0.05,
                     alpha=None, c=5):

    mictools.utils.check_data(X, labels=labels, Y=Y)

    if labels is None:
        labels = pd.Series('None', index=X.columns)

    # compute MIC_e for pairs with at least one p-value < t
    index = pval.index[(pval < t).sum(axis=1) > 0]
  
    if alpha is None:
        sys.stdout.write("Automatically chosen alphas:\n")

    strength_handle = open(output_fn, 'w')
    strength_writer = csv.writer(strength_handle, delimiter='\t',
                                 lineterminator='\n')
    header = ["Class", "Var1", "Var2", "TICePVal", "PearsonR", "SpearmanRho",
              "MICe"]

    strength_writer.writerow(header)

    clss = sorted(labels.unique())
    for cl in clss:
        keep = (cl == labels)
        X_cl = X.loc[:, keep]

        if Y is not None:
            Y_cl = Y.loc[:, keep]

        if alpha is None:
            alpha_cl = compute_alpha(X_cl.shape[1])
            sys.stdout.write("* {}: {:f}\n".format(cl, alpha_cl))
        else:
            alpha_cl = alpha
        
        mine = minepy.MINE(alpha=alpha_cl, c=c, est="mic_e")

        for var1, var2 in index:
            x = X_cl.loc[var1]
            y = X_cl.loc[var2] if Y is None else Y_cl.loc[var2]
            mine.compute_score(x, y)
            mic = mine.mic()
            p = pval.loc[(var1, var2), cl]
            R, _ = scipy.stats.pearsonr(x, y)
            rho, _ = scipy.stats.spearmanr(x, y)

            row = [cl,
                   var1,
                   var2,
                   "{:e}".format(p),
                   "{:.6f}".format(R),
                   "{:.6f}".format(rho),
                   "{:.6f}".format(mic)]

            strength_writer.writerow(row)

    strength_handle.close()


def strength_cmd(xvars_fn, pval_fn, output_fn, labels_fn=None, target=None,
                 yvars_fn=None, t=0.05, alpha=None, clumps=5):

    X, labels, Y = mictools.utils.read_data(xvars_fn, labels_fn, target,
                                            yvars_fn)

    pval = pd.read_csv(pval_fn, sep='\t', dtype={"Var1": str, "Var2": str})
    pval.set_index(["Var1", "Var2"], inplace=True)
   
    compute_strength(X=X,
                     pval=pval,
                     output_fn=output_fn,
                     labels=labels, 
                     Y=Y,
                     t=t,
                     alpha=alpha,
                     c=clumps)
