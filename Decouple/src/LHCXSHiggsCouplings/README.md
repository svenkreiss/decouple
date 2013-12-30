# Higgs Couplings

All is based on numbers produced by the LHC Higgs Cross Section Working Group for the Yellow Report 3. To download those and set the environment variable to this data which is required by this package:

```
svn co https://svn.cern.ch/reps/lhchiggsxs/repository/Higgs-coupling/data Higgs-coupling-data
export HIGGSCOUPLINGDATA=$PWD/Higgs-coupling-data
```

This package is just a wrapper for python with convenience functions like linear interpolation in m_H.


# Test

You have to be able to do

```
import LHCXSHiggsCouplings
LHCXSHiggsCouplings.kH2(0.2,0.2,0.2,0.2)
```
in python and get back `0.039985238812654623`.


As a cheap unit test, add this to main:

```
# these should all be one
print( kGamma2(1,1,1,1) )
print( kHGluGlu2(1,1) )
print( kHZGamma2(1,1,1,1) )
print( kH2(1,1,1,1) )
```