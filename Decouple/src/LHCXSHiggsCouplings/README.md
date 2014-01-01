# Higgs Couplings

All is based on numbers produced by the LHC Higgs Cross Section Working Group for the Yellow Report 3. This package is just a wrapper for python with convenience functions like linear interpolation in m_H. __You need SVN read access to svn.cern.ch/reps/lhchiggsxs/repository/Higgs-coupling/__.

The data can either reside in a local directory called `Higgs-coupling-data` inside this python module or somewhere on your filesystem and then the `HIGGSCOUPLINGDATA` environment variable needs to be set:

### Yellow Report 3 data in local directory (recommended)
From inside the LHCXSHiggsCouplings directory:

```
svn co https://svn.cern.ch/reps/lhchiggsxs/repository/Higgs-coupling/data Higgs-coupling-data
```

### Yellow Report 3 data somewhere else
To download the data into the subdirectory `Higgs-coupling-data` under the current directory and set the environment variable to tell this module where the data is:

```
svn co https://svn.cern.ch/reps/lhchiggsxs/repository/Higgs-coupling/data Higgs-coupling-data
export HIGGSCOUPLINGDATA=$PWD/Higgs-coupling-data
```


# Test

The default unittests can be run with [nose](http://nose.readthedocs.org/en/latest/) by running

```
nosetests
```
in this directory.
 
To run a test by hand, run

```
import LHCXSHiggsCouplings
LHCXSHiggsCouplings.kH2(0.2,0.2,0.2,0.2)
```
in python and get back `0.039985238812654623`.
