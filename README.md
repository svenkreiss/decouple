# Decouple and Recouple

This repository contains the software implementation for our paper __A Novel Approach to Higgs Coupling Measurements__ (Cranmer, Kreiss, Lopez-Val, Plehn), [arXiv:1401.0080 \[hep-ph\]](http://arxiv.org/abs/1401.0080). It contains tools to apply the discussed methods to new models and contains a Makefile to recreate the plots in the paper.

A demo for the recoupling stage where the effective likelihood and template parametrization are readily provided is at [decoupledDemo](http://github.com/svenkreiss/decoupledDemo).


# Install

Clone the repository. Then create a `virtualenv` (which usually comes with your python environment or can be insalled) and install this package and all requirements with pip:

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

For development and to use the latest versions of all dependencies, use `requirements_dev.txt`.


# Running on any model

You can create your own model and run `decouple` and `recouple` on them. `decouple` takes root files with a RooWorkspace, containing the model as input and produces the effective Likelihood and eta files. `recouple` takes eta files and effective Likelihoods (also from multiple channels to do a combination) and produces coupling results.

Example models are in the module ModelGenerators.

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


# Related Packages

This package depends on a few related Python packages that are generally useful. For this package, they are installed automatically by `pip` with the install instructions above.

* [LHCHiggsCouplings](http://github.com/svenkreiss/LHCHiggsCouplings): Interface to cross sections and branching ratios published by the LHC Higgs Cross Section Working Group with interpolation in Higgs mass.
* [BatchLikelihoodScan](http://github.com/svenkreiss/BatchLikelihoodScan): Powerful tool for likelihood scans and easily runs on batch clusters.
* [PyROOTUtils](http://github.com/svenkreiss/PyROOTUtils): Collection of useful tools for working with TGraphs and generally plotting with ROOT.