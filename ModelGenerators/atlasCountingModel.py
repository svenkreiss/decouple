#!/usr/bin/env python

#  Created on: September 30, 2013

__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"

__description__ = """
Creates a counting model using HistFactory for the H2ph, HZZ4l and HWWlvlv
channels in ATLAS. 

The numbers are taken from these papers and conf notes:
- http://arxiv.org/pdf/1307.1427v1.pdf (combination paper)
- https://cds.cern.ch/record/1523698/files/ATLAS-CONF-2013-012.pdf (2ph conf note)
- http://cds.cern.ch/record/1523699/files/ATLAS-CONF-2013-013.pdf (4l conf note)
"""

import optparse
parser = optparse.OptionParser(version=__version__, description=__description__)
parser.add_option("-q", "--quiet", dest="verbose", action="store_false", default=True, help="Quiet output.")
options,args = parser.parse_args()

import os
import ROOT
ROOT.gROOT.SetBatch( True )


container = []



def factory_2phCombPaper_category( name, nData, nBackground, nGGFTTH, nVBFVH,  ggFTheory = 0.08, nJets = 0 ):
	""" Creates a category with the structure used for 2ph in combination paper table 5. """

	channel = ROOT.RooStats.HistFactory.Channel( name )
	container.append(channel)
	channel.SetData(nData)

	background = ROOT.RooStats.HistFactory.Sample("background")
	background.SetValue(nBackground)
	channel.AddSample(background)
	container.append(background)

	signalGGFttH = ROOT.RooStats.HistFactory.Sample("signalGGFttH")
	signalGGFttH.SetValue(nGGFTTH)
	signalGGFttH.AddNormFactor("mu", 1, 0, 6)
	signalGGFttH.AddNormFactor("mu_XS8_ggF", 1, -5, 10)
	signalGGFttH.AddNormFactor("muT_2ph", 1, -5, 10)
	signalGGFttH.AddOverallSys("QCDscale_Higgs_ggH",  0.87, 1.13)
	if nJets == 2: signalGGFttH.AddOverallSys("QCDscale_Higgs_ggH2in", 1.0-ggFTheory, 1.0+ggFTheory)
	signalGGFttH.AddOverallSys("H2ph_deltaPhiModeling", 0.9, 1.1)
	signalGGFttH.AddOverallSys("H2ph_etaModeling", 0.93, 1.07)
	if nJets == 2: signalGGFttH.AddOverallSys("UE_2jet", 0.92, 1.08)
	channel.AddSample(signalGGFttH)
	container.append(signalGGFttH)

	signalVBFVH = ROOT.RooStats.HistFactory.Sample("signalVBFVH")
	signalVBFVH.SetValue(nVBFVH)
	signalVBFVH.AddNormFactor("mu", 1, 0, 6)
	signalVBFVH.AddNormFactor("mu_XS8_VBF", 1, -5, 10)
	signalVBFVH.AddNormFactor("muW_2ph", 1, -5, 10)
	channel.AddSample(signalVBFVH)
	container.append(signalVBFVH)

	return channel

# From the combination paper. Problem is that the constraint on ggF is actually very 
# loose with these numbers (S/B for untagged category is bad). So these categories should
# not be used here. Better use the set of functions below for numbers from the 2ph note.
def channel_2phCombPaper_looseHighMass2Jets():
	return factory_2phCombPaper_category( "H2phLooseHighMass2Jets", 41, 28, 2.3, 2.7, ggFTheory=0.28, nJets=2 )

def channel_2phCombPaper_tightHighMass2Jets():
	return factory_2phCombPaper_category( "H2phTightHighMass2Jets", 23, 13, 1.8, 5.9, ggFTheory=0.48, nJets=2 )

def channel_2phCombPaper_lowMass2Jets():
	return factory_2phCombPaper_category( "H2phTightLowMass2Jets", 19, 21, 1.5, 1.46, ggFTheory=0.30, nJets=2 )

def channel_2phCombPaper_EtMissSignificance():
	return factory_2phCombPaper_category( "H2phEtMissSignificance", 8, 4, 0.14, 1.0 )

def channel_2phCombPaper_lepton():
	return factory_2phCombPaper_category( "H2phLepton", 20, 12, 0.50, 2.11 )

