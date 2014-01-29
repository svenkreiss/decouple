#!/usr/bin/env python

#  Created on: November 26, 2013
__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"

__description__ = """
First stage of Decouple.
"""

import optparse
parser = optparse.OptionParser(version=__version__, description=__description__)
parser.add_option("-i", "--input", dest="input", default="../output/atlas_counting/standard_combined_meas_model.root", help="Input root model.")
parser.add_option("-w", "--wsName", help="Workspace name", type="string", dest="wsName", default="combined")
parser.add_option("-m", "--mcName", help="ModelConfig name", type="string", dest="mcName", default="ModelConfig")
parser.add_option("-d", "--dataName", help="data name", type="string", dest="dataName", default="obsData")

parser.add_option("-p", "--parameters", help="parameters", type="string", dest="parameters", default="")

parser.add_option("-r", "--range", dest="range", default="0.3,0.3,2.0,2.0", help="Range for plot.")
parser.add_option("-b", "--bins", dest="bins", default="100,100", help="Bins for plot.")

parser.add_option(      "--skip_etas", dest="skip_etas", default=False, action="store_true", help="Skip etas.")
parser.add_option(      "--skip_eff", dest="skip_eff", default=False, action="store_true", help="Skip eff.")
parser.add_option(      "--skip_fullScan", dest="skip_fullScan", default=False, action="store_true", help="Skip scan of the full model.")

parser.add_option("-o", "--output", dest="output", default=None, help="Output directory. If not given, a directory with the same name as the input file will be created.")

parser.add_option("-q", "--quiet", dest="verbose", action="store_false", default=True, help="Quiet output.")
options,args = parser.parse_args()

if not options.output:
	options.output = options.input.replace(".root","/")

plotRange = options.range.split(",")
bins = options.bins.split(",")
parameters = options.parameters.split(",")



import os



def main():
	print( "Creating output directory." )
	os.system( "mkdir -p "+options.output )

	wsMcData = ' -w '+options.wsName+' -m '+options.mcName+' -d '+options.dataName


	# parameters for Likelihood scans
	params = wsMcData+' \
		--reorderParameters=1,0 --reversedParameters=0 \
		--printAllNuisanceParameters \
		-q  \
		-j 1 -c 0 \
		--minStrategy=2  \
		--minOptimizeConst=0  \
		--enableOffset \
		--evaluateWithoutOffset \
		--overwriteRange=muT=['+plotRange[0]+':'+plotRange[2]+'],muW=['+plotRange[1]+':'+plotRange[3]+'] \
		--overwriteBins=muT='+bins[0]+',muW='+bins[1]


	# effective Likelihood scan
	if not options.skip_eff:
		parametersZero = [ p+"=0.000000001" for p in parameters ]
		# --setConstant='+(','.join(parametersZero))+'
		r = os.system( 'batch_likelihood_scan \
			-i '+options.input+' \
			--plugins=BatchLikelihoodScan.Plugins.muTmuW,Decouple.BatchPlugins.mleCommonNPExceptMuProd \
			'+params+' \
			> '+options.output+'muTmuW_eff.log'
		)
		if r != 0: raise
		#plot eff
		r = os.system( 'batch_likelihood_plot \
			-i '+options.output+'muTmuW_eff.log \
			-o '+options.output+'muTmuW_eff.root \
			--subtractMinNLL \
			-q'
		)
		if r != 0: raise

		r = os.system( 'batch_likelihood_scan \
			-i '+options.input+' \
			--plugins=BatchLikelihoodScan.Plugins.muTmuW,Decouple.BatchPlugins.mleAllExceptMuProd \
			--setConstant='+(','.join(parametersZero))+' \
			'+params+' \
			> '+options.output+'muTmuW_statOnly.log'
		)
		if r != 0: raise
		#plot statOnly
		r = os.system( 'batch_likelihood_plot \
			-i '+options.output+'muTmuW_statOnly.log \
			-o '+options.output+'muTmuW_statOnly.root \
			--subtractMinNLL \
			-q'
		)
		if r != 0: raise


	# full model scan
	if not options.skip_fullScan:
		r = os.system( 'batch_likelihood_scan \
			-i '+options.input+' \
			--plugins=BatchLikelihoodScan.Plugins.muTmuW \
			'+params+' \
			> '+options.output+'muTmuW.log'
		)
		if r != 0: raise
		r = os.system( 'batch_likelihood_plot \
			-i '+options.output+'muTmuW.log \
			-o '+options.output+'muTmuW.root \
			--subtractMinNLL \
			-q'
		)
		if r != 0: raise


	# obtain etas
	if not options.skip_etas:
		r = os.system( 'decouple_obtain_etas -q -i '+options.input+' -o '+options.output+' '+wsMcData+' -p '+options.parameters )
		if r != 0: raise




if __name__ == "__main__":
	main()


