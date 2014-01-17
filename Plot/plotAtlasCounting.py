#!/usr/bin/env python

#  Created on: July 10, 2013

__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"


import optparse
parser = optparse.OptionParser(version=__version__)
parser.add_option("-q", "--quiet", dest="verbose", action="store_false", default=True, help="Quiet output.")
options,args = parser.parse_args()


import ROOT
ROOT.gROOT.SetBatch( True )
import glob, re, os
from array import array

import helperStyle
import PyROOTUtils

from parameterNames import parameterNames
from Decouple.src.plot_utils import getContours, getSmallestBinMarker, getInterpolatedMinimumMarker, drawContours, drawH, draw_muTmuW_frame, draw_kVkF_frame, draw_kGlukGamma_frame







SMMarker = ROOT.TMarker( 1.0, 1.0, 34 )
SMMarker.SetMarkerColor( ROOT.kBlack )
blackSolid = ROOT.TLine( 1.2,1.2,1.4,1.4 )
blackSolid.SetLineWidth( 2 )
blackSolidThin = ROOT.TLine( 1.2,1.2,1.4,1.4 )
blackSolidThin.SetLineWidth( 1 )
blackDashed = ROOT.TLine( 1.2,1.2,1.4,1.4 )
blackDashed.SetLineWidth( 2 )
blackDashed.SetLineStyle( ROOT.kDashed )
blackDashedThick = ROOT.TLine( 1.2,1.2,1.4,1.4 )
blackDashedThick.SetLineWidth( 3 )
blackDashedThick.SetLineStyle( ROOT.kDashed )
blackDotted = ROOT.TLine( 1.2,1.2,1.4,1.4 )
blackDotted.SetLineWidth( 2 )
blackDotted.SetLineStyle( ROOT.kDotted )
graySolid = ROOT.TLine( 1.2,1.2,1.4,1.4 )
graySolid.SetLineColor( ROOT.kGray )
graySolid.SetLineWidth( 2 )









container = []
openFiles = []



def countingMuTMuW( opts ):
	mainModelSuffix = ""
	profileSuffix = ""
	modelSuffix = ""
	if 'model' in opts  and  opts['model'] != ""  and  opts['model'] != "template4": 
		profileSuffix = "_"+opts['model']
	if 'model' in opts  and  'box' in opts['model']: 
		mainModelSuffix = "_box"
	if 'model' in opts  and  'wideGauss' in opts['model']: 
		mainModelSuffix = "_wideGauss"
	if 'interpCode0' in opts:
		modelSuffix = '_interpCode0'
	# if 'model' in opts  and  ('template0' in opts['model'] or 'template10' in opts['model']): 
	# if 'model' in opts  and  ('template0' in opts['model']): 
	# 	modelSuffix = "_interpCode0"

	c68_2ph = drawContours( "output/atlas_counting/2ph"+modelSuffix+mainModelSuffix+"/muTmuW.root", "profiledNLL", scale=2.0, color = ROOT.kRed-3, lineStyle=ROOT.kDashed, lineWidth=3, drawSmallestBinMarker=True )
	c68_4l = drawContours( "output/atlas_counting/4l"+modelSuffix+mainModelSuffix+"/muTmuW.root", "profiledNLL", scale=2.0, color = ROOT.kBlue, lineStyle=ROOT.kDashed, lineWidth=3, drawSmallestBinMarker=True )
	c68_lvlv = drawContours( "output/atlas_counting/lvlv"+modelSuffix+mainModelSuffix+"/muTmuW.root", "profiledNLL", scale=2.0, color = ROOT.kGreen-2, lineStyle=ROOT.kDashed, lineWidth=3, drawSmallestBinMarker=True )

	c68_2ph_f = drawContours( "output/atlas_counting/2ph"+modelSuffix+"/muTmuW_eff.root", "profiledNLL", scale=2.0, color = ROOT.kRed-3, lineStyle=ROOT.kDotted )
	c68_4l_f = drawContours( "output/atlas_counting/4l"+modelSuffix+"/muTmuW_eff.root", "profiledNLL", scale=2.0, color = ROOT.kBlue, lineStyle=ROOT.kDotted )
	c68_lvlv_f = drawContours( "output/atlas_counting/lvlv"+modelSuffix+"/muTmuW_eff.root", "profiledNLL", scale=2.0, color = ROOT.kGreen-2, lineStyle=ROOT.kDotted )

	# c68_2ph_s = drawContours( "output/atlas_counting/2ph"+modelSuffix+"/muTmuW_statOnly.root", "profiledNLL", scale=2.0, color = ROOT.kRed-3, lineStyle=ROOT.kDashed, lineWidth=4, drawSmallestBinMarker=True )
	# c68_4l_s = drawContours( "output/atlas_counting/4l"+modelSuffix+"/muTmuW_statOnly.root", "profiledNLL", scale=2.0, color = ROOT.kBlue, lineStyle=ROOT.kDashed, lineWidth=4 )
	# c68_lvlv_s = drawContours( "output/atlas_counting/lvlv"+modelSuffix+"/muTmuW_statOnly.root", "profiledNLL", scale=2.0, color = ROOT.kGreen-2, lineStyle=ROOT.kDashed, lineWidth=4 )

	if 'model' in opts:
		c68_2ph_p = drawContours( "output/atlas_counting/2ph"+modelSuffix+"/muTmuW_profiledContour"+profileSuffix+".root", "muTmuW", color = ROOT.kRed-4, lineStyle=ROOT.kSolid, drawSmallestBinMarker=True )
		c68_4l_p = drawContours( "output/atlas_counting/4l"+modelSuffix+"/muTmuW_profiledContour"+profileSuffix+".root", "muTmuW", color = ROOT.kAzure-4, lineStyle=ROOT.kSolid, drawSmallestBinMarker=True )
		c68_lvlv_p = drawContours( "output/atlas_counting/lvlv"+modelSuffix+"/muTmuW_profiledContour"+profileSuffix+".root", "muTmuW", color = ROOT.kGreen+1, lineStyle=ROOT.kSolid, drawSmallestBinMarker=True )

	leg = PyROOTUtils.Legend( 0.2, 0.20, textSize=0.025, valign="bottom" )
	leg.AddEntry( SMMarker, "Standard Model", "P" )
	leg.AddEntry( blackDashedThick, "68% CL full model", "L" )
	leg.AddEntry( blackDotted, "68% CL w/o theory uncert.", "L" )
	if 'model' in opts: leg.AddEntry( blackSolid, "68% CL recoupled", "L" )
	leg.Draw()
	
	leg2 = PyROOTUtils.Legend( 0.65, 0.90, textSize = 0.025 )
	l2ph = PyROOTUtils.DrawHLine(400.0, lineWidth=2, lineColor=ROOT.kRed-3)
	l4l = PyROOTUtils.DrawHLine(400.0, lineWidth=2, lineColor=ROOT.kBlue)
	llvlv = PyROOTUtils.DrawHLine(400.0, lineWidth=2, lineColor=ROOT.kGreen-2)
	container.append( (l2ph,l4l,llvlv) )
	if c68_2ph:  leg2.AddEntry( l2ph,  "H #rightarrow #gamma#gamma", "L" )
	if c68_4l:   leg2.AddEntry( l4l,   "H #rightarrow ZZ* #rightarrow 4l", "L" )
	if c68_lvlv: leg2.AddEntry( llvlv, "H #rightarrow WW* #rightarrow l#nul#nu", "L" )
	leg2.Draw()


