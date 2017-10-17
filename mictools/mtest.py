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


from __future__ import division

import warnings

import numpy as np
import scipy.interpolate
import scipy.stats
import statsmodels.stats.multitest


def pi0est(pvals, lmb=np.arange(0.05, 1, 0.05), method="smoother"):
    pvals_arr = np.asarray(pvals, dtype=np.float)
    lmb_arr = np.atleast_1d(lmb)

    if pvals_arr.ndim != 1:
        raise ValueError("p must be an 1d array_like object")

    if lmb_arr.ndim > 1:
        raise ValueError("lmb must be an 1d array_like object or a single "
                         "value")

    m = pvals_arr.shape[0]
    n = lmb_arr.shape[0]
    lmb_arr = np.sort(lmb_arr)

    if (pvals_arr.min() < 0) or (pvals_arr.max() > 1):
        raise ValueError("p-values ('pvals') are not in valid range [0, 1]")
    
    if (n > 1) and (n <4):
        raise ValueError("if length of lambda ('lmb') is greater than 1, you "
                         "need at least 4 values")

    if (lmb_arr.min() < 0) or (lmb_arr.max() >= 1):
        raise ValueError("lambdas ('lmb') are not in valid range [0, 1)")

    if n == 1:
        pi0 = np.mean(pvals_arr >= lmb[0]) / (1 - lmb[0])
        pi0_lambda = pi0
        pi0 = min(pi0, 1)
        pi0_smooth = None
    else:
        pi0 = np.asarray([np.mean(pvals_arr > l) / (1 - l) for l in lmb])
        pi0_lambda = pi0

        if method == "smoother":
            spl = scipy.interpolate.LSQUnivariateSpline(lmb, pi0, t=[], k=2)
            pi0_smooth = spl(lmb)
            pi0 = min(pi0_smooth[-1], 1)

        elif method == "bootstrap":
            pi0_min = np.percentile(pi0, 10)
            w = np.asarray([np.sum(pvals_arr > l) for l in lmb])
            mse = (w / (m**2 * (1 - lmb)**2)) * (1 - w/m) + (pi0 - pi0_min)**2
            pi0 = min(pi0[np.where(mse == np.min(mse))[0][0]], 1)
            pi0_smooth = None

        else:
            raise ValueError("method must be one of 'smoother' or 'bootstrap'")

    if pi0 <= 0:
        warnings.warn("estimated pi0 <= 0. Check that you have valid "
                      "p-values or use a different range of lambda")
    
    return pi0, pi0_lambda, lmb_arr, pi0_smooth


def qvalue(pvals, pfdr=False, **kwargs):
    pvals_arr = np.asarray(pvals, dtype=np.float)

    if pvals_arr.ndim != 1:
        raise ValueError("p must be an 1d array_like object")

    pi0, pi0_lmb, lmb, pi0_smooth = pi0est(pvals_arr, **kwargs)

    m = pvals_arr.shape[0]
    u = np.argsort(pvals_arr)
    v = scipy.stats.rankdata(pvals_arr, method='max')

    if pfdr:
        with np.errstate(invalid='ignore', divide='ignore'):
            qvals = (pi0 * m * pvals_arr) / (v * (1 - (1 - pvals_arr)**m))
    else:
        qvals = (pi0 * m * pvals_arr) / v
    
    qvals[u[m-1]] = min(qvals[u[m-1]], 1)
    for i in range(m-2, -1, -1):
        qvals[u[i]] = min(qvals[u[i]], qvals[u[i+1]])

    return qvals, pi0, pi0_lmb, lmb, pi0_smooth


def multipletests(pvals, method='hs'):
    _, pvals_adj, _, _ = statsmodels.stats.multitest.multipletests(
        pvals, method=method)

    return pvals_adj