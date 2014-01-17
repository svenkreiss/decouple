#!/usr/bin/env python

#  Created on: October 30, 2013

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

from Decouple.src.plot_utils import getContours, getSmallestBinMarker, getInterpolatedMinimumMarker, drawContours, drawH, draw_muTmuW_frame, draw_kVkF_frame, draw_kGlukGamma_frame






SMMarker = ROOT.TMarker( 1.0, 1.0, 34 )
SMMarker.SetMarkerColor( ROOT.kBlack )
blackSolid = ROOT.TLine( 1.2,1.2,1.4,1.4 )
blackSolid.SetLineWidth( 2 )
blackDashed = ROOT.TLine( 1.2,1.2,1.4,1.4 )
blackDashed.SetLineWidth( 2 )
blackDashed.SetLineStyle( ROOT.kDashed )









container = []
openFiles = []




def muTMuWOverviewNegScenarios(opts={}):
	cont = [
		("1x sys, cat. uni.", ROOT.kRed-3, "output/twoBin/oneAlpha_catUniversal/muTmuW.root"),
		("1x sys, not cat. uni.", ROOT.kGreen, "output/twoBin/oneAlpha_catNonUniversal/muTmuW.root"),
		("2x sys, cat. uni.", ROOT.kOrange, "output/twoBin/twoAlpha_catUniversal/muTmuW.root"),
		("2x sys, not cat. uni.", ROOT.kBlue, "output/twoBin/twoAlpha_catNonUniversal/muTmuW.root"),
	]

	leg2 = PyROOTUtils.Legend( 0.65, 0.90, textSize = 0.03 )
	for name,color,inFile in cont:
		c68 = drawContours( inFile, "profiledNLL", scale=2.0, color=color )
		c68_f = drawContours( inFile.replace(".root","_eff.root"), "profiledNLL", scale=2.0, color=color, lineStyle=ROOT.kDashed )
		container.append( (c68,c68_f) )

		leg2.AddEntry( c68[0], name, "L" )
	leg2.Draw()

	leg = PyROOTUtils.Legend( 0.2, 0.90, textSize=0.03 )
	leg.AddEntry( SMMarker, "Standard Model", "P" )
	leg.AddEntry( blackSolid, "68% CL full model", "L" )
	leg.AddEntry( blackDashed, "68% CL fixed effective", "L" )
	leg.Draw()
	
def muTMuWOverview(opts={}):
	cont = [
		("scenarioA", ROOT.kRed-3, "output/twoBin/scenarioA/muTmuW.root"),
		("scenarioB", ROOT.kGreen, "output/twoBin/scenarioB/muTmuW.root"),
		("scenarioC", ROOT.kBlue, "output/twoBin/scenarioC/muTmuW.root"),
	]

	leg2 = PyROOTUtils.Legend( 0.65, 0.90, textSize = 0.03 )
	for name,color,inFile in cont:
		c68 = drawContours( inFile, "profiledNLL", scale=2.0, color=color )
		c68_f = drawContours( inFile.replace(".root","_eff.root"), "profiledNLL", scale=2.0, color=color, lineStyle=ROOT.kDashed )
		container.append( (c68,c68_f) )

		if c68: leg2.AddEntry( c68[0], name, "L" )
	leg2.Draw()

	leg = PyROOTUtils.Legend( 0.2, 0.90, textSize=0.03 )
	leg.AddEntry( SMMarker, "Standard Model", "P" )
	leg.AddEntry( blackSolid, "68% CL full model", "L" )
	leg.AddEntry( blackDashed, "68% CL fixed effective", "L" )
	leg.Draw()

def muTMuWInterpCodes(opts={}):
	cont = [
		("InterpCode=0", ROOT.kRed-3, "output/twoBin/scenarioC/muTmuW_profiledContour_template0.root"),
		("InterpCode=4", ROOT.kGreen, "output/twoBin/scenarioC/muTmuW_profiledContour.root"),
		("InterpCode=-1", ROOT.kBlue, "output/twoBin/scenarioC/muTmuW_profiledContour_templateM1.root"),
		("InterpCode=-4", ROOT.kGray, "output/twoBin/scenarioC/muTmuW_profiledContour_template14_etasgeneric_M4.root"),
	]

	leg2 = PyROOTUtils.Legend( 0.65, 0.90, textSize = 0.03 )
	for name,color,inFile in cont:
		c68 = drawContours( inFile, "muTmuW", scale=2.0, color=color )
		container.append( c68 )

		if c68: leg2.AddEntry( c68[0], name, "L" )
	leg2.Draw()

	leg = PyROOTUtils.Legend( 0.2, 0.90, textSize=0.03 )
	leg.AddEntry( SMMarker, "Standard Model", "P" )
	leg.AddEntry( blackSolid, "68% CL full model", "L" )
	leg.AddEntry( blackDashed, "68% CL fixed effective", "L" )
	leg.Draw()
	

