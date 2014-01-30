#!/usr/bin/env python

""" Created on: April 5, 2013 """

__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"


import time
import ROOT
import argparse


nuisanceParameters = {}

def configure( options ):
   global nuisanceParameters

   parser = argparse.ArgumentParser()
   parser.add_argument('--commonNP')
   args = parser.parse_known_args(options.split(' '))[0]

   # overwrite nuisanceParameters list
   nuisanceParameters = dict([(np,0.0) for np in args.commonNP.split(',')])

   print( 'Plugin mleCommonNPExceptMuProd -- configure()' )
   print( 'List of nuisance parameters set to:' )
   print( nuisanceParameters )
   print( '' )



def postUnconditionalFit( f,w,mc,data ):
   """ setting some variables constant """
   
   mcNuisPars = mc.GetNuisanceParameters()

   count = 0
   for np in nuisanceParameters.keys():
      v = mcNuisPars.find(np)
      if not v:
         print( "ERROR -- Nuisance parameter >>"+np+"<< not in the ModelConfig's list of nuisance parameters." )
         raise( "Could not find a nuisance parameter in the ModelConfig." )
      if v.GetName() in ["muT","muW","muVBF","muVH"]:
         print( "Not setting "+v.GetName()+" to constant." )
         continue
      print( "Setting "+v.GetName()+" constant at: "+str(v.getVal()) )
      v.setConstant()
      count += 1

   print( "Done setting "+str(count)+" systematics to constant." )   

