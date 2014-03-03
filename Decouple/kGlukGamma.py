#!/usr/bin/env python

#  Created on: August 20, 2013
__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"


import effectiveModel

import optparse
parser = optparse.OptionParser(version=__version__)
parser.add_option("-i", "--input", dest="input", default="inputs/atlas_prodModes_hists_and_response_functions.root:ggFttH_VBFVH_eff_2ph", help="""Input. 
	The syntax is rootFileName:histName. It is assumed that the etasFile is 
	rootFileName.replace('.root','_table_etas.py'). If that is not the case, 
	it can be specified with rootFileName:histName:etasFileName. It is also 
	assumed that the input is a histogram containing values for -2 ln Lambda. 
	If it is -ln Lambda, a scale of 2 can be specified as the fourth 
	element: rootFileName:histName:etasFileName:2. If a fifth argument is specified,
	then it is assumed that also a name for the etas type is given:
	rootFileName:histName:etasFileName:etasType:2
	Multiple inputs can be separated by commas and/or spaces.
""" )
effectiveModel.addOptionsToParser( parser )
parser.add_option("-o", "--output", dest="output", default="output/kGlukGamma.root", help="Output root file.")
parser.add_option("-r", "--range", dest="range", default="0.8,0.6,1.9,1.6", help="Range for plot.")
parser.add_option("-b", "--bins", dest="bins", default="200,200", help="Bins for plot.")
parser.add_option("-q", "--quiet", dest="verbose", action="store_false", default=True, help="Quiet output.")
options,args = parser.parse_args()

plotRange = [ float(v) for v in options.range.split(",") ]
bins = [ int(v) for v in options.bins.split(",") ]

import ROOT
ROOT.gROOT.SetBatch( True )
import PyROOTUtils


from LHCHiggsCouplings import *

def map_2ph( kGam,kGlu ):
	# convert to muT,muW coordinates
	muT = kGlu*kGlu * kGam*kGam / kH2_GamGlu(kGam,kGlu)
	muW = kGam*kGam             / kH2_GamGlu(kGam,kGlu)
	return (muT,muW)

def map_4l( kGam,kGlu ):
	# convert to muT,muW coordinates
	muT = kGlu*kGlu / kH2_GamGlu(kGam,kGlu)
	muW = 1.0       / kH2_GamGlu(kGam,kGlu)
	return (muT,muW)

def map_lvlv( kGam,kGlu ):
	# convert to muT,muW coordinates
	muT = kGlu*kGlu / kH2_GamGlu(kGam,kGlu)
	muW = 1.0       / kH2_GamGlu(kGam,kGlu)
	return (muT,muW)


def main():
	inputs = effectiveModel.getInputs( options.input )
	for i in inputs:
		if "2ph" in i[2]: i[2] = map_2ph
		elif "4l" in i[2]: i[2] = map_4l
		elif "lvlv" in i[2]: i[2] = map_lvlv
		else:
			print( "WARNING: Didn't find functional replacement for "+i[2] )

	kGam = [bins[0], plotRange[0], plotRange[2]]
	kGlu = [bins[1], plotRange[1], plotRange[3]]
	h = ROOT.TH2F( "kGlukGamma", "Couplings in (k_{g},k_{#gamma});#kappa_{#gamma};#kappa_{g};-2 ln #Lambda",  kGam[0], kGam[1], kGam[2],  kGlu[0], kGlu[1], kGlu[2] )

	npHistograms = {}
	effectiveModel.fillHist( h,kGam,kGlu,inputs, options, npHistograms=npHistograms )
	PyROOTUtils.subtractMinFromHist( h )


	outF = effectiveModel.outFileName( options.output, options )
	fOut = ROOT.TFile.Open( outF, "RECREATE" )
	h.Write()
	for npH in npHistograms.values(): npH.Write()
	fOut.Close()
	print( "Output written to: "+outF )


if __name__ == "__main__":
	main()