def profiledContour(opts={}):
	if opts["type"] == "oneAlpha_catUniversal":
		modelType = "oneAlpha_catUniversal"
		color = ROOT.kRed-3
	elif opts["type"] == "oneAlpha_catNonUniversal":
		modelType = "oneAlpha_catNonUniversal"
		color = ROOT.kGreen-2
	elif opts["type"] == "twoAlpha_catUniversal":
		modelType = "twoAlpha_catUniversal"
		color = ROOT.kOrange-3
	elif opts["type"] == "twoAlpha_catNonUniversal":
		modelType = "twoAlpha_catNonUniversal"
		color = ROOT.kBlue

	elif opts["type"] == "oneAlpha_catUniversal_interpCode0":
		modelType = "oneAlpha_catUniversal_interpCode0"
		color = ROOT.kRed-3
	elif opts["type"] == "oneAlpha_catNonUniversal_interpCode0":
		modelType = "oneAlpha_catNonUniversal_interpCode0"
		color = ROOT.kGreen-2
	elif opts["type"] == "twoAlpha_catUniversal_interpCode0":
		modelType = "twoAlpha_catUniversal_interpCode0"
		color = ROOT.kOrange-3
	elif opts["type"] == "twoAlpha_catNonUniversal_interpCode0":
		modelType = "twoAlpha_catNonUniversal_interpCode0"
		color = ROOT.kBlue


	elif opts["type"] == "scenarioA":
		modelType = "scenarioA"
		color = ROOT.kRed-3
	elif opts["type"] == "scenarioA2":
		modelType = "scenarioA2"
		color = ROOT.kRed-3
	elif opts["type"] == "scenarioB":
		modelType = "scenarioB"
		color = ROOT.kGreen-2
	elif opts["type"] == "scenarioC":
		modelType = "scenarioC"
		color = ROOT.kBlue
	elif opts["type"] == "scenarioC2":
		modelType = "scenarioC2"
		color = ROOT.kBlue
	elif opts["type"] == "scenarioD":
		modelType = "scenarioD"
		color = ROOT.kGreen

	elif opts["type"] == "scenarioA_interpCode0":
		modelType = "scenarioA_interpCode0"
		color = ROOT.kRed-3
	elif opts["type"] == "scenarioA2_interpCode0":
		modelType = "scenarioA2_interpCode0"
		color = ROOT.kRed-3
	elif opts["type"] == "scenarioB_interpCode0":
		modelType = "scenarioB_interpCode0"
		color = ROOT.kGreen-2
	elif opts["type"] == "scenarioC_interpCode0":
		modelType = "scenarioC_interpCode0"
		color = ROOT.kBlue
	elif opts["type"] == "scenarioC2_interpCode0":
		modelType = "scenarioC2_interpCode0"
		color = ROOT.kBlue
	elif opts["type"] == "scenarioD_interpCode0":
		modelType = "scenarioD_interpCode0"
		color = ROOT.kGreen


	effFile = "output/twoBin/"+modelType+"/muTmuW_eff.root"
	if "template0" in opts:
		inFile = "output/twoBin/"+modelType+"_interpCode0/muTmuW.root"
		profiledFile = "output/twoBin/"+modelType+"/muTmuW_profiledContour_template0.root"
	elif "templateM1" in opts:
		inFile = "output/twoBin/"+modelType+"_additiveMu_interpCode0/muTmuW.root"
		profiledFile = "output/twoBin/"+modelType+"/muTmuW_profiledContour_templateM1.root"
	elif "template14_etasgeneric_M4" in opts:
		inFile = "output/twoBin/"+modelType+"/muTmuW.root"
		profiledFile = "output/twoBin/"+modelType+"/muTmuW_profiledContour_template14_etasgeneric_M4.root"
	elif "template14_etasgeneric_M5" in opts:
		inFile = "output/twoBin/"+modelType+"/muTmuW.root"
		profiledFile = "output/twoBin/"+modelType+"/muTmuW_profiledContour_template14_etasgeneric_M5.root"
	elif "template14_etasgeneric_fisherInfo" in opts:
		inFile = "output/twoBin/"+modelType+"/muTmuW.root"
		profiledFile = "output/twoBin/"+modelType+"/muTmuW_profiledContour_template14_etasgeneric_fisherInfo.root"

	elif "template10_etasgeneric10_learning" in opts:
		inFile = "output/twoBin/"+modelType+"/muTmuW.root"
		profiledFile = "output/twoBin/"+modelType+"/muTmuW_profiledContour_template10_etasgeneric10_learning.root"
	elif "template14_etasgeneric14_learning" in opts:
		inFile = "output/twoBin/"+modelType+"/muTmuW.root"
		profiledFile = "output/twoBin/"+modelType+"/muTmuW_profiledContour_template14_etasgeneric14_learning.root"
	elif "template20_etasgeneric20_learning" in opts:
		inFile = "output/twoBin/"+modelType+"/muTmuW.root"
		profiledFile = "output/twoBin/"+modelType+"/muTmuW_profiledContour_template20_etasgeneric20_learning.root"
	elif "template24_etasgeneric24_learning" in opts:
		inFile = "output/twoBin/"+modelType+"/muTmuW.root"
		profiledFile = "output/twoBin/"+modelType+"/muTmuW_profiledContour_template24_etasgeneric24_learning.root"

	elif "template20_etasgeneric20_learning_box1.0" in opts:
		inFile = "output/twoBin/"+modelType+"_box/muTmuW.root"
		profiledFile = "output/twoBin/"+modelType+"/muTmuW_profiledContour_template20_etasgeneric20_learning_box1.0.root"

	else:
		inFile = "output/twoBin/"+modelType+"/muTmuW.root"
		profiledFile = "output/twoBin/"+modelType+"/muTmuW_profiledContour.root"

	c68 = drawContours( inFile, "profiledNLL", scale=2.0, color=color )
	c68_f = drawContours( effFile, "profiledNLL", scale=2.0, color=color, lineStyle=ROOT.kDashed )
	c68_p = drawContours( 
		profiledFile, 
		"muTmuW", color = ROOT.kGray+2, lineStyle=ROOT.kDotted
	)
	container.append( (c68,c68_f,c68_p) )

	PyROOTUtils.DrawText(0.66, 0.88, "68% CL contours", textSize=0.03)
	leg2 = PyROOTUtils.Legend( 0.65, 0.85, textSize = 0.03 )
	leg2.AddEntry( SMMarker, "Standard Model", "P" )
	if c68:   leg2.AddEntry( c68[0], "full model", "L" )
	if c68_f: leg2.AddEntry( c68_f[0], "fixed effective", "L" )
	if c68_p: leg2.AddEntry( c68_p[0], "profiled effective", "L" )
	leg2.Draw()

	# if "template0" in opts:
	# 	PyROOTUtils.DrawText(0.2,0.88,"template = 0",textSize=0.03)
	# elif "templateM1" in opts:
	# 	PyROOTUtils.DrawText(0.2,0.88,"template = -1",textSize=0.03)
	# elif "template14_etasgeneric_M4" in opts:
	# 	PyROOTUtils.DrawText(0.2,0.88,"template = 14 (etas from M4)",textSize=0.03)
	# elif "template14_etasgeneric_M5" in opts:
	# 	PyROOTUtils.DrawText(0.2,0.88,"template = 14 (etas from M5)",textSize=0.03)
	# elif "template14_etasgeneric_fisherInfo" in opts:
	# 	PyROOTUtils.DrawText(0.2,0.88,"template = 14 (etas from fisherInfo)",textSize=0.03)

	# elif "template10_etasgeneric10_learning" in opts:
	# 	PyROOTUtils.DrawText(0.2,0.88,"template = 10 (etas from learning)",textSize=0.03)
	# elif "template14_etasgeneric14_learning" in opts:
	# 	PyROOTUtils.DrawText(0.2,0.88,"template = 14 (etas from learning)",textSize=0.03)
	# elif "template20_etasgeneric20_learning" in opts:
	# 	PyROOTUtils.DrawText(0.2,0.88,"template = 20 (etas from learning)",textSize=0.03)
	# elif "template24_etasgeneric24_learning" in opts:
	# 	PyROOTUtils.DrawText(0.2,0.88,"template = 24 (etas from learning)",textSize=0.03)
	# else:
	# 	PyROOTUtils.DrawText(0.2,0.88,"template = 4",textSize=0.03)



