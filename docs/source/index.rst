.. STAVAG documentation master file, created by
   sphinx-quickstart on Wed Nov 12 15:28:06 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Uncovering directionally and temporally variable genes with STAVAG
==================================================================

.. toctree::
   :maxdepth: 1
   :titlesonly:
   :caption: Tutorials

   Case_I_STAVAG_on_2D_cSCC_data
   Case_II_STAVAG_on_3D_planarian_data
   Case_III_STAVAG_on_STARmap_3D_cortex
   Case_IV_STAVAG_on_mouse_myocardial_infarction_progression_data
   Case_V_STAVAG_on_mouse_embryonic_development_data

----

Overview of STAVAG
==================

.. image:: STAVAG_overview.png
   :width: 600
   :align: left


STAVAG can handle spatial transcriptomics data for single, 3D, or multiple slices coupled with temporal information. STAVAG takes spatial transcriptomics data as input and then fits the spatial or temporal direction of spatial data with gene expression using a gradient boosting tree for regression. STAVAG calculates the gene contribution score along any given direction or temporal progression for each gene and identifies directionally variable genes (DVGs) and temporally variable genes (TVGs) for different scenarios.

Installation
============

Set up conda environment for STAVAG:

.. code-block:: bash

   conda create -n STAVAG python==3.9

activate STAVAG from shell:

.. code-block:: bash

   conda activate STAVAG

you can install the important Python packages used to run the model are as follows:

.. code-block:: bash

   pip install "scanpy[leiden]"
   pip install lightgbm
   pip install numpy
   pip install matplotlib
   pip install scikit-learn
   pip install scipy

Citation
========

Shen Q, Gai K, Li S, et al. Uncovering directionally and temporally variable genes with STAVAG. bioRxiv, 2025. doi:10.1101/2025.09.02.673732
