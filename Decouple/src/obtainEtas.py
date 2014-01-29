#!/usr/bin/env python

#  Created on: October 7, 2013

__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"


import optparse
parser = optparse.OptionParser(version=__version__)
parser.add_option("-i", "--input", dest="input", default="invalid.root", help="Input root model.")
parser.add_option("-w", "--wsName", help="Workspace name", type="string", dest="wsName", default="combined")
parser.add_option("-m", "--mcName", help="ModelConfig name", type="string", dest="mcName", default="ModelConfig")
parser.add_option("-d", "--dataName", help="data name", type="string", dest="dataName", default="obsData")

parser.add_option("-p", "--parameters", help="parameters", type="string", dest="parameters", default="")

parser.add_option(      "--minStrategy", help="Minuit Strategies: 0 fastest, 1 intermediate, 2 slow", dest="minStrategy", default=2, type=int)
parser.add_option(      "--enableOffset", help="enable likelihood offsetting", dest="enableOffset", default=False, action="store_true")

parser.add_option("-o", "--output", dest="output", default="output/standard_", help="Output prefix.")

parser.add_option("-q", "--quiet", dest="verbose", action="store_false", default=True, help="Quiet output.")
options,args = parser.parse_args()

options.parameters = options.parameters.split(",")

import ROOT
if not options.verbose: ROOT.gROOT.SetBatch( True )

from multiprocessing import Pool
from pprint import pprint

import BatchLikelihoodScan.Plugins.muTmuW

from fullModel_utils import *
from scipy import optimize

import PyROOTUtils # just for debug
import numpy as np

import pickle
import math
import numpy








# cached numerical values
sqrt7 = math.sqrt(7)
pow713 = math.pow(7,1.0/3.0)
pow723 = math.pow(7,2.0/3.0)

def interpCode4EtaFromSlope(slope):
	"""
	Straight copy'n'paste out of mathematica:
	   a = (21 Slope + Sqrt[7] Sqrt[64 + 63 Slope^2])^(1/3)
	   eta = 2 (-(4/(7^(1/3) a)) + a/7^(2/3))

	"""

	a = math.pow( (21.0*slope + sqrt7*math.sqrt(64.0 + 63.0*slope*slope)), 1.0/3.0 )
	eta = 2.0*( -4.0/(pow713*a)  +  a/pow723 )
	return eta


def getInterpCodes(ws,params):
	"""
	Returns a dictionary of paramName=interpCode.
	Only really works when the interpCode for a parameter is the same
	in all flexibleInterpVars.
	"""

	interpCodes = {}
	parL = ROOT.RooArgList( params )
	funcs = ROOT.RooArgList( ws.allFunctions() )
	for i in range( funcs.getSize() ):
		o = funcs.at(i)
		if hasattr(o,"getInterpCode"):
			for j in range( parL.getSize() ):
				interpCodes[ parL.at(j).GetName() ] = o.getInterpCode( parL.at(j) )

	return interpCodes









def oneEta(nll, parameter, mu, allMu, eps=1.0):
	""" 
	This is the core function of this script.
	parameter ... RooRealVar of nuisance parameter.
	All input parameters are constant and set to their best fit values.
	"""

	initP = parameter.getVal()
	initMu = mu.getVal()

	mu.setConstant( False )

	# first term calculation
	parameter.setVal( initP-eps )
	minimize( nll )
	minMu = mu.getVal()
	parameter.setVal( initP+eps )
	minimize( nll )
	maxMu = mu.getVal()
	firstTerm = -1.0/initMu * (maxMu-minMu)/(2.0*eps)

	# second term calculation
	secondTerm = 0.0
	for i in range( allMu.getSize() ):
		otherMuVar = allMu.at(i)
		if otherMuVar.GetName() == mu.GetName(): continue

		print( "working on second term ("+otherMuVar.GetName()+")" )
		initOtherMu = otherMuVar.getVal()

		# otherMuVar.setVal( initOtherMu-eps )
		# parameter.setVal( initP-eps )
		# minimize( nll )
		# minMu = mu.getVal()
		# parameter.setVal( initP+eps )
		# minimize( nll )
		# maxMu = mu.getVal()
		# lowDiff = (maxMu-minMu)/(2.0*eps)
		# otherMuVar.setVal( initOtherMu+eps )
		# parameter.setVal( initP-eps )
		# minimize( nll )
		# minMu = mu.getVal()
		# parameter.setVal( initP+eps )
		# minimize( nll )
		# maxMu = mu.getVal()
		# highDiff = (maxMu-minMu)/(2.0*eps)

		# secondTerm += (highDiff-lowDiff)/(2.0*eps)  *  initOtherMu


		otherMuVar.setVal( initOtherMu-eps )
		parameter.setVal( initP-eps )
		minimize( nll )
		mmMu = mu.getVal()
		
		parameter.setVal( initP+eps )
		minimize( nll )
		mpMu = mu.getVal()

		otherMuVar.setVal( initOtherMu+eps )
		parameter.setVal( initP-eps )
		minimize( nll )
		pmMu = mu.getVal()

		parameter.setVal( initP+eps )
		minimize( nll )
		ppMu = mu.getVal()

		secondTerm += (ppMu+mmMu-pmMu-mpMu)/(4.0*eps*eps)  *  initOtherMu



		otherMuVar.setVal( initOtherMu )


	secondTerm /= -initMu

	print( "---> eta for "+parameter.GetName()+" "+mu.GetName()+": "+str(firstTerm)+" + "+str(secondTerm)+" = "+str(firstTerm+secondTerm) )
	return firstTerm + secondTerm

def oneEtaMuPPrimeZero(nll, parameter, mu, allMu, eps=0.3):
	""" 
	This is the core function of this script.
	parameter ... RooRealVar of nuisance parameter.
	All input parameters are constant and set to their best fit values.

	This is the method where eta is obtained from a partial derivative at mu_pPrime = 0.
	This choice is not good in principal as we want eta around \hat{mu}_{p'}, but
	it simplifies the math.
	"""

	initP = parameter.getVal()
	initMu = mu.getVal()

	mu.setConstant( False )

	for i in range( allMu.getSize() ):
		otherMuVar = allMu.at(i)
		if otherMuVar.GetName() == mu.GetName(): continue

		otherMuVar.setVal( 0.0 )

	# for i in range(10):
	# 	parameter.setVal( initP-eps + i/10.0*2*eps )
	# 	minimize( nll )
	# 	print( parameter.GetName()+" "+str(parameter.getVal())+" ----> mu "+str(mu.getVal()) )

	# get initMu along the line mu_p'=0
	minimize( nll )
	initMu = mu.getVal()

	# first term calculation
	parameter.setVal( initP-eps )
	minimize( nll )
	minMu = mu.getVal()
	parameter.setVal( initP+eps )
	minimize( nll )
	maxMu = mu.getVal()
	print( "initMu="+str(initMu)+" max="+str(maxMu)+" min="+str(minMu)+" 2eps="+str(2*eps))
	firstTerm = -1.0/initMu * (maxMu-minMu)/(2.0*eps)

	print( "---> eta for "+parameter.GetName()+" "+mu.GetName()+": "+str(firstTerm) )
	return firstTerm

def plotScan1D(nll,param, minRange=None, maxRange=None,points=100):
	scan = []

	if minRange == None: minRange = param.getMin()
	if maxRange == None: maxRange = param.getMax()

	paramOrigVal = param.getVal()
	for i in range(points):
		x = minRange + float(i)/points*(maxRange-minRange)
		param.setVal(x)
		val = nll.getVal()
		if val == val:
			scan.append( (x,val) )
	param.setVal( paramOrigVal )

	c = ROOT.TCanvas("c1","c1",800,600)
	g = PyROOTUtils.Graph( scan )
	g.Draw("L AXIS")
	c.SaveAs("output/debug_scan.eps")





def minScan1D(nll,param, minRange=None, maxRange=None, points=100, minMaxEnd = 1e-7):
	""" Recursing grid scan. """

	if minRange == None: minRange = param.getMin()
	if maxRange == None: maxRange = param.getMax()

	print( "Scanning in parameter "+param.GetName()+" ["+str(minRange)+","+str(maxRange)+"]." )
	scan = []
	paramOrigVal = param.getVal()
	for i in range(points):
		x = minRange + float(i)/points*(maxRange-minRange)
		param.setVal(x)
		val = nll.getVal()
		if val != val: val = 1e30
		scan.append( (i,x,val) )
	param.setVal( paramOrigVal )

	# get index of minimum point
	minI = min( [(v[2],v[0]) for v in scan] )[1]
	maxI = max( [(v[2],v[0]) for v in scan] )[1]

	if scan[maxI][2]-scan[minI][2] < minMaxEnd:
		print( "ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" )
		return None

	if max( scan[minI-1][2], scan[minI+1][2] )  -  scan[minI][2]   <   minMaxEnd:
		return scan[minI][1]
	else:
		return minScan1D(nll,param,minRange=scan[minI-1][1],maxRange=scan[minI+1][1],points=points,minMaxEnd=minMaxEnd)