def channel_2phCombPaper_untagged():
	return factory_2phCombPaper_category( "H2phUntagged", 14248, 13582, 321, 30 )





def factory_2phConfNote_category( name, nData, nBackground, nGGFTTH, nVBFVH,  ggFTheory = 0.08, nJets = 0 ):
	""" Creates a category with the structure used in 2ph conf note in table 1. """

	# shrink uncertainties (1.0 for "do nothing")
	su = 1.0

	# adjust for better agreement with published ATLAS result
	nGGFTTH *= 1.12
	nVBFVH *= 1.05

	# make sure that the systematics have the same for signal and sideband region.
	nameSys = name.replace("Side","")

	channel = ROOT.RooStats.HistFactory.Channel( name )
	container.append(channel)
	channel.SetData(nData)

	background = ROOT.RooStats.HistFactory.Sample("background")
	background.SetValue(nBackground)
	#background.AddOverallSys("H2ph_"+nameSys+"_backgroundModeling", 0.90, 1.10)
	channel.AddSample(background)
	container.append(background)

	signalGGFttH = ROOT.RooStats.HistFactory.Sample("signalGGFttH")
	signalGGFttH.SetValue(nGGFTTH)
	signalGGFttH.AddNormFactor("mu", 1, 0, 6)
	signalGGFttH.AddNormFactor("mu_XS8_ggF", 1, -5, 10)
	signalGGFttH.AddNormFactor("muT_2ph", 1, -5, 10)
	signalGGFttH.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	signalGGFttH.AddOverallSys("QCDscale_Higgs_ggH",  0.87, 1.13)
	if nJets == 2: signalGGFttH.AddOverallSys("QCDscale_Higgs_ggH2in", 1.0 - su*ggFTheory, 1.0 + su*ggFTheory)
	signalGGFttH.AddOverallSys("H2ph_deltaPhiModeling",  1.0 - su*0.1,  1.0 + su*0.1)
	signalGGFttH.AddOverallSys("H2ph_etaModeling",       1.0 - su*0.07, 1.0 + su*0.07)
	if nJets == 2: signalGGFttH.AddOverallSys("UE_2jet", 1.0 - su*0.08, 1.0 + su*0.08)
	channel.AddSample(signalGGFttH)
	container.append(signalGGFttH)

	signalVBFVH = ROOT.RooStats.HistFactory.Sample("signalVBFVH")
	signalVBFVH.SetValue(nVBFVH)
	signalVBFVH.AddNormFactor("mu", 1, 0, 6)
	signalVBFVH.AddNormFactor("mu_XS8_VBF", 1, -5, 10)
	signalVBFVH.AddNormFactor("muW_2ph", 1, -5, 10)
	signalVBFVH.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	channel.AddSample(signalVBFVH)
	container.append(signalVBFVH)

	return channel

# Numbers from the 2ph conf note for the untagged categories. Taking the absolute numbers from table 2
# and it's 90%-of-expected-signal-range, but using the fractional breakdown in production modes form table 1.
#
# For sideband, get expected background from narrow window using the observed events ratio in the 
# Conv. transition category (because it has the lowest S/B): 1 - 2554/14864 = 0.828
# Or using the unconv central low ptt: 1 - 881/(10900-51.8) = 0.919
def channel_2phConfNote_looseHighMass2Jets():
	return factory_2phConfNote_category( "H2phLooseHighMass2Jets", 40, 28, 4.8*0.451, 4.8*(1-0.451), ggFTheory=0.28, nJets=2 )

def channel_2phConfNote_tightHighMass2Jets():
	return factory_2phConfNote_category( "H2phTightHighMass2Jets", 24, 13, 7.3*0.238, 7.3*(1-0.238), ggFTheory=0.48, nJets=2 )

def channel_2phConfNote_lowMass2Jets():
	return factory_2phConfNote_category( "H2phTightLowMass2Jets", 21, 21, 3.0*0.500, 3.0*(1-0.500), ggFTheory=0.30, nJets=2 )

def channel_2phConfNote_EtMissSignificance():
	return factory_2phConfNote_category( "H2phEtMissSignificance", 8, 4, 1.1*0.162, 1.1*(1-0.162) )

