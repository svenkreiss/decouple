#!/usr/bin/env python

#  Created on: October 21, 2013

__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"

__description__ = """
Creates a 2-bin counting model using HistFactory. 
"""

import optparse
parser = optparse.OptionParser(version=__version__, description=__description__)
parser.add_option(      "--scenario", dest="scenario", default=-1, type="float", help="Scenario 1, 2 or 3. Use zero for default scenario that is also valid for #alphas!=2.")
parser.add_option(      "--additiveMu", dest="additiveMu", default=False, action="store_true", help="Enables emulation of additive mu.")
parser.add_option("-n", "--name", dest="name", default="meas", help="Name for output filename.")
parser.add_option("-p", "--prefix", dest="prefix", default="standard", help="Prefix for output filename.")
parser.add_option("-q", "--quiet", dest="verbose", action="store_false", default=True, help="Quiet output.")
options,args = parser.parse_args()

import os
import ROOT
ROOT.gROOT.SetBatch( True )


container = []



def category_ggFLike(n=100.0, fGGF=0.9, fVBF=0.1, fB=0.0, etaGGF=0.2, etaVBF=0.2):
	"""
	Toy model bin with ggF-like systematics.
	"""
	
	channel = ROOT.RooStats.HistFactory.Channel("ggFLike")
	container.append(channel)
	channel.SetData(n)

	signalGGF = ROOT.RooStats.HistFactory.Sample("signalGGF")
	signalGGF.SetValue(n*fGGF)
	if not options.additiveMu:
		signalGGF.AddNormFactor("mu", 1, 0, 6)
		signalGGF.AddNormFactor("mu_XS8_ggF", 1, -5, 10)
	signalGGF.AddOverallSys("sys",  1.0-etaGGF, 1.0+etaGGF)
	signalGGF.AddOverallSys("sys_GGF",  1.0-etaGGF, 1.0+etaGGF)
	channel.AddSample(signalGGF)
	container.append(signalGGF)

	signalVBF = ROOT.RooStats.HistFactory.Sample("signalVBF")
	signalVBF.SetValue(n*fVBF)
	if not options.additiveMu:
		signalVBF.AddNormFactor("mu", 1, 0, 6)
		signalVBF.AddNormFactor("mu_XS8_VBF", 1, -5, 10)
	signalVBF.AddOverallSys("sys",  1.0-etaVBF, 1.0+etaVBF)
	signalVBF.AddOverallSys("sys_VBF",  1.0-etaVBF, 1.0+etaVBF)
	channel.AddSample(signalVBF)
	container.append(signalVBF)

	if options.additiveMu:
		signalGGFMu = ROOT.RooStats.HistFactory.Sample("signalGGFMu")
		signalGGFMu.SetValue(n*fGGF)
		signalGGFMu.AddNormFactor("mu", 1, 0, 6)
		signalGGFMu.AddNormFactor("mu_XS8_ggF", 1, -5, 10)
		channel.AddSample(signalGGFMu)
		container.append(signalGGFMu)

		signalGGFM1 = ROOT.RooStats.HistFactory.Sample("signalGGFM1")
		signalGGFM1.SetValue(-n*fGGF)
		channel.AddSample(signalGGFM1)
		container.append(signalGGFM1)

		signalVBFMu = ROOT.RooStats.HistFactory.Sample("signalVBFMu")
		signalVBFMu.SetValue(n*fVBF)
		signalVBFMu.AddNormFactor("mu", 1, 0, 6)
		signalVBFMu.AddNormFactor("mu_XS8_VBF", 1, -5, 10)
		channel.AddSample(signalVBFMu)
		container.append(signalVBFMu)

		signalVBFM1 = ROOT.RooStats.HistFactory.Sample("signalVBFM1")
		signalVBFM1.SetValue(-n*fVBF)
		channel.AddSample(signalVBFM1)
		container.append(signalVBFM1)

	background = ROOT.RooStats.HistFactory.Sample("background")
	background.SetValue(n*fB)
	channel.AddSample(background)
	container.append(background)

	return channel