def oneEtaMuPhiSubstitution(nll, parameter, mu, allMu, eps=0.01):
	""" 
	This is the core function of this script.
	parameter ... RooRealVar of nuisance parameter.
	All input parameters are constant and set to their best fit values.

	This employs a substitution of mu -> mu*phi where then it is possible
	to take the partial derivative wrt to phi to extract mu.
	"""

	initP = parameter.getVal()
	initMu = mu.getVal()

	mu.setConstant( False )

	phi = nll.getVariables().find( {"muT":"mu_XS8_ggF_phi","muW":"mu_XS8_VBF_phi"}[mu.GetName()] )
	initPhi = phi.getVal() # should be one
	print( "initPhi="+str(initPhi) )

	# phi.setVal( initPhi-eps )
	# parameter.setVal( initP-eps )
	# #minimize( nll )
	# #minMu = mu.getVal()
	# minMu = minScan1D( nll,mu )
	# parameter.setVal( initP+eps )
	# # minimize( nll )
	# # maxMu = mu.getVal()
	# maxMu = minScan1D( nll,mu )
	# lowDiff = (maxMu-minMu)/(2.0*eps)
	# phi.setVal( initPhi+eps )
	# parameter.setVal( initP-eps )
	# # minimize( nll )
	# # minMu = mu.getVal()
	# minMu = minScan1D( nll,mu )
	# parameter.setVal( initP+eps )
	# # minimize( nll )
	# # maxMu = mu.getVal()
	# maxMu = minScan1D( nll,mu )
	# highDiff = (maxMu-minMu)/(2.0*eps)

	# swapped order
	# parameter.setVal( initP-eps )
	# phi.setVal( initPhi-eps )
	# minimize( nll )
	# minMu = mu.getVal()
	# phi.setVal( initPhi+eps )
	# minimize( nll )
	# maxMu = mu.getVal()
	# lowDiff = (maxMu-minMu)/(2.0*eps)
	# parameter.setVal( initP+eps )
	# phi.setVal( initPhi-eps )
	# minimize( nll )
	# minMu = mu.getVal()
	# phi.setVal( initPhi+eps )
	# minimize( nll )
	# maxMu = mu.getVal()
	# highDiff = (maxMu-minMu)/(2.0*eps)

	#minimize( nll ) # to set optimize const mode
	plotScan1D( nll,mu,0.5,2,1000 )


	phi.setVal( initPhi-eps )
	parameter.setVal( initP-eps )
	minimize( nll )
	mmMu = mu.getVal()
	# mmMu = minScan1D( nll,mu )

	parameter.setVal( initP+eps )
	minimize( nll )
	mpMu = mu.getVal()
	# mpMu = minScan1D( nll,mu )
	
	phi.setVal( initPhi+eps )
	parameter.setVal( initP-eps )
	minimize( nll )
	pmMu = mu.getVal()
	# pmMu = minScan1D( nll,mu )

	parameter.setVal( initP+eps )
	minimize( nll )
	ppMu = mu.getVal()
	# ppMu = minScan1D( nll,mu )
	


	phi.setVal( initPhi )

	# print( "lowDiff="+str(lowDiff)+" highDiff="+str(highDiff) )
	# firstTerm = -1.0/initMu * (highDiff-lowDiff)/(2.0*eps)
	firstTerm = -1.0/initMu * (mmMu + ppMu - mpMu - pmMu)/(4.0*eps*eps)

	print( "---> eta for "+parameter.GetName()+" "+mu.GetName()+": "+str(firstTerm) )
	return firstTerm



def oneEtaSystemOfPDEs(nll, parameter, mu, allMu, eps=0.5):
	""" 
	This is the core function of this script.
	parameter ... RooRealVar of nuisance parameter.
	All input parameters are constant and set to their best fit values.
	"""

	initP = parameter.getVal()
	initMu = mu.getVal()

	# get some info about the nll first
	initNll = nll.getVal()
	parameter.setVal( initP-eps )
	print( "NLL change for changing "+parameter.GetName()+" by eps(="+str(eps)+"): "+str(initNll-nll.getVal()) )
	parameter.setVal( initP )

	mu.setConstant( False )

	for i in range( allMu.getSize() ):
		allMu.at(i).setConstant( False )
		# otherMuVar = allMu.at(i)
		# if otherMuVar.GetName() == mu.GetName(): continue

		# print( "working on second term ("+otherMuVar.GetName()+")" )
		# otherMuVar.setConstant( False )

	# first term calculation
	parameter.setVal( initP-eps )
	minimize( nll )
	minMu = mu.getVal()
	parameter.setVal( initP+eps )
	minimize( nll )
	maxMu = mu.getVal()
	firstTerm = -1.0/initMu * (maxMu-minMu)/(2*eps)

	#print( "---> eta for "+parameter.GetName()+" "+mu.GetName()+": "+str(firstTerm)+" + "+str(secondTerm)+" = "+str(firstTerm+secondTerm) )
	return firstTerm



# =================== Functions to extract etas from Hessian matrix of fit result ===================

def toNumpyMatrix(mIn,nx,ny):
	""" 
	mIn is for example a TMatrixDSym as for example a covariance matrix
	in a RooFitResult, but any object that has an accessor (row,column) defined
	works. 
	"""

	mOut = []
	for y in range(ny):
		row = []
		for x in range(nx):
			row.append( mIn(y,x) )
		mOut.append( row )
	return np.matrix(mOut)

def npCov( fitResult ):
	"""
	Returns a numpy array containing the full Hessian matrix and the variable
	names of the elements.
	"""
	pars = fitResult.floatParsFinal()
	varNames = [ pars.at(i).GetName() for i in range(pars.getSize()) ]

	cov = toNumpyMatrix(fitResult.covarianceMatrix(), nx=pars.getSize(), ny=pars.getSize())
	return (cov,varNames)

def npSigma12( fitResult, nuisFilter="alpha_" ):
	"""
	Returns the 12 block that is obtained for separating the matrix into blocks
	by filtering on the variable names.

	number of rows: n_{POI}
	number of columns: n_{nuisance parameters}
	"""
	cov,pars = npCov( fitResult )
	newPars = [[],[]]
	for i in reversed( range(len(pars)) ):
		if nuisFilter in pars[i]:
			cov = np.delete( cov, i, 0 )
			newPars[1].insert( 0,pars[i] )
		else:
			cov = np.delete( cov, i, 1 )
			newPars[0].insert( 0,pars[i] )

	return cov,newPars

def npI12( fitResult, nuisFilter="alpha_" ):
	"""
	Returns the 12 block that is obtained for separating the matrix into blocks
	by filtering on the variable names.

	number of rows: n_{POI}
	number of columns: n_{nuisance parameters}
	"""
	cov,pars = npCov( fitResult )
	I = cov.getI()
	newPars = [[],[]]
	for i in reversed( range(len(pars)) ):
		if nuisFilter in pars[i]:
			I = np.delete( I, i, 0 )
			newPars[1].insert( 0,pars[i] )
		else:
			I = np.delete( I, i, 1 )
			newPars[0].insert( 0,pars[i] )

	return I,newPars

def npSigma11( fitResult, nuisFilter="alpha_" ):
	"""
	Returns the block of the covariance matrix that corresponds to the main term.
	"""
	cov,pars = npCov( fitResult )
	newPars = list( pars )
	for i in reversed( range(len(pars)) ):
		if nuisFilter not in pars[i]: continue

		cov = np.delete( cov, i, 0 )
		cov = np.delete( cov, i, 1 )

		newPars.remove( pars[i] )
	return cov,newPars

def npSigma22( fitResult, nuisFilter="alpha_" ):
	"""
	Returns the block of the covariance matrix that corresponds to the constraint term.
	"""
	cov,pars = npCov( fitResult )
	newPars = list( pars )
	for i in reversed( range(len(pars)) ):
		if nuisFilter in pars[i]: continue

		cov = np.delete( cov, i, 0 )
		cov = np.delete( cov, i, 1 )

		newPars.remove( pars[i] )
	return cov,newPars

def npBestFit( fitResult, filter=None ):
	"""
	Returns a vector of best fit results for the parameters that match the filter and the
	corresponding list of parameter names.
	"""
	pars = fitResult.floatParsFinal()
	l = [ (pars.at(i).getVal(),pars.at(i).GetName()) for i in range( pars.getSize() ) if not filter or filter in pars.at(i).GetName() ]
	return ([v[0] for v in l], [v[1] for v in l])

def npBestFitDiag( fitResult, filter=None ):
	"""
	Returns a vector of best fit results for the parameters that match the filter and the
	corresponding list of parameter names.
	"""
	pars = fitResult.floatParsFinal()
	l = [ (pars.at(i).getVal(),pars.at(i).GetName()) for i in range( pars.getSize() ) if not filter or filter in pars.at(i).GetName() ]
	return (np.matrix(np.diag([v[0] for v in l])), [v[1] for v in l])

