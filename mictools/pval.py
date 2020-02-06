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


import os
import os.path
import sys
import itertools

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import minepy
import mictools.utils
import mictools.mtest
from mictools import NULL_HIST_RES


def compute_pval_oneclass(X, null_dist, Y=None, single=False, B=9, c=5):

    mictools.utils.check_data(X, Y=Y)

    bins = np.linspace(0, 1, NULL_HIST_RES+1)

    # observed values/distribution
    names=['Var1', 'Var2']
    Xa = X.values
    if Y is None:
        _, tic = minepy.pstats(Xa, alpha=B, c=c, est="mic_e")
        index = pd.MultiIndex.from_tuples(
            list(itertools.combinations(X.index, 2)), names=names)
    else:
        Ya = Y.values
        if single:
            _, tic = mictools.utils.sstats(Xa, Ya, alpha=B, c=c, est="mic_e")
            index = pd.MultiIndex.from_arrays([X.index, Y.index], names=names)
        else:
            _, tic = minepy.cstats(Xa, Ya, alpha=B, c=c, est="mic_e")
            index = pd.MultiIndex.from_product([X.index, Y.index], names=names)
            tic = tic.flatten()

    observed_hist = np.histogram(tic, bins)[0].astype(np.int64)

    # right-tailed area
    observed_hist_cum = np.cumsum(observed_hist[::-1])[::-1]

    # p-values
    null_hist_cum = null_dist["NullCountCum"].values
    pval = (np.interp(tic, bins[:-1], null_hist_cum) + 1) / \
        (null_hist_cum[0] + 1)
    pval = pd.Series(pval, index=index)
    
    # observed
    obs = pd.Series(tic, index=index)
    
    # distribution
    index = pd.MultiIndex.from_arrays([bins[:-1], bins[1:]],
                                      names=('BinStart', 'BinEnd'))
    obs_dist = pd.DataFrame({"ObsCount": observed_hist,
                             "ObsCountCum": observed_hist_cum},
                            index=index,
                            columns=["ObsCount", "ObsCountCum"])

    return obs_dist, obs, pval


def compute_pval(X, null_dist, labels=None, Y=None, single=False, B=9, c=5):

    mictools.utils.check_data(X, labels=labels, Y=Y)

    if labels is None:
        labels = pd.Series('None', index=X.columns)

    clss = sorted(labels.unique())
    obs_dist_list, obs_list, pval_list = [], [], []
    for cl in clss:
        keep = (cl == labels)
        X_cl = X.loc[:, keep]
        null_dist_cl = null_dist.loc[cl]

        if Y is None:
            Y_cl = None
        else:
            Y_cl = Y.loc[:, keep]
            
        obs_dist_cl, obs_cl, pval_cl = compute_pval_oneclass(
            X_cl, null_dist_cl, Y_cl, single=single, B=B, c=c)

        obs_cl.name = cl
        pval_cl.name = cl
        obs_dist_list.append(obs_dist_cl)
        obs_list.append(obs_cl)
        pval_list.append(pval_cl)
    
    obs_dist = pd.concat(obs_dist_list, axis=0, keys=clss, names=["Class"])
    obs = pd.concat(obs_list, axis=1)
    pval = pd.concat(pval_list, axis=1)
    
    return obs_dist, obs, pval


def plot_pval(pval, output_dir):

    BINS = 50

    for cl in pval.columns:
        fig = plt.figure(figsize=(10, 4))
        ax1 = plt.subplot(111)
        bins = np.linspace(0, 1, BINS+1)
        hist, bin_edges = np.histogram(pval[cl], bins=bins, density=True)
        plt.bar(bin_edges[:-1], hist, width=1/BINS, log=False,
                linewidth=1, color="white", edgecolor="black")
        plt.xlabel("p-value")
        plt.ylabel("Density")

        output_fn = os.path.join(output_dir, "pval_{}.png".format(cl))
        fig.savefig(output_fn, bbox_inches='tight', dpi=300, format='png')


def pval_cmd(xvars_fn, null_fn, output_dir, labels_fn=None, target=None,
             yvars_fn=None, single=False, grid=9, clumps=5):

    X, labels, Y = mictools.utils.read_data(xvars_fn, labels_fn, target,
                                            yvars_fn)    
    null_dist = pd.read_csv(null_fn, sep='\t', index_col=[0, 1, 2])

    obs_dist, obs, pval = compute_pval(X=X,
                                       null_dist=null_dist,
                                       labels=labels, 
                                       Y=Y, 
                                       single=single,
                                       B=grid, 
                                       c=clumps)

    ntotperm = null_dist["NullCountCum"].iloc[0]
    minpval = 1 / ntotperm
    sys.stdout.write("The minimum p-value with a total of {:d} permutations is "
                     "{:e}\n".format(ntotperm, minpval))

    try:
        os.makedirs(output_dir)
    except OSError:
        if not os.path.isdir(output_dir):
            sys.stderr.write("directory {} cannot be created\n".\
                             format(output_dir))
            exit(1)
    
    obs_dist.to_csv(os.path.join(output_dir, "obs_dist.txt"), sep='\t',
                    float_format="%.6f")
    obs.to_csv(os.path.join(output_dir, "obs.txt"), sep='\t',
               float_format='%.6f')
    pval.to_csv(os.path.join(output_dir, "pval.txt"), sep='\t',
                float_format='%e')
    plot_pval(pval, output_dir)


def plot_pi0(pi0, pi0_lmb, lmb, pi0_smooth, output_fn):
    fig = plt.figure(figsize=(6, 6))
    ax1 = plt.subplot(111)
    plt.plot(lmb, pi0_lmb, 'ko')
    if not pi0_smooth is None:
        plt.plot(lmb, pi0_smooth, 'k', label='Quadratic smoothing')
    plt.axhline(pi0, linestyle='--', color='r', label='pi0')
    plt.xlabel("lambda")
    plt.ylabel("pi0(lambda)")
    plt.legend()
    fig.savefig(output_fn, bbox_inches='tight', dpi=300, format='png')


def adjust_cmd(pval_fn, output_dir, method='qvalue'):

    pval = pd.read_csv(pval_fn, sep='\t', index_col=[0, 1])
    pval_adj = pd.DataFrame(index=pval.index, columns=pval.columns)
    
    try:
        os.makedirs(output_dir)
    except OSError:
        if not os.path.isdir(output_dir):
            sys.stderr.write("directory {} cannot be created\n".\
                             format(output_dir))
            exit(1)

    for cl in pval.columns:
        if method == 'qvalue':
            pval_adj[cl], pi0, pi0_lmb, lmb, pi0_smooth = \
                mictools.mtest.qvalue(pval[cl])
            output_plot_fn = os.path.join(output_dir, "pi0_{}.png".format(cl))
            plot_pi0(pi0, pi0_lmb, lmb, pi0_smooth, output_plot_fn)
        else:
            pval_adj[cl] = mictools.mtest.multipletests(pval[cl], method=method)
    
    output_fn = os.path.join(output_dir, "pval_adj.txt")
    pval_adj.to_csv(output_fn, sep='\t', float_format='%e')