def category_VBFLike(n=100.0, fGGF=0.1, fVBF=0.9, fB=0.0, etaGGF=0.2, etaVBF=0.2, etaGGFAsym=0.0):
	"""
	Toy model bin with VBF-like systematics.
	"""
	
	channel = ROOT.RooStats.HistFactory.Channel("VBFLike")
	container.append(channel)
	channel.SetData(n)

	signalGGF = ROOT.RooStats.HistFactory.Sample("signalGGF")
	signalGGF.SetValue(n*fGGF)
	if not options.additiveMu:
		signalGGF.AddNormFactor("mu", 1, 0, 6)
		signalGGF.AddNormFactor("mu_XS8_ggF", 1, -5, 10)
	signalGGF.AddOverallSys("sys",  1.0-etaGGF, 1.0+etaGGF)
	signalGGF.AddOverallSys("sys_GGF",  1.0-etaGGF+etaGGFAsym/2.0, 1.0+etaGGF+etaGGFAsym/2.0)
	channel.AddSample(signalGGF)
	container.append(signalGGF)

	signalVBF = ROOT.RooStats.HistFactory.Sample("signalVBF")
	signalVBF.SetValue(n*fVBF)
	if not options.additiveMu:
		signalVBF.AddNormFactor("mu", 1, 0, 6)
		signalVBF.AddNormFactor("mu_XS8_VBF", 1, -5, 10)
	signalVBF.AddOverallSys("sys",  1.0-etaVBF, 1.0+etaVBF)
	signalVBF.AddOverallSys("sys_VBF",  1.0-etaVBF, 1.0+etaVBF)
	channel.AddSample(signalVBF)
	container.append(signalVBF)

	if options.additiveMu:
		signalGGFMu = ROOT.RooStats.HistFactory.Sample("signalGGFMu")
		signalGGFMu.SetValue(n*fGGF)
		signalGGFMu.AddNormFactor("mu", 1, 0, 6)
		signalGGFMu.AddNormFactor("mu_XS8_ggF", 1, -5, 10)
		channel.AddSample(signalGGFMu)
		container.append(signalGGFMu)

		signalGGFM1 = ROOT.RooStats.HistFactory.Sample("signalGGFM1")
		signalGGFM1.SetValue(-n*fGGF)
		channel.AddSample(signalGGFM1)
		container.append(signalGGFM1)

		signalVBFMu = ROOT.RooStats.HistFactory.Sample("signalVBFMu")
		signalVBFMu.SetValue(n*fVBF)
		signalVBFMu.AddNormFactor("mu", 1, 0, 6)
		signalVBFMu.AddNormFactor("mu_XS8_VBF", 1, -5, 10)
		channel.AddSample(signalVBFMu)
		container.append(signalVBFMu)

		signalVBFM1 = ROOT.RooStats.HistFactory.Sample("signalVBFM1")
		signalVBFM1.SetValue(-n*fVBF)
		channel.AddSample(signalVBFM1)
		container.append(signalVBFM1)

	background = ROOT.RooStats.HistFactory.Sample("background")
	background.SetValue(n*fB)
	channel.AddSample(background)
	container.append(background)

	return channel







