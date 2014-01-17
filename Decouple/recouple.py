#!/usr/bin/env python

#  Created on: November 26, 2013
__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"

__description__ = """
Second stage of Decouple.
"""

import Decouple.src.effectiveModel

import optparse
parser = optparse.OptionParser(version=__version__, description=__description__)
parser.add_option("-i", "--input", dest="input", default="inputs/atlas_prodModes_hists_and_response_functions.root:ggFttH_VBFVH_eff_2ph", help="Input. The syntax is rootFileName:histName. It is assumed that the etasFile is rootFileName.replace('.root','_table_etas.py'). If that is not the case, it can be specified with rootFileName:histName:etasFileName. It is also assumed that the input is a histogram containing values for -2 ln Lambda. If it is -ln Lambda, a scale of 2 can be specified as the fourth element: rootFileName:histName:etasFileName:2." )
Decouple.src.effectiveModel.addOptionsToParser( parser )
parser.add_option("-o", "--output", dest="output", default=None, help="Output directory. If not given, a directory with the same name as the input file will be created.")
parser.add_option(      "--options_muTmuW", dest="options_muTmuW", default="--range=0.2,0.2,2.5,2.5 --bins=100,100", help="Options for muTmuW scan.")
parser.add_option(      "--options_kVkF", dest="options_kVkF", default="--range=0.2,0.2,2.5,2.5 --bins=100,100", help="Options for kVkF scan.")
parser.add_option(      "--options_kGlukGamma", dest="options_kGlukGamma", default="--range=0.2,0.2,2.5,2.5 --bins=100,100", help="Options for kGlukGamma scan.")

parser.add_option(      "--skip_muTmuW", dest="skip_muTmuW", default=False, action="store_true", help="Skip muTmuW profiled effective scan.")
parser.add_option(      "--skip_kVkF", dest="skip_kVkF", default=False, action="store_true", help="Skip kVkF profiled effective scan.")
parser.add_option(      "--skip_kGlukGamma", dest="skip_kGlukGamma", default=False, action="store_true", help="Skip kGlukGamma profiled effective scan.")

parser.add_option("-q", "--quiet", dest="verbose", action="store_false", default=True, help="Quiet output.")
options,args = parser.parse_args()

if not options.output:
	if ',' in options.input or ' ' in options.input:
		print( "ERROR -- automatic output filename is not supported when doing combination of models. Please specify an output directory using '-o SOMEDIR'.")
		raise

	# determine input filename first from the string of filename:histname:etasfile
	inputFile = options.input
	if ':' in inputFile: inputFile = inputFile[:inputFile.find(':')]
	options.output = inputFile[:inputFile.rfind('/')+1]     # remove filename
	print( "Output will be written to: "+options.output )


import os


def main():
	print( "Creating output directory." )
	os.system( "mkdir -p "+options.output )

	# muTmuW: profiled
	if not options.skip_muTmuW:
		print("\n\n----- muTmuW scan -----\n")
		r = os.system( 'time recouple_mutmuw \
			-i "'+options.input+'" \
			'+options.options_muTmuW+' \
			'+Decouple.src.effectiveModel.optionsString(options)+' \
			--profile \
			--output='+options.output+'muTmuW_profiledContour.root'
		)
		if r != 0: raise

	# kVkF: profiled
	if not options.skip_kVkF:
		print("\n\n----- kVkF scan -----\n")
		r = os.system( 'time recouple_kvkf \
			-i "'+options.input+'" \
			'+options.options_kVkF+' \
			'+Decouple.src.effectiveModel.optionsString(options)+' \
			--profile \
			--output='+options.output+'kVkF_profiledContour.root'
		)
		if r != 0: raise

	# kGlukGamma: profiled
	if not options.skip_kGlukGamma:
		print("\n\n----- kGlukGamma scan -----\n")
		r = os.system( 'time recouple_kglukgamma \
			-i "'+options.input+'" \
			'+options.options_kGlukGamma+' \
			'+Decouple.src.effectiveModel.optionsString(options)+' \
			--profile \
			--output='+options.output+'kGlukGamma_profiledContour.root'
		)
		if r != 0: raise


if __name__ == "__main__":
	main()


