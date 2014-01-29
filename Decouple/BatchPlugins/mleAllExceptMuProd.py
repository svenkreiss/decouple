#!/usr/bin/env python

""" Created on: April 5, 2013 """

__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"


import time
import ROOT


def postUnconditionalFit( f,w,mc,data ):
   """ setting some variables constant """
   
   #vars = ROOT.RooArgList( mc.GetNuisanceParameters().selectByName("*ATLAS_LUMI_*,*pdf_Higgs_*,*QCDscale_Higgs_*") )
   vars = ROOT.RooArgList( mc.GetNuisanceParameters() )
   count = 0
   for i in range( vars.getSize() ):
      v = vars.at( i )
      if v.GetName() in ["muT","muW","muVBF","muVH"]:
         print( "Not setting "+v.GetName()+" to constant." )
         continue
      print( "Setting "+v.GetName()+" constant at: "+str(v.getVal()) )
      v.setConstant()
      count += 1

   print( "Done setting "+str(count)+" systematics to constant." )   