def etasFromCovariance(nll, poiL, nuisL, w):
	""" 
	This is the core function of this script.
	parameter ... RooRealVar of nuisance parameter.
	All input parameters are constant and set to their best fit values.
	"""

	for i in range( poiL.getSize() ):
		poiL.at(i).setConstant( False )

	# get Hessian matrix for effective model (\alpha = \hat{\alpha})
	fr = minimize_fitResult( nll )
	print( "" )
	print( "" )
	print( "----- Covariance matrix and Hessian for effective model: -----" )
	covEff,pars = npCov(fr)
	print( pars )
	print( covEff )
	print( covEff.getI() )
	print( "" )
	print( "" )

	# get Hessian matrix for full model
	print( "Setting variables to floating for full model:")
	for i in range( nuisL.getSize() ): 
		print( "  - "+nuisL.at(i).GetName()  )
		nuisL.at(i).setConstant( False )
	fr = minimize_fitResult( nll )
	print( "" )
	print( "" )
	print( "----- Covariance matrix and Hessian for full model: -----" )
	cov,pars = npCov(fr)
	print( pars )
	print( cov )
	print( cov.getI() )
	s12,parsPOIAndNuis = npSigma12(fr)    # parameters defined here determine shape/ordering of final answer
	s22Inv = npSigma22(fr)[0].getI()
	print( parsPOIAndNuis )
	print( s12*s22Inv )
	print( "hatsInv:" )
	hats,pars = npBestFitDiag(fr, filter="mu")
	print( pars )
	print( hats.getI() )
	print( "========================== Etas from Sigma_c Sigma_alpha^-1 (method 2) =======================" )
	etasMatrix = -1.0*hats.getI() * s12*s22Inv  # TODO: is this correct?
	print( etasMatrix )
	print( "" )
	print( "" )
	# divide rows by corresponding mus
	# etas = []
	# for r,muhat in zip((covEff*I12).tolist(),hatsVec):
	# 	etas.append( [v/muhat for v in r] )
	# print( etas  )
	# print( "" )
	# print( "" )


	# interpcodes
	interpCodes = getInterpCodes( w, nuisL )

	# create return dictionary
	etas = {}
	for ni in range( len(parsPOIAndNuis[1]) ):  # ni = nuisance parameter index
		for pi in range( len(parsPOIAndNuis[0]) ):  # pi = POI index
			if parsPOIAndNuis[1][ni] not in etas: etas[ parsPOIAndNuis[1][ni] ] = {}

			interpCode = 0
			if parsPOIAndNuis[1][ni] in interpCodes: interpCode = interpCodes[ parsPOIAndNuis[1][ni] ]

			if interpCode == 4:
				etas[ parsPOIAndNuis[1][ni] ][ parsPOIAndNuis[0][pi] ] = interpCode4EtaFromSlope( etasMatrix[pi,ni] )
			else:
				print(etasMatrix)
				print(etas)
				etas[ parsPOIAndNuis[1][ni] ][ parsPOIAndNuis[0][pi] ] = etasMatrix[pi,ni]

	return etas



def etasFromFisherInfo(nll, poiL, nuisL, w):
	""" 
	This is the core function of this script.
	parameter ... RooRealVar of nuisance parameter.
	All input parameters are constant and set to their best fit values.
	"""

	for i in range( poiL.getSize() ):
		poiL.at(i).setConstant( False )

	# get Hessian matrix for effective model (\alpha = \hat{\alpha})
	fr = minimize_fitResult( nll )
	print( "" )
	print( "" )
	print( "----- Covariance matrix and Hessian for effective model: -----" )
	covEff,pars = npCov(fr)
	print( pars )
	print( covEff )
	print( covEff.getI() )
	print( "" )
	print( "" )

	# get Hessian matrix for full model
	print( "Setting variables to floating for full model:")
	for i in range( nuisL.getSize() ): 
		print( "  - "+nuisL.at(i).GetName()  )
		nuisL.at(i).setConstant( False )
	fr = minimize_fitResult( nll )
	print( "" )
	print( "" )
	print( "----- Covariance matrix and Hessian for full model: -----" )
	cov,pars = npCov(fr)
	print( pars )
	print( cov )
	print( cov.getI() )
	s12,parsPOIAndNuis = npSigma12(fr)    # parameters defined here determine shape/ordering of final answer
	s22Inv = npSigma22(fr)[0].getI()
	print( parsPOIAndNuis )
	print( s12*s22Inv )
	print( "hatsInv:" )
	hats,pars = npBestFitDiag(fr, filter="mu")
	print( pars )
	print( hats.getI() )
	print( "========================== Etas from I_eff inversion (method 1) =======================" )
	I12,pars = npI12(fr)
	hatsVec,pars = npBestFit(fr, filter="mu")
	# divide rows by corresponding mus
	etasMatrix = []
	for r,muhat in zip((covEff*I12).tolist(),hatsVec):
		etasMatrix.append( [v/muhat for v in r] )
	print( etasMatrix )
	print( "" )
	print( "" )


	# interpcodes
	interpCodes = getInterpCodes( w, nuisL )

	# create return dictionary
	etas = {}
	for ni in range( len(parsPOIAndNuis[1]) ):  # ni = nuisance parameter index
		for pi in range( len(parsPOIAndNuis[0]) ):  # pi = POI index
			if parsPOIAndNuis[1][ni] not in etas: etas[ parsPOIAndNuis[1][ni] ] = {}

			interpCode = 0
			if parsPOIAndNuis[1][ni] in interpCodes: interpCode = interpCodes[ parsPOIAndNuis[1][ni] ]

			if interpCode == 4:
				etas[ parsPOIAndNuis[1][ni] ][ parsPOIAndNuis[0][pi] ] = interpCode4EtaFromSlope( etasMatrix[pi][ni] )
			else:
				etas[ parsPOIAndNuis[1][ni] ][ parsPOIAndNuis[0][pi] ] = etasMatrix[pi][ni]

	return etas


def etasGenericFromFisherInfo(nll, poiL, nuisL, w):
	""" 
	This is the core function of this script.
	parameter ... RooRealVar of nuisance parameter.
	All input parameters are constant and set to their best fit values.
	"""

	for i in range( poiL.getSize() ):
		poiL.at(i).setConstant( False )

	# get Hessian matrix for effective model (\alpha = \hat{\alpha})
	fr = minimize_fitResult( nll )
	print( "" )
	print( "" )
	print( "----- Covariance matrix and Hessian for effective model: -----" )
	covEff,pars = npCov(fr)
	print( pars )
	print( covEff )
	print( covEff.getI() )
	print( "" )
	print( "" )

	# get Hessian matrix for full model
	print( "Setting variables to floating for full model:")
	for i in range( nuisL.getSize() ): 
		print( "  - "+nuisL.at(i).GetName()  )
		nuisL.at(i).setConstant( False )
	fr = minimize_fitResult( nll )
	print( "" )
	print( "" )
	print( "----- Covariance matrix and Hessian for full model: -----" )
	cov,pars = npCov(fr)
	print( pars )
	print( cov )
	print( cov.getI() )
	s12,parsPOIAndNuis = npSigma12(fr)    # parameters defined here determine shape/ordering of final answer
	s22Inv = npSigma22(fr)[0].getI()
	print( parsPOIAndNuis )
	print( s12*s22Inv )
	print( "hatsInv:" )
	hats,pars = npBestFitDiag(fr, filter="mu")
	print( pars )
	print( hats.getI() )
	print( "========================== Generic Etas from I_eff inversion (method 1) =======================" )
	I12,pars = npI12(fr)
	hatsVec,pars = npBestFit(fr, filter="mu")
	# divide rows by corresponding mus
	etasMatrix = []
	for r,muhat in zip((covEff*I12).tolist(),hatsVec):
		etasMatrix.append( [v/muhat for v in r] )
	print( etasMatrix )
	print( "" )
	print( "" )

	# interpcodes
	interpCodes = getInterpCodes( w, nuisL )

	# create return dictionary
	etas = {}
	for ni in range( len(parsPOIAndNuis[1]) ):  # ni = nuisance parameter index
		for pi1 in range( len(parsPOIAndNuis[0]) ):  # pi = POI index
			for pi2 in range( len(parsPOIAndNuis[0]) ):  # pi = POI index
				if parsPOIAndNuis[1][ni] not in etas: etas[ parsPOIAndNuis[1][ni] ] = {}
				
				# fill diagonal term as usual and off-diagonal with zero
				if pi1 == pi2: 
					interpCode = 0
					if parsPOIAndNuis[1][ni] in interpCodes: interpCode = interpCodes[ parsPOIAndNuis[1][ni] ]

					if interpCode == 4: val = interpCode4EtaFromSlope( etasMatrix[pi1][ni] )
					else:               val = etasMatrix[pi1][ni]
				else:
					val = 0.0

				etas[ parsPOIAndNuis[1][ni] ][ parsPOIAndNuis[0][pi1]+'__'+parsPOIAndNuis[0][pi2] ] = val
			# fill phi with zero
			etas[ parsPOIAndNuis[1][ni] ][ parsPOIAndNuis[0][pi1]+'__phi' ] = 0.0
	return etas