def channel_2phConfNote_lepton():
	return factory_2phConfNote_category( "H2phLepton", 19, 12, 2.6*0.208, 2.6*(1-0.208) )


def channel_2phConfNote_unconvCentralLowPTt():
	return factory_2phConfNote_category( "H2phUnconvCentralLowPTt", 911, 881, 46.6*0.935, 46.6*(1-0.935) )

def channel_2phConfNote_unconvCentralHighPTt():
	return factory_2phConfNote_category( "H2phUnconvCentralHighPTt", 49, 44, 7.1*0.807, 7.1*(1-0.807) )

def channel_2phConfNote_unconvRestLowPTt():
	return factory_2phConfNote_category( "H2phUnconvRestLowPTt", 4611, 4347, 97.1*0.933, 97.1*(1-0.933) )

def channel_2phConfNote_unconvRestHighPTt():
	return factory_2phConfNote_category( "H2phUnconvRestHighPTt", 292, 247, 14.4*0.792, 14.4*(1-0.792) )


def channel_2phConfNote_convCentralLowPTt():
	return factory_2phConfNote_category( "H2phConvCentralLowPTt", 722, 687, 29.8*0.938, 29.8*(1-0.938) )

def channel_2phConfNote_convCentralHighPTt():
	return factory_2phConfNote_category( "H2phConvCentralHighPTt", 39, 31, 4.6*0.804, 4.6*(1-0.804) )

def channel_2phConfNote_convRestLowPTt():
	return factory_2phConfNote_category( "H2phConvRestLowPTt", 4865, 4657, 88.0*0.933, 88.0*(1-0.933) )

def channel_2phConfNote_convRestHighPTt():
	return factory_2phConfNote_category( "H2phConvRestHighPTt", 276, 266, 12.9*0.788, 12.9*(1-0.788) )


def channel_2phConfNote_convTransition():
	return factory_2phConfNote_category( "H2phConvTransition", 2554, 2499, 36.1*0.909, 36.1*(1-0.909) )




def channel_4lVBFLike():
	"""
	VBF-like category:
	- 1 observed
	- 0.71 +/- 0.10 expected signel (60% from VBF), cross check with table 2: 0.43 and 0.28
	- S/B = 5
	- sys unc from table 4:
		- theory xs: ggF (21%), VBF (4%), ZZ (35%)
		- ue:        ggF (19%), VBF (4%)
		- jes:       ggF (14%), VBF (10%), ZZ (10%)
	"""
	
	channel = ROOT.RooStats.HistFactory.Channel("HZZ4lVBFLike")
	container.append(channel)
	channel.SetData(1.0)

	signalVBF = ROOT.RooStats.HistFactory.Sample("signalVBF")
	signalVBF.SetValue(0.71 * 0.6)  # 0.71 total signal expected with 60% from VBF
	signalVBF.AddNormFactor("mu", 1, 0, 6)
	signalVBF.AddNormFactor("mu_XS8_VBF", 1, -5, 10)
	signalVBF.AddNormFactor("muW_4l", 1, -5, 10)
	signalVBF.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	signalVBF.AddOverallSys("thxs_VBF",  0.96, 1.04)
	signalVBF.AddOverallSys("UE", 0.96, 1.04)
	signalVBF.AddOverallSys("JES", 0.90, 1.10)
	channel.AddSample(signalVBF)
	container.append(signalVBF)

	signalGGF = ROOT.RooStats.HistFactory.Sample("signalGGF")
	signalGGF.SetValue(0.71 * 0.4)  # 0.71 total signal expected with 40% from ggF
	signalGGF.AddNormFactor("mu", 1, 0, 6)
	signalGGF.AddNormFactor("mu_XS8_ggF", 1, -5, 10)
	signalGGF.AddNormFactor("muT_4l", 1, -5, 10)
	signalGGF.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	signalGGF.AddOverallSys("QCDscale_Higgs_ggH",  0.87, 1.13)
	signalGGF.AddOverallSys("QCDscale_Higgs_ggH2in",  0.79, 1.21)
	signalGGF.AddOverallSys("UE", 0.81, 1.19)
	signalGGF.AddOverallSys("JES", 0.86, 1.14)
	channel.AddSample(signalGGF)
	container.append(signalGGF)

	# to optimize agreement with official ATLAS result, remove ZZ bkg completely
	# ZZ = ROOT.RooStats.HistFactory.Sample("ZZ")
	# ZZ.SetValue( (0.71-0.65) / 5.0 )  # S/B=5
	# channel.AddSample(ZZ)
	# container.append(ZZ)

	return channel

