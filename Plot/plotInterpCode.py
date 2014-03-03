#!/usr/bin/env python

#  Created on: August 2, 2013

__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"


import optparse
parser = optparse.OptionParser(version=__version__)
parser.add_option("-c", "--interpcode", dest="interpcode", default=4, type="int", help="InterpCode to be investigated.")

parser.add_option("-o", "--output", dest="output", default="output/interpCode.eps", help="Output root file.")

parser.add_option("-q", "--quiet", dest="verbose", action="store_false", default=True, help="Quiet output.")
options,args = parser.parse_args()



import ROOT
from array import array
import math

import PyROOTUtils
PyROOTUtils.style()

container = []



def secondDerivative(data):
	secondDerivative = []
	for i in range(1,len(data)-1):
		val = (data[i+1][1] - 2*data[i][1] + data[i-1][1])/(abs(data[i+1][0]-data[i][0])*abs(data[i][0]-data[i-1][0]))
		secondDerivative.append( (data[i][0], val) )
	return secondDerivative



def dataFlexibleInterpVar(eps=0.01,nominal=1.0):
	w = ROOT.RooWorkspace( "test" )
	w.factory("alpha[-10,10]")
	w.defineSet("nuis", "alpha")

	pL = ROOT.RooArgList( w.set("nuis") )



	values = []
	for eta in [0.8,1.0,1.2,1.4]:
		down = ROOT.std.vector("double")()
		up = ROOT.std.vector("double")()
		down.push_back( nominal-eta )
		up.push_back( nominal+eta )
		flex = ROOT.RooStats.HistFactory.FlexibleInterpVar("flex","flex",pL,nominal,down,up)
		flex.setAllInterpCodes(options.interpcode)

		# w.var("alpha").setVal(0.0)
		# print( "========== Flex with eta="+str(eta)+" and interpcode="+str(options.interpcode)+" at zero: "+str( flex.getVal() ))

		thisEtaValues = []
		for i in range(1000):
			alpha = -1.2 + 2.4*i/999.0
			w.var("alpha").setVal(alpha)
			thisEtaValues.append( (alpha*eta,flex.getVal()) )
		if eta == 1.2:
			print( thisEtaValues )

		w.var("alpha").setVal( eps )
		flexPlus = flex.getVal()
		w.var("alpha").setVal( -eps )
		flexMinus = flex.getVal()
		slopeAtZero = (flexPlus-flexMinus)/(2.*eta*eps)
		values.append( {"eta":eta,"data":thisEtaValues,"slopeAtZero":slopeAtZero} )

	return values





def dataPiecewiseInterpolation(eps=0.01,nominal=1.0, python2ndDer=False):
	w = ROOT.RooWorkspace( "test" )
	w.factory("nominal["+str(nominal)+",-10,10]")
	# w.defineSet("nomS", "nominal")
	w.factory("low[-10,10]")
	w.defineSet("lowS", "low")
	w.factory("high[-10,10]")
	w.defineSet("highS", "high")

	w.factory("alpha[-10,10]")
	w.defineSet("nuis", "alpha")
	pL = ROOT.RooArgList( w.set("nuis") )


	# nomL = ROOT.RooArgList( w.set("nomS") )
	lowL = ROOT.RooArgList( w.set("lowS") )
	highL = ROOT.RooArgList( w.set("highS") )

	values = []
	for eta in [0.2,0.4,0.6,0.8,1.0,1.2]:
		w.var("low").setVal(nominal-eta)
		w.var("high").setVal(nominal+2*eta)

		pi = ROOT.PiecewiseInterpolation("pi","pi",w.var('nominal'),lowL,highL,pL)
		pi.setAllInterpCodes(options.interpcode)

		thisEtaValues = []
		for i in range(1000):
			alpha = -1.2 + 2.4*i/999.0
			w.var("alpha").setVal(alpha)
			thisEtaValues.append( (alpha*eta,pi.getVal()) )

		w.var("alpha").setVal( eps )
		piPlus = pi.getVal()
		w.var("alpha").setVal( -eps )
		piMinus = pi.getVal()
		slopeAtZero = (piPlus-piMinus)/(2.*eta*eps)

		result = {"eta":eta,"data":thisEtaValues,"slopeAtZero":slopeAtZero}
		if python2ndDer:
			result['secondDerivative'] = secondDerivative(thisEtaValues)
		values.append( result )

	return values