def etasGenericM4(nll, poiL, nuisL, w):
	etas = etasGenericFromFisherInfo(nll,poiL,nuisL,w)

	for i in range( nuisL.getSize() ):
		etasMuPZero = {}
		for mu in ["muT","muW"]:
			muVar = w.var(mu)
			w.loadSnapshot("ucmlesPOI")
			w.loadSnapshot("ucmlesNuis")
			etasMuPZero[mu] = oneEtaMuPPrimeZero( nll, nuisL.at(i), muVar, poiL )

		etasFisher = etas[nuisL.at(i).GetName()]
		length2 = etasFisher['muT__muT']*etasFisher['muT__muT'] + etasFisher['muW__muW']*etasFisher['muW__muW']
		angle = math.atan2(etasFisher['muT__muT'],etasFisher['muW__muW'])
		length2MuPZero = etasMuPZero['muT']*etasMuPZero['muT'] + etasMuPZero['muW']*etasMuPZero['muW']
		angleMuPZero = math.atan2(etasMuPZero['muT'],etasMuPZero['muW'])

		if abs( math.sqrt(length2MuPZero/length2) - 1.0 )  > 0.50  or  \
		   abs( angle - angleMuPZero ) > 3.141/4:
			# do interpcode -1
			etas[nuisL.at(i).GetName()]['muT__phi'] = etas[nuisL.at(i).GetName()]['muT__muT']
			etas[nuisL.at(i).GetName()]['muT__muT'] = 0
			etas[nuisL.at(i).GetName()]['muW__phi'] = etas[nuisL.at(i).GetName()]['muW__muW']
			etas[nuisL.at(i).GetName()]['muW__muW'] = 0

	return etas

def etasGenericM5(nll, poiL, nuisL, w):
	etas = etasGenericFromFisherInfo(nll,poiL,nuisL,w)

	# need muhats for swap
	fr = minimize_fitResult( nll )
	hatsVec,pars = npBestFit(fr, filter="mu")
	# convert to dict of form {'muT':1.0, 'muW':1.0}
	muhats = dict( zip(pars,hatsVec) )

	for i in range( nuisL.getSize() ):
		etasMuPZero = {}
		for mu in ["muT","muW"]:
			muVar = w.var(mu)
			w.loadSnapshot("ucmlesPOI")
			w.loadSnapshot("ucmlesNuis")
			etasMuPZero[mu] = oneEtaMuPPrimeZero( nll, nuisL.at(i), muVar, poiL )

		etasFisher = etas[nuisL.at(i).GetName()]
		length2 = etasFisher['muT__muT']*etasFisher['muT__muT'] + etasFisher['muW__muW']*etasFisher['muW__muW']
		angle = math.atan2(etasFisher['muT__muT'],etasFisher['muW__muW'])
		length2MuPZero = etasMuPZero['muT']*etasMuPZero['muT'] + etasMuPZero['muW']*etasMuPZero['muW']
		angleMuPZero = math.atan2(etasMuPZero['muT'],etasMuPZero['muW'])

		if abs( math.sqrt(length2MuPZero/length2) - 1.0 )  > 0.50  or  \
		   abs( angle - angleMuPZero ) > 3.141/4:
			# flip the axis it scales with: second entry is the axis it scales with
			etas[nuisL.at(i).GetName()]['muT__muW'] = muhats['muT']/muhats['muW'] * etas[nuisL.at(i).GetName()]['muT__muT']
			etas[nuisL.at(i).GetName()]['muT__muT'] = 0
			etas[nuisL.at(i).GetName()]['muW__muT'] = muhats['muW']/muhats['muT'] * etas[nuisL.at(i).GetName()]['muW__muW']
			etas[nuisL.at(i).GetName()]['muW__muW'] = 0

	return etas



# map function for muTmuW for loss function
def unit( x,y ):
	return (x,y)

def etasDictToArray( etasDict ):
	etasArray = []
	for np in etasDict.values():
		for pn,pp in np.iteritems():
			# if pn in ['muW__phi','muT__phi','muW__phi__down','muT__phi__down','muW__phi__up','muT__phi__up']: continue
			if 'muW__phi' in pn: continue
			etasArray.append( pp )
	return etasArray

def etasArrayFillsDict( etasArray, etasDict ):
	eACopy = [ a for a in etasArray ]
	for np in etasDict.values():
		for pp in np.keys():
			# if pp in ['muW__phi','muT__phi','muW__phi__down','muT__phi__down','muW__phi__up','muT__phi__up']: continue
			if 'muW__phi' in pp: continue
			np[ pp ] = eACopy.pop(0)
			if 'muT__phi' in pp:
				np[ pp.replace('muT','muW') ] = np[ pp ]

def etasDictToNPArray( etasDict ):
	etasArray = [] # 2x3 matrix: rows: mu_eff, columns: mu, phi
	for np in etasDict.values():
		etasArray.append([
			[np['muT__muT'],np['muT__muW'],np['muT__phi']], 
			[np['muW__muT'],np['muW__muW'],np['muW__phi']],
		])
	return numpy.array(etasArray)

def etasNPArrayFillsDict( etasArray, etasDict ):
	for npDict,npArray in zip(etasDict.values(),etasArray):
		npDict['muT__muT'] = npArray[0][0]
		npDict['muT__muW'] = npArray[0][1]
		npDict['muT__phi'] = npArray[0][2]
		npDict['muW__muT'] = npArray[1][0]
		npDict['muW__muW'] = npArray[1][1]
		npDict['muW__phi'] = npArray[1][2]


import effectiveModel
import math
container = []
c3 = None
hD = None
hD2 = None
debugCounter = -1
def loss( MCMCPoints, MCMCPointsMinNll, effHist2Nll, etasDict, etasArrayAndOffset, MCMCNllName="nll", offset=None, muHat=None, template=20, verbose=False ):
	global c3, hD, hD2, container, debugCounter
	debugCounter += 1

	if offset == None:
		offset = etasArrayAndOffset[-1]
		etasArray = etasArrayAndOffset[:-1]
	else:
		etasArray = etasArrayAndOffset
	etasArrayFillsDict( etasArray, etasDict )

	if debugCounter % 100 == 0:
		print( etasDict )
		print( "offset: "+str(offset) )
	m = effectiveModel.EffectiveParametrization( [ [effHist2Nll,etasDict,unit] ] )
	m.muHat = muHat
	m.template = template
	m.profile = False

	loss = 0
	sumWeights = 0
	points = MCMCPoints.numEntries()
	step = 1
	# if points > 2000:
	# 	points = 2000
	# 	step = int(points/2000)

	if not c3: 
		c3 = ROOT.TCanvas("debug","debug",1000,600)
		c3.Divide(2)
		c3.cd(1).SetRightMargin(0.16)
		c3.cd(2).SetRightMargin(0.16)
	if not hD or not hD2:
		hD = ROOT.TH2F( "loss1_debug", "loss;muT;muW", 30, 0.0, 3.5,  30, 0.0,5.5 )
		hD2 = ROOT.TH2F( "loss2_debug", "loss;muT;muW", 30, 0.0, 3.5,  30, 0.0,5.5 )
		container.append(hD)
		container.append(hD2)
	else:
		#clean
		hD.Scale(1e-12)
		hD2.Scale(1e-12)
	if debugCounter % 100 == 0:
		hD.GetZaxis().SetRangeUser( 0.0,1.0 )
		hD2.GetZaxis().SetRangeUser( 0.0,1.0 )

	# setup parameters in eff model
	m.setParametersFromRooArgSet(MCMCPoints.get(0), xName='muT', yName='muW', filter=[MCMCNllName])

	debugInfo = []
	compensation = 0.0  # see Kahan sum
	for i in range( points ):
		e = MCMCPoints.get(i*step)
		w = MCMCPoints.weight()
		fullNll = e.getRealValue( MCMCNllName ) - MCMCPointsMinNll
		if fullNll > 3.0: continue

		# if e.getRealValue('muT') < 0.2  or  e.getRealValue('muW') < 0.2: continue
		# if e.getRealValue('muT') > 2.5  or  e.getRealValue('muW') > 3.5: continue
		# if e.getRealValue('alpha_QCDscale_Higgs_ggH2in') > 0.8  or  e.getRealValue('alpha_QCDscale_Higgs_ggH2in') < -0.8: continue
		# eL = ROOT.RooArgList(e)
		# npOutsideRange = False
		# for i in range( eL.getSize() ):
		# 	if eL.at(i).GetName() in [MCMCNllName,'muT','muW']: continue
		# 	if eL.at(i).getVal() > 0.3  or  eL.at(i).getVal() < -0.3:
		# 		npOutsideRange = True
		# 		break
		# if npOutsideRange: continue

		#m.setParametersFromRooArgSet(e, xName='muT', yName='muW', filter=[MCMCNllName])
		m.setParametersFromRooArgSetFast(e, xName='muT', yName='muW')
		# if m.pois[0] > effHist2Nll.GetXaxis().GetXmax()  or  m.pois[0] < effHist2Nll.GetXaxis().GetXmin()  or  \
		#    m.pois[1] > effHist2Nll.GetYaxis().GetXmax()  or  m.pois[1] < effHist2Nll.GetYaxis().GetXmin():
		#    	# print("------------------------------------ skipping")
		#    	continue
		effNll = m.evalTwoNll() / 2.0

		sumWeights += w
		t = math.exp(-fullNll)-math.exp(-effNll + offset)
		# t = fullNll - effNll + offset
		# loss += w*abs( t )   # L1 loss
		thisLoss = w * 0.5*t*t  -  compensation  # quadratic loss
		newLoss = loss + thisLoss
		compensation = (newLoss - loss) - thisLoss # for next time
		loss = newLoss

		if debugCounter % 100 == 0:
			drawPoint = 1
			# for i in range( eL.getSize() ):
			# 	if eL.at(i).GetName() in [MCMCNllName,'muT','muW']: continue		
			# 	if eL.at(i).getVal() > 0.8  or  eL.at(i).getVal() < -0.8: drawPoint = -1
			# hD.SetBinContent( hD.FindBin(e.getRealValue('muT'), e.getRealValue('muW')), 0.5*t*t*drawPoint )
			b = hD.FindBin( e.getRealValue('muT'), e.getRealValue('muW') )
			if math.exp(-fullNll) > hD.GetBinContent(b): hD.SetBinContent( b, math.exp(-fullNll) )
			if math.exp(-effNll+offset) > hD2.GetBinContent(b): hD2.SetBinContent( b, math.exp(-effNll+offset) )
			# hD2.SetBinContent( hD.FindBin( e.getRealValue('alpha_sys'), e.getRealValue('muW') ), 0.5*t*t*drawPoint )
			if verbose:
				# print( math.exp(-effNll) )
				# print( math.exp(-fullNll + offset) )
				print( str(fullNll)+" \t--- "+str(effNll) )
				e.Print("V")
				# print( t )
				# debugInfo.append([
				# 	w*0.5*t*t,fullNll,effNll,offset,t,
				# 	e.getRealValue('alpha_QCDscale_Higgs_ggH'),
				# 	e.getRealValue('alpha_QCDscale_Higgs_ggH2in'),
				# 	e.getRealValue('alpha_ATLAS_LUMI_2012'),
				# ])

	if verbose:
		debugInfo = sorted( debugInfo )[-30:]
		pprint( debugInfo )

	if debugCounter % 100 == 0:
		c3.cd(1)
		hD.Draw("COLZ")
		c3.cd(2)
		hD2.Draw("COLZ")
		c3.Update()
		# if verbose: c3.SaveAs("test.eps")

		print(loss)

	loss /= sumWeights
	return loss