def channel_4lVHLike():
	"""
	VH-like category:
	- 0 observed
	- ggF: 0.06 events, VBF-VH: 0.14 events, ZZ: 0.69 events
	"""
	
	channel = ROOT.RooStats.HistFactory.Channel("HZZ4lVHLike")
	container.append(channel)
	channel.SetData(0.0)

	signalVBF = ROOT.RooStats.HistFactory.Sample("signalVBF")
	signalVBF.SetValue(0.14)
	signalVBF.AddNormFactor("mu", 1, 0, 6)
	signalVBF.AddNormFactor("mu_XS8_VBF", 1, -5, 10)
	signalVBF.AddNormFactor("muW_4l", 1, -5, 10)
	signalVBF.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	# signalVBF.AddOverallSys("thxs_VBF",  0.96, 1.04)
	# signalVBF.AddOverallSys("UE", 0.96, 1.04)
	# signalVBF.AddOverallSys("JES", 0.90, 1.10)
	channel.AddSample(signalVBF)
	container.append(signalVBF)

	signalGGF = ROOT.RooStats.HistFactory.Sample("signalGGF")
	signalGGF.SetValue(0.06)
	signalGGF.AddNormFactor("mu", 1, 0, 6)
	signalGGF.AddNormFactor("mu_XS8_ggF", 1, -5, 10)
	signalGGF.AddNormFactor("muT_4l", 1, -5, 10)
	signalGGF.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	signalGGF.AddOverallSys("QCDscale_Higgs_ggH",  0.87, 1.13)
	# signalGGF.AddOverallSys("QCDscale_Higgs_ggH2in",  0.79, 1.21)
	# signalGGF.AddOverallSys("UE", 0.81, 1.19)
	# signalGGF.AddOverallSys("JES", 0.86, 1.14)
	channel.AddSample(signalGGF)
	container.append(signalGGF)

	ZZ = ROOT.RooStats.HistFactory.Sample("ZZ")
	ZZ.SetValue( 0.69 )
	# ZZ.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	#ZZ.AddOverallSys("JES", 0.90, 1.10)
	channel.AddSample(ZZ)
	container.append(ZZ)

	return channel




def channel_4lggFLike_4mu():
	"""
	ggF-like categories:
	- sys unc from table 1 in combination paper:
		- QCDscale:       ggF (8%), VBF/VH (1%), ttH(+4 -9%)
		- PDF + alpha_s:  ggF (8%), VBF/VH (4%)

	data from table 7 (combination paper):
	- 4mu:    observed 13, signal 6.3, ZZ 2.8, Z+jets 0.55

	Subtracted out the 0.85 expected signal events for VBF and VH categories.
	"""
	
	channel = ROOT.RooStats.HistFactory.Channel("HZZ4lggFLike_4mu")
	container.append(channel)
	channel.SetData(13.0)

	signalGGF = ROOT.RooStats.HistFactory.Sample("signalGGF")
	signalGGF.SetValue((6.3-0.85-1.0) * 0.92)
	signalGGF.AddNormFactor("mu", 1, 0, 6)
	signalGGF.AddNormFactor("mu_XS8_ggF", 1, -5, 10)
	signalGGF.AddNormFactor("muT_4l", 1, -5, 10)
	signalGGF.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	signalGGF.AddOverallSys("QCDscale_Higgs_ggH",  0.87, 1.13)
	signalGGF.AddOverallSys("PDFalphas", 0.92, 1.08)
	#signalGGF.AddOverallSys("UE", 0.81, 1.19)
	channel.AddSample(signalGGF)
	container.append(signalGGF)

	signalVBF = ROOT.RooStats.HistFactory.Sample("signalVBF")
	signalVBF.SetValue((6.3-0.85) * 0.08)
	signalVBF.AddNormFactor("mu", 1, 0, 6)
	signalVBF.AddNormFactor("mu_XS8_VBF", 1, -5, 10)
	signalVBF.AddNormFactor("muW_4l", 1, -5, 10)
	signalVBF.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	signalVBF.AddOverallSys("PDFalphas", 0.92, 1.08)
	#signalVBF.AddOverallSys("UE", 0.81, 1.19)
	channel.AddSample(signalVBF)
	container.append(signalVBF)

	ZZ = ROOT.RooStats.HistFactory.Sample("ZZ")
	ZZ.SetValue( 2.8 )
	# ZZ.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	channel.AddSample(ZZ)
	container.append(ZZ)

	Zjets = ROOT.RooStats.HistFactory.Sample("Zjets")
	Zjets.SetValue( 0.55 )
	#Zjets.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)  # ---- data driven
	channel.AddSample(Zjets)
	container.append(Zjets)

	return channel


