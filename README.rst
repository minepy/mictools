MICtools
========

MICtools is an open source pipeline which combines the TIC_e and MIC_e measures
[Reshef2016]_ into a two-step procedure that allows to identify relationships of
various degrees of complexity in large datasets. TIC_e is used to perform 
efficiently a high throughput screening of all the possible pairwise
relationships assessing their significance, while MICe is used to rank 
the subset of significant associations on the bases of their strength.

.. image:: docs/images/schema.png
    :width: 200pt

The procedure can be broken into 4 steps (see Figure): i) Given variables pairs
and  measured in  samples, the empirical TIC_e null distribution is estimated by 
permutation; ii) TIC_e statistics and the associated empirical p-values are
computed for all variable pairs; iii) p-values are corrected for multiplicity in
order to control the family-wise error rate (FWER) or the FDR; iv) finally, the
strengths of the relationships called significant are estimated using the MICe
estimator.
