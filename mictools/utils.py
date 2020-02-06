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


import numpy as np
import pandas as pd

import minepy


def sstats(X, Y, alpha=0.6, c=15, est="mic_approx"):
    mic, tic = [], []
    mine = minepy.MINE(alpha=alpha, c=c, est=est)
    for i in range(min(X.shape[0], Y.shape[0])):
        mine.compute_score(X[i], Y[i])
        mic.append(mine.mic())
        tic.append(mine.tic(norm=True))
    mic, tic = np.asarray(mic), np.asarray(tic)

    return mic, tic


def read_table(input_fn):
    """Read table.
    """
    
    table = pd.read_csv(input_fn, sep='\t', index_col=0)
    # cast index into string
    table.index = [str(elem) for elem in table.index]

    return table


def check_data(X, Y=None, labels=None):
    if not (Y is None):
        if X.shape[1] != Y.shape[1]:
            raise ValueError("different number of samples between X and Y")

        if not (X.columns == Y.columns).all():
            raise ValueError("sample names mismatch between X and Y")

    if not (labels is None):
        if X.shape[1] != labels.shape[0]:
            raise ValueError("different number of samples between X and labels")

        if not (X.columns == labels.index).all():
            raise ValueError("sample names mismatch between X and labels")


def read_data(xvars_fn, labels_fn=None, target=None, yvars_fn=None):

    X = read_table(xvars_fn)
    sample_ids = sorted(X.columns)
    labels = None
    Y = None
    
    if not labels_fn is None:
        if target is None:
            raise ValueError("target (labels file column) is required when the "
                             "labels file is provided")

        labels_df = read_table(labels_fn)

        if not (target in labels_df.columns):
            raise Exception("target {} is not in the labels file".\
                            format(target))
        
        labels = labels_df.loc[labels_df[target].notnull(), target]
        sample_ids = sorted(set(sample_ids) & set(labels.index))

    if not yvars_fn is None:
        Y = read_table(yvars_fn)
        sample_ids = sorted(set(sample_ids) & set(Y.columns))
        Y = Y[sample_ids]
    
    X = X[sample_ids]

    if not labels_fn is None:
        labels = labels[sample_ids]
        
    return X, labels, Y