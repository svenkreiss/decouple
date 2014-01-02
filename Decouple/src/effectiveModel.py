#!/usr/bin/env python

#  Created on: August 2, 2013

__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"


import ROOT
from PyROOTUtils import interpolate

from scipy.optimize import minimize
import math
from pprint import pprint

container = []

import re, pickle
import numpy

from multiprocessing import Pool
from progressbar import ProgressBar


def addOptionsToParser( parser ):
	parser.add_option(      "--single", dest="single", default=False, action="store_true", help="Only run one process.")
	parser.add_option("-p", "--profile", dest="profile", default=False, action="store_true", help="Whether to profile in this script.")

	parser.add_option(      "--template", help="set template (where 0 and 4 are inspired by FlexibleInterpVar codes)", dest="template", default=4, type="int")
	parser.add_option("-d", "--doubleConstr", dest="doubleConstr", default=False, action="store_true", help="Keep double or tripple counted constraint terms.")
	parser.add_option(      "--box", dest="box", default=None, type="float", help="Use box constraints (RFit) with the given half-width.")
	parser.add_option(      "--wideGauss", dest="wideGauss", default=None, type="float", help="Use wideGauss constraints with given width.")
	parser.add_option("-s", "--setParameter", dest="setParameter", default=None, help="Sets value for a nuisance paramter.")

def optionsString( opts ):
	s = ''
	s += ' --template='+str(opts.template)
	if opts.single:       s += ' --single'
	if opts.profile:      s += ' --profile'
	if opts.doubleConstr: s += ' --doubleConstr'
	if opts.box:          s += ' --box='+str(opts.box)
	if opts.wideGauss:    s += ' --wideGauss='+str(opts.wideGauss)
	if opts.setParameter: s += ' --setParameter='+str(opts.setParameter)
	return s

def outFileName( orig, opts ):
	# determine suffix
	s = ''
	if opts.template != 4:
		s += '_template'
		if opts.template < 0: s += 'M'
		s += str( abs(opts.template) )
	# determine if there is a non-standard etas type
	for i in re.split(',| ', opts.input):
		if len( i.split(':') ) == 5:
			fileName, histName, etasFile, etasName, scale = i.split(':')
			if etasName != 'fisherInfo':
				s += '_etas'+etasName
				break
	if not opts.profile:
		s += '_fixed'
	if opts.doubleConstr:
		s += '_doubleConstr'
	if opts.box:
		s += '_box'+str(opts.box)
	if opts.wideGauss:
		s += '_wideGauss'+str(opts.wideGauss)
	if opts.setParameter:
		s += '_setParameter'+opts.setParameter.replace('=','_')
	return orig.replace('.root',s+'.root')

def getInputs( inputString ):
	""" 
	Returns a list of input histograms, etas, and the part of the input string. 
	The idea is that once the input string is replaced with a function, this can
	be used directly with EffectiveParamatrization. 
	"""
	inputs = []

	for i in re.split(',| ', inputString):
		if len( i.split(':') ) == 2:
			fileName, histName = i.split(':')
			etasFile = fileName.replace('.root','_table_etas.py')
			etasName = 'fisherInfo'
			scale = 1.0
		elif len( i.split(':') ) == 3:
			fileName, histName, etasFile = i.split(':')
			etasName = 'fisherInfo'
			scale = 1.0
		elif len( i.split(':') ) == 4:
			fileName, histName, etasFile, scale = i.split(':')
			etasName = 'fisherInfo'
			scale = float(scale.strip(', '))
		elif len( i.split(':') ) == 5:
			fileName, histName, etasFile, etasName, scale = i.split(':')
			scale = float(scale.strip(', '))


		print( "From "+fileName+" reading "+histName+" and scaling by "+str(scale)+"." )
		f = ROOT.TFile.Open( fileName, "READ" )
		h = f.Get( histName )
		h.Scale( scale )
		container.append( h )

		if ".pickle" in etasFile:
			print( "Loading etas from pickle file." )
			with open(etasFile, "rb") as f:
				etas = pickle.load( f )[ etasName ]
		elif etasFile != 'None':
			print( "Loading etas from python module." )
			etasF = __import__(etasFile)
			etas = etasF.etas[ etasName ]
		else:
			etas = {}
		inputs.append( [h,etas,fileName+'_'+histName] )

	return inputs











