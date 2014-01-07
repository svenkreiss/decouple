# Decouple and Recouple

This repository contains the software implementation for our paper __A Novel Approach to Higgs Coupling Measurements__ (Cranmer, Kreiss, Lopez-Val, Plehn), [arXiv:1401.0080 \[hep-ph\]](http://arxiv.org/abs/1401.0080). It contains tools to apply the discussed methods to new models and contains a Makefile to recreate the plots in the paper.

A demo for the recoupling stage where the effective likelihood and template parametrization are readily provided is at [decoupledDemo](http://github.com/svenkreiss/decoupledDemo).


# Prerequisites

On the python side, please have the modules `numpy` and `progressbar` installed and extend your PYTHONPATH environment variable with the path to `decouple`:

```
export PYTHONPATH=/Path/to/your/decouple:$PYTHONPATH
```

You will also need a version of ROOT with PyROOT enabled.

**Higgs Coupling numbers from Yellow Report 3**:
The module `LHCXSHiggsCouplings` (included in this repository) is required to run the benchmark coupling models. Please see the [README file](Decouple/src/LHCXSHiggsCouplings/README.md). To get started quickly, just run from the root repository directory:

```
svn co https://svn.cern.ch/reps/lhchiggsxs/repository/Higgs-coupling/data Decouple/src/LHCXSHiggsCouplings/Higgs-coupling-data
```


### Additional prerequisites for decouple.py

You don't need this additional part for the `decoupledDemo` project.

You need the right ROOT version. There are a few features that are not in main root yet:

- BatchProfileLikelihood scripts
- proper HistFactory copy constructors for python counting models

To get the version that is used for development, use something like:

```
git clone -b development https://github.com/svenkreiss/root.git root_branch_v534
```

NOTE: currently, you need the special branch `hfBugs` instead of `development` that fixes the copy constructors in HistFactory.

In addition to the PYTHONPATH extension above, you will then also need:

```
export PYTHONPATH=$ROOTSYS/tutorials/roostats/py:$PYTHONPATH
```



# Running on any model

You can create your own model and run `decouple.py` and `recouple.py` on them. `decouple.py` takes root files with a RooWorkspace, containing the model as input and produces the effective Likelihood and eta files. `recouple.py` takes eta files and effective Likelihoods (also from multiple channels to do a combination) and produces coupling results.

Example models are in the module ModelGenerators ([README file](ModelGenerators/README.md)).

A fully working example that _recouples_ a model that someone else decoupled is implemented in the [decoupledDemo](http://github.com/svenkreiss/decoupledDemo) project.


# Creating plots for the paper

Run everything with

```
make -j8
```

This tells `make` to use parallel builds with 8 jobs in parallel. All profiled effective scans are implemented using the `multiprocessing` python module which will use as many jobs as there are CPUs. So this can lead to 8 make jobs where each runs 8 multiprocessing jobs.

For finer control, the framework can also be run step-by-step:

1. `make models`: runs the makefile inside the `ModelGenerators` module
2. `make decouple`: runs Decouple/decouple.py on all the models generated with `ModelGenerators`. For finer control, `make decoupleTwoBin` and `make decoupleAtlasCounting` runs the two sets individually.
3. `make recouple`: runs Decouple/recouple.py on all decouple outputs. Also here, there are `make recoupleTwoBin` and `make recoupleAtlasCounting`.
4. `make plots`

The above chain can be used as a best-practice example to setup your own models. The Makefile is just a guide so that you can see how to run `Decouple/decouple.py` and `Decouple/recouple.py` yourself on your own models.