def lossFast( MCMCPoints, MCMCPointsMinNll, effHist2Nll, etasDict, etasAndPhi, MCMCNllName="nll", offset=None, muHat=None, template=20, verbose=False,etasShape=None ):

	etasArrayFillsDict( etasAndPhi, etasDict )
	m = effectiveModel.EffectiveParametrization( [ [effHist2Nll,etasDict,unit] ] )
	m.muHat = muHat
	m.template = template
	m.profile = False

	loss = 0
	sumWeights = 0

	# setup parameters in eff model
	m.setParametersFromRooArgSet(MCMCPoints.get(0), xName='muT', yName='muW', filter=[MCMCNllName])

	npArray = m.nuisanceParameters.values() # TODO !!!!!

	debugInfo = []
	compensation = 0.0  # see Kahan sum
	for i in range( MCMCPoints.numEntries() ):
		e = MCMCPoints.get(i)
		w = MCMCPoints.weight()
		fullNll = e.getRealValue( MCMCNllName ) - MCMCPointsMinNll

		m.setParametersFromRooArgSetFast(e, xName='muT', yName='muW')

		effNll = m.evalTwoNllFast(etasAndPhi.reshape(etasShape), npArray) / 2.0

		if fullNll > 5.0: continue

		sumWeights += w
		t = math.exp(-fullNll)-math.exp(-effNll + offset)
		# t = fullNll - effNll + offset
		# loss += w*abs( t )   # L1 loss
		thisLoss = w * 0.5*t*t  -  compensation  # quadratic loss
		newLoss = loss + thisLoss
		compensation = (newLoss - loss) - thisLoss # for next time
		loss = newLoss

	loss /= sumWeights
	return loss