def channel_4lggFLike_2e2mu():
	"""
	ggF-like categories:
	- sys unc from table 1 in combination paper:
		- QCDscale:       ggF (8%), VBF/VH (1%), ttH(+4 -9%)
		- PDF + alpha_s:  ggF (8%), VBF/VH (4%)

	data from table 7 (combination paper):
	- 2e2mu: observed 13, signal 7.0, ZZ 3.5, Z+jets 2.11

	Subtracted out the 0.85 expected signal events for VBF and VH categories.
	"""
	
	channel = ROOT.RooStats.HistFactory.Channel("HZZ4lggFLike_2e2mu")
	container.append(channel)
	channel.SetData(13.0)

	signalGGF = ROOT.RooStats.HistFactory.Sample("signalGGF")
	signalGGF.SetValue((7.0-0.85-1.0) * 0.92)
	signalGGF.AddNormFactor("mu", 1, 0, 6)
	signalGGF.AddNormFactor("mu_XS8_ggF", 1, -5, 10)
	signalGGF.AddNormFactor("muT_4l", 1, -5, 10)
	signalGGF.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	signalGGF.AddOverallSys("QCDscale_Higgs_ggH",  0.87, 1.13)
	signalGGF.AddOverallSys("PDFalphas", 0.92, 1.08)
	#signalGGF.AddOverallSys("UE", 0.81, 1.19)
	channel.AddSample(signalGGF)
	container.append(signalGGF)

	signalVBF = ROOT.RooStats.HistFactory.Sample("signalVBF")
	signalVBF.SetValue((7.0-0.85) * 0.08)
	signalVBF.AddNormFactor("mu", 1, 0, 6)
	signalVBF.AddNormFactor("mu_XS8_VBF", 1, -5, 10)
	signalVBF.AddNormFactor("muW_4l", 1, -5, 10)
	signalVBF.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	signalVBF.AddOverallSys("PDFalphas", 0.92, 1.08)
	#signalVBF.AddOverallSys("UE", 0.81, 1.19)
	channel.AddSample(signalVBF)
	container.append(signalVBF)

	ZZ = ROOT.RooStats.HistFactory.Sample("ZZ")
	ZZ.SetValue( 3.5 )
	# ZZ.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	channel.AddSample(ZZ)
	container.append(ZZ)

	Zjets = ROOT.RooStats.HistFactory.Sample("Zjets")
	Zjets.SetValue( 2.11 )
	channel.AddSample(Zjets)
	container.append(Zjets)

	return channel