def profiledContourOverlay(opts={}):
	if 'box' not in opts: fullFile = "output/twoBin/"+opts['type']+"/muTmuW.root"
	else:                 fullFile = "output/twoBin/"+opts['type']+"_box/muTmuW.root"
	effFile = "output/twoBin/"+opts['type']+"/muTmuW_eff.root"
	learningSuffix = ''
	if 'learningFull' in opts: learningSuffix = 'Full'

	profiledFiles = [
		('aligned', "output/twoBin/"+opts['type']+"/muTmuW_profiledContour_template0.root", ROOT.kRed, ROOT.kSolid),
		('learning', "output/twoBin/"+opts['type']+"/muTmuW_profiledContour_template20_etasgeneric20_learning"+learningSuffix+".root", ROOT.kBlue, 5),
	]
	if 'byHand' in opts:
		profiledFiles.insert(1, 
			('by hand', "output/twoBin/"+opts['type']+"/muTmuW_profiledContour_template10_etasgeneric_M5.root", ROOT.kGreen+2, ROOT.kDashed)
		)
	if 'box' in opts:
		profiledFiles = [(n,f.replace('.root','_box1.0.root'),c,s) for n,f,c,s in profiledFiles]


	PyROOTUtils.DrawText(0.22, 0.88, "Recoupled contours", textSize=0.03)
	leg2 = PyROOTUtils.Legend( 0.22, 0.86, textSize = 0.03 )

	for label, fileName, color, lineStyle in profiledFiles:
		c68_p = drawContours( fileName, "muTmuW", color=color, lineStyle=lineStyle )
		if c68_p: leg2.AddEntry( c68_p[0], label, "L" )
	leg2.Draw()


	PyROOTUtils.DrawText(0.66, 0.88, "68% CL contours", textSize=0.03)
	leg = PyROOTUtils.Legend( 0.65, 0.86, textSize = 0.03 )
	leg.AddEntry( SMMarker, "Standard Model", "P" )

	c68 = drawContours( fullFile, "profiledNLL", scale=2.0, color=ROOT.kBlack, lineStyle=ROOT.kDashed, lineWidth=3 )
	c68_f = drawContours( effFile, "profiledNLL", scale=2.0, color=ROOT.kBlack, lineStyle=ROOT.kDotted )

	if c68:   leg.AddEntry( c68[0], "full model", "L" )
	if c68_f: leg.AddEntry( c68_f[0], "fixed effective", "L" )
	leg.Draw()







