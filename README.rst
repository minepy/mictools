MICtools
========

.. image:: https://travis-ci.org/minepy/mictools.svg?branch=master
    :target: https://travis-ci.org/minepy/mictools

MICtools is an open source pipeline which combines the TIC_e and MIC_e measures
[Reshef2016]_ into a two-step procedure that allows to identify relationships of
various degrees of complexity in large datasets. TIC_e is used to perform 
efficiently a high throughput screening of all the possible pairwise
relationships assessing their significance, while MIC_e is used to rank 
the subset of significant associations on the bases of their strength.

.. image:: docs/images/schema.png

The MICtools pipeline can be broken into 4 steps (see the figure above):

#. given M variables pairs x_i and y_i measured in n samples, the empirical
   TIC_e null distribution is estimated by permutation;
#. TIC_e statistics and the associated empirical p-values are computed for all 
   variable pairs;
#. p-values are corrected for multiplicity in order to control the family-wise
   error rate (FWER) or the false discovery rate (FDR);
#. finally, the strengths of the relationships called significant are estimated 
   using the MIC_e estimator.

Install
-------

Using pip
^^^^^^^^^

.. code-block:: sh

    pip install mictools 

Docker
^^^^^^

#. Install Docker for `Linux <https://docs.docker.com/linux/>`_,
   `Mac OS X <https://docs.docker.com/mac/>`_ or
   `Windows <https://docs.docker.com/windows/>`_.

#. Run the ``Docker Quickstart Terminal`` (Mac OS X, Windows) or the
   ``docker`` daemon (Linux, ``sudo service docker start``).

#. Follow the instructions at https://hub.docker.com/r/minepy/mictools/.

From source
^^^^^^^^^^^

If you are installing from source, the following dependences must be installed:
Python >= 2.7, Click >= 5.1, numpy >= 1.7.0, scipy >= 0.13, pandas >= 0.17.0,
matplotlib >= 1.2.0,<2, statsmodels >= 0.6.1, minepy >= 1.2. We suggest to
install these dependences using the OS package manager (Linux), Homebrew 
(macOS/OS X) or pip.

Download the latest stable version from https://github.com/minepy/mictools/releases
and complete the installation:

.. code-block:: sh

   tar -zxvf mictools-X.Y.Z.tar.gz
   python setup.py install

Usage
-----

MICtools can handle different types of experiments:

* given a single dataset X, with M variables and N samples, MICtools evaluates
  the M+(M-1)/2 possible associations;
* given two datasets, X (MxN) and Y (KxN) (parameter -y/--yvars) MICtools 
  evaluates all the pairwise relationships between the variables of the two
  datasets (for a total of MxK associations). Note that the number samples (N)
  in the datasets X and Y must be the same.
* given two datasets, X (MxN) and Y (KxN) it evaluates all the rowwise 
  relationships (see -r/--rowwise), i.e. only the variables pairs X_i and Y_i
  (for each i in min(M, K)) will be tested;
* moreover, for each experiments listed above, if the sample classes are 
  provided (see -l/--labels and -t/--target), the analysis will be performed 
  within each class independently.

MICtools is implemented as a single command (``mictools'') with the following
subcommands:

``null``
  Compute the TIC_e null distribution.

``mergenull``
  Merge multiple TIC_e null distributions.

``pval``
  Compute TIC_e p-values.

``adjust``
  Multiple testing correction.

``strength``
  Compute the strength (MIC_e).

Tutorials
^^^^^^^^^

.. code-block:: sh

  cd datasets
  X=datasaurus.txt
  ODIR=output
  mkdir $ODIR

  mictools null $X $ODIR/null_dist.txt
  mictools pval $X $ODIR/null_dist.txt $ODIR
  mictools adjust $ODIR/pval.txt $ODIR
  mictools strength $X $ODIR/pval_adj.txt $ODIR/strength.txt











.. [Reshef2016] Yakir A. Reshef, David N. Reshef, Hilary K. Finucane and 
                Pardis C. Sabeti and Michael Mitzenmacher. Measuring Dependence
                Powerfully and Equitably. Journal of Machine Learning Research, 
                2016.