#!/usr/bin/env python

#  Created on: October 30, 2013

__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"


import optparse
parser = optparse.OptionParser(version=__version__)
parser.add_option("-i", "--input", dest="input", default="atlas_counting_model/standard_combined_meas_2ph_model.root", help="Input root model.")
parser.add_option("-w", "--wsName", help="Workspace name", type="string", dest="wsName", default="combined")
parser.add_option(      "--interpCode", help="interpcode", type="int", dest="interpCode", default=4)
parser.add_option("-o", "--output", dest="output", default="output/modelWithDifferentInterpcode.root", help="Output file.")

parser.add_option("-q", "--quiet", dest="verbose", action="store_false", default=True, help="Quiet output.")
options,args = parser.parse_args()

import ROOT
ROOT.gROOT.SetBatch( True )



def ModifyInterpolationForAll(ws, code):
	""" Modifies the interpolation code for all FlexibleInterpVars in the workspace. """
	
	funcs = ROOT.RooArgList( ws.allFunctions() )
	for i in range( funcs.getSize() ):
		o = funcs.at(i)
		if hasattr(o,"setAllInterpCodes"):
			print( "Changing interpcode for "+o.GetName()+" from: " )
			o.printAllInterpCodes()
			o.setAllInterpCodes(code)
			print( "to" )
			o.printAllInterpCodes()
			print( "--------" )


if __name__ == "__main__":
	f = ROOT.TFile.Open( options.input, "READ" )
	w = f.Get( options.wsName )

	# modify interp codes
	ModifyInterpolationForAll( w, options.interpCode )	

	w.writeToFile( options.output )
