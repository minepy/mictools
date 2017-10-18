MICtools
========

MICtools is an open source pipeline which combines the TIC_e and MIC_e measures
[Reshef2016]_ into a two-step procedure that allows to identify relationships of
various degrees of complexity in large datasets. TIC_e is used to perform 
efficiently a high throughput screening of all the possible pairwise
relationships assessing their significance, while MIC_e is used to rank 
the subset of significant associations on the bases of their strength.

.. image:: docs/images/schema.png

The procedure can be broken into 4 steps (see Figure):

#. given variables pairs and  measured in  samples, the empirical TIC_e null 
   distribution is estimated by permutation;
#. TIC_e statistics and the associated empirical p-values are computed for all 
   variable pairs;
#. p-values are corrected for multiplicity in order to control the family-wise
   error rate (FWER) or the false discovery rate (FDR);
#. finally, the strengths of the relationships called significant are estimated 
   using the MIC_e estimator.










.. [Reshef2016] Yakir A. Reshef, David N. Reshef, Hilary K. Finucane and 
                Pardis C. Sabeti and Michael Mitzenmacher. Measuring Dependence
                Powerfully and Equitably. Journal of Machine Learning Research, 
                2016.