import etas
import pickle
def countingMuTMuWShifted( opts ):
	modelSuffix = ''
	if 'interpCode0' in opts: modelSuffix = '_interpCode0'

	drawMarker = True
	if 'etaArrows' in opts: drawMarker = False
	c68_2ph_f = drawContours( "output/atlas_counting/2ph"+modelSuffix+"/muTmuW_eff_"+opts['model']+"_0.0.root", "muTmuW", color = ROOT.kRed-3, drawSmallestBinMarker=drawMarker )
	c68_4l_f = drawContours( "output/atlas_counting/4l"+modelSuffix+"/muTmuW_eff_"+opts['model']+"_0.0.root", "muTmuW", color = ROOT.kBlue, drawSmallestBinMarker=drawMarker )
	c68_lvlv_f = drawContours( "output/atlas_counting/lvlv"+modelSuffix+"/muTmuW_eff_"+opts['model']+"_0.0.root", "muTmuW", color = ROOT.kGreen-2, drawSmallestBinMarker=drawMarker )

	c68_2ph_s = drawContours( "output/atlas_counting/2ph"+modelSuffix+"/muTmuW_eff_"+opts['model']+"_1.0.root", "muTmuW", color = ROOT.kRed-3, lineStyle=ROOT.kDashed, drawSmallestBinMarker=drawMarker )
	c68_4l_s = drawContours( "output/atlas_counting/4l"+modelSuffix+"/muTmuW_eff_"+opts['model']+"_1.0.root", "muTmuW", color = ROOT.kBlue, lineStyle=ROOT.kDashed, drawSmallestBinMarker=drawMarker )
	c68_lvlv_s = drawContours( "output/atlas_counting/lvlv"+modelSuffix+"/muTmuW_eff_"+opts['model']+"_1.0.root", "muTmuW", color = ROOT.kGreen-2, lineStyle=ROOT.kDashed, drawSmallestBinMarker=drawMarker )

	if 'etaArrows' in opts:
		arrows = []
		for c in ['2ph','4l','lvlv']:
			try:
				with open("output/atlas_counting/"+c+modelSuffix+"/table_etas.pickle", "rb") as f:
					etasAll = pickle.load( f )
					muHat = {
						'muT':etasAll['generic20_learning'].values()[0]['muT__hat'],
						'muW':etasAll['generic20_learning'].values()[0]['muW__hat'],
					}
					arrows = etas.drawArrows( etasAll['fisherInfo'], muHat, lineWidth=1.0, template=0 )
					container.append(arrows)
			except IOError:
				print( "WARNING: Could not open:" )
				print( "output/atlas_counting/"+c+modelSuffix+"/table_etas.pickle" )
			except:
				print( "ERROR!!!!!!!!!!")
		leg = PyROOTUtils.Legend( 0.64,0.78, textSize=0.025 )
		for a,p in arrows: leg.AddEntry( a, parameterNames[p.replace("alpha_","")], "L" )
		leg.Draw()

	leg = PyROOTUtils.Legend( 0.2, 0.30, textSize=0.025 )
	leg.AddEntry( SMMarker, "Standard Model", "P" )
	leg.AddEntry( blackSolid, "68% CL with #alpha at nominal", "L" )
	leg.AddEntry( blackDashed, "68% CL with #alpha at +1 #sigma", "L" )
	leg.Draw()
	
	leg2 = PyROOTUtils.Legend( 0.64, 0.90, textSize = 0.025 )
	if c68_2ph_f:  leg2.AddEntry( c68_2ph_f[0],  "H #rightarrow #gamma#gamma", "L" )
	if c68_4l_f:   leg2.AddEntry( c68_4l_f[0],   "H #rightarrow ZZ* #rightarrow 4l", "L" )
	if c68_lvlv_f: leg2.AddEntry( c68_lvlv_f[0], "H #rightarrow WW* #rightarrow l#nul#nu", "L" )
	leg2.Draw()

