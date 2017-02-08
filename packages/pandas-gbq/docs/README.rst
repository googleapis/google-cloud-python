To build a local copy of the pandas-gbq docs, install the programs in
requirements-docs.txt and run 'make html'. If you use the conda package manager
these commands suffice::

  git clone git@github.com:pydata/pandas-gbq.git
  cd dask/docs
  conda create -n pandas-gbq-docs --file requirements-docs.txt
  source activate pandas-gbq-docs
  make html
  open build/html/index.html