def etasGenericLearning(nll, poiL, nuisL, nuisLAll, w, effHist2Nll, template=20):

	# init etas from fisher info
	etas = etasGenericM5(nll,poiL,nuisL,w)
	# etas = etasGenericFromFisherInfo(nll,poiL,nuisL,w)
	# etas['constant'] = dict([(k,0.0) for k in etas.values()[0].keys() if "__phi" not in k])

	# extend the set of etas for asymmetric responses
	if template >= 20 and template <= 29:
		etasAsym = {}
		for par,prods in etas.iteritems():
			etasAsym[par] = {}
			for prod,eta in prods.iteritems():
				etasAsym[par][prod+'__up'] = eta
				etasAsym[par][prod+'__down'] = eta
		etas = etasAsym

	# normal etas
	etasArray = etasDictToArray( etas )
	print("                array eta: \n"+str(etasArray[0]))
	print("                array phi: \n"+str(etasArray[1]))
	etasArrayFillsDict( etasArray, etas )
	etasArray = etasDictToArray( etas )
	print("after test dict cycle: "+str(etasArray))

	# np etas
	# etasNpArray = etasDictToNPArray( etas )
	# print("                array eta: \n"+str(etasNpArray))
	# etasNPArrayFillsDict( etasNpArray, etas )
	# etasNpArray = etasDictToNPArray( etas )
	# print("after test dict cycle: "+str(etasNpArray))


	# ------ create conditional MLEs --------
	w.loadSnapshot("ucmlesPOINonConst")
	w.loadSnapshot("ucmlesNuisNonConst")
	for i in range( nuisLAll.getSize() ): 
		if nuisLAll.at(i).GetName() in options.parameters: 
			nuisLAll.at(i).setConstant(True)
			nuisLAll.at(i).setVal(1e-9)
	print("------------------ NSUIANCE PARAMETERS")
	nuisLAll.Print("v")
	poiL.Print("v")
	minimize( nll )
	minNll = nll.getVal()
	print( "nll = "+str(nll.getVal()) )
	for i in range( nuisLAll.getSize() ): 
		if nuisLAll.at(i).GetName() in options.parameters: 
			nuisLAll.at(i).setConstant(False)
		else:
			nuisLAll.at(i).setConstant(True)
	muHat = { 'muT': w.var('muT').getVal(), 'muW': w.var('muW').getVal() }
	print( "---- muHat (conditional with alpha_th=0) ----" )
	print( muHat )
	print()

	print("------------------ NSUIANCE PARAMETERS")
	nuisLAll.Print("v")
	poiL.Print("v")

	mc = w.obj( options.mcName )
	data = w.data( options.dataName )

	# We want to create an overview using the following proposal functions
	proposalFunction = { 
		"proposal": ROOT.RooStats.SequentialProposal(10), 
		"id"      : "SequentialProposal",
		"title"   : "Standard configuration"
	}
	# if options.fullRun:
	#    proposalFunctions += [
	#       { "proposal": ROOT.RooStats.SequentialProposal(100), 
	#         "id"      : "SequentialProposal_100",
	#         "title"   : "Divisor = 100" },
	#       { "proposal": ROOT.RooStats.SequentialProposal(10, mc.GetParametersOfInterest(), 3), 
	#         "id"      : "SequentialProposal_10_03",
	#         "title"   : "Divisor = 10, Importance factor of POI = 3" },
	#       { "proposal": ROOT.RooStats.SequentialProposal(10, mc.GetParametersOfInterest(), 10), 
	#         "id"      : "SequentialProposal_10_10",
	#         "title"   : "Divisor = 10, Importance factor of POI = 10" },
	#    ]

	# all poi and the nuis pars that will be part of the profiling
	# on top of the effective Likelihood are part of chain (ie need to set them floating)
	#
	# Keeping the other parameters fixed is an approximation.
	for i in range( poiL.getSize() ): poiL.at(i).setConstant(False)
	for i in range( nuisL.getSize() ): 
		if nuisL.at(i).GetName() in options.parameters: 
			nuisL.at(i).setConstant(False)
		else:
			del etas[nuisL.at(i).GetName()]

	# reset all etas to zero
	# for np in etas.values():
	# 	for pp in np.keys():
	# 		np[ pp ] = 0.0

	# etas['alpha_sys']['muT__muT'] = 0.30
	# etas['alpha_sys']['muT__muW'] = 0.10
	# etas['alpha_sys']['muW__muW'] = 0.30
	# etas['alpha_sys']['muW__muT'] = 0.10
	# etas['alpha_sys']['muT__phi'] = 0.06


	# w.saveSnapshot("nuisMCMCSafe",ROOT.RooArgSet(nuisL))
	# for param in options.parameters:
	# 	w.loadSnapshot("nuisMCMCSafe")
	# 	for i in options.parameters:
	# 		if i == param: w.var(i).setConstant(False)
	# 		else:          w.var(i).setConstant()

	# set reasonable ranges for params to get nice proposal function
	# w.var('muT').setRange(0,4)
	# w.var('muW').setRange(0,4)

	# w.var(param).setConstant()
	# w.var(param).setVal(1.0)

	# run MCMC
	mcmc = ROOT.RooStats.MCMCCalculator(data,mc)
	mcmc.SetConfidenceLevel(0.95) # 95% interval
	mcmc.SetNumIters(120000)          # Metropolis-Hastings algorithm iterations
	mcmc.SetLeftSideTailFraction(0);  # for one-sided Bayesian interval
	mcmc.SetProposalFunction( proposalFunction["proposal"] )
	interval = mcmc.GetInterval()
	interval.SetNumBurnInForNumEntries( 100000 )

	# debug plot
	c1 = ROOT.TCanvas("Walk", "Walk", 800, 600)
	plot = ROOT.RooStats.MCMCIntervalPlot(interval)
	tg = plot.GetChainScatterWalk( poiL.at(0), poiL.at(1) )
	tg.Draw("AL")
	c1.SaveAs( options.output+"Learning_MCMCWalk.png" )
	c1.SetRightMargin( 0.16 )
	h = plot.GetHist2D( poiL.at(0), poiL.at(1) )
	h.Scale( 1.0/h.Integral("width") )
	h.GetZaxis().SetTitle( "posterior distribution" )
	h.Draw("COLZ")
	c1.SaveAs( options.output+"Learning_Posterior.png" )

	chain_all = interval.GetChain().GetAsConstDataSet()



	# create MCMC chain by using MetropolisHastings directly
	mh = ROOT.RooStats.MetropolisHastings()
	mh.SetFunction(nll)
	mh.SetType(ROOT.RooStats.MetropolisHastings.kLog)
	mh.SetSign(ROOT.RooStats.MetropolisHastings.kNegative)
	params = ROOT.RooArgSet( nuisL )
	params.add(poiL)
	ROOT.RooStats.RemoveConstantParameters(params)
	print( "=================== PARAMS for METRPOPOLISHASTING")
	params.Print("v")
	mh.SetParameters(params)
	mh.SetProposalFunction( proposalFunction["proposal"] )
	mh.SetNumIters(105000)
	chain_all = mh.ConstructChain().GetAsConstDataSet()



	# determine minNll of chain
	nllVar = interval.GetNLLVar()
	# minNll = 1e12
	# for i in range( chain_all.numEntries() ):
	# 	nllV = chain_all.get(i).getRealValue( nllVar.GetName() )
	# 	if nllV < minNll: minNll = nllV

		# for i in range( nuisL.getSize() ):
		# 	nuisL.at(i).setVal( chain_all.get(i).getRealValue(nuisL.at(i).GetName()) )
		# 	print("set")
		# for i in range( poiL.getSize() ):
		# 	poiL.at(i).setVal( chain_all.get(i).getRealValue(poiL.at(i).GetName()) )
		# 	print("setP")
		# print( "nll")
		# print( nll.getVal() )
		# print( "chain" )
		# print( nllV )
	# cut away burn-in
	chain = chain_all.emptyClone("main_chain")
	steps = 0
	for i in range( chain_all.numEntries() ):
		entry = chain_all.get(i)
		weight = chain_all.weight()
		steps += weight
		if steps < 100000: continue
		chain.add( entry,weight )

	print( "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" )
	print( chain.numEntries() )


	# # ------ etas
	# allEtas = dict([(p,v) for p,v in etas.iteritems()])
	# etas = {param: allEtas[param]}
	# print( "Etas before learning" )
	# print( etas )

	print( "First entry of mcmc chain" )
	nllVar.Print()
	chain.get(0).Print("v")

	# minimizer boundaries
	bounds = [ (-0.30,0.30) for e in etasArray ]
	# bounds = [ (None,None) for e in etasArray ]

	# offset = [0.0]
	# print( "Optimizing offset" )
	# r = optimize.minimize( lambda v: loss(chain,minNll,effHist2Nll,etas,etasArray,nllVar.GetName(),offset=v,        muHat=muHat,template=template),             offset,           method="L-BFGS-B", bounds=[(-5.0,5.0)] )
	# print( r.x )
	# offset = list(r.x) # want to append this list and not add element-wise, so need to convert from ndarray to list
	# print( "Optimized offset" )
	# loss(                                 chain,minNll,effHist2Nll,etas,etasArray,nllVar.GetName(),offset=offset[0],muHat=muHat,template=template,verbose=True)
	# # raw_input("offset optimized")
	# optimize.minimize( lambda v: loss(    chain,minNll,effHist2Nll,etas,v,        nllVar.GetName(),                 muHat=muHat,template=template),             etasArray+offset, method="L-BFGS-B", bounds=bounds+[(-5.0,5.0)] )
	# loss(chain,minNll,effHist2Nll,etas,etasArray,nllVar.GetName(),offset=0.0,verbose=True)
	# raw_input("offset optimized")
	optimize.minimize( lambda v:       loss(chain,minNll,effHist2Nll,etas,v,nllVar.GetName(),offset=0.0,              muHat=muHat,template=template),             etasArray,        method="L-BFGS-B", bounds=bounds )
	
	# build etas np array
	# etasNpArrayShape = etasNpArray.shape
	# etasNpArray = etasNpArray.reshape( -1 )
	# print( "" )
	# print( etasNpArrayShape )
	# print( etasNpArray )
	# optimize.minimize( lambda v:       lossFast(chain,minNll,effHist2Nll,etas,v,nllVar.GetName(),offset=0.0,              muHat=muHat,template=template,etasShape=etasNpArrayShape),             etasNpArray,        method="L-BFGS-B" )

	# # ----- reassign etas
	# allEtas[ etas.keys()[0] ] = etas.values()[0]
	# etas = allEtas


	w.loadSnapshot("ucmlesPOI")
	w.loadSnapshot("ucmlesNuis")
	muHat = { 'muT': w.var('muT').getVal(), 'muW': w.var('muW').getVal() }
	print( "---- muHat ----" )
	print( muHat )
	print()

	for p in etas.values():
		p['muT__hat'] = muHat['muT']
		p['muW__hat'] = muHat['muW']

	print( "Etas after learning")
	print( etas )

	return etas







class FullModelScan:
	hist_twoNll = None
	hist_nuisanceParameters = {}
	bestFit = None
	bestFit_nuisanceParameters = {}

	def __init__(self, fileName, smooth=True):
		""" Takes a file produced by BatchProfileLikelihoodPlot. """
		print("Opening file: "+fileName)
		f = ROOT.TFile.Open(fileName,"READ")
		self.hist_twoNll = f.Get("profiledNLL")
		self.hist_twoNll.Scale(2)

		# get all nuisance parameter histograms
		npNames = [ k.GetName() for k in f.GetListOfKeys() if "nuisParValue_" in k.GetName() ]
		for n in npNames: self.hist_nuisanceParameters[n.replace('nuisParValue_','')] = f.Get(n)

		# smooth
		if smooth:
			PyROOTUtils.nonLinearSmooth(self.hist_twoNll)
			for h in self.hist_nuisanceParameters.values(): PyROOTUtils.nonLinearSmooth(h)

		self.bestFit = f.Get("bestFit")
		self.bestFit_nuisanceParameters = self.npValues( self.bestFit.GetX(), self.bestFit.GetY() )


	def twoNll(self,x,y):
		return PyROOTUtils.interpolate( self.hist_twoNll,x,y )
	def twoNllInBin(self,x,y):
		return self.hist_twoNll.GetBinContent( self.hist_twoNll.GetBin(x,y) )

	def npValues(self,x,y):
		return dict( ((n,PyROOTUtils.interpolate(h,x,y)) for n,h in self.hist_nuisanceParameters.iteritems()) )
	def npValuesInBin(self,x,y):
		return dict( ((n,h.GetBinContent( h.GetBin(x,y) )) for n,h in self.hist_nuisanceParameters.iteritems()) )

	def getCoords(self):
		return (
			self.hist_twoNll.GetXaxis().GetBinCenter(self.x),
			self.hist_twoNll.GetYaxis().GetBinCenter(self.y),
		)

	# --------- Iterate over all bins ---------
	def __iter__(self):
		self.x, self.y = (0,1)
		return self

	def next(self):
		# increment
		if self.x < self.hist_twoNll.GetXaxis().GetNbins()-1:
			self.x += 10
		else:
			self.x = 1
			if self.y < self.hist_twoNll.GetYaxis().GetNbins()-1:
				self.y += 10
			else:
				self.x, self.y = (0,1)
				raise StopIteration

		return self.twoNllInBin(self.x,self.y)