def interpCode4( low, high, x ):
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


def dataFlexibleInterpVarPython(nominal=1.0):
	values = []
	for eta in [0.2,0.4,0.6,0.8,1.0,1.2]:
		low = nominal-eta
		high = nominal+eta
		data = []
		for i in range(1000):
			a = -1.2 + 2.4*i/999.0

			val = interpCode4( low, high, a )
			data.append( (eta*a,val) )

		values.append( {'eta':eta,'data':data,'secondDerivative':secondDerivative(data)} )

	return values









def dataPiecewiseInterpolationPython(nominal=1.0):
	values = []
	for eta in [0.2,0.4,0.6,0.8,1.0,1.2]:
		low = nominal-eta
		high = nominal+2*eta
		data = []
		for i in range(1000):
			a = -1.2 + 2.4*i/999.0

			val = None
			if a < -1: val = nominal + a*(nominal-low)
			elif a > 1: val = nominal + a*(high-nominal)
			else:
				S = (high-low)/2
				A = (high - 2*nominal +low)/16
				val = nominal + S*a + A*(15*a*a - 10*a*a*a*a + 3*a*a*a*a*a*a)
				#val = nominal + a*(S + A*a*(15 + a*a*(-10 + a*a*3))) #Horner scheme

			data.append( (eta*a,val) )

		values.append( {'eta':eta,'data':data,'secondDerivative':secondDerivative(data)} )

	return values




def plot( values,suffix=None ):
	canvas = ROOT.TCanvas( "canvas","canvas",800,600 )
	axes = canvas.DrawFrame( -1.55,-0.6,1.15,2.6 )
	axes.GetXaxis().SetTitle( "#eta#alpha" )
	axes.GetYaxis().SetTitle( "response" )
	axes.GetYaxis().SetTitleOffset( 1.2 )

	PyROOTUtils.DrawText( 0.2, 0.87, "InterpCode = "+str(options.interpcode), textSize=0.03 )
	leg = PyROOTUtils.Legend( 0.2, 0.83, textSize=0.03 )

	for etaData in values:
		eta = etaData['eta']
		data = etaData['data']

		g = PyROOTUtils.Graph( data )
		container.append(g)

		gDerivative = PyROOTUtils.Graph( g.derivativeData(), lineStyle=ROOT.kDashed )
		container.append(gDerivative)

		gDerivative2 = PyROOTUtils.Graph( g.derivative2Data(), lineStyle=ROOT.kDotted )
		if 'secondDerivative' in etaData: 
			gDerivative2 = PyROOTUtils.Graph( etaData['secondDerivative'], lineStyle=ROOT.kDotted )
		gDerivative2.transformY( lambda y: y/10.0 )
		container.append(gDerivative2)

		infoStr = "#eta = "+str(eta)+"  "
		if 'slopeAtZero' in etaData: infoStr += "\nslope(0) = %.2f  " % (etaData['slopeAtZero'])
		t = PyROOTUtils.DrawText( data[0][0],data[0][1], infoStr, textSize=0.025, halign="right", valign="center", NDC=False )
		container.append(t)

		g.Draw("L")
		gDerivative.Draw("L")
		gDerivative2.Draw("L")

	leg.AddEntry(g,           "f(#eta#alpha)",  "L")
	leg.AddEntry(gDerivative, "f'(#eta#alpha)", "L")
	leg.AddEntry(gDerivative2, "1/10 f''(#eta#alpha)", "L")
	leg.Draw()

	outFileName = options.output
	if suffix: outFileName = outFileName.replace(".eps",suffix+".eps")
	canvas.SaveAs( outFileName )




def main():
	plot( dataFlexibleInterpVar(nominal=1.0),      suffix='_flexibleInterpVar' )
	plot( dataFlexibleInterpVarPython(nominal=1.0), suffix='_flexibleInterpVarPythonTest' )

	plot( dataPiecewiseInterpolation(nominal=1.0), suffix='_piecewiseInterpolation' )
	plot( dataPiecewiseInterpolationPython(nominal=1.0), suffix='_piecewiseInterpolationPythonTest' )
	plot( dataPiecewiseInterpolation(nominal=1.0,python2ndDer=True), suffix='_noTG1For2ndDerTest' )


if __name__ == "__main__":
	main()
