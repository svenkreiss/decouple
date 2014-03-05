#!/usr/bin/env python

#  Created on: July 8, 2013
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
parser.add_option("-o", "--output", dest="output", default="output/muTmuW_profiledContour.root", help="Output root file.")
parser.add_option("-r", "--range", dest="range", default="0.2,-1.5,2.5,6.0", help="Range for plot.")
parser.add_option("-b", "--bins", dest="bins", default="50,50", help="Bins for plot.")
parser.add_option("-q", "--quiet", dest="verbose", action="store_false", default=True, help="Quiet output.")
options,args = parser.parse_args()

plotRange = [ float(v) for v in options.range.split(",") ]
bins = [ int(v) for v in options.bins.split(",") ]

import ROOT
ROOT.gROOT.SetBatch( True )
import PyROOTUtils



def unit( x,y ):
	return (x,y)

def main():
	inputs = effectiveModel.getInputs( options.input )
	for i in inputs: i[2] = unit   # This function has to be pickle'able. Lambda functions are not allowed.

	x = [bins[0], plotRange[0], plotRange[2]]
	y = [bins[1], plotRange[1], plotRange[3]]
	h  = ROOT.TH2F( "muTmuW", "(#mu^{f}_{ggF+ttH},#mu^{f}_{VBF+VH}) plane;#mu^{f}_{ggF+ttH};#mu^{f}_{VBF+VH};-2 ln #Lambda",  x[0], x[1], x[2],  y[0], y[1], y[2] )

	npHistograms = {}
	effectiveModel.fillHist( h,x,y,inputs, options, npHistograms=npHistograms )
	PyROOTUtils.subtractMinFromHist( h )


	outF = effectiveModel.outFileName( options.output, options )
	fOut = ROOT.TFile.Open( outF, "RECREATE" )
	h.Write()
	for npH in npHistograms.values(): npH.Write()
	fOut.Close()
	print( "Output written to: "+outF )


if __name__ == "__main__":
	main()