def countingMuTMuWArrowsAtMuHat( opts ):
	modelSuffix = ''
	if 'interpCode0' in opts: modelSuffix = '_interpCode0'

	arrows = []
	for c in ['2ph','4l','lvlv']:
		try:
			with open("output/atlas_counting/"+c+modelSuffix+"/table_etas.pickle", "rb") as f:
				etasAll = pickle.load( f )
				muHat = {
					'muT':etasAll['generic20_learning'].values()[0]['muT__hat'],
					'muW':etasAll['generic20_learning'].values()[0]['muW__hat'],
				}
				arrows = etas.drawArrows( 'fisherInfo', etasAll['fisherInfo'], muHat, lineWidth=2.0 )
				container.append(arrows)
				label = PyROOTUtils.DrawText( muHat['muT'], muHat['muW'], {
					'2ph':'H#rightarrow#gamma#gamma  ',
					'4l':'H#rightarrowZZ*#rightarrow4l  ',
					'lvlv':'H#rightarrowWW*#rightarrowl#nul#nu  ',
				}[c], textSize=0.03, halign="right", valign="top", NDC=False )
				container.append(label)
		except IOError:
			print( "WARNING: Could not open:" )
			print( "output/atlas_counting/"+c+modelSuffix+"/table_etas.pickle" )
		except:
			print( "ERROR!!!!!!!!!!!!" )
			
	leg = PyROOTUtils.Legend( 0.2,0.9, textSize=0.03 )
	for a,p in arrows: leg.AddEntry( a, p.replace("alpha_",""), "L" )
	leg.Draw()



def draw_CouplingContour( 
		model, opts, 
		colorFull = ROOT.kBlue, colorRecoupled = ROOT.kRed, 
		lineStyleFull1s=ROOT.kSolid, lineStyleFull2s=ROOT.kDashed, 
		lineStyleRecoupled1s=ROOT.kSolid, lineStyleRecoupled2s=ROOT.kDashed,
		lineWidthFull1s=2, lineWidthFull2s=2, 
		lineWidthRecoupled1s=2, lineWidthRecoupled2s=2,
		couplingType = 'kVkF',
	):
	combination = "2ph_4l_lvlv"
	drawMarkers = True
	recoupledLabel = 'recoupled'
	recoupledLabel2 = None
	mainModelSuffix = ""
	profileSuffix = ""
	if 'interpCode0' in opts: combination += "_interpCode0"
	if model != "": profileSuffix = "_"+model
	if 'box' in model: 
		mainModelSuffix += "_box"
		drawMarkers = False
		recoupledLabel = 'recoupled (Rfit)'
	if 'wideGauss' in model: 
		mainModelSuffix += "_wideGauss"
		recoupledLabel = 'recoupled'
		recoupledLabel2 = '(x1.3 uncertainty)'

	c68 = drawContours( "output/atlas_counting/"+combination+mainModelSuffix+"/"+couplingType+".root", couplingType, color = colorFull, lineStyle=lineStyleFull1s, lineWidth=lineWidthFull1s, drawSmallestBinMarker=drawMarkers )
	c95 = drawContours( "output/atlas_counting/"+combination+mainModelSuffix+"/"+couplingType+".root", couplingType, color = colorFull, lineStyle=lineStyleFull2s, lineWidth=lineWidthFull2s, level=6.0, levelName="95" )

	c68_p = drawContours( "output/atlas_counting/"+combination+"/"+couplingType+"_profiledContour"+profileSuffix+".root", couplingType, color = colorRecoupled, lineStyle=lineStyleRecoupled1s, lineWidth=lineWidthRecoupled1s, drawSmallestBinMarker=drawMarkers )
	c95_p = drawContours( "output/atlas_counting/"+combination+"/"+couplingType+"_profiledContour"+profileSuffix+".root", couplingType, color = colorRecoupled, lineStyle=lineStyleRecoupled2s, lineWidth=lineWidthRecoupled2s, level=6.0, levelName="95" )

	if 'box' not in model and 'wideGauss' not in model and 'skipNaive' not in opts:
		c68_n = drawContours( "output/atlas_counting/"+combination+"/"+couplingType+"_profiledContour_template20_etasNone.root", couplingType, color = ROOT.kGreen-2, drawSmallestBinMarker=drawMarkers )
		c95_n = drawContours( "output/atlas_counting/"+combination+"/"+couplingType+"_profiledContour_template20_etasNone.root", couplingType, color = ROOT.kGreen-2, lineStyle=ROOT.kDashed, level=6.0, levelName="95" )
	else:
		c68_n,c95_n = (None,None)

	return (c68,c68_p,c68_n,recoupledLabel,recoupledLabel2)


