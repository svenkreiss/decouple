#!/usr/bin/env python

""" Created on: April 5, 2013 """

__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"


import time
import ROOT


nuisanceParameters = {
   "ATLAS_LUMI_2011": 0.0,
   "ATLAS_LUMI_2012": 0.0,

   "pdf_Higgs_ggH": 0.0,
   "pdf_Higgs_qqH": 0.0,
   "QCDscale_Higgs_ggH": 0.0,
   "QCDscale_Higgs_qqH": 0.0,
   "QCDscale_Higgs_VH": 0.0,
   "QCDscale_Higgs_ttH": 0.0,
   "QCDscale_Higgs_ggH1in":0.0,
   "QCDscale_Higgs_ggH2in":0.0,
   "QCDscale_Higgs_ggH3in":0.0,
   "QCDscale_Higgs_ggH_ACCEPT":0.0,
   "QCDscale_Higgs_qqH_ACCEPT":0.0,

   # Atlas counting model
   "Lumi":0.0,
   "alpha_ATLAS_LUMI_2011": 0.0,
   "alpha_ATLAS_LUMI_2012": 0.0,
   "alpha_QCDscale_Higgs_ggH": 0.0,
   "alpha_QCDscale_Higgs_qqH": 0.0,
   "alpha_QCDscale_Higgs_VH": 0.0,
   "alpha_QCDscale_Higgs_ttH": 0.0,
   "alpha_QCDscale_Higgs_ggH1in":0.0,
   "alpha_QCDscale_Higgs_ggH2in":0.0,
   "alpha_QCDscale_Higgs_ggH3in":0.0,
   #"alpha_QCDscale_Higgs_ggH_ACCEPT":0.0,
   "alpha_QCDscale_Higgs_acceptance_2jet":0.0,

   # twoBin model
   "alpha_sys": 0.0,
   "alpha_sys_VBF": 0.0,
   "alpha_sys_GGF": 0.0,

   # for Hbb
   # the 2011 and 2012 lumis are already included above in ATLAS counting model
   "alpha_SysTheoryVHPdf":0.0,
   "alpha_SysTheoryWHScale":0.0,
   "alpha_SysTheoryZHScale":0.0,
}


def postUnconditionalFit( f,w,mc,data ):
   """ setting some variables constant """
   
   #vars = ROOT.RooArgList( mc.GetNuisanceParameters().selectByName("*ATLAS_LUMI_*,*pdf_Higgs_*,*QCDscale_Higgs_*") )
   #vars = ROOT.RooArgList( mc.GetNuisanceParameters().selectByName("*QCDscale_Higgs_*") )
   vars = ROOT.RooArgList( mc.GetNuisanceParameters().selectByName(",".join(nuisanceParameters.keys())) )
   # "QCDscale_Higgs_ggH2in

   #vars = ROOT.RooArgList( mc.GetNuisanceParameters() )
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