def channel_4lggFLike_4e():
	"""
	ggF-like categories:
	- sys unc from table 1 in combination paper:
		- QCDscale:       ggF (8%), VBF/VH (1%), ttH(+4 -9%)
		- PDF + alpha_s:  ggF (8%), VBF/VH (4%)

	data from table 7 (combination paper):
	- 4e:    observed 6,  signal 2.6, ZZ 1.2, Z+jets 1.11

	Subtracted out the 0.85 expected signal events for VBF and VH categories.
	"""
	
	channel = ROOT.RooStats.HistFactory.Channel("HZZ4lggFLike_4e")
	container.append(channel)
	channel.SetData(6.0)

	signalGGF = ROOT.RooStats.HistFactory.Sample("signalGGF")
	signalGGF.SetValue((6.3-0.85-1.0) * 0.92)
	signalGGF.AddNormFactor("mu", 1, 0, 6)
	signalGGF.AddNormFactor("mu_XS8_ggF", 1, -5, 10)
	signalGGF.AddNormFactor("muT_4l", 1, -5, 10)
	signalGGF.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	signalGGF.AddOverallSys("QCDscale_Higgs_ggH",  0.87, 1.13)
	signalGGF.AddOverallSys("PDFalphas", 0.92, 1.08)
	#signalGGF.AddOverallSys("UE", 0.81, 1.19)
	channel.AddSample(signalGGF)
	container.append(signalGGF)

	signalVBF = ROOT.RooStats.HistFactory.Sample("signalVBF")
	signalVBF.SetValue((6.3-0.85) * 0.08)
	signalVBF.AddNormFactor("mu", 1, 0, 6)
	signalVBF.AddNormFactor("mu_XS8_VBF", 1, -5, 10)
	signalVBF.AddNormFactor("muW_4l", 1, -5, 10)
	signalVBF.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	signalVBF.AddOverallSys("PDFalphas", 0.92, 1.08)
	#signalVBF.AddOverallSys("UE", 0.81, 1.19)
	channel.AddSample(signalVBF)
	container.append(signalVBF)

	ZZ = ROOT.RooStats.HistFactory.Sample("ZZ")
	ZZ.SetValue( 1.2 )
	# ZZ.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	channel.AddSample(ZZ)
	container.append(ZZ)

	Zjets = ROOT.RooStats.HistFactory.Sample("Zjets")
	Zjets.SetValue( 1.11 )
	channel.AddSample(Zjets)
	container.append(Zjets)

	return channel






# From the combination paper:
# "The VBF process contributes 2%,
# 12% and 81% of the predicted signal in the Njet=0,=1,
# and >= 2 final states, respectively"
#
# The cross sections are more like 87.8% (ggF) versus 12.2% (VBF) which is not used here.

def channel_lvlv_0jet():
	""" Mostly based on table 8 of the combination paper for the uncertainties and
	table 9 for the event counts. """

	channel = ROOT.RooStats.HistFactory.Channel( "HWWlvlv0Jet" )
	container.append(channel)
	channel.SetData(831)

	background = ROOT.RooStats.HistFactory.Sample("background")
	background.SetValue(739*1.02)
	# background.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	# background.AddOverallSys("JES", 0.98, 1.02)
	channel.AddSample(background)
	container.append(background)

	signalGGFttH = ROOT.RooStats.HistFactory.Sample("signalGGFttH")
	signalGGFttH.SetValue(100*1.00*0.98)  # increase by a factor for better agreement with ATLAS contour
	signalGGFttH.AddNormFactor("mu", 1, 0, 6)
	signalGGFttH.AddNormFactor("mu_XS8_ggF", 1, -5, 10)
	signalGGFttH.AddNormFactor("muT_lvlv", 1, -5, 10)
	signalGGFttH.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	signalGGFttH.AddOverallSys("QCDscale_Higgs_ggH",  0.87, 1.13)
	signalGGFttH.AddOverallSys("QCDscale_Higgs_ggH1in",  0.90, 1.10)
	signalGGFttH.AddOverallSys("QCDscale_Higgs_acceptance",  0.96, 1.04)
	signalGGFttH.AddOverallSys("UE", 0.97, 1.03)
	signalGGFttH.AddOverallSys("JES", 0.95, 1.05)
	channel.AddSample(signalGGFttH)
	container.append(signalGGFttH)

	signalVBFVH = ROOT.RooStats.HistFactory.Sample("signalVBFVH")
	signalVBFVH.SetValue(100*1.000*0.02)  # increase by a factor for better agreement with ATLAS contour
	signalVBFVH.AddNormFactor("mu", 1, 0, 6)
	signalVBFVH.AddNormFactor("mu_XS8_VBF", 1, -5, 10)
	signalVBFVH.AddNormFactor("muW_lvlv", 1, -5, 10)
	signalVBFVH.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	signalVBFVH.AddOverallSys("UE", 0.97, 1.03)
	signalVBFVH.AddOverallSys("JES", 0.95, 1.05)
	channel.AddSample(signalVBFVH)
	container.append(signalVBFVH)

	return channel