def makeMeasurement( name="meas", outDir="../output/twoBin/", prefix="standard" ):
	meas = ROOT.RooStats.HistFactory.Measurement(name, name)
	container.append( meas )

	meas.SetOutputFilePrefix(outDir+prefix)
	meas.SetPOI("mu")
	meas.AddConstantParam("Lumi")    # 2ph does not have lumi uncertainty. Need to introduce separate systematics
	meas.AddConstantParam("mu_XS8_ggF")
	meas.AddConstantParam("mu_XS8_VBF")

	meas.SetLumi(1.0)
	meas.SetLumiRelErr(0.036)
	meas.SetExportOnly(True)

	# first set of scenarios
	if options.scenario == -1:		
		# one sys, cat uni etas
		meas.AddChannel( category_ggFLike() )
		meas.AddChannel( category_VBFLike() )
		meas.AddConstantParam("alpha_sys_VBF")
		meas.AddConstantParam("alpha_sys_GGF")
	elif options.scenario == -2:		
		# one sys, not cat uni etas
		meas.AddChannel( category_ggFLike() )
		meas.AddChannel( category_VBFLike( etaVBF=0.1 ) )
		meas.AddConstantParam("alpha_sys_VBF")
		meas.AddConstantParam("alpha_sys_GGF")
	elif options.scenario == -3:		
		# one sys, cat uni etas
		meas.AddChannel( category_ggFLike() )
		meas.AddChannel( category_VBFLike() )
		meas.AddConstantParam("alpha_sys")
	elif options.scenario == -4:		
		# one sys, not cat uni etas
		meas.AddChannel( category_ggFLike( fB=0.04, etaGGF=0.0 ) )
		meas.AddChannel( category_VBFLike( fGGF=0.5, fVBF=0.4, etaVBF=0.1, etaGGF=0.2, etaGGFAsym=0.2, fB=0.04 ) )
		meas.AddConstantParam("alpha_sys")

	# scenarios suggested by Kyle
	if options.scenario == 1:
		meas.AddChannel( category_ggFLike( fGGF=0.45, fVBF=0.05, fB=0.5 ) ) 
		meas.AddChannel( category_VBFLike() )
		meas.AddConstantParam("alpha_sys_VBF")
		meas.AddConstantParam("alpha_sys_GGF")
	elif options.scenario == 1.1: # same as scenario 1 with twice as many events, but same signal xs
		meas.AddChannel( category_ggFLike( n=125, fGGF=0.45/1.25, fVBF=0.05/1.25, fB=0.5/1.25 ) ) 
		meas.AddChannel( category_VBFLike() )
		meas.AddConstantParam("alpha_sys_VBF")
		meas.AddConstantParam("alpha_sys_GGF")
	elif options.scenario == 2:
		meas.AddChannel( category_ggFLike( etaGGF=0.1, fGGF=0.45, fVBF=0.05, fB=0.5 ) )
		meas.AddChannel( category_VBFLike( etaGGF=0.3 ) )
		meas.AddConstantParam("alpha_sys_VBF")
		meas.AddConstantParam("alpha_sys_GGF")
	elif options.scenario == 3:
		meas.AddChannel( category_ggFLike( etaGGF=0.0, etaVBF=0.0, fGGF=0.45, fVBF=0.05, fB=0.5 ) )
		meas.AddChannel( category_VBFLike( etaGGF=0.2, etaVBF=0.0, fGGF=0.4,  fVBF=0.6,  fB=0.0 ) )
		meas.AddConstantParam("alpha_sys_VBF")
		meas.AddConstantParam("alpha_sys_GGF")
	elif options.scenario == 3.1: # same as scenario 3, but with best fit values moved
		meas.AddChannel( category_ggFLike( etaGGF=0.0, etaVBF=0.0, fGGF=0.45/1.25, fVBF=0.05/1.5, fB=0.5/1.25 ) )
		meas.AddChannel( category_VBFLike( etaGGF=0.2, etaVBF=0.0, fGGF=0.4/1.25,  fVBF=0.6/1.5,  fB=0.0/1.25 ) )
		meas.AddConstantParam("alpha_sys_VBF")
		meas.AddConstantParam("alpha_sys_GGF")
	elif options.scenario == 4: # like 2, but with doubled etas
		meas.AddChannel( category_ggFLike( etaGGF=0.2, etaVBF=0.4, fGGF=0.45, fVBF=0.05, fB=0.5 ) ) 
		meas.AddChannel( category_VBFLike( etaGGF=0.6, etaVBF=0.4 ) )
		meas.AddConstantParam("alpha_sys_VBF")
		meas.AddConstantParam("alpha_sys_GGF")




	#meas.CollectHistograms()
	meas.PrintTree()
	print( "Creating output directory." )
	os.system( "mkdir -p "+outDir )
	meas.PrintXML(outDir+name+"_xml", meas.GetOutputFilePrefix());
	ROOT.RooStats.HistFactory.MakeModelAndMeasurementFast(meas);

	# change from std histfactory naming
	print("mv "+outDir+"/"+prefix+"_combined_"+name+"_model.root "+outDir+"/"+name+".root")
	os.system("mv "+outDir+"/"+prefix+"_combined_"+name+"_model.root "+outDir+"/"+name+".root")

	print( "Done "+name+"." )
 



if __name__ == "__main__":
	makeMeasurement( name=options.name, prefix=options.prefix )




