#!/usr/bin/env python

#  Created on: January 2, 2014

__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"


import ROOT
import PyROOTUtils
from array import array



SMMarker = ROOT.TMarker( 1.0, 1.0, 34 )
SMMarker.SetMarkerColor( ROOT.kBlack )



container = []
openFiles = []



def getContours( hist, level, levelName, canvas=None, scale=1.0 ):
	tmpCanvas = False
	if not canvas:
		canvas = ROOT.TCanvas()
		tmpCanvas = True

	hist.Scale(scale)
	hist.SetContour( 1, array('d',[level]) )
	hist.Draw( "COLZ CONT LIST" )
	canvas.Update()
	listOfGraphs = ROOT.gROOT.GetListOfSpecials().FindObject("contours").At(0)
	contours = [ ROOT.TGraph( listOfGraphs.At(i) ) for i in range( listOfGraphs.GetSize() ) ]
	for co in range( len(contours) ):
		contours[co].SetName( "Contour%s_%d" % (levelName,co) )

	if tmpCanvas: del(canvas)

	return contours

def getSmallestBinMarker( hist, color=ROOT.kBlack ):
	bx,by,bz = (ROOT.Long(),ROOT.Long(),ROOT.Long())
	hist.GetBinXYZ( hist.GetMinimumBin(),bx,by,bz )
	cm = PyROOTUtils.CrossMarker( 
		hist.GetXaxis().GetBinCenter(bx), 
		hist.GetYaxis().GetBinCenter(by), 
		markerColor=color,
	)
	return cm

def getInterpolatedMinimumMarker( hist, color=ROOT.kBlack ):
	"""
	This takes the neighboring two bins and plots a parabola through the three
	points defined by the three bins (parabolas are uniquely defined by three points).
	No fitting has to be done. The minimum of that parabola is used as the 
	interpolated minimum. 

	For the bin heights y1, y2 and y3 at the bin positions 0, \Delta x and 2\Delta x,
	the parabola minimum x0 is at:
		-x0 = [4(y2-y1) - (y3-y1)]\Delta x  /  [2(y3-y1) - 4(y2-y1)]

	This ignores (off-)diagonal neighboring cells which would go beyond what can be
	uniquely defined for a parabola.
	"""
	bx,by,bz = (ROOT.Long(),ROOT.Long(),ROOT.Long())
	hist.GetBinXYZ( hist.GetMinimumBin(),bx,by,bz )

	# interpolate position horizontally
	y1 = hist.GetBinContent( hist.GetMinimumBin()-1 )
	y2 = hist.GetBinContent( hist.GetMinimumBin() )
	y3 = hist.GetBinContent( hist.GetMinimumBin()+1 )
	deltax = (hist.GetXaxis().GetBinCenter(bx+1) - hist.GetXaxis().GetBinCenter(bx-1))/2.0
	x0 = hist.GetXaxis().GetBinCenter(bx-1)  +  ((4.0*(y2-y1)-(y3-y1))*(-deltax))  /  (2.0*(y3-y1)-4.0*(y2-y1))

	# interpolate position vertically
	bU = hist.GetMinimumBin()+(hist.GetXaxis().GetNbins()+2) # bin up
	bD = hist.GetMinimumBin()-(hist.GetXaxis().GetNbins()+2) # bin down
	y1 = hist.GetBinContent( bU )
	y2 = hist.GetBinContent( hist.GetMinimumBin() )
	y3 = hist.GetBinContent( bD )
	deltay = (hist.GetYaxis().GetBinCenter(by+1) - hist.GetYaxis().GetBinCenter(by-1))/2.0
	y0 = hist.GetYaxis().GetBinCenter(by-1)  +  ((4.0*(y2-y1)-(y3-y1))*(-deltay))  /  (2.0*(y3-y1)-4.0*(y2-y1))

	cm = PyROOTUtils.CrossMarker( 
		x0, 
		y0, 
		markerColor=color,
	)
	return cm

def drawContours( filename, histname, lineWidth=2, color=ROOT.kBlack, lineStyle=ROOT.kSolid, level=2.3, levelName="68",scale=1.0,drawStyle="L",drawSmallestBinMarker=False,printSamllestBinMarkerCoordinates=False ):
	f = ROOT.TFile.Open( filename, "READ" )
	if not f: return None

	h = f.Get(histname)
	container.append(h)

	contours = getContours( h,level,levelName,scale=scale )
	for c in contours:
		c.SetLineColor( color )
		c.SetLineWidth( lineWidth )
		c.SetLineStyle( lineStyle )
		c.SetFillColor( color )
		c.Draw( drawStyle )

	if drawSmallestBinMarker:
		# m = getSmallestBinMarker( h,color )
		# m.Draw()
		# container.append( m )
		m2 = getInterpolatedMinimumMarker( h,color )
		m2.Draw()
		container.append( m2 )
		if printSamllestBinMarkerCoordinates:
			print( "Smallest bin marker: ("+str(m2.GetX())+", "+str(m2.GetY()) )

	openFiles.append( f )
	container.append( contours )
	return contours

def drawH( filename, histname ):
	f = ROOT.TFile.Open( filename, "READ" )
	h = f.Get(histname)
	h.SetStats( False )
	h.SetContour( 100 )
	#h.Scale( 2 )
	h.SetMinimum( -1e-6 )
	h.SetMaximum( 6 )
	#h.GetZaxis().SetTitle( "-2 ln #Lambda" )
	h.Draw("COLZ,SAME")
	container.append( h )

	bFOrig = f.Get( histname+"_bestFit" )
	bF = PyROOTUtils.CrossMarker( bFOrig.GetX(),bFOrig.GetY() )
	bF.Draw()
	container.append( bF )

	openFiles.append( f )
	return (h,bF)


def draw_muTmuW_frame( content, outFile, opts={}, r=[0.5,0.5,2.0,2.0] ):
	global openFiles

	canvas = ROOT.TCanvas( "canvas","canvas",600,600 )
	axes = canvas.DrawFrame( r[0],r[1],r[2],r[3] )
	axes.GetXaxis().SetTitle( "#mu^{f}_{ggF+ttH}" )
	axes.GetYaxis().SetTitle( "#mu^{f}_{VBF+VH}" )
	# axes.GetYaxis().SetTitleOffset( 1.2 )

	SMMarker.Draw()

	content( opts=opts )

	canvas.SaveAs( outFile )
	[f.Close() for f in openFiles]
	openFiles = []

def draw_kVkF_frame( content, outFile, opts={}, r=[0.5,0.5,2.0,2.0] ):
	canvas = ROOT.TCanvas( "canvas","canvas",600,600 )
	axes = canvas.DrawFrame( r[0],r[1],r[2],r[3] )
	axes.GetXaxis().SetTitle( "#kappa_{V}" )
	axes.GetYaxis().SetTitle( "#kappa_{F}" )
	# axes.GetYaxis().SetTitleOffset( 1.2 )

	SMMarker.Draw()

	content( opts=opts )

	canvas.SaveAs( outFile )


def draw_kGlukGamma_frame( content, outFile, opts={}, r=[0.5,0.5,2.0,2.0] ):
	canvas = ROOT.TCanvas( "canvas","canvas",600,600 )
	axes = canvas.DrawFrame( r[0],r[1],r[2],r[3] )
	axes.GetXaxis().SetTitle( "#kappa_{#gamma}" )
	axes.GetYaxis().SetTitle( "#kappa_{g}" )
	# axes.GetYaxis().SetTitleOffset( 1.2 )

	SMMarker.Draw()

	content( opts=opts )

	canvas.SaveAs( outFile )
