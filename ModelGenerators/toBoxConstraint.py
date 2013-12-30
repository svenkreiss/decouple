#!/usr/bin/env python

#  Created on: September 30, 2013

__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"

__description__ = """
Creates a counting model with box constraint (RFit) by replacing the constraint
term in the model. 
"""

import optparse
parser = optparse.OptionParser(version=__version__, description=__description__)
parser.add_option("-i", "--input", dest="input", default="invalid.root", help="Input root model.")
parser.add_option("-w", "--wsName", help="Workspace name", type="string", dest="wsName", default="combined")
parser.add_option("-m", "--mcName", help="ModelConfig name", type="string", dest="mcName", default="ModelConfig")
parser.add_option("-d", "--dataName", help="data name", type="string", dest="dataName", default="obsData")

parser.add_option("-b", "--boxVariables", dest="boxVariables", default="*QCDscale_Higgs_*,alpha_sys,alpha_sys_GGF", help="Specify a regular expression for the variables you want a box constraint for (expr as taken by RooArgSet::selectByName() ).")
parser.add_option(      "--wideGauss", dest="wideGauss", default=False, action="store_true")
parser.add_option(      "--centeredAtMLE", dest="centeredAtMLE", default=False, action="store_true")
parser.add_option("-o", "--output", dest="output", default=None, help="Output prefix.")

parser.add_option("-q", "--quiet", dest="verbose", action="store_false", default=True, help="Quiet output.")
options,args = parser.parse_args()

import ROOT
ROOT.gROOT.SetBatch( True )
from Decouple.src.fullModel_utils import *

container = []




def createConstraintFor( w, nuisName, boxHalfWidth=1, gaussSigma=10000.0, boxCenter=0.0 ):
	if options.verbose:
		print( "Creating box constraint term for: "+nuisName )

	nuisExpr = nuisName+'[0,'+str(boxCenter-boxHalfWidth)+','+str(boxCenter+boxHalfWidth)+']'
	globsExpr = 'nom_'+nuisName+'[0,-10,10]'
	constrName = nuisName+'Constraint'
	w.factory( 'RooGaussian::'+constrName+'('+globsExpr+','+nuisExpr+','+str(gaussSigma)+')' )


def argsetNames( argset ):
	l = ROOT.RooArgList( argset )
	names = []
	for i in range( l.getSize() ):
		names.append( l.at(i).GetName() )
	return names

def createWorkspace( inFile ):
	"""
	The strategy is to create a model with the new constraint terms and then do a
	roofit workspace import with RecycleConflictNodes.
	"""

	f = ROOT.TFile.Open( inFile, "READ" )
	w = f.Get( options.wsName )
	mc = w.obj( options.mcName )
	data = w.data( options.dataName )

	if options.centeredAtMLE:
		nll = getNll( mc.GetPdf(), data, minStrategy=2, enableOffset=False, globObs=mc.GetGlobalObservables() )
		minimize( nll )

	# new workspace
	newW = ROOT.RooWorkspace( "combined" )
	qcdscaleSignalNuis = ROOT.RooArgList( mc.GetNuisanceParameters().selectByName(options.boxVariables) )
	for i in range( qcdscaleSignalNuis.getSize() ):
		nuisParName = qcdscaleSignalNuis.at(i).GetName()
		boxCenter = 0.0
		if options.centeredAtMLE:
			boxCenter = w.var(nuisParName).getVal()
			print( 'For '+nuisParName+', using boxCenter='+str(boxCenter)+'.' )
		if options.wideGauss:
			createConstraintFor( newW, nuisParName, boxCenter=boxCenter, boxHalfWidth=20.0, gaussSigma=1.3 )
		else:
			createConstraintFor( newW, nuisParName, boxCenter=boxCenter )

	print( "------------- Workspace with constraint terms only -------------")
	newW.Print()
	print( "------------- End workspace printout ---------------------------")

	# import modelconfig from old workspace (propagates to everything else apart from data)
	getattr(newW,"import")( mc.GetPdf(), ROOT.RooFit.RecycleConflictNodes(), ROOT.RooFit.Silence() )

	newMC = ROOT.RooStats.ModelConfig("ModelConfig")
	newMC.SetWorkspace(newW)
	newMC.SetPdf( newW.pdf(mc.GetPdf().GetName()) )
	newMC.SetNuisanceParameters( ",".join( argsetNames(mc.GetNuisanceParameters()) ) )
	newMC.SetGlobalObservables( ",".join( argsetNames(mc.GetGlobalObservables()) ) )
	newMC.SetParametersOfInterest( ",".join( argsetNames(mc.GetParametersOfInterest()) ) )
	getattr(newW,"import")( newMC )

	# also add data
	getattr(newW,"import")( data )

	# print( "------------- Workspace with constraint terms only -------------")
	# newW.Print()
	# print( "------------- End workspace printout ---------------------------")

	newMC.Print()

	if options.wideGauss:
		outFile = inFile.replace(".root","_wideGauss.root")
	else:
		outFile = inFile.replace(".root","_box.root")
	print( "Writing output to "+outFile )
	newW.SaveAs( outFile )



if __name__ == "__main__":
	createWorkspace( options.input )




