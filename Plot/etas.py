#!/usr/bin/env python

#  Created on: December 16, 2013

__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"

__description__ = """
Requires Decouple package in Pythonpath.
"""

if __name__ == "__main__":
	import optparse
	parser = optparse.OptionParser(version=__version__)
	parser.add_option("-i", "--input", dest="input", default=None, help="Input pickle file.")
	parser.add_option("-o", "--output", dest="output", default="output/etas/", help="output directory.")
	options,args = parser.parse_args()


import ROOT
if __name__ == "__main__": ROOT.gROOT.SetBatch( True )
import PyROOTUtils
PyROOTUtils.style()
import os

import pickle
import Decouple.src.effectiveModel
import math
from parameterNames import parameterNames

container = []



def drawArrows( etas, muIn={'muT':1.0,'muW':1.0}, npVal=1.0, lineWidth=3.0, cut=0.03, template=10, flipSign=True ):

	m = Decouple.src.effectiveModel.EffectiveParametrization()
	m.extractNuisanceParametersFromEtas(etas)
	m.template = template

	arrows = []
	color = 1
	for p in m.nuisanceParameters.keys():
		# color: always increase color no matter whether this will be skipped to keep it "in sync"
		# and skip the color blacklist
		color += 1
		while color in [5,10]: color += 1

		if type(npVal) == float:
			thisNpVal = npVal
		else:
			thisNpVal = npVal[p]

		if flipSign: m.nuisanceParameters[p] = -thisNpVal
		else:        m.nuisanceParameters[p] = thisNpVal
		muOut = m.responseFunction(muIn,etas)
		m.nuisanceParameters[p] = 0.0

		length = math.sqrt(
			(muOut['muT']-muIn['muT'])*(muOut['muT']-muIn['muT']) +
			(muOut['muW']-muIn['muW'])*(muOut['muW']-muIn['muW'])
		)
		if length < cut: continue

		a = ROOT.TArrow( muIn['muT'],muIn['muW'], muOut['muT'],muOut['muW'], 0.01*lineWidth, "|>" )
		a.SetLineColor(color)
		a.SetFillColor(color)
		a.SetLineWidth(int(lineWidth))
		a.Draw()
		arrows.append( (a,p) )

	return arrows


def drawAllArrows( allEtas, cut=0.03, detailed=False ):
	for etasName,etas in allEtas.iteritems():
		canvas = ROOT.TCanvas( "c1","c1", 600, 600 )

		if detailed: axes = canvas.DrawFrame( 0.48,0.48,1.62,1.82 )
		else:        axes = canvas.DrawFrame( 0.58,0.58,1.42,1.42 )
		axes.GetXaxis().SetTitle( "#mu^{f}_{ggF+ttH}" )
		axes.GetYaxis().SetTitle( "#mu^{f}_{VBF+VH}" )
		#axes.GetYaxis().SetTitleOffset( 1.2 )

		template = 0
		if 'generic' in etasName: template = 10
		if 'generic10' in etasName: template = 10
		if 'generic14' in etasName: template = 14
		if 'generic20' in etasName: template = 20
		if 'generic24' in etasName: template = 24
		print( "For "+etasName+" chose template "+str(template)+"." )

		scanPoints = [{'muT':1.0, 'muW':1.0}]
		npVals = [(1.0,3.0)] # nuis par values and line widths
		if detailed:
			scanPoints = [{'muT':1.0, 'muW':1.0},{'muT':1.3, 'muW':1.0},{'muT':1.0, 'muW':1.3}]
			npVals = [(-1.0,1.5),(1.0,2.5)]
		for muIn in scanPoints:
			for npVal,lineWidth in npVals:
				arrows = drawArrows( etas, muIn, npVal, lineWidth, cut, template=template )
				container.append(arrows)
		
		leg = PyROOTUtils.Legend( 0.2,0.85, textSize=0.035 )
		for a,p in arrows:
			leg.AddEntry( a, parameterNames[p.replace("alpha_","")], "L" )
		leg.Draw()

		if cut > 0.0:
			PyROOTUtils.DrawText( 0.2,0.88, "showing only |#eta| > %.0f%%" % (cut*100.0), textSize=0.035 )
		if detailed:
			PyROOTUtils.DrawText( 0.2, 0.25, "positive variation thick\nnegative variation thin", textSize=0.035 )

		if detailed: canvas.SaveAs( options.output+etasName+"_detailed.eps" )
		else: canvas.SaveAs( options.output+etasName+".eps" )


def convertEtasDictToTex( etasDict, selectChannel=None ):
	""" expects a dict where top level is the channel and then under it are the two 
	axes muT and muW """

	byParameters = {}
	columns = []
	for channel,parameters in etasDict.iteritems():
		if selectChannel and channel not in selectChannel: continue

		for p,axes in parameters.iteritems():
			for axis,eta in axes.iteritems():
				if p not in byParameters.keys(): byParameters[p] = {}
				if channel+"_"+axis not in columns: columns.append( channel+"_"+axis )
				byParameters[p][channel+"_"+axis] = eta

	columns=sorted(columns)

	# store header
	header = "parameter & " + (" \t& ".join( ["$\eta_{\\textrm{"+c+"}}$" for c in columns] )) + "\n"

	# row
	out = ""
	for p,values in sorted(byParameters.iteritems()):
		formattedP = p.replace("_", " ")
		formattedP = formattedP.replace("alpha ","")
		out += formattedP+" \t& "
		formattedValues = []
		for c in columns:
			if c in values.keys() and abs(values[c]) > 0.001:
				formattedValues.append( "$%+.2f\\%%$" % (values[c]*100.0) )
			else:
				formattedValues.append( "$-$" )
		out += " \t& ".join( formattedValues )
		out += " \\\\ \n"

	return "%%"+header+out


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
	os.system('mkdir -p '+options.output)

	with open(options.input, "rb") as f:
		allEtas = pickle.load( f )

	drawAllArrows( allEtas )
	drawAllArrows( allEtas, detailed=True )

	latexTable = convertEtasDictToTex( allEtas, selectChannel=["fisherInfo","covarianceMatrix","partialDerivatives"] )
	print( latexTable )
	with open( options.output+"table_etas.tex", "w" ) as f:
		f.write( str(latexTable) )

	pyTable = convertEtasDictToPy( allEtas )
	print( pyTable )
	with open( options.output+"table_etas.py", "w" ) as f:
		f.write( str(pyTable) )



if __name__ == "__main__":
	main()
