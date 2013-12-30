#!/usr/bin/env python

#  Created on: December 13, 2013

__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"


import optparse
parser = optparse.OptionParser(version=__version__)
parser.add_option("-i", "--input", dest="input", default=None, help="Input folder.")
parser.add_option("-f", "--inputFull", dest="inputFull", default=None, help="Input folder for full model.")
parser.add_option("-s", "--suffix", dest="suffix", default="", help="File suffix of profiled contour.")
parser.add_option("-o", "--output", dest="output", default="output/npComparison/", help="output directory.")
options,args = parser.parse_args()

if not options.inputFull: options.inputFull = options.input

import ROOT
ROOT.gROOT.SetBatch( True )
import helperStyle
import os


def main():
	os.system('mkdir -p '+options.output)

	files = [
		ROOT.TFile.Open( options.inputFull+'muTmuW.root', "READ" ),
		ROOT.TFile.Open( options.input+'muTmuW_statOnly.root', "READ" ),
		ROOT.TFile.Open( options.input+'muTmuW_eff.root', "READ" ),
		ROOT.TFile.Open( options.input+'muTmuW_profiledContour'+options.suffix+'.root', "READ" ),
	]

	namesL = [ k.GetName() for k in files[0].GetListOfKeys() if "nuisParValue_" in k.GetName() ]
	print( 'Plotting these: '+(', '.join(namesL)) )

	c = ROOT.TCanvas( "c1","c1", 1200, 300 )
	for n in namesL:
		c.Clear()
		c.Divide(4,1)

		hists = [ f.Get(n) for f in files if f ]
		print( hists )
		mins = [ h.GetMinimum() for h in hists if h ]
		maxs = [ h.GetMaximum() for h in hists if h ]

		[ (h.SetMinimum( min(mins) ), h.SetMaximum( max(maxs) )) for h in hists if h ]

		for i,h in zip(range(len(hists)), hists):
			if h:
				c.cd(i+1).SetRightMargin(0.16)
				h.GetZaxis().SetTitle("")
				h.Draw("COLZ")

		c.SaveAs(options.output+n+'.eps')


if __name__ == "__main__":
	main()
