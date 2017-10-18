# MICtools - Docker

MICtools is an open source pipeline which combines the TIC_e and MIC_e measures
into a two-step procedure that allows to identify relationships of
various degrees of complexity in large datasets. TIC_e is used to perform 
efficiently a high throughput screening of all the possible pairwise
relationships assessing their significance, while MIC_e is used to rank 
the subset of significant associations on the bases of their strength.
Homepage: https://github.com/minepy/mictools.

## Quickstart

1. Download the latest version:

   `docker pull minepy/mictools`

2. Run an instance of the image, mounting the host working directory
   (e.g. ``/Users/davide/mictools``) on to the container working directory
   ``/mictools``:

   `docker run --rm -t -i -v /Users/davide/mictools:/mictools -w /mictools minepy/mictools /bin/bash`

   You need to write something like ``-v //c/Users/davide/mictools:/mictools`` if
   you are in Windows or ``-v /home/davide/mictools:/mictools`` in Linux. The
   ``--rm`` option automatically removes the container when it exits.

3. Run mictools without parameters:

   `root@68f6784e1101:/mictools# mictools`