def counting_kVkF_overlay(opts):
	leg2 = PyROOTUtils.Legend( 0.67, 0.44, textSize=0.03, valign="bottom" )
	leg2.AddEntry( SMMarker, "Standard Model", "P" )
	color = [(ROOT.kAzure-4,ROOT.kAzure+2),(ROOT.kRed-4,ROOT.kRed+1)]
	lineStyle = [
		(ROOT.kSolid,ROOT.kSolid,ROOT.kDashed,ROOT.kDashed),
		(ROOT.kSolid,ROOT.kSolid,ROOT.kDashed,ROOT.kDashed),
	]
	lineWidth = [
		(2,1,2,1),
		(2,1,2,1),
	]
	ci = 0
	for m in opts['model']:
		c68,c68_p,c68_n,recoupledLabel,recoupledLabel2 = draw_CouplingContour(m,opts,
			color[ci][0],color[ci][1],
			lineStyleFull1s=lineStyle[ci][0],lineStyleFull2s=lineStyle[ci][1],
			lineStyleRecoupled1s=lineStyle[ci][2],lineStyleRecoupled2s=lineStyle[ci][3],
			lineWidthFull1s=lineWidth[ci][0],lineWidthFull2s=lineWidth[ci][1],
			lineWidthRecoupled1s=lineWidth[ci][2],lineWidthRecoupled2s=lineWidth[ci][3],
		)

		lL = PyROOTUtils.DrawHLine( 400, lineWidth=2, lineColor=color[ci][1] )
		container.append(lL)
		if 'wideGauss' in m: leg2.AddEntry( lL, 'uncertainties x1.3', "L" )
		else:                leg2.AddEntry( lL, 'nominal', "L" )

		ci += 1
	leg2.Draw()

	leg = PyROOTUtils.Legend( 0.67, 0.2, textSize=0.03, valign="bottom" )
	# leg.AddEntry( bestFitBlack, "Best fit", "P" )
	leg.AddEntry( blackSolid, "full", "L")
	leg.AddEntry( blackDashed, "recoupled", "L")
	leg.AddEntry( None, "", "" )
	leg.AddEntry( blackSolid, "68% CL", "L" )
	leg.AddEntry( blackSolidThin, "95% CL", "L" )
	leg.Draw()


def counting_kVkF( opts ):
	leg2 = PyROOTUtils.Legend( 0.67, 0.35, textSize=0.03, valign="bottom" )
	c68,c68_p,c68_n,recoupledLabel,recoupledLabel2 = draw_CouplingContour(opts['model'],opts)
	if c68:   leg2.AddEntry( c68[0], "full", "L" )
	if c68_n: leg2.AddEntry( c68_n[0], "naive", "L" )
	if c68_p: 
		leg2.AddEntry( c68_p[0], recoupledLabel, "L" )
		if recoupledLabel2: leg2.AddEntry( c68_p[0], recoupledLabel2, "" )
		leg2.AddEntry( None, "", "" )
	leg2.Draw()

	leg = PyROOTUtils.Legend( 0.67, 0.2, textSize=0.03, valign="bottom" )
	# leg.AddEntry( bestFitBlack, "Best fit", "P" )
	leg.AddEntry( SMMarker, "Standard Model", "P" )
	leg.AddEntry( blackSolid, "68% CL", "L" )
	leg.AddEntry( blackDashed, "95% CL", "L" )
	leg.Draw()







def counting_kGlukGamma_overlay(opts):
	leg2 = PyROOTUtils.Legend( 0.65, 0.90, textSize=0.03 )
	leg2.AddEntry( SMMarker, "Standard Model", "P" )
	color = [(ROOT.kAzure-4,ROOT.kAzure+2),(ROOT.kRed-4,ROOT.kRed+1)]
	lineStyle = [
		(ROOT.kSolid,ROOT.kSolid,ROOT.kDashed,ROOT.kDashed),
		(ROOT.kSolid,ROOT.kSolid,ROOT.kDashed,ROOT.kDashed),
	]
	lineWidth = [
		(2,1,2,1),
		(2,1,2,1),
	]
	ci = 0
	for m in opts['model']:
		c68,c68_p,c68_n,recoupledLabel,recoupledLabel2 = draw_CouplingContour(m,opts,
			color[ci][0],color[ci][1],
			lineStyleFull1s=lineStyle[ci][0],lineStyleFull2s=lineStyle[ci][1],
			lineStyleRecoupled1s=lineStyle[ci][2],lineStyleRecoupled2s=lineStyle[ci][3],
			lineWidthFull1s=lineWidth[ci][0],lineWidthFull2s=lineWidth[ci][1],
			lineWidthRecoupled1s=lineWidth[ci][2],lineWidthRecoupled2s=lineWidth[ci][3],
			couplingType='kGlukGamma',
		)

		lL = PyROOTUtils.DrawHLine( 400, lineWidth=2, lineColor=color[ci][1] )
		container.append(lL)
		if 'wideGauss' in m: leg2.AddEntry( lL, 'uncertainties x1.3', "L" )
		else:                leg2.AddEntry( lL, 'nominal', "L" )

		ci += 1
	leg2.Draw()

	leg = PyROOTUtils.Legend( 0.74, 0.75, textSize=0.03 )
	# leg.AddEntry( bestFitBlack, "Best fit", "P" )
	leg.AddEntry( blackSolid, "full", "L")
	leg.AddEntry( blackDashed, "recoupled", "L")
	leg.AddEntry( None, "", "" )
	leg.AddEntry( blackSolid, "68% CL", "L" )
	leg.AddEntry( blackSolidThin, "95% CL", "L" )
	leg.Draw()


