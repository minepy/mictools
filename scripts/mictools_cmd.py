#! /usr/bin/env python

##    Copyright 2016 Davide Albanese <davide.albanese@gmail.com>
##    Copyright 2016 Fondazione Edmund Mach (FEM)

##    This file is part of strainest.
##
##    strainest is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    strainest is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.

##    You should have received a copy of the GNU General Public License
##    along with strainest.  If not, see <http://www.gnu.org/licenses/>.

import os
import os.path

import click

import mictools.null
import mictools.pval
import mictools.strength
from mictools import __version__


labels_help = 'tab-delimited sample labels file (samples x metadata). If this ' \
              'file is provided, the analysis will be performed within each ' \
              'class independently. In order to obtain meaningful results, the ' \
              'number of samples in each class should be roughly the same. The ' \
              'first column must contain the sample IDs.'

target_help = 'labels file column to be used in the per-class analysis (see ' \
              '-l/--labels).'

yvars_help = 'tab-delimited data file (K x N). If this file is provided, the ' \
             'analysis will be performed between all variables of the dataset ' \
             'XVARS and of those of the dataset YVARS.'

rowwise_help = 'when the dataset Y is provided, compute the TICe values between ' \
               'XVARS_i and YVARS_i for each i, instead of XVARS_i and YVARS_j ' \
               'for each i, j.'
    

@click.group()
def cli():
    """MICtools v. {}.""".format(__version__)
    pass

@cli.command()
@click.argument('xvars', type=click.Path(exists=True))
@click.argument('output', type=click.Path(exists=False, writable=True))
@click.option('-l', '--labels', type=click.Path(exists=True), help=labels_help)
@click.option('-t', '--target', type=click.STRING, help=target_help)
@click.option('-y', '--yvars', type=click.Path(exists=True), help=yvars_help)
@click.option('-r', '--rowwise', is_flag=True, help=rowwise_help)
@click.option('-p', '--nperm', type=click.INT, default=200000,
              show_default=True, help='number of permutations.')
@click.option('-s', '--seed', type=click.INT, default=0,
              show_default=True, help="random seed.")
@click.option('-b', '--grid', type=click.INT, default=9,
              show_default=True, help='TICe maximum grid size B(n). Set to 4 '
              'or 6 for less complex alternative hypotheses and to 12 or more '
              'for more complex alternative hypotheses.')
@click.option('-c', '--clumps', type=click.INT, default=5,
              show_default=True, help="TICe c parameter.")
def null(xvars, output, labels, target, yvars, rowwise, nperm, seed, grid,
         clumps):
    """Compute the TICe null distribution.

    XVARS is a tab-delimited data file. The file must contain the variables by
    rows and the samples by columns (M x N columns). The first column
    must contain the variable IDs and the first row the sample IDs. By default,
    all the possible variable pairs ((M*(M-1))/2) are tested.
    
    If YVARS (K x N) is provided, the analysis will be performed between all 
    variables of the dataset XVARS and of those of the dataset YVARS, for a
    total of M x K variable pairs. When the option -r/--rowwise is set, only the
    pairs XVARS_i and YVARS_i for each i are tested.

    If sample classes are provided (see -l/--labels and -t/--target), the
    analysis will be performed within each class independently. Otherwise, a
    single class will be named None.   

    The command returns the TICe null distribution (OUTPUT) for each class.

    Example:

        mictools null data1.txt null_dist.txt -y data2.txt

    will compute the empirical null distribution considering all the variable
    pairs between the dataset data1.txt and the dataset data2.txt.
    """

    mictools.null.null_cmd(xvars, output, labels, target, yvars, rowwise, nperm,
                           seed, grid, clumps)


@cli.command()
@click.argument('null', nargs=-1, type=click.Path(exists=True))
@click.argument('output', nargs=1, type=click.Path(exists=False, writable=True))
def mergenull(null, output):
    """Merge multiple TICe null distributions.

    NULL is the input null distribution(s) and output is the output null
    distribution.

    Example:

        mictools mergenull null_dist_1.txt null_dist_2.txt null_dist.txt

    will merge the independent null distributions null_dist_1.txt and 
    null_dist_2.txt into the output file null_dist.txt.
    """

    mictools.mergenull.mergenull_cmd(null, output)


@cli.command()
@click.argument('xvars', type=click.Path(exists=True))
@click.argument('null', type=click.Path(exists=True))
@click.argument('output', type=click.Path(writable=True, dir_okay=True,
                resolve_path=True))
@click.option('-l', '--labels', type=click.Path(exists=True), help=labels_help)
@click.option('-t', '--target', type=click.STRING, help=target_help)
@click.option('-y', '--yvars', type=click.Path(exists=True), help=yvars_help)
@click.option('-r', '--rowwise', is_flag=True, help=rowwise_help)
@click.option('-b', '--grid', type=click.INT, default=9,
              show_default=True, help='TICe maximum grid size B(n). Set to 4 '
              'or 6 for less complex alternative hypotheses and to 12 or more '
              'for more complex alternative hypotheses.')