def channel_lvlv_1jet():
	""" Mostly based on table 8 of the combination paper for the uncertainties and
	table 9 for the event counts. """

	channel = ROOT.RooStats.HistFactory.Channel( "HWWlvlv1Jet" )
	container.append(channel)
	channel.SetData(309)

	background = ROOT.RooStats.HistFactory.Sample("background")
	background.SetValue(261*1.02)
	# background.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	# background.AddOverallSys("JES", 0.97, 1.03)
	channel.AddSample(background)
	container.append(background)

	signalGGFttH = ROOT.RooStats.HistFactory.Sample("signalGGFttH")
	signalGGFttH.SetValue(41*1.00*0.88)  # increase by a factor for better agreement with ATLAS contour
	signalGGFttH.AddNormFactor("mu", 1, 0, 6)
	signalGGFttH.AddNormFactor("mu_XS8_ggF", 1, -5, 10)
	signalGGFttH.AddNormFactor("muT_lvlv", 1, -5, 10)
	signalGGFttH.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	signalGGFttH.AddOverallSys("QCDscale_Higgs_ggH",  0.87, 1.13)
	signalGGFttH.AddOverallSys("QCDscale_Higgs_ggH1in",  1.27, 0.77)
	signalGGFttH.AddOverallSys("QCDscale_Higgs_ggH2in",  1.15, 0.85)
	signalGGFttH.AddOverallSys("QCDscale_Higgs_acceptance",  0.96, 1.04)
	signalGGFttH.AddOverallSys("UE", 1.10, 0.90)
	signalGGFttH.AddOverallSys("JES", 0.98, 1.02)
	channel.AddSample(signalGGFttH)
	container.append(signalGGFttH)

	signalVBFVH = ROOT.RooStats.HistFactory.Sample("signalVBFVH")
	signalVBFVH.SetValue(41*1.000*0.12)  # increase by a factor for better agreement with ATLAS contour
	signalVBFVH.AddNormFactor("mu", 1, 0, 6)
	signalVBFVH.AddNormFactor("mu_XS8_VBF", 1, -5, 10)
	signalVBFVH.AddNormFactor("muW_lvlv", 1, -5, 10)
	signalVBFVH.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	signalVBFVH.AddOverallSys("UE", 1.10, 0.90)
	signalVBFVH.AddOverallSys("JES", 0.98, 1.02)
	channel.AddSample(signalVBFVH)
	container.append(signalVBFVH)

	return channel


def channel_lvlv_2jet():
	""" Mostly based on table 8 of the combination paper for the uncertainties and
	table 9 for the event counts. """

	channel = ROOT.RooStats.HistFactory.Channel( "HWWlvlv2Jet" )
	container.append(channel)
	channel.SetData(55)

	background = ROOT.RooStats.HistFactory.Sample("background")
	background.SetValue(36*1.1)
	# background.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	# background.AddOverallSys("JES", 0.93, 1.07)
	channel.AddSample(background)
	container.append(background)

	signalGGFttH = ROOT.RooStats.HistFactory.Sample("signalGGFttH")
	signalGGFttH.SetValue(10.9*1.00*0.19)  # increase by a factor for better agreement with ATLAS contour
	signalGGFttH.AddNormFactor("mu", 1, 0, 6)
	signalGGFttH.AddNormFactor("mu_XS8_ggF", 1, -5, 10)
	signalGGFttH.AddNormFactor("muT_lvlv", 1, -5, 10)
	signalGGFttH.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	signalGGFttH.AddOverallSys("QCDscale_Higgs_ggH",  0.87, 1.13)
	signalGGFttH.AddOverallSys("QCDscale_Higgs_ggH2in",  0.96, 1.04)
	signalGGFttH.AddOverallSys("QCDscale_Higgs_ggH3in",  0.96, 1.04)
	signalGGFttH.AddOverallSys("QCDscale_Higgs_acceptance_2jet",  0.97, 1.03)
	signalGGFttH.AddOverallSys("UE_2jet", 0.95, 1.05)
	signalGGFttH.AddOverallSys("JES", 0.94, 1.06)
	channel.AddSample(signalGGFttH)
	container.append(signalGGFttH)

	signalVBFVH = ROOT.RooStats.HistFactory.Sample("signalVBFVH")
	signalVBFVH.SetValue(10.9*1.000*0.81)   # increase by a factor for better agreement with ATLAS contour
	signalVBFVH.AddNormFactor("mu", 1, 0, 6)
	signalVBFVH.AddNormFactor("mu_XS8_VBF", 1, -5, 10)
	signalVBFVH.AddNormFactor("muW_lvlv", 1, -5, 10)
	signalVBFVH.AddOverallSys("ATLAS_LUMI_2012",  1.0-0.036, 1.0+0.036)
	signalVBFVH.AddOverallSys("UE_2jet", 0.95, 1.05)
	signalVBFVH.AddOverallSys("JES", 0.94, 1.06)
	channel.AddSample(signalVBFVH)
	container.append(signalVBFVH)

	return channel