import Plot.etas
def plotArrows( fullModel, etasDict, template=10 ):
	canvas = ROOT.TCanvas("c","c",600,600)
	axes = canvas.DrawFrame( 0.0, 0.0, 3.0,5.0)
	axes.Draw()

	arrows = []
	for fullTwoNll in fullModel:
		if fullTwoNll > 1.0: continue
		npVals = fullModel.npValuesInBin(fullModel.x,fullModel.y)
		npVals = dict( ((n,v-fullModel.bestFit_nuisanceParameters[n]) for n,v in npVals.iteritems()) )
		x,y = fullModel.getCoords()
		mu = {'muT':x, 'muW':y}

		arrows.append( Plot.etas.drawArrows( etasDict, mu, npVals, lineWidth=1.0, template=template ) )
	if options.verbose: canvas.SaveAs("test.png")


def lossFull( fullModel, effHist2Nll, etasDict, etasAndPhi, offset=None, muHat=None, template=20, verbose=False ):
	global c3, hD, hD2, container, debugCounter
	debugCounter += 1

	if not c3: 
		c3 = ROOT.TCanvas("debug","debug",1000,600)
		c3.Divide(2)
		c3.cd(1).SetRightMargin(0.16)
		c3.cd(2).SetRightMargin(0.16)
	if not hD or not hD2:
		hD = ROOT.TH2F( "loss1_debug", "hD;muT;muW", 30, 0.0, 3.5,  30, 0.0,5.5 )
		hD2 = ROOT.TH2F( "loss2_debug", "hD2;muT;muW", 30, 0.0, 3.5,  30, 0.0,5.5 )
		container.append(hD)
		container.append(hD2)
	else:
		#clean
		hD.Scale(1e-12)
		hD2.Scale(1e-12)
	if debugCounter % 100 == 0:
		hD.GetZaxis().SetRangeUser( -0.002,0.002 )
		hD2.GetZaxis().SetRangeUser( 0.0,1.0 )




	
	etasArrayFillsDict( etasAndPhi, etasDict )
	if debugCounter % 100 == 0: print(etasDict)
	if debugCounter % 100 == 0: plotArrows(fullModel,etasDict,template)
	m = effectiveModel.EffectiveParametrization( [ [effHist2Nll,etasDict,unit] ] )
	m.muHat = muHat
	m.template = template
	m.profile = False

	loss = 0
	sumWeights = 0

	compensation = 0.0  # see Kahan sum
	losses = []
	for fullTwoNll in fullModel:
		if fullTwoNll > 1.0: continue

		npVals = fullModel.npValuesInBin(fullModel.x,fullModel.y)
		npVals = dict( ((n,v-fullModel.bestFit_nuisanceParameters[n]) for n,v in npVals.iteritems()) )
		x,y = fullModel.getCoords()
		# print( str(x)+", "+str(y) )

		m.nuisanceParameters = dict( (n,v) for n,v in npVals.iteritems() if n in etasDict )
		effTwoNll = m.evalTwoNll(x,y)

		sumWeights += 1
		t = math.exp(-fullTwoNll)-math.exp(-effTwoNll + offset)
		# t = fullNll - effNll + offset
		# thisLoss = abs( t ) - compensation   # L1 loss
		thisLoss = 100.0 * 0.5*t*t  -  compensation  # quadratic loss
		newLoss = loss + thisLoss
		compensation = (newLoss - loss) - thisLoss # for next time
		# print( str(loss+100.0*0.5*t*t)+" == "+str(newLoss) )
		# print( compensation )
		loss = newLoss
		#loss += thisLoss
		losses.append(thisLoss)

		if debugCounter % 100 == 0:
			b = hD.FindBin( x,y )
			#hD.SetBinContent( b, math.exp(-fullNll) )
			if abs(t) > abs(hD.GetBinContent(b)): hD.SetBinContent( b, t )
			hD2.SetBinContent( b, math.exp(-effTwoNll+offset) )

	# apply median filter to losses
	if debugCounter % 100 == 0: print("Loss before median filter: "+str(loss))
	n = int(len(losses)*0.1)
	loss = sum( sorted(losses)[0:-n] )
	if debugCounter % 100 == 0: print("Loss after median filter: "+str(loss))

	
	if debugCounter % 100 == 0:
		c3.cd(1)
		hD.Draw("COLZ")
		c3.cd(2)
		hD2.Draw("COLZ")
		c3.Update()
		if options.verbose: c3.SaveAs("testLoss.png")
		
		print( loss )


	# loss /= sumWeights
	return loss



def etasGenericLearningFull(nll, poiL, nuisL, nuisLAll, w, fullModel, effHist2Nll, template=20):

	# init etas from fisher info
	etas = etasGenericM5(nll,poiL,nuisL,w)
	# etas = etasGenericFromFisherInfo(nll,poiL,nuisL,w)
	etas['constant'] = dict([(k,0.0) for k in etas.values()[0].keys() if "__phi" not in k])

	# extend the set of etas for asymmetric responses
	if template >= 20 and template <= 29:
		etasAsym = {}
		for par,prods in etas.iteritems():
			etasAsym[par] = {}
			for prod,eta in prods.iteritems():
				etasAsym[par][prod+'__up'] = eta
				etasAsym[par][prod+'__down'] = eta
		etas = etasAsym

	# normal etas
	etasArray = etasDictToArray( etas )
	print("                array eta: \n"+str(etasArray[0]))
	print("                array phi: \n"+str(etasArray[1]))
	etasArrayFillsDict( etasArray, etas )
	etasArray = etasDictToArray( etas )
	print("after test dict cycle: "+str(etasArray))

	# load MLEs
	w.loadSnapshot("ucmlesPOI")
	w.loadSnapshot("ucmlesNuis")
	muHat = { 'muT': w.var('muT').getVal(), 'muW': w.var('muW').getVal() }
	print( muHat )
	print()

	print("------------------ NSUIANCE PARAMETERS")
	nuisLAll.Print("v")
	poiL.Print("v")


	# minimizer boundaries
	bounds = [ (-0.30,0.30) for e in etasArray ]
	# bounds = [ (None,None) for e in etasArray ]

	# offset = [0.0]
	# print( "Optimizing offset" )
	# r = optimize.minimize( lambda v: loss(chain,minNll,effHist2Nll,etas,etasArray,nllVar.GetName(),offset=v,        muHat=muHat,template=template),             offset,           method="L-BFGS-B", bounds=[(-5.0,5.0)] )
	# print( r.x )
	# offset = list(r.x) # want to append this list and not add element-wise, so need to convert from ndarray to list
	# print( "Optimized offset" )
	# loss(                                 chain,minNll,effHist2Nll,etas,etasArray,nllVar.GetName(),offset=offset[0],muHat=muHat,template=template,verbose=True)
	# # raw_input("offset optimized")
	# optimize.minimize( lambda v: loss(    chain,minNll,effHist2Nll,etas,v,        nllVar.GetName(),                 muHat=muHat,template=template),             etasArray+offset, method="L-BFGS-B", bounds=bounds+[(-5.0,5.0)] )
	# loss(chain,minNll,effHist2Nll,etas,etasArray,nllVar.GetName(),offset=0.0,verbose=True)
	# raw_input("offset optimized")
	optimize.minimize( lambda v:       lossFull(fullModel,effHist2Nll,etas,v,offset=0.0,              muHat=muHat,template=template),             etasArray,        method="L-BFGS-B", bounds=bounds )
	
	# build etas np array
	# etasNpArrayShape = etasNpArray.shape
	# etasNpArray = etasNpArray.reshape( -1 )
	# print( "" )
	# print( etasNpArrayShape )
	# print( etasNpArray )
	# optimize.minimize( lambda v:       lossFast(chain,minNll,effHist2Nll,etas,v,nllVar.GetName(),offset=0.0,              muHat=muHat,template=template,etasShape=etasNpArrayShape),             etasNpArray,        method="L-BFGS-B" )

	# # ----- reassign etas
	# allEtas[ etas.keys()[0] ] = etas.values()[0]
	# etas = allEtas


	for p in etas.values():
		p['muT__hat'] = muHat['muT']
		p['muW__hat'] = muHat['muW']

	print( "Etas after learningFull")
	print( etas )

	return etas