@click.option('-c', '--clumps', type=click.INT, default=5,
              show_default=True, help="TICe c parameter.")

def pval(xvars, null, output, labels, target, yvars, rowwise, grid, clumps):
    """Compute TICe p-values.

    XVARS is a tab-delimited data file. The file must contain the variables by
    rows and the samples by columns (M x N columns). The first column
    must contain the variable IDs and the first row the sample IDs. By default,
    all the possible variable pairs ((M*(M-1))/2) are tested.

    NULL is the empirical TICe null distribution (see the null subcommand).
    
    If YVARS (K x N) is provided, the analysis will be performed between all 
    variables of the dataset XVARS and of those of the dataset YVARS, for a
    total of M x K variable pairs. When the option -r/--rowwise is set, only the
    pairs XVARS_i and YVARS_i for each i are tested.

    If sample classes are provided (see -l/--labels and -t/--target), the
    analysis will be performed within each class independently. Otherwise, a
    single class will be named None.

    The command returns in the OUTPUT directory the following files:
        
    \b
    - obs_dist.txt: the observed TICe distribution for each class;
    - obs.txt: the observed TICe values for each variable pair tested in 
               each class;
    - pval.txt: empirical p values for each variable pair tested in 
                each class;
    - pval_CLASS.png: the p values distribution for each class.

    Example:

        mictools pval data1.txt null_dist.txt pval.txt . -y data2.txt

    will compute the TICe p values for each variable pair between the dataset
    data1.txt and the dataset data2.txt.
    """
    
    mictools.pval.pval_cmd(xvars, null, output, labels, target, yvars, rowwise, 
                           grid, clumps)


@cli.command()
@click.argument('pval', type=click.Path(exists=True))
@click.argument('output', type=click.Path(writable=True, dir_okay=True,
                resolve_path=True))
@click.option('-m', '--method', default='qvalue', help='correction method.')
def adjust(pval, output, method):
    """Multiple testing correction.

    PVAL is the input file containing the uncorrected p values (see the 
    pval subcommand). The command returns in the OUTPUT directory the following 
    files: 

    \b
    - pval_adj.txt: adjusted p values for each variable pair tested in 
                    each class.
    - pi0_CLASS.png: if the method (-m/--method) is the qvalue, command will
                     return the estimated pi_0 versus the tuning parameter
                     lambda for each class. 

    The available methods are:

    \b
    - bonferroni: one-step correction
    - sidak: one-step correction
    - holm-sidak: step down method using Sidak adjustments
    - holm: step-down method using Bonferroni adjustments
    - simes-hochberg: step-up method  (independent)
    - hommel: closed method based on Simes tests (non-negative)
    - fdr_bh: Benjamini/Hochberg  (non-negative)
    - fdr_by: Benjamini/Yekutieli (negative)
    - fdr_tsbh: two stage fdr correction (non-negative)
    - fdr_tsbky: two stage fdr correction (non-negative)
    - qvalue: Storey's q value (smoother method)

    Example:

        mictools adjust pval.txt .
    """

    mictools.pval.adjust_cmd(pval, output, method)


@cli.command()
@click.argument('xvars', type=click.Path(exists=True))
@click.argument('pval', type=click.Path(exists=True))
@click.argument('output', type=click.Path(exists=False, writable=True))
@click.option('-l', '--labels', type=click.Path(exists=True), help=labels_help)
@click.option('-t', '--target', type=click.STRING, help=target_help)
@click.option('-y', '--yvars', type=click.Path(exists=True), help=yvars_help)
@click.option('-p', '--thr', type=click.FLOAT, default=0.05,
              show_default=True, help="significance threshold.")
@click.option('-a', '--alpha', type=click.FLOAT, default=None,
              show_default=True, help="MICe alpha parameter. Automatically "
              "chosen by default.")
@click.option('-c', '--clumps', type=click.INT, default=5,
              show_default=True, help="MICe c parameter.")
def strength(xvars, pval, output, labels, target, yvars, thr, alpha, clumps):
    """Compute the strength (MICe).
    
    Compute the strength (MICe) on the variable pairs called significant at
    the significance threshold THR (parameter -p/--thr).
    
    XVARS is a tab-delimited data file. The file must contain the variables by
    rows and the samples by columns (M x N columns). The first column
    must contain the variable IDs and the first row the sample IDs. By default,
    all the possible variable pairs ((M*(M-1))/2) are tested.
    
    If YVARS (K x N) is provided, the analysis will be performed between all 
    variables of the dataset XVARS and of those of the dataset YVARS, for a
    total of M x K variable pairs.

    If sample classes are provided (see -l/--labels and -t/--target), the
    analysis will be performed within each class independently. In this case,
    the relationships called significant in at least one class are evaluated.

    The OUTPUT file contains MICe, the Pearson and the Spearman's rank 
    correlation coefficients and the TICe p values in each class.

    Example:

        mictools strength data1.txt pval_adj.txt strength.txt -y data2.txt
    """

    mictools.strength.strength_cmd(xvars, pval, output, labels, target, yvars,
                                   thr, alpha, clumps)
                                   