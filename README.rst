MICtools
========

MICtools is an open source pipeline which combines the TIC_e and MIC_e measures
[Reshef2016]_ into a two-step procedure that allows to identify relationships of
various degrees of complexity in large datasets. TIC_e is used to perform 
efficiently a high throughput screening of all the possible pairwise
relationships assessing their significance, while MIC_e is used to rank 
the subset of significant associations on the bases of their strength.

Usage
-----

.. image:: docs/images/schema.png

The MICtools pipeline can be broken into 4 steps (see the figure above):

#. given variables pairs and  measured in samples, the empirical TIC_e null 
   distribution is estimated by permutation;
#. TIC_e statistics and the associated empirical p-values are computed for all 
   variable pairs;
#. p-values are corrected for multiplicity in order to control the family-wise
   error rate (FWER) or the false discovery rate (FDR);
#. finally, the strengths of the relationships called significant are estimated 
   using the MIC_e estimator.

MICtools can handle different types of experiments:

* given a single dataset X, it can evaluate all the pairwise relationships, i.e.
  if your dataset is composed by M variables and N samples, MICtools will test
  M+(M-1)/2 associations;
* given two datasets, X (MxN) and Y (KxN) it can evaluate all the pairwise
  relationships between the variables of the two datasets (parameter 
  -y/--yvars). Note that the number samples (N) in the datasets X and Y must be 
  the same.
* given two datasets, X (MxN) and Y (KxN) it can evaluate all the rowwise 
  relationships, i.e. only the variables X_i and Y_i (for each i in min(M, K))
  will be tested;
* moreover, for each experiments listed above, if the sample classes are 
  provided (see -l/--labels and -t/--target), the analysis will be performed 
  within each class independently.

Usage
-----










.. [Reshef2016] Yakir A. Reshef, David N. Reshef, Hilary K. Finucane and 
                Pardis C. Sabeti and Michael Mitzenmacher. Measuring Dependence
                Powerfully and Equitably. Journal of Machine Learning Research, 
                2016.