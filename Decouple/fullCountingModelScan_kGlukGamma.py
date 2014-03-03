#!/usr/bin/env python

#  Created on: October 8, 2013

__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"


import optparse
parser = optparse.OptionParser(version=__version__)
parser.add_option("-i", "--input", dest="input", default="output/atlas_counting/comb.root", help="Input root model.")
parser.add_option("-w", "--wsName", help="Workspace name", type="string", dest="wsName", default="combined")
parser.add_option("-m", "--mcName", help="ModelConfig name", type="string", dest="mcName", default="ModelConfig")
parser.add_option("-d", "--dataName", help="data name", type="string", dest="dataName", default="obsData")

parser.add_option("-o", "--output", dest="output", default="output/atlas_counting/2ph_4l_lvlv/kGlukGamma.root", help="Output root file.")
parser.add_option("-r", "--range", dest="range", default="0.6,0.4, 1.8,1.6", help="Range for plot.")

parser.add_option("-q", "--quiet", dest="verbose", action="store_false", default=True, help="Quiet output.")
options,args = parser.parse_args()

plotRange = [ float(v) for v in options.range.split(",") ]

import ROOT
import kGlukGamma
import PyROOTUtils
from fullModel_utils import *



def main():
	f = ROOT.TFile.Open( options.input, "READ" )
	w = f.Get( options.wsName )
	mc = w.obj( options.mcName )
	data = w.data( options.dataName )

	# prepare model
	w.var("mu").setVal( 1.0 )
	w.var("mu").setConstant()

	# get nll
	nll = getNll( mc.GetPdf(), data )


	kGam = [100, plotRange[0], plotRange[2]]
	kGlu = [100, plotRange[1], plotRange[3]]
	h = ROOT.TH2F( "kGlukGamma", "Couplings in (k_{g},k_{#gamma});#kappa_{#gamma};#kappa_{g};-2 ln #Lambda",  kGam[0], kGam[1], kGam[2],  kGlu[0], kGlu[1], kGlu[2] )

	for x in range( kGam[0] ):
		kGamVal = kGam[1] + (x+0.5)*(kGam[2]-kGam[1]) / kGam[0]
		print( "Progress: %.0f%%" % (100.0*x/kGam[0]) )
		for y in range( kGlu[0] ):
			kGluVal = kGlu[1] + (y+0.5)*(kGlu[2]-kGlu[1]) / kGlu[0]

			muTmuW2ph = kGlukGamma.map_2ph( kGamVal, kGluVal )
			w.var("muT_2ph").setVal( muTmuW2ph[0] )
			w.var("muW_2ph").setVal( muTmuW2ph[1] )

			muTmuW4l = kGlukGamma.map_4l( kGamVal, kGluVal )
			w.var("muT_4l").setVal( muTmuW4l[0] )
			w.var("muW_4l").setVal( muTmuW4l[1] )

			muTmuWlvlv = kGlukGamma.map_lvlv( kGamVal, kGluVal )
			w.var("muT_lvlv").setVal( muTmuWlvlv[0] )
			w.var("muW_lvlv").setVal( muTmuWlvlv[1] )

			minimize( nll )
			h.SetBinContent( h.FindBin( kGamVal, kGluVal ), 2.0*nll.getVal() )


	PyROOTUtils.subtractMinFromHist( h )

	fOut = ROOT.TFile.Open( options.output, "RECREATE" )
	h.Write()
	fOut.Close()
	print( "Output written to: "+options.output )


if __name__ == "__main__":
	if not options.verbose:
		ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.FATAL)

	main()