def makeMeasurement( name="comb", H2ph=True, HZZ4l=True, HWWlvlv=True, outDir="../output/atlas_counting/", prefix="standard" ):
	meas = ROOT.RooStats.HistFactory.Measurement(name, name)
	container.append( meas )

	meas.SetOutputFilePrefix(outDir+prefix)
	meas.SetPOI("mu")
	meas.AddConstantParam("Lumi")    # 2ph does not have lumi uncertainty. Need to introduce separate systematics
	meas.AddConstantParam("mu_XS8_ggF")
	meas.AddConstantParam("mu_XS8_VBF")
	meas.AddConstantParam("muT_2ph")
	meas.AddConstantParam("muW_2ph")
	meas.AddConstantParam("muT_4l")
	meas.AddConstantParam("muW_4l")
	meas.AddConstantParam("muT_lvlv")
	meas.AddConstantParam("muW_lvlv")

	meas.SetLumi(1.0)
	meas.SetLumiRelErr(0.036)
	meas.SetExportOnly(True)


	if H2ph:
		# meas.AddChannel( channel_2phCombPaper_looseHighMass2Jets() )
		# meas.AddChannel( channel_2phCombPaper_tightHighMass2Jets() )
		# meas.AddChannel( channel_2phCombPaper_lowMass2Jets() )
		# meas.AddChannel( channel_2phCombPaper_EtMissSignificance() )
		# meas.AddChannel( channel_2phCombPaper_lepton() )
		# meas.AddChannel( channel_2phCombPaper_untagged() )

		meas.AddChannel( channel_2phConfNote_looseHighMass2Jets() )
		meas.AddChannel( channel_2phConfNote_tightHighMass2Jets() )
		meas.AddChannel( channel_2phConfNote_lowMass2Jets() )
		meas.AddChannel( channel_2phConfNote_EtMissSignificance() )
		meas.AddChannel( channel_2phConfNote_lepton() )

		meas.AddChannel( channel_2phConfNote_unconvCentralLowPTt() )
		meas.AddChannel( channel_2phConfNote_unconvCentralHighPTt() )
		meas.AddChannel( channel_2phConfNote_unconvRestLowPTt() )
		meas.AddChannel( channel_2phConfNote_unconvRestHighPTt() )
		meas.AddChannel( channel_2phConfNote_convCentralLowPTt() )
		meas.AddChannel( channel_2phConfNote_convCentralHighPTt() )
		meas.AddChannel( channel_2phConfNote_convRestLowPTt() )
		meas.AddChannel( channel_2phConfNote_convRestHighPTt() )

		meas.AddChannel( channel_2phConfNote_convTransition() )


	if HZZ4l:
		meas.AddChannel( channel_4lVBFLike() )
		meas.AddChannel( channel_4lVHLike() )
		meas.AddChannel( channel_4lggFLike_4mu() )
		meas.AddChannel( channel_4lggFLike_2e2mu() )
		meas.AddChannel( channel_4lggFLike_4e() )

	if HWWlvlv:
		meas.AddChannel( channel_lvlv_0jet() )
		meas.AddChannel( channel_lvlv_1jet() )
		meas.AddChannel( channel_lvlv_2jet() )


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
	makeMeasurement( "comb" )
	makeMeasurement( "2ph",  H2ph=True,  HZZ4l=False, HWWlvlv=False )
	makeMeasurement( "4l",   H2ph=False, HZZ4l=True,  HWWlvlv=False )
	makeMeasurement( "lvlv", H2ph=False, HZZ4l=False, HWWlvlv=True  )




