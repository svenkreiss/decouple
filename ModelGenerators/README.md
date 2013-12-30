# Two Bin

Simple test models for the paper.


# ATLAS counting

More realistic test models with numbers taken from ATLAS papers.


# Notes for ATLAS official model

## HepData submission scripts

ATLAS internal script to convert ROOT objects to hepdata format:

```
svn co svn+ssh://skreiss@svn.cern.ch/reps/atlasphys/Physics/SUSY/Tools/HepDataTools/trunk HepDataTools

python HepDataTools/hepconverter.py -i inputs/atlas_prodModes_hists.root --supress-errors -o inputs/atlas_prodModes_hists
```


## For comparison

For comparison, the expressions that Haoshuang uses are in these xml files:

```
/afs/cern.ch/atlas/project/HSG7/Spring2013/Couplings/combination/v8/coupling/xml/CVCF_125.5.xml
/afs/cern.ch/atlas/project/HSG7/Spring2013/Couplings/combination/v8/coupling/xml/CGaCGl_125.5.xml
```


As a cheap unit test, add this to main:

```
# these should all be one
print( kGamma2(1,1,1,1) )
print( kHGluGlu2(1,1) )
print( kHZGamma2(1,1,1,1) )
print( kH2(1,1,1,1) )
```