class EffectiveParametrization:
	"""
	Inputs are the effective likelihood histogram, the remaining nuisance
	parameters and their eta values.
	"""

	pois = [None,None]
	nuisanceParameters = {}
	responseTGraphs = {}
	inputs = None

	# options
	template = 4
	box = None
	wideGauss = None
	profile = True

	# optional for some templates
	muHat = {}


	def __init__(self, inputs=None, options=None):
		self.inputs = inputs
		if inputs != None: self.extractNuisanceParametersFromInputs( inputs )
		if options != None: self.applyOptions( options )

	def applyOptions(self, options):
		self.template = options.template
		self.box = options.box
		self.wideGauss = options.wideGauss
		self.profile = options.profile
		if options.setParameter:
			for p,v in [(pv.split('=')[0],pv.split('=')[1]) for pv in options.setParameter.split(',')]:
				self.nuisanceParameters[p] = float(v)



	def resetNuisanceParameters(self):
		for k in self.nuisanceParameters.keys(): self.nuisanceParameters[k] = 0.0

	def extractNuisanceParametersFromEtas(self,etas):
		self.nuisanceParameters = dict([ (k,0.0) for k in etas.keys() if k != 'constant'])

	def extractNuisanceParametersFromInputs(self,inputs):
		nps = []
		for i in inputs: 
			etas = i[1]
			nps += [ (k,0.0) for k in etas.keys() if k != 'constant']
		self.nuisanceParameters = dict(nps)

	def setParametersFromRooArgSet(self, rooargset, xName=None, yName=None, filter=[]):
		# print( "-------------" )
		# rooargset.Print("V")

		setL = ROOT.RooArgList( rooargset )
		for i in range( setL.getSize() ):
			pName = setL.at(i).GetName()
			if pName in filter: continue

			if   pName == xName: self.pois[ 0 ] = setL.at(i).getVal()
			elif pName == yName: self.pois[ 1 ] = setL.at(i).getVal()
			else: self.nuisanceParameters[ pName ] = setL.at(i).getVal()

		# print(self.nuisanceParameters)
		# print(self.pois)

	def setParametersFromRooArgSetFast(self, rooargset, xName=None, yName=None):
		# print( "-------------" )
		# rooargset.Print("V")

		for pName in self.nuisanceParameters.keys():
			self.nuisanceParameters[ pName ] = rooargset.getRealValue( pName )

		self.pois[ 0 ] = rooargset.getRealValue( xName )
		self.pois[ 1 ] = rooargset.getRealValue( yName )

		# print(self.nuisanceParameters)
		# print(self.pois)




	def getConstraintTermsHists( self, filename, suffix=None, useAverage=False, priority=None ):
		""" Constructs constraint term values as a function of muT,muW
		but only keeps terms that were not seens in a previous channel. """

		if not priority:
			priority = reversed(["2ph","4l","lvlv"])


		f = ROOT.TFile.Open( filename, "READ" )

		l = f.GetListOfKeys()
		nuisParams = []
		for i in range( l.GetSize() ):
			if "nuisParValue_" == l.At(i).GetName()[:13]:
				nuisName = l.At(i).GetName()[13:]
				nuisName = nuisName[:nuisName.rfind("_")] # remove channel label
				if suffix:
					if suffix not in nuisName: continue
					nuisName = nuisName.replace(suffix, "")
				else:
					containsSuffix = False
					for possibleSuffix in ["_eff","_forCouplingsFromProdModes"]:
						if possibleSuffix in nuisName:
							containsSuffix = True
							break
					if containsSuffix: continue
				if nuisName in nuisParams: continue
				nuisParams.append( nuisName )
		print( "======== Nuisance Parameters taken into account for constraint term ========")
		print( nuisParams )
		print( "" )

		# Average nuisance parameter value.
		# When having three Gaussians with the same width at different positions
		# (or as here, the same Gaussian three times with different pulls), then
		# the maximum of the product of the three Gaussians is at the arithmetic
		# mean of the three Gaussian mean values.
		# 
		# Do not use for now because the different histogram boundaries between
		# the channels are a problem.

		# averageNuisParValues = {}
		# for n in nuisParams:

		# 	maxBinsMuT,maxBinsMuW = (0,0)
		# 	maxMuT,maxMuW = (0,0)
		# 	minMuT,minMuW = (10,10)
		# 	for c in ["4l","2ph","lvlv"]: # give priority to 4l because we need the maximum parameter range
		# 		n_h = f.Get( "nuisParValue_"+n+suffix+"_"+c )
		# 		if not n_h: continue

		# 		muT = [ n_h.GetXaxis().GetNbins(), n_h.GetXaxis().GetXmin(), n_h.GetXaxis().GetXmax() ] 
		# 		muW = [ n_h.GetYaxis().GetNbins(), n_h.GetYaxis().GetXmin(), n_h.GetYaxis().GetXmax() ]
		# 		if muT[0] > maxBinsMuT: maxBinsMuT = muT[0]
		# 		if muW[0] > maxBinsMuW: maxBinsMuW = muW[0]
		# 		if muT[1] < minMuT: minMuT = muT[1]
		# 		if muW[1] < minMuW: minMuW = muW[1]
		# 		if muT[2] > maxMuT: maxMuT = muT[2]
		# 		if muW[2] > maxMuW: maxMuW = muW[2]

		# 		if n in averageNuisParValues.keys():
		# 			averageNuisParValues[n].append( n_h )
		# 		else:
		# 			averageNuisParValues[n] = [ n_h ]

		# 	muT = [ 2*maxBinsMuT, minMuT, maxMuT ]
		# 	muW = [ 2*maxBinsMuW, minMuW, maxMuW ]
		# 	h_average = ROOT.TH2F( "average_"+n, "Average value of "+n+";muT;muW;average value",  muT[0], muT[1], muT[2],  muW[0], muW[1], muW[2] )
		# 	for x in range(muT[0] ):
		# 		muTVal = muT[1] + (x+0.5)*(muT[2]-muT[1]) / muT[0]
		# 		for y in range( muW[0] ):
		# 			muWVal = muW[1] + (y+0.5)*(muW[2]-muW[1]) / muW[0]

		# 			count = 0
		# 			sumVal = 0.0
		# 			for h in averageNuisParValues[n]:
		# 				val = interpolate( h, muTVal, muWVal, outOfRangeValue=2345789 )
		# 				if val != 2345789:
		# 					sumVal += val
		# 					count += 1

		# 			if count > 0:
		# 				bin = h_average.FindBin( muTVal, muWVal )
		# 				h_average.SetBinContent( bin, sumVal/count )

		# 	averageNuisParValues[n] = h_average


		h = { "2ph":None, "4l":None, "lvlv":None }
		seenNuisParams = []
		for c in priority:
			muT,muW = (None,None)
			for n in nuisParams:
				n_h = f.Get( "nuisParValue_"+n+suffix+"_"+c )
				if not n_h: continue

				if h[c] is None:
					muT = [ n_h.GetXaxis().GetNbins(), n_h.GetXaxis().GetXmin(), n_h.GetXaxis().GetXmax() ] 
					muW = [ n_h.GetYaxis().GetNbins(), n_h.GetYaxis().GetXmin(), n_h.GetYaxis().GetXmax() ] 
					h[c] = ROOT.TH2F( "constr_"+c, "Constraint term value for "+c+";muT;muW;-2 ln #Lambda",  muT[0], muT[1], muT[2],  muW[0], muW[1], muW[2] )


				if (not useAverage) and n not in seenNuisParams: 
					seenNuisParams.append( n )
				else:
					for x in range(muT[0] ):
						muTVal = muT[1] + (x+0.5)*(muT[2]-muT[1]) / muT[0]
						for y in range( muW[0] ):
							muWVal = muW[1] + (y+0.5)*(muW[2]-muW[1]) / muW[0]

							bin = h[c].FindBin( muTVal, muWVal )
							if n_h:
								v = n_h.GetBinContent(bin)
								ave = 0.0
								if useAverage:
									ave = interpolate( averageNuisParValues[n], muTVal, muWVal, outOfRangeValue=0.0 )
								h[c].SetBinContent( bin, h[c].GetBinContent(bin) + (v-ave)*(v-ave) )

		container.append( h )
		return (h["2ph"],h["4l"],h["lvlv"])




	def getResponseTGraphs( self, inFileName=None ):
		if len(self.responseTGraphs.keys()) > 0: return self.responseTGraphs
		if not inFileName:
			print( "ERROR in getResponseTGraphs(): please specify a file to read from at least once." )
			return "ERROR"

		f = ROOT.TFile.Open( inFileName, "READ" )
		for c in ["2ph","4l","lvlv"]:
			self.responseTGraphs[c] = {}
			for r in ["muT","muW"]:
				# plain one-parameter graphs
				self.responseTGraphs[c][r] = {}
				graphs = self.responseTGraphs[c][r]
				for n in self.nuisanceParameters.keys():			
					g = f.Get("ggFttH_VBFVH_Nuis__"+n+"__response_"+r+"_fit_"+c)
					if g: graphs[ n ] = g

		return self.responseTGraphs


	# def responseFunction( nuisPars, channel="2ph", doProduct=True ):
	# 	""" Input are the TGraphs of tau(alpha).
	#   
	#   Response in the two axes muT and muW. For lognormal constraint terms,
	# 	the combination of many responses is done multiplicative (which is additive
	# 	after taking the log). """

	# 	scales = {"muT":1.0, "muW":1.0}
	# 	for axis in scales.keys():
	# 		respFuncs = getResponseTGraphs()[ channel ][ axis ]
	# 		for n,v in nuisPars.iteritems():
	# 			if n in respFuncs.keys():
	# 				if doProduct:
	# 					scales[axis] *= respFuncs[n].Eval( v )
	# 				else:
	# 					scales[axis] += respFuncs[n].Eval( v ) - 1

	# 	return ( scales['muT'], scales['muW'] )

	def interpCode4( self, low, high, x ):
		""" 
		Implements the gist of interpcode4 from FlexibleInterpVar.cxx. 

		low = 1 - eta*boundary
		high = 1 + eta*boundary
		"""
		if x >= 1.0:
			if high>0.0 and x<10: return high**x
			return 0.0
		elif x <= -1.0:
			if low>0.0 and x>-10: return low**-x
			return 0.0

		# below we know we are between the boundaries: do polynomial interpolation
		logHi = math.log(high) if high > 0.0 else 0.0
		logLo = math.log(low)  if low  > 0.0 else 0.0

		pow_up = high     if high > 0.0   else 0.0
		pow_down = low    if low  > 0.0   else 0.0
		pow_up_log   = pow_up * logHi     if high > 0.0   else 0.0
		pow_down_log = -pow_down * logLo  if low  > 0.0   else 0.0
		pow_up_log2   = pow_up_log * logHi     if high > 0.0   else 0.0
		pow_down_log2 = -pow_down_log * logLo  if low  > 0.0   else 0.0

		S0 = (pow_up+pow_down)/2
		A0 = (pow_up-pow_down)/2
		S1 = (pow_up_log+pow_down_log)/2
		A1 = (pow_up_log-pow_down_log)/2
		S2 = (pow_up_log2+pow_down_log2)/2
		A2 = (pow_up_log2-pow_down_log2)/2

		# fcns+der+2nd_der are eq at bd
		a = 1./8 * (      15*A0 -  7*S1 + A2)
		b = 1./8 * (-24 + 24*S0 -  9*A1 + S2)
		c = 1./4 * (    -  5*A0 +  5*S1 - A2)
		d = 1./4 * ( 12 - 12*S0 +  7*A1 - S2)
		e = 1./8 * (    +  3*A0 -  3*S1 + A2)
		f = 1./8 * ( -8 +  8*S0 -  5*A1 + S2)

		xx = x*x
		xxx = xx*x
		return 1. + a*x + b*xx + c*xxx + d*xx*xx + e*xxx*xx + f*xxx*xxx;


	def responseFunctionFast( self, muIn, etasAndPhi, npArray ):
		"""
		muIn and muOut are column matrices.

		All inputs and outputs are numpy arrays.
		Etas is an array (nuisance parameter) of matrices (pois).
		"""

		muOut = numpy.matrix( muIn )
		muInExt = numpy.vstack( (muIn,[1]) )

		if self.template == 10:
			for etaMatrix,alpha in zip(etasAndPhi,npArray):
				muOut += etaMatrix*muInExt*alpha
		else:
			print( "ERROR" )

		# print( "muIn")
		# print( muIn)
		# print("muOut")
		# print( muOut)

		return muOut



	def responseFunctionInv( self, muIn, etas ):
		""" Input is python table of etas.

		Response in the two axes muT and muW. For lognormal constraint terms,
		the combination of many responses is done multiplicative (which is additive
		after taking the log). """

		# deep copy
		mu = dict([ (p,v) for p,v in muIn.iteritems() ])

		# subtract phi term
		for a in mu.keys():
			for n,v in self.nuisanceParameters.iteritems():
				mu[a] -= etas[n][a+'__phi']*v

		# invert matrix
		a = 1.0
		for n,v in self.nuisanceParameters.iteritems():
			a += etas[n]['muT__muT']*v
		b = 0.0
		for n,v in self.nuisanceParameters.iteritems():
			b += etas[n]['muW__muT']*v
		c = 0.0
		for n,v in self.nuisanceParameters.iteritems():
			c += etas[n]['muT__muW']*v
		d = 1.0
		for n,v in self.nuisanceParameters.iteritems():
			d += etas[n]['muW__muW']*v

		# deep copy
		muSubt = dict([ (p,v) for p,v in mu.iteritems() ])

		mu['muT'] = 1.0/(a*d-b*c) * ( d*muSubt['muT'] - b*muSubt['muW'])
		mu['muW'] = 1.0/(a*d-b*c) * (-c*muSubt['muT'] + a*muSubt['muW'])

		return mu



	def responseFunction( self, muIn, etas ):
		""" Input is python table of etas.

		Response in the two axes muT and muW. For lognormal constraint terms,
		the combination of many responses is done multiplicative (which is additive
		after taking the log). """

		# deep copy
		mu = dict([ (p,v) for p,v in muIn.iteritems() ])

		for a in mu.keys():
			if self.template == 4:  # special and exact handling of interpcode 4
				for n,v in self.nuisanceParameters.iteritems():
					if n not in etas: continue
					mu[a] *= self.interpCode4( 1-etas[n][a], 1+etas[n][a], v )
			elif self.template in [3]:  # generically handling all exponential extrap codes by using multiplicative response
				for n,v in self.nuisanceParameters.iteritems():
					if n not in etas: continue
					mu[a] *= 1.0 + etas[n][a]*v
			elif self.template in [-1]:   # linear version (even linear between eta*alpha _and_ mu)
				for n,v in self.nuisanceParameters.iteritems():
					if n not in etas: continue
					mu[a] += etas[n][a]*v
			elif self.template in [10]:  # generic model with additive responses
				for aPrime in mu.keys():
					for n,v in self.nuisanceParameters.iteritems():
						if n not in etas: continue
						mu[a] += muIn[aPrime] * etas[n][a+'__'+aPrime] * v  # similar to eqn in "else"
					if 'constant' in etas: 
						mu[a] += muIn[aPrime] * etas['constant'][a+'__'+aPrime]
				for n,v in self.nuisanceParameters.iteritems():
					mu[a] += etas[n][a+'__phi']*v
			elif self.template in [14]:  # generic model with multiplicative responses
				for n,v in self.nuisanceParameters.iteritems():
					if n not in etas: continue
					eta = 0.0
					for aPrime in mu.keys():
						scaling = muIn[aPrime]/muIn[a]
						if aPrime == a: scaling = 1.0  # for numerical stability
						if scaling > 10: scaling = 10
						if scaling < -10: scaling = -10
						eta += scaling * etas[n][a+'__'+aPrime]
					mu[a] *= self.interpCode4( 1-eta, 1+eta, v )
				for n,v in self.nuisanceParameters.iteritems():
					if n not in etas: continue
					mu[a] += etas[n][a+'__phi']*v
			elif self.template in [20]:  # generic model with additive responses
				for aPrime in mu.keys():
					for n,v in self.nuisanceParameters.iteritems():
						if n not in etas: continue
						suffix = '__up'
						if v < 0.0: suffix = '__down'
						mu[a] += muIn[aPrime] * etas[n][a+'__'+aPrime+suffix] * v  # similar to eqn in "else"
					if 'constant' in etas: 
						mu[a] += muIn[aPrime] * etas['constant'][a+'__'+aPrime+suffix]
				for n,v in self.nuisanceParameters.iteritems():
					mu[a] += etas[n][a+'__phi'+suffix]*v
			elif self.template in [24]:  # generic model with multiplicative responses (asym responses)
				for n,v in self.nuisanceParameters.iteritems():
					if n not in etas: continue
					# if a+'__hat' in etas[n]: self.muHat[a] = etas[n][a+'__hat']
					eta_up = 0.0
					eta_down = 0.0
					for aPrime in mu.keys():
						# if aPrime+'__hat' in etas[n]: self.muHat[aPrime] = etas[n][aPrime+'__hat']
						# scaling = muIn[aPrime]/self.muHat[aPrime]
						scaling = muIn[aPrime]/muIn[a]
						if aPrime == a: scaling = 1.0  # for numerical stability
						if scaling > 10: scaling = 10
						if scaling < -10: scaling = -10
						eta_up += scaling * etas[n][a+'__'+aPrime+'__up']
						eta_down += scaling * etas[n][a+'__'+aPrime+'__down']
					mu[a] *= self.interpCode4( 1-eta_down, 1+eta_up, v )
				for n,v in self.nuisanceParameters.iteritems():
					if n not in etas: continue
					suffix = '__up'
					if v < 0.0: suffix = '__down'
					mu[a] += etas[n][a+'__phi'+suffix]*v

			else: # all other interpcodes handled with additive response
				for n,v in self.nuisanceParameters.iteritems():
					if n not in etas: continue
					mu[a] += muIn[a] * etas[n][a] * v

		return mu


	def constraintTerms(self):
		""" Gaussian constraint terms. One 1D Gaussian per nuisance parameter. """

		twoNll = 0.0
		for name,v in self.nuisanceParameters.iteritems():
			if self.box is not None and ("QCDscale_Higgs_" in name or name in['alpha_sys','alpha_sys_GGF']):
				# boundary is handled as input to minimize function for better convergence
				twoNll += v*v / (10000.0*10000.0)
			elif self.wideGauss is not None and ("QCDscale_Higgs_" in name or name in['alpha_sys','alpha_sys_GGF']):
				twoNll += v*v / (self.wideGauss*self.wideGauss)
			else:
				twoNll += v*v

		return twoNll


	def evalTwoNllFast( self, etasAndPhi, npArray ):
		twoNll = 0.0
		for hist,etas,mapFunc in self.inputs:
			mu = numpy.matrix( mapFunc(self.pois[0], self.pois[1]) ).transpose()
			muR = self.responseFunctionFast( mu, etasAndPhi, npArray )
			twoNll += interpolate( hist, muR[0], muR[1] )

		# constraint term fast
		twoNll += sum( v*v for v in npArray )
		return twoNll		

	def evalTwoNll( self, x=None, y=None, values=None ):
		""" 
		h is a dictionary of channel:(muTmuW histograms,mapFunction). 
		For the muTmuW plot, mapFunc is the identity. For the coupling plots,
		mapFunction is the map from couplings to muTmuW.
		"""

		if x != None: self.pois[0] = x
		if y != None: self.pois[1] = y

		if values!=None:
			for k,v in zip(self.nuisanceParameters.keys(),values): self.nuisanceParameters[k] = v


		twoNll = 0.0
		for hist,etas,mapFunc in self.inputs:
			muT,muW = mapFunc(self.pois[0], self.pois[1])
			muR = self.responseFunction( {'muT':muT, 'muW':muW}, etas )
			twoNll += interpolate( hist, muR['muT'], muR['muW'], outOfRangeValue=1e6 )

		twoNll += self.constraintTerms()
		return twoNll


	def evalTwoNllFullMu( self, x=None, y=None, values=None ):
		""" 
		h is a dictionary of channel:(muTmuW histograms,mapFunction). 
		For the muTmuW plot, mapFunc is the identity. For the coupling plots,
		mapFunction is the map from couplings to muTmuW.
		"""

		if x != None: self.pois[0] = x
		if y != None: self.pois[1] = y

		if values!=None:
			for k,v in zip(self.nuisanceParameters.keys(),values): self.nuisanceParameters[k] = v


		twoNll = 0.0
		for hist,etas,mapFunc in self.inputs:
			muT,muW = mapFunc(self.pois[0], self.pois[1])
			muR = self.responseFunctionInv( {'muT':muT, 'muW':muW}, etas )
			twoNll += interpolate( hist, muR['muT'], muR['muW'], outOfRangeValue=1e6 )

		twoNll += self.constraintTerms()
		return twoNll



	def profileTwoNll( self, x=None, y=None, threshold=5000 ):
		""" 
		h is a dictionary of channel:muTmuW histograms. 

		Minimization is done using L-BFGS-B here, but most minimization algorithms should be fine.
		For more info: R. H. Byrd, P. Lu and J. Nocedal. A Limited Memory Algorithm for Bound 
		Constrained Optimization, (1995), SIAM Journal on Scientific and 
		Statistical Computing, 16, 5, pp. 1190-1208.
		"""
		if not self.profile or len(self.nuisanceParameters.keys())==0:
			return self.evalTwoNll(x,y)

		initial = self.evalTwoNll(x,y)
		if initial > threshold:
			# print( "Trying setting all QCDscale parameters to a positive value.")
			for n in self.nuisanceParameters.keys():
				if ("QCDscale_Higgs_" in n or n in['alpha_sys','alpha_sys_GGF']):
					self.nuisanceParameters[n] = -1.5
					initial = self.evalTwoNll(x,y)
					if initial < threshold: break
					else: self.nuisanceParameters[n] = 0.0
		if initial > threshold:
			# print( "Trying setting all QCDscale parameters to a negative value.")
			for n in self.nuisanceParameters.keys():
				if ("QCDscale_Higgs_" in n or n in['alpha_sys','alpha_sys_GGF']):
					self.nuisanceParameters[n] = +1.5
					initial = self.evalTwoNll(x,y)
					if initial < threshold: break
					else: self.nuisanceParameters[n] = 0.0

		if initial < threshold:
			bounds = []
			for n in self.nuisanceParameters.keys():
				if self.box is not None and ("QCDscale_Higgs_" in n or n in['alpha_sys','alpha_sys_GGF']):
					bounds.append( (-self.box,self.box) )
				else:
					bounds.append( (None,None) )

			# BFGS algorithm in optimize package does not support parameter bounds. L-BFGS-B does.
			minimize( lambda v: self.evalTwoNll(x,y,v), self.nuisanceParameters.values(), method="L-BFGS-B", bounds=bounds )
		else:
			# print( "fit skipped due to too large initial nll value" )
			pass

		return self.evalTwoNll(x,y)