def counting_kGlukGamma( opts ):
	leg2 = PyROOTUtils.Legend( 0.67, 0.77, textSize=0.03 )
	c68,c68_p,c68_n,recoupledLabel,recoupledLabel2 = draw_CouplingContour(opts['model'],opts,couplingType='kGlukGamma')
	if c68:   leg2.AddEntry( c68[0], "full", "L" )
	if c68_n: leg2.AddEntry( c68_n[0], "naive", "L" )
	if c68_p: 
		leg2.AddEntry( c68_p[0], recoupledLabel, "L" )
		if recoupledLabel2: leg2.AddEntry( c68_p[0], recoupledLabel2, "" )
		leg2.AddEntry( None, "", "" )
	leg2.Draw()

	leg = PyROOTUtils.Legend( 0.67, 0.90, textSize=0.03 )
	# leg.AddEntry( bestFitBlack, "Best fit", "P" )
	leg.AddEntry( SMMarker, "Standard Model", "P" )
	leg.AddEntry( blackSolid, "68% CL", "L" )
	leg.AddEntry( blackDashed, "95% CL", "L" )
	leg.Draw()














def main():

	# draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/muTmuW.eps", r=[-0.1,-2.2,3.0,6.5] )
	draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/interpCode0_muTmuW.eps", opts={'interpCode0':True}, r=[-0.1,-2.2,3.0,6.5] )
	# draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/muTmuW_template4_etasfisherInfo.eps",         opts={'model':"template4"},         r=[-0.1,-2.2,3.0,6.5] )
	# draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/muTmuW_template0_etasfisherInfo.eps",         opts={'model':"template0"},         r=[-0.1,-2.2,3.0,6.5] )

	# draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/muTmuW_template14_etasgeneric_M4.eps",        opts={'model':"template14_etasgeneric_M4"},        r=[-0.1,-2.2,3.0,6.5] )
	# draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/muTmuW_template14_etasgeneric_M4_box1.0.eps", opts={'model':"template14_etasgeneric_M4_box1.0"}, r=[-0.1,-2.2,3.0,6.5] )
	# draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/muTmuW_template14_etasgeneric_M5.eps",        opts={'model':"template14_etasgeneric_M5"},        r=[-0.1,-2.2,3.0,6.5] )
	# draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/muTmuW_template14_etasgeneric_M5_box1.0.eps", opts={'model':"template14_etasgeneric_M5_box1.0"}, r=[-0.1,-2.2,3.0,6.5] )
	# draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/muTmuW_template10_etasgeneric_M5.eps",        opts={'model':"template10_etasgeneric_M5"},        r=[-0.1,-2.2,3.0,6.5] )
	# draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/muTmuW_template10_etasgeneric_M5_box1.0.eps", opts={'model':"template10_etasgeneric_M5_box1.0"}, r=[-0.1,-2.2,3.0,6.5] )

	# draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/muTmuW_template10_etasgeneric10_learning.eps",        opts={'model':"template10_etasgeneric10_learning"},        r=[-0.1,-2.2,3.0,6.5] )
	# draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/muTmuW_template10_etasgeneric10_learning_box1.0.eps", opts={'model':"template10_etasgeneric10_learning_box1.0"}, r=[-0.1,-2.2,3.0,6.5] )
	# draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/muTmuW_template14_etasgeneric14_learning.eps",        opts={'model':"template14_etasgeneric14_learning"},        r=[-0.1,-2.2,3.0,6.5] )
	# draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/muTmuW_template14_etasgeneric14_learning_box1.0.eps", opts={'model':"template14_etasgeneric14_learning_box1.0"}, r=[-0.1,-2.2,3.0,6.5] )
	# draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/muTmuW_template20_etasgeneric20_learning.eps",        opts={'model':"template20_etasgeneric20_learning"},        r=[-0.1,-2.2,3.0,6.5] )
	# draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/muTmuW_template20_etasgeneric20_learning_box1.0.eps", opts={'model':"template20_etasgeneric20_learning_box1.0"}, r=[-0.1,-2.2,3.0,6.5] )
	# draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/muTmuW_template24_etasgeneric24_learning.eps",        opts={'model':"template24_etasgeneric24_learning"},        r=[-0.1,-2.2,3.0,6.5] )
	# draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/muTmuW_template24_etasgeneric24_learning_box1.0.eps", opts={'model':"template24_etasgeneric24_learning_box1.0"}, r=[-0.1,-2.2,3.0,6.5] )

	# draw_muTmuW_frame( countingMuTMuWShifted, "plots/atlas_counting/muTmuW_shifted.eps", opts={'model':"template0_fixed_setParameteralpha_QCDscale_Higgs_ggH"}, r=[-0.1,-2.2,3.0,6.5] )
	# draw_muTmuW_frame( countingMuTMuWShifted, "plots/atlas_counting/muTmuW_shifted_etaArrows.eps", opts={'etaArrows':True, 'model':"template0_fixed_setParameteralpha_QCDscale_Higgs_ggH"}, r=[-0.1,-2.2,3.0,6.5] )
	draw_muTmuW_frame( countingMuTMuWShifted, "plots/atlas_counting/interpCode0_muTmuW_shifted.eps", opts={'interpCode0':True, 'model':"template0_fixed_setParameteralpha_QCDscale_Higgs_ggH"}, r=[-0.1,-2.2,3.0,6.5] )
	draw_muTmuW_frame( countingMuTMuWShifted, "plots/atlas_counting/interpCode0_muTmuW_shifted_etaArrows.eps", opts={'etaArrows':True, 'interpCode0':True, 'model':"template0_fixed_setParameteralpha_QCDscale_Higgs_ggH"}, r=[-0.1,-2.2,3.0,6.5] )

	# draw_muTmuW_frame( countingMuTMuWArrowsAtMuHat, "plots/atlas_counting/muTmuW_etaArrows.eps",             opts={},                   r=[0.1,0.5,2.1,2.5] )
	draw_muTmuW_frame( countingMuTMuWArrowsAtMuHat, "plots/atlas_counting/interpCode0_muTmuW_etaArrows.eps", opts={'interpCode0':True}, r=[0.1,0.5,2.1,2.5] )

	draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/interpCode0_muTmuW_template0_etasfisherInfo.eps",                 opts={'interpCode0':True,'model':"template0"},                                r=[-0.1,-2.2,3.0,6.5] )
	draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/interpCode0_muTmuW_template10_etasgeneric_M5.eps",                opts={'interpCode0':True,'model':"template10_etasgeneric_M5"},                r=[-0.1,-2.2,3.0,6.5] )
	draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/interpCode0_muTmuW_template10_etasgeneric_M5_box1.0.eps",                opts={'interpCode0':True,'model':"template10_etasgeneric_M5_box1.0"},                r=[-0.1,-2.2,3.0,6.5] )
	draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/interpCode0_muTmuW_template10_etasgeneric_M5_wideGauss1.3.eps",                opts={'interpCode0':True,'model':"template10_etasgeneric_M5_wideGauss1.3"},                r=[-0.1,-2.2,3.0,6.5] )
	draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/interpCode0_muTmuW_template10_etasgeneric10_learning.eps",        opts={'interpCode0':True,'model':"template10_etasgeneric10_learning"},                r=[-0.1,-2.2,3.0,6.5] )
	draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/interpCode0_muTmuW_template10_etasgeneric10_learning_box1.0.eps",        opts={'interpCode0':True,'model':"template10_etasgeneric10_learning_box1.0"},        r=[-0.1,-2.2,3.0,6.5] )
	draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/interpCode0_muTmuW_template20_etasgeneric20_learning.eps",        opts={'interpCode0':True,'model':"template20_etasgeneric20_learning"},        r=[-0.1,-2.2,3.0,6.5] )
	draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/interpCode0_muTmuW_template20_etasgeneric20_learning_box1.0.eps", opts={'interpCode0':True,'model':"template20_etasgeneric20_learning_box1.0"}, r=[-0.1,-2.2,3.0,6.5] )
	draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/interpCode0_muTmuW_template10_etasgeneric10_learningFull.eps",        opts={'interpCode0':True,'model':"template10_etasgeneric10_learningFull"},                r=[-0.1,-2.2,3.0,6.5] )
	draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/interpCode0_muTmuW_template10_etasgeneric10_learningFull_box1.0.eps",        opts={'interpCode0':True,'model':"template10_etasgeneric10_learningFull_box1.0"},        r=[-0.1,-2.2,3.0,6.5] )
	draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/interpCode0_muTmuW_template10_etasgeneric10_learningFull_wideGauss1.3.eps",        opts={'interpCode0':True,'model':"template10_etasgeneric10_learningFull_wideGauss1.3"},        r=[-0.1,-2.2,3.0,6.5] )
	draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/interpCode0_muTmuW_template20_etasgeneric20_learningFull.eps",        opts={'interpCode0':True,'model':"template20_etasgeneric20_learningFull"},        r=[-0.1,-2.2,3.0,6.5] )
	draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/interpCode0_muTmuW_template20_etasgeneric20_learningFull_box1.0.eps", opts={'interpCode0':True,'model':"template20_etasgeneric20_learningFull_box1.0"}, r=[-0.1,-2.2,3.0,6.5] )
	draw_muTmuW_frame( countingMuTMuW, "plots/atlas_counting/interpCode0_muTmuW_template20_etasgeneric20_learningFull_wideGauss1.3.eps", opts={'interpCode0':True,'model':"template20_etasgeneric20_learningFull_wideGauss1.3"}, r=[-0.1,-2.2,3.0,6.5] )


	# draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/kVkF_combined.eps",                                                            r=[0.65,-1.7,1.5,2.0] )
	# draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/kVkF_combined_template14_etasgeneric_M4.eps",        opts={'model':'template14_etasgeneric_M4'},         r=[0.65,-1.7,1.5,2.0] )
	# draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/kVkF_combined_template14_etasgeneric_M4_box1.0.eps", opts={'model':'template14_etasgeneric_M4_box1.0'},  r=[0.65,-1.7,1.5,2.0] )
	# draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/kVkF_combined_template14_etasgeneric_M5.eps",        opts={'model':'template14_etasgeneric_M5'},         r=[0.65,-1.7,1.5,2.0] )
	# draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/kVkF_combined_template14_etasgeneric_M5_box1.0.eps", opts={'model':'template14_etasgeneric_M5_box1.0'},  r=[0.65,-1.7,1.5,2.0] )
	# draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/kVkF_combined_template10_etasgeneric_M5.eps",        opts={'model':'template10_etasgeneric_M5'},         r=[0.65,-1.7,1.5,2.0] )
	# draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/kVkF_combined_template10_etasgeneric_M5_box1.0.eps", opts={'model':'template10_etasgeneric_M5_box1.0'},  r=[0.65,-1.7,1.5,2.0] )
	draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/kVkF_combined_template20_etasgeneric20_learning.eps",        opts={'model':'template20_etasgeneric20_learning'},         r=[0.65,-1.7,1.5,2.0] )
	draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/kVkF_combined_template20_etasgeneric20_learning_box1.0.eps", opts={'model':'template20_etasgeneric20_learning_box1.0'},  r=[0.65,-1.7,1.5,2.0] )
	draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/interpCode0_kVkF_combined_template10_etasgeneric10_learning.eps",        opts={'interpCode0':True,'model':'template10_etasgeneric10_learning'},         r=[0.65,-1.7,1.5,2.0] )
	draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/interpCode0_kVkF_combined_template10_etasgeneric10_learning_box1.0.eps", opts={'interpCode0':True,'model':'template10_etasgeneric10_learning_box1.0'},  r=[0.65,-1.7,1.5,2.0] )
	draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/interpCode0_kVkF_combined_template20_etasgeneric20_learning.eps",        opts={'interpCode0':True,'model':'template20_etasgeneric20_learning'},         r=[0.65,-1.7,1.5,2.0] )
	draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/interpCode0_kVkF_combined_template20_etasgeneric20_learning_box1.0.eps", opts={'interpCode0':True,'model':'template20_etasgeneric20_learning_box1.0'},  r=[0.65,-1.7,1.5,2.0] )
	draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/interpCode0_kVkF_combined_template10_etasgeneric10_learningFull.eps",        opts={'interpCode0':True,'model':'template10_etasgeneric10_learningFull'},         r=[0.65,-1.7,1.5,2.0] )
	draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/interpCode0_kVkF_combined_template10_etasgeneric10_learningFull_box1.0.eps", opts={'interpCode0':True,'model':'template10_etasgeneric10_learningFull_box1.0'},  r=[0.65,-1.7,1.5,2.0] )
	draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/interpCode0_kVkF_combined_template10_etasgeneric10_learningFull_wideGauss1.3.eps", opts={'interpCode0':True,'model':'template10_etasgeneric10_learningFull_wideGauss1.3'},  r=[0.65,-1.7,1.5,2.0] )
	draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/interpCode0_kVkF_combined_template20_etasgeneric20_learningFull.eps",        opts={'interpCode0':True,'model':'template20_etasgeneric20_learningFull'},         r=[0.65,-1.7,1.5,2.0] )
	draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/interpCode0_kVkF_combined_template20_etasgeneric20_learningFull_box1.0.eps", opts={'interpCode0':True,'model':'template20_etasgeneric20_learningFull_box1.0'},  r=[0.65,-1.7,1.5,2.0] )
	draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/interpCode0_kVkF_combined_template20_etasgeneric20_learningFull_wideGauss1.3.eps", opts={'interpCode0':True,'model':'template20_etasgeneric20_learningFull_wideGauss1.3'},  r=[0.65,-1.7,1.5,2.0] )
	draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/interpCode0_kVkF_combined_template10_etasgeneric_M5.eps",        opts={'interpCode0':True,'model':'template10_etasgeneric_M5'},         r=[0.65,-1.7,1.5,2.0] )
	draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/interpCode0_kVkF_combined_template10_etasgeneric_M5_box1.0.eps", opts={'interpCode0':True,'model':'template10_etasgeneric_M5_box1.0'},  r=[0.65,-1.7,1.5,2.0] )
	draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/interpCode0_kVkF_combined_template10_etasgeneric_M5_wideGauss1.3.eps", opts={'interpCode0':True,'model':'template10_etasgeneric_M5_wideGauss1.3'},  r=[0.65,-1.7,1.5,2.0] )
	# draw_kVkF_frame( counting_kVkF, "plots/atlas_counting/interpCode0_kVkF_combined_naive.eps",        opts={'interpCode0':True,'model':'template20_etasNone'},         r=[0.65,-1.7,1.5,2.0] )
	draw_kVkF_frame( counting_kVkF_overlay, "plots/atlas_counting/interpCode0_kVkF_combined_template10_etasgeneric10_learningFull_overlay.eps", opts={'interpCode0':True,'skipNaive':True,'model':['template10_etasgeneric10_learningFull','template10_etasgeneric10_learningFull_wideGauss1.3']},  r=[0.65,-1.7,1.5,2.0] )

	# draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/kGlukGamma_combined.eps",                                                            r=[0.8,0.6,1.9,1.6] )
	# draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/kGlukGamma_combined_template14_etasgeneric_M4.eps",        opts={'model':'template14_etasgeneric_M4'},         r=[0.8,0.6,1.9,1.6] )
	# draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/kGlukGamma_combined_template14_etasgeneric_M4_box1.0.eps", opts={'model':'template14_etasgeneric_M4_box1.0'},  r=[0.8,0.6,1.9,1.6] )
	# draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/kGlukGamma_combined_template14_etasgeneric_M5.eps",        opts={'model':'template14_etasgeneric_M5'},         r=[0.8,0.6,1.9,1.6] )
	# draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/kGlukGamma_combined_template14_etasgeneric_M5_box1.0.eps", opts={'model':'template14_etasgeneric_M5_box1.0'},  r=[0.8,0.6,1.9,1.6] )
	# draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/kGlukGamma_combined_template10_etasgeneric_M5.eps",        opts={'model':'template10_etasgeneric_M5'},         r=[0.8,0.6,1.9,1.6] )
	# draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/kGlukGamma_combined_template10_etasgeneric_M5_box1.0.eps", opts={'model':'template10_etasgeneric_M5_box1.0'},  r=[0.8,0.6,1.9,1.6] )
	draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/kGlukGamma_combined_template20_etasgeneric20_learning.eps",        opts={'model':'template20_etasgeneric20_learning'},         r=[0.8,0.6,1.9,1.6] )
	draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/kGlukGamma_combined_template20_etasgeneric20_learning_box1.0.eps", opts={'model':'template20_etasgeneric20_learning_box1.0'},  r=[0.8,0.6,1.9,1.6] )
	draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/interpCode0_kGlukGamma_combined_template10_etasgeneric10_learning.eps",        opts={'interpCode0':True,'model':'template10_etasgeneric10_learning'},         r=[0.8,0.6,1.9,1.6] )
	draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/interpCode0_kGlukGamma_combined_template10_etasgeneric10_learning_box1.0.eps", opts={'interpCode0':True,'model':'template10_etasgeneric10_learning_box1.0'},  r=[0.8,0.6,1.9,1.6] )
	draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/interpCode0_kGlukGamma_combined_template20_etasgeneric20_learning.eps",        opts={'interpCode0':True,'model':'template20_etasgeneric20_learning'},         r=[0.8,0.6,1.9,1.6] )
	draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/interpCode0_kGlukGamma_combined_template20_etasgeneric20_learning_box1.0.eps", opts={'interpCode0':True,'model':'template20_etasgeneric20_learning_box1.0'},  r=[0.8,0.6,1.9,1.6] )
	draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/interpCode0_kGlukGamma_combined_template10_etasgeneric10_learningFull.eps",        opts={'interpCode0':True,'model':'template10_etasgeneric10_learningFull'},         r=[0.8,0.6,1.9,1.6] )
	draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/interpCode0_kGlukGamma_combined_template10_etasgeneric10_learningFull_box1.0.eps", opts={'interpCode0':True,'model':'template10_etasgeneric10_learningFull_box1.0'},  r=[0.8,0.6,1.9,1.6] )
	draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/interpCode0_kGlukGamma_combined_template10_etasgeneric10_learningFull_wideGauss1.3.eps", opts={'interpCode0':True,'model':'template10_etasgeneric10_learningFull_wideGauss1.3'},  r=[0.8,0.6,1.9,1.6] )
	draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/interpCode0_kGlukGamma_combined_template20_etasgeneric20_learningFull.eps",        opts={'interpCode0':True,'model':'template20_etasgeneric20_learningFull'},         r=[0.8,0.6,1.9,1.6] )
	draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/interpCode0_kGlukGamma_combined_template20_etasgeneric20_learningFull_box1.0.eps", opts={'interpCode0':True,'model':'template20_etasgeneric20_learningFull_box1.0'},  r=[0.8,0.6,1.9,1.6] )
	draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/interpCode0_kGlukGamma_combined_template20_etasgeneric20_learningFull_wideGauss1.3.eps", opts={'interpCode0':True,'model':'template20_etasgeneric20_learningFull_wideGauss1.3'},  r=[0.8,0.6,1.9,1.6] )
	draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/interpCode0_kGlukGamma_combined_template10_etasgeneric_M5.eps",        opts={'interpCode0':True,'model':'template10_etasgeneric_M5'},         r=[0.8,0.6,1.9,1.6] )
	draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/interpCode0_kGlukGamma_combined_template10_etasgeneric_M5_box1.0.eps", opts={'interpCode0':True,'model':'template10_etasgeneric_M5_box1.0'},  r=[0.8,0.6,1.9,1.6] )
	draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/interpCode0_kGlukGamma_combined_template10_etasgeneric_M5_wideGauss1.3.eps", opts={'interpCode0':True,'model':'template10_etasgeneric_M5_wideGauss1.3'},  r=[0.8,0.6,1.9,1.6] )
	# draw_kGlukGamma_frame( counting_kGlukGamma, "plots/atlas_counting/interpCode0_kGlukGamma_combined_naive.eps", opts={'interpCode0':True,'model':'template20_etasNone'},  r=[0.8,0.6,1.9,1.6] )
	draw_kGlukGamma_frame( counting_kGlukGamma_overlay, "plots/atlas_counting/interpCode0_kGlukGamma_combined_template10_etasgeneric10_learningFull_overlay.eps", opts={'interpCode0':True,'skipNaive':True,'model':['template10_etasgeneric10_learningFull','template10_etasgeneric10_learningFull_wideGauss1.3']},  r=[0.8,0.6,1.9,1.6] )


	fileList = "`\ls plots/twoBin/*.eps plots/atlas_counting/*.eps`"
	# print( "Merging eps files" )
	# os.system( "gs -q -dNOPAUSE -dBATCH -sEPSCrop -sDEVICE=pdfwrite -sOutputFile=plots/plots.pdf "+fileList )
	print( "Creating zip file" )
	os.system( "rm plots/plots.zip" )
	os.system( "zip -r plots/plots.zip "+fileList )



if __name__ == "__main__":
	main()