def getAllEtas( inFile, method = "fisherInfo" ):
	"""
	High level function. Processes according to command line parameters. 
	Returns dictionary of etas. 
	method is one of "partialDerivatives", "covMatrix" or "fisherInfo".
	"""
	f = ROOT.TFile.Open( inFile, "READ" )
	w = f.Get( options.wsName )
	mc = w.obj( options.mcName )
	data = w.data( options.dataName )


	# convert input model into a muT,muW model
	BatchLikelihoodScan.Plugins.muTmuW.preprocess( f,w,mc,data )

	poiL = ROOT.RooArgList( mc.GetParametersOfInterest() )
	nuisLAll = ROOT.RooArgList( mc.GetNuisanceParameters() )
	nuisL = ROOT.RooArgList()
	for i in range( nuisLAll.getSize() ):
		if nuisLAll.at(i).GetName() in options.parameters:
			nuisL.add( nuisLAll.at(i) )

	nll = getNll( mc.GetPdf(), data, minStrategy=options.minStrategy, enableOffset=options.enableOffset, globObs=mc.GetGlobalObservables() )

	# global fit
	minimize( nll )
	w.saveSnapshot("ucmlesNuisNonConst",mc.GetNuisanceParameters())
	w.saveSnapshot("ucmlesPOINonConst",mc.GetParametersOfInterest())
	# setting all constant
	for i in range( nuisLAll.getSize() ): nuisLAll.at(i).setConstant()
	for i in range( poiL.getSize() ): poiL.at(i).setConstant()
	# saving as initial state for loops
	w.saveSnapshot("ucmlesNuis",mc.GetNuisanceParameters())
	w.saveSnapshot("ucmlesPOI",mc.GetParametersOfInterest())

	etas = {}
	if method == "partialDerivatives":
		for i in range( nuisL.getSize() ):
			etas[nuisL.at(i).GetName()] = {}
			for mu in ["muT","muW"]:
				muVar = w.var(mu)
				w.loadSnapshot("ucmlesPOI")
				w.loadSnapshot("ucmlesNuis")
				#etas[nuisL.at(i).GetName()][mu] = oneEta( nll, nuisL.at(i), muVar, poiL )
				etas[nuisL.at(i).GetName()][mu] = oneEtaMuPPrimeZero( nll, nuisL.at(i), muVar, poiL )
				#etas[nuisL.at(i).GetName()][mu] = oneEtaMuPhiSubstitution( nll, nuisL.at(i), muVar, poiL )
				#etas[nuisL.at(i).GetName()][mu] = oneEtaSystemOfPDEs( nll, nuisL.at(i), muVar, poiL )

		print( "================= etas from partial mu/alpha =============" )
		pprint( etas )

	elif method == "covMatrix":
		# obtain etas from covariance matrix
		w.loadSnapshot("ucmlesPOI")
		w.loadSnapshot("ucmlesNuis")
		etas = etasFromCovariance( nll, poiL, nuisL, w )

	elif method == "fisherInfo":
		# obtain etas from covariance matrix
		w.loadSnapshot("ucmlesPOI")
		w.loadSnapshot("ucmlesNuis")
		etas = etasFromFisherInfo( nll, poiL, nuisL, w )
	
	elif method == "generic_fisherInfo":
		# obtain etas from covariance matrix
		w.loadSnapshot("ucmlesPOI")
		w.loadSnapshot("ucmlesNuis")
		etas = etasGenericFromFisherInfo( nll, poiL, nuisL, w )
	
	elif method == "generic_M4":
		# obtain etas from covariance matrix
		w.loadSnapshot("ucmlesPOI")
		w.loadSnapshot("ucmlesNuis")
		etas = etasGenericM4( nll, poiL, nuisL, w )
	
	elif method == "generic_M5":
		# obtain etas from covariance matrix
		w.loadSnapshot("ucmlesPOI")
		w.loadSnapshot("ucmlesNuis")
		etas = etasGenericM5( nll, poiL, nuisL, w )
	
	elif method in ["generic10_learning","generic14_learning","generic20_learning","generic24_learning"]:
		# obtain etas from covariance matrix
		w.loadSnapshot("ucmlesPOI")
		w.loadSnapshot("ucmlesNuis")

		effFileName = inFile.replace(".root","/muTmuW_statOnly.root")
		effFile = ROOT.TFile.Open( effFileName, "READ" )
		effHist2Nll = effFile.Get( "profiledNLL" )
		effHist2Nll.Scale(2)
		effHist2Nll.Draw("COLZ")
		# raw_input("wait")

		template = 20
		if method == 'generic10_learning': template = 10
		if method == 'generic14_learning': template = 14
		if method == 'generic20_learning': template = 20
		if method == 'generic24_learning': template = 24
		etas = etasGenericLearning( nll, poiL, nuisL, nuisLAll, w, effHist2Nll, template=template )

		effFile.Close()
	
	elif method in ["generic10_learningFull","generic14_learningFull","generic20_learningFull","generic24_learningFull"]:
		# obtain etas from covariance matrix
		w.loadSnapshot("ucmlesPOI")
		w.loadSnapshot("ucmlesNuis")

		fullModel = FullModelScan(inFile.replace(".root","/muTmuW.root"))

		effFileName = inFile.replace(".root","/muTmuW_eff.root")
		effFile = ROOT.TFile.Open( effFileName, "READ" )
		effHist2Nll = effFile.Get( "profiledNLL" )
		effHist2Nll.Scale(2)
		PyROOTUtils.nonLinearSmooth(effHist2Nll)
		effHist2Nll.Draw("COLZ")
		# raw_input("wait")

		template = 20
		if method == 'generic10_learningFull': template = 10
		if method == 'generic14_learningFull': template = 14
		if method == 'generic20_learningFull': template = 20
		if method == 'generic24_learningFull': template = 24
		etas = etasGenericLearningFull( nll, poiL, nuisL, nuisLAll, w, fullModel, effHist2Nll, template=template )

		effFile.Close()
	
	else:
		print( "!!! ERROR getAllEtas(): Invlid method specified." )

	return etas


def convertEtasDictToTexHeader( etasDict ):
	""" expects a dict where top level is the channel and then under it are the two 
	axes muT and muW """

	# initialize lines to first column filled
	format = "l"
	headerTop = ""
	headerBottom = "Parameter "
	for channel,parameters in etasDict.iteritems():
		format += " |"
		axes = parameters.values()[0].keys()
		headerTop += "& \multicolumn{%d}{|c}{%s}" % (len(axes),channel)
		for axis in axes:
			format += " c"
			headerBottom += "& $\eta_{\\textrm{"+axis+"}}$ "

	headerTop += "\\\\ \n"
	headerBottom += "\\\\ \n"

	return (format,headerTop+headerBottom)



def convertEtasDictToPy( etasDict ):
	""" expects a dict where top level is the channel and then under it are the two 
	axes muT and muW """

	out = "etas = {\n"
	for channel,parameters in etasDict.iteritems():
		out += "\t'"+channel+"': {\n"
		for parameter,axes in parameters.iteritems():
			out += "\t\t'"+parameter+"': { "+(', '.join([ "'"+axis+"': "+str(eta) for axis,eta in sorted(axes.iteritems()) ]))+" },\n"
		out += "\t},\n"
	out += "}"

	return out


def main():
	if not options.verbose:
		ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.FATAL)

	etasAll = { 
		"partialDerivatives":getAllEtas( options.input,method="partialDerivatives" ),
		"covarianceMatrix":getAllEtas( options.input, method="covMatrix" ),
		"fisherInfo":getAllEtas( options.input, method="fisherInfo" ),
		"generic_fisherInfo":getAllEtas( options.input, method="generic_fisherInfo" ),
		"generic_M4":getAllEtas( options.input, method="generic_M4" ),
		"generic_M5":getAllEtas( options.input, method="generic_M5" ),
		# "generic10_learning":getAllEtas( options.input, method="generic10_learning" ),
		# "generic14_learning":getAllEtas( options.input, method="generic14_learning" ),
		# "generic20_learning":getAllEtas( options.input, method="generic20_learning" ),
		# "generic24_learning":getAllEtas( options.input, method="generic24_learning" ),

		"generic10_learningFull":getAllEtas( options.input, method="generic10_learningFull" ),
		# "generic14_learningFull":getAllEtas( options.input, method="generic14_learningFull" ),
		"generic20_learningFull":getAllEtas( options.input, method="generic20_learningFull" ),
		# "generic24_learningFull":getAllEtas( options.input, method="generic24_learningFull" ),
	}
	pprint( etasAll )

	pyTable = convertEtasDictToPy( etasAll )
	print( pyTable )
	with open( options.output+"table_etas_full.py", "w" ) as f:
		f.write( str(pyTable) )
	with open( options.output+"table_etas_full.pickle", "wb" ) as f:
		pickle.dump( etasAll, f )

	# write out a reduced set of etas that are fixed uncertainties
	for t,prods in etasAll.iteritems():
		for n in prods.keys():
			if n not in options.parameters and n != 'constant': del etasAll[t][n]
	
	pyTable = convertEtasDictToPy( etasAll )
	print( pyTable )
	with open( options.output+"table_etas.py", "w" ) as f:
		f.write( str(pyTable) )
	with open( options.output+"table_etas.pickle", "wb" ) as f:
		pickle.dump( etasAll, f )

	print( "Output written to: "+options.output )

if __name__ == "__main__":
	main()