def _fill(x_y_inputs_options):
	x,y, inputs, options = x_y_inputs_options
	m = EffectiveParametrization(inputs, options)
	value = m.profileTwoNll( x, y )
	return (x,y,value,m.nuisanceParameters)

def fillHist(h,x,y, inputs, options, npHistograms=None):
	""" Give an empty dictionary to npHistograms to have it filled. """

	if options.single:
		m = EffectiveParametrization(inputs, options)
		for i in range(x[0] ):
			xVal = x[1] + (i+0.5)*(x[2]-x[1]) / x[0]
			print( "progress: %.0f%%" % (100.0*i/x[0]) )
			for j in range( y[0] ):
				yVal = y[1] + (j+0.5)*(y[2]-y[1]) / y[0]

				v = m.profileTwoNll( xVal, yVal )
				bin = h.FindBin( xVal, yVal )
				h.SetBinContent( bin, v )

				# fill nuisance parameter histograms
				if npHistograms != None:
					for npName,npValue in m.nuisanceParameters.iteritems():
						if npName not in npHistograms.keys(): 
							npHistograms[npName] = h.Clone( "nuisParValue_"+npName )
							npHistograms[npName].SetTitle( 'value of '+npName )
							npHistograms[npName].GetZaxis().SetTitle( 'nuisance parameter value' )
						npHistograms[npName].SetBinContent( bin, npValue )

	else:
		paramPoints = []
		for i in range(x[0] ):
			xVal = x[1] + (i+0.5)*(x[2]-x[1]) / x[0]
			for j in range( y[0] ):
				yVal = y[1] + (j+0.5)*(y[2]-y[1]) / y[0]
				paramPoints.append( (xVal,yVal) )

		p = Pool()
		progress = ProgressBar(maxval=len(paramPoints))
		progress.start()
		for i,values in enumerate(p.imap_unordered(_fill, [(x,y,inputs,options) for x,y in paramPoints], len(paramPoints)/100)):
			# print( 'progress: %0.1f%%' % (100.0*i/(len(paramPoints))) )
			progress.update(i)

			x,y,value,nps = values
			bin = h.FindBin( x,y )
			h.SetBinContent( bin,value )

			# fill nuisance parameter histograms
			if npHistograms != None:
				for npName,npValue in nps.iteritems():
					if npName not in npHistograms.keys():
						npHistograms[npName] = h.Clone( "nuisParValue_"+npName )
						npHistograms[npName].SetTitle( 'value of '+npName )
						npHistograms[npName].GetZaxis().SetTitle( 'nuisance parameter value' )
					npHistograms[npName].SetBinContent( bin, npValue )

		progress.finish()