def main():

	print( "Creating plot directories." )
	os.system( "mkdir -p plots/twoBin" )
	os.system( "mkdir -p plots/atlas_counting" )

	draw_muTmuW_frame( muTMuWOverviewNegScenarios, "plots/twoBin/overviewNegScenarios_muTmuW.eps" )
	draw_muTmuW_frame( profiledContour, "plots/twoBin/oneAlpha_catUniversal_muTmuW.eps",                opts={"type":"oneAlpha_catUniversal"} )
	draw_muTmuW_frame( profiledContour, "plots/twoBin/oneAlpha_catUniversal_muTmuW_template0.eps",    opts={"type":"oneAlpha_catUniversal","template0":True} )
	draw_muTmuW_frame( profiledContour, "plots/twoBin/oneAlpha_catNonUniversal_muTmuW.eps",             opts={"type":"oneAlpha_catNonUniversal"} )
	draw_muTmuW_frame( profiledContour, "plots/twoBin/oneAlpha_catNonUniversal_muTmuW_template0.eps", opts={"type":"oneAlpha_catNonUniversal","template0":True} )
	draw_muTmuW_frame( profiledContour, "plots/twoBin/twoAlpha_catUniversal_muTmuW.eps",                opts={"type":"twoAlpha_catUniversal"} )
	draw_muTmuW_frame( profiledContour, "plots/twoBin/twoAlpha_catUniversal_muTmuW_template0.eps",    opts={"type":"twoAlpha_catUniversal","template0":True} )
	draw_muTmuW_frame( profiledContour, "plots/twoBin/twoAlpha_catNonUniversal_muTmuW.eps",             opts={"type":"twoAlpha_catNonUniversal"} )
	draw_muTmuW_frame( profiledContour, "plots/twoBin/twoAlpha_catNonUniversal_muTmuW_template0.eps", opts={"type":"twoAlpha_catNonUniversal","template0":True} )

	draw_muTmuW_frame( profiledContour, "plots/twoBin/twoAlpha_catNonUniversal_muTmuW_template10_etasgeneric_learning.eps",             opts={"type":"twoAlpha_catNonUniversal",'template10_etasgeneric10_learning':True} )
	draw_muTmuW_frame( profiledContour, "plots/twoBin/twoAlpha_catNonUniversal_muTmuW_template14_etasgeneric_learning.eps",             opts={"type":"twoAlpha_catNonUniversal",'template14_etasgeneric14_learning':True} )
	draw_muTmuW_frame( profiledContour, "plots/twoBin/twoAlpha_catNonUniversal_muTmuW_template20_etasgeneric_learning.eps",             opts={"type":"twoAlpha_catNonUniversal",'template20_etasgeneric20_learning':True} )
	draw_muTmuW_frame( profiledContour, "plots/twoBin/twoAlpha_catNonUniversal_muTmuW_template24_etasgeneric_learning.eps",             opts={"type":"twoAlpha_catNonUniversal",'template24_etasgeneric24_learning':True} )

	draw_muTmuW_frame( profiledContour, "plots/twoBin/twoAlpha_catNonUniversal_interpCode0_muTmuW_template10_etasgeneric_learning.eps",             opts={"type":"twoAlpha_catNonUniversal_interpCode0",'template10_etasgeneric10_learning':True} )
	draw_muTmuW_frame( profiledContour, "plots/twoBin/twoAlpha_catNonUniversal_interpCode0_muTmuW_template14_etasgeneric_learning.eps",             opts={"type":"twoAlpha_catNonUniversal_interpCode0",'template14_etasgeneric14_learning':True} )
	draw_muTmuW_frame( profiledContour, "plots/twoBin/twoAlpha_catNonUniversal_interpCode0_muTmuW_template20_etasgeneric_learning.eps",             opts={"type":"twoAlpha_catNonUniversal_interpCode0",'template20_etasgeneric20_learning':True} )
	draw_muTmuW_frame( profiledContour, "plots/twoBin/twoAlpha_catNonUniversal_interpCode0_muTmuW_template24_etasgeneric_learning.eps",             opts={"type":"twoAlpha_catNonUniversal_interpCode0",'template24_etasgeneric24_learning':True} )

	draw_muTmuW_frame( muTMuWOverview, "plots/twoBin/overview_muTmuW.eps" )
	draw_muTmuW_frame( muTMuWInterpCodes, "plots/twoBin/interpcodes_muTmuW.eps" )

	scenarios = [
		'scenarioA',
		'scenarioA2',
		'scenarioB',
		'scenarioC',
		'scenarioC2',
		'scenarioD',
	]
	for s in scenarios:
		draw_muTmuW_frame( profiledContour, "plots/twoBin/"+s+"_muTmuW_template4_etasfisherInfo.eps",  opts={"type":s} )
		draw_muTmuW_frame( profiledContour, "plots/twoBin/"+s+"_muTmuW_template0_etasfisherInfo.eps",  opts={"type":s,"template0":True} )
		draw_muTmuW_frame( profiledContour, "plots/twoBin/"+s+"_muTmuW_templateM1_etasfisherInfo.eps", opts={"type":s,"templateM1":True} )
		draw_muTmuW_frame( profiledContour, "plots/twoBin/"+s+"_muTmuW_template14_etasgeneric_M4.eps", opts={"type":s,"template14_etasgeneric_M4":True} )
		draw_muTmuW_frame( profiledContour, "plots/twoBin/"+s+"_muTmuW_template14_etasgeneric_M5.eps", opts={"type":s,"template14_etasgeneric_M5":True} )
		draw_muTmuW_frame( profiledContour, "plots/twoBin/"+s+"_muTmuW_template14_etasgeneric_fisherInfo.eps", opts={"type":s,"template14_etasgeneric_fisherInfo":True} )

		# draw_muTmuW_frame( profiledContour, "plots/twoBin/"+s+"_muTmuW_template10_etasgeneric10_learning.eps", opts={"type":s,"template10_etasgeneric10_learning":True} )
		# draw_muTmuW_frame( profiledContour, "plots/twoBin/"+s+"_muTmuW_template14_etasgeneric14_learning.eps", opts={"type":s,"template14_etasgeneric14_learning":True} )
		# draw_muTmuW_frame( profiledContour, "plots/twoBin/"+s+"_muTmuW_template20_etasgeneric20_learning.eps", opts={"type":s,"template20_etasgeneric20_learning":True} )
		# draw_muTmuW_frame( profiledContour, "plots/twoBin/"+s+"_muTmuW_template24_etasgeneric24_learning.eps", opts={"type":s,"template24_etasgeneric24_learning":True} )

		draw_muTmuW_frame( profiledContour, "plots/twoBin/"+s+"_muTmuW_template10_etasgeneric10_learningFull.eps", opts={"type":s,"template10_etasgeneric10_learningFull":True} )
		draw_muTmuW_frame( profiledContour, "plots/twoBin/"+s+"_muTmuW_template14_etasgeneric14_learningFull.eps", opts={"type":s,"template14_etasgeneric14_learningFull":True} )
		draw_muTmuW_frame( profiledContour, "plots/twoBin/"+s+"_muTmuW_template20_etasgeneric20_learningFull.eps", opts={"type":s,"template20_etasgeneric20_learningFull":True} )
		draw_muTmuW_frame( profiledContour, "plots/twoBin/"+s+"_muTmuW_template24_etasgeneric24_learningFull.eps", opts={"type":s,"template24_etasgeneric24_learningFull":True} )

	for s in scenarios:
		for i in ['_interpCode0']:
			draw_muTmuW_frame( profiledContour, "plots/twoBin/"+s+i+"_muTmuW_template20_etasgeneric20_learning_box1.0.eps", opts={"type":s+i,"template20_etasgeneric20_learning_box1.0":True} )
			draw_muTmuW_frame( profiledContour, "plots/twoBin/"+s+i+"_muTmuW_template20_etasgeneric20_learningFull_box1.0.eps", opts={"type":s+i,"template20_etasgeneric20_learningFull_box1.0":True} )

			opts = {"type":s+i}
			if "scenarioC" in s: opts['byHand'] = True

			draw_muTmuW_frame( profiledContourOverlay, "plots/twoBin/"+s+i+"_muTmuW_overlay.eps", opts=opts,     r=[0.5,0.3,1.8,2.2] )
			optsFull = dict( [(k,v) for k,v in opts.iteritems()] )
			optsFull['learningFull'] = True
			draw_muTmuW_frame( profiledContourOverlay, "plots/twoBin/"+s+i+"_muTmuW_overlay_learningFull.eps", opts=optsFull,     r=[0.5,0.3,1.8,2.2] )

			opts['box'] = True
			draw_muTmuW_frame( profiledContourOverlay, "plots/twoBin/"+s+i+"_muTmuW_overlay_box.eps", opts=opts, r=[0.5,0.3,1.8,2.2] )
			optsFull = dict( [(k,v) for k,v in opts.iteritems()] )
			optsFull['learningFull'] = True
			draw_muTmuW_frame( profiledContourOverlay, "plots/twoBin/"+s+i+"_muTmuW_overlay_box_learningFull.eps", opts=optsFull, r=[0.5,0.3,1.8,2.2] )


	fileList = "`\ls plots/twoBin/*.eps plots/atlas_counting/*.eps`"
	# print( "Merging eps files" )
	# os.system( "gs -q -dNOPAUSE -dBATCH -sEPSCrop -sDEVICE=pdfwrite -sOutputFile=plots/plots.pdf "+fileList )
	print( "Creating zip file" )
	os.system( "rm plots/plots.zip" )
	os.system( "zip -r plots/plots.zip "+fileList )



if __name__ == "__main__":
	main()
