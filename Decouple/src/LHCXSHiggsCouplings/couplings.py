#!/usr/bin/env python

#  Created on: August 2, 2013
__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"

from reader import readYR3



def kGlu2_7TeV( kb, kt , mH=125.5 ):
	s = readYR3( "ggH_7TeV.txt", mH )
	return kb*kb*s['sigma_bb/sigma_ggH']  +  \
	       kt*kt*s['sigma_tt/sigma_ggH']  +  \
	       kb*kt*s['sigma_tb/sigma_ggH']

def kGlu2_8TeV( kb, kt , mH=125.5 ):
	s = readYR3( "ggH_8TeV.txt", mH )
	return kb*kb*s['sigma_bb/sigma_ggH']  +  \
	       kt*kt*s['sigma_tt/sigma_ggH']  +  \
	       kb*kt*s['sigma_tb/sigma_ggH']


def kGamma2( kb, kt, ktau, kW, mH=125.5 ):
	G = readYR3( "Gamma_Hgammagamma.txt", mH )
	return kb*kb*G['G_bb/G_gaga']  +  kt*kt*G['G_tt/G_gaga']  +  \
	       kW*kW*G['G_WW/G_gaga']  +  kt*kb*G['G_tb/G_gaga']  +  \
	       kt*kW*G['G_tW/G_gaga']  +  kb*kW*G['G_bW/G_gaga']  +  \
	       ktau*ktau*G['G_ll/G_gaga']  +  \
	       ktau*kt*G['G_tl/G_gaga']  +  ktau*kb*G['G_bl/G_gaga']  +  \
	       ktau*kW*G['G_lW/G_gaga']
def kGamma2_expr( mH=125.5 ):
	""" build a C expression for this function and this particular value of mH """
	G = readYR3( "Gamma_Hgammagamma.txt", mH )
	return "kb*kb*("+str(G['G_bb/G_gaga'])+")  +  kt*kt*("+str(G['G_tt/G_gaga'])+")  +  "\
		   "kW*kW*("+str(G['G_WW/G_gaga'])+")  +  kt*kb*("+str(G['G_tb/G_gaga'])+")  +  "\
		   "kt*kW*("+str(G['G_tW/G_gaga'])+")  +  kb*kW*("+str(G['G_bW/G_gaga'])+")  +  "\
		   "ktau*ktau*("+str(G['G_ll/G_gaga'])+")  +  "\
	       "ktau*kt*("+str(G['G_tl/G_gaga'])+")  +  ktau*kb*("+str(G['G_bl/G_gaga'])+")  +  "\
	       "ktau*kW*("+str(G['G_lW/G_gaga'])+")"
def kGamma2_C( mH=125.5 ):
	return "double kGamma2(double kb, double kt, double ktau, double kW) { return "+kGamma2_expr(mH)+"; }"


def kHGluGlu2( kb, kt, mH=125.5 ):
	G = readYR3( "Gamma_Hgluongluon.txt", mH )
	return kb*kb*G['G_bb/G_gg']  +  kt*kt*G['G_tt/G_gg']  +  \
	       kt*kb*G['G_tb/G_gg']
def kHGluGlu2_expr( mH=125.5 ):
	""" build a C expression for this function and this particular value of mH """
	G = readYR3( "Gamma_Hgluongluon.txt", mH )
	return "kb*kb*("+str(G['G_bb/G_gg'])+")  +  kt*kt*("+str(G['G_tt/G_gg'])+")  +  "+\
	       "kt*kb*("+str(G['G_tb/G_gg'])+")"
def kHGluGlu2_C( mH=125.5 ):
	return "double kHGluGlu2(double kb, double kt) { return "+kHGluGlu2_expr(mH)+"; }"


def kHZGamma2( kb, kt, ktau, kW, mH=125.5 ):
	G = readYR3( "Gamma_HZgamma.txt", mH )
	return kb*kb*G['G_bb/G_Zga']  +  kt*kt*G['G_tt/G_Zga']  +  \
	       kW*kW*G['G_WW/G_Zga']  +  kt*kb*G['G_tb/G_Zga']  +  \
	       kt*kW*G['G_tW/G_Zga']  +  kb*kW*G['G_bW/G_Zga']  +  \
	       ktau*ktau*G['G_ll/G_Zga']  +  \
	       ktau*kt*G['G_tl/G_Zga']  +  ktau*kb*G['G_bl/G_Zga']  +  \
	       ktau*kW*G['G_lW/G_Zga']
def kHZGamma2_expr( mH=125.5 ):
	""" build a C expression for this function and this particular value of mH """
	G = readYR3( "Gamma_HZgamma.txt", mH )
	return "kb*kb*("+str(G['G_bb/G_Zga'])+")  +  kt*kt*("+str(G['G_tt/G_Zga'])+")  +  "+\
	       "kW*kW*("+str(G['G_WW/G_Zga'])+")  +  kt*kb*("+str(G['G_tb/G_Zga'])+")  +  "+\
	       "kt*kW*("+str(G['G_tW/G_Zga'])+")  +  kb*kW*("+str(G['G_bW/G_Zga'])+")  +  "+\
	       "ktau*ktau*("+str(G['G_ll/G_Zga'])+")  +  "+\
	       "ktau*kt*("+str(G['G_tl/G_Zga'])+")  +  ktau*kb*("+str(G['G_bl/G_Zga'])+")  +  "+\
	       "ktau*kW*("+str(G['G_lW/G_Zga'])+")"
def kHZGamma2_C( mH=125.5 ):
	return "double kHZGamma2(double kb, double kt, double ktau, double kW) { return "+kHZGamma2_expr(mH)+"; }"



def kH2( kb, kt, ktau, kW, kZ=None, kmu=None, ks=None, kc=None, mH=125.5 ):
	if not kZ: kZ=kW
	if not kmu: kmu=ktau
	if not ks: ks=kb
	if not kc: kc=ks

	BR  = readYR3( "sm/br/BR.txt", mH )
	BR1 = readYR3( "sm/br/BR1.txt", mH )
	return BR['H_gg']*kHGluGlu2(kb,kt,mH)  +  \
	       BR['H_gamgam']*kGamma2(kb,kt,ktau,kW,mH)  +  \
	       BR['H_Zgam']*kHZGamma2(kb,kt,ktau,kW,mH)  +  \
	       BR['H_WW']*kW*kW  +  \
	       BR['H_ZZ']*kZ*kZ  +  \
	       BR1['H_bb']*kb*kb  +  \
	       BR1['H_tautau']*ktau*ktau  +  \
	       BR1['H_mumu']*kmu*kmu  +  \
	       BR1['H_ssbar']*ks*ks  +  \
	       BR1['H_ccbar']*kc*kc  +  \
	       BR1['H_ttbar']*kt*kt
def kH2_expr( mH=125.5 ):
	""" Build a C expression for this function and this particular value of mH. 
	This also needs other functions implemented in C. """
	BR  = readYR3( "sm/br/BR.txt", mH )
	BR1 = readYR3( "sm/br/BR1.txt", mH )
	return "("+str(BR['H_gg'])+")*kHGluGlu2(kb,kt)  +  "+\
	       "("+str(BR['H_gamgam'])+")*kGamma2(kb,kt,ktau,kW)  +  "+\
	       "("+str(BR['H_Zgam'])+")*kHZGamma2(kb,kt,ktau,kW)  +  "+\
	       "("+str(BR['H_WW'])+")*kW*kW  +  "+\
	       "("+str(BR['H_ZZ'])+")*kZ*kZ  +  "+\
	       "("+str(BR1['H_bb'])+")*kb*kb  +  "+\
	       "("+str(BR1['H_tautau'])+")*ktau*ktau  +  "+\
	       "("+str(BR1['H_mumu'])+")*kmu*kmu  +  "+\
	       "("+str(BR1['H_ssbar'])+")*ks*ks  +  "+\
	       "("+str(BR1['H_ccbar'])+")*kc*kc  +  "+\
	       "("+str(BR1['H_ttbar'])+")*kt*kt"
def kH2_C( mH=125.5 ):
	return "double kH2(double kb, double kt, double ktau, double kW, double kZ, double kmu, double ks, double kc) { return "+kH2_expr(mH)+"; }"



def kH2_GamGlu( kGam,kGlu, mH=125.5 ):
	""" This is a special version for the kGlukGamma model that removes the functional dependence of these two. """
	BR  = readYR3( "sm/br/BR.txt", mH )
	BR1 = readYR3( "sm/br/BR1.txt", mH )
	return BR['H_gg']*kGlu*kGlu  +  \
	       BR['H_gamgam']*kGam*kGam  +  \
	       BR['H_Zgam']*1.0  +  \
	       BR['H_WW']*1.0  +  \
	       BR['H_ZZ']*1.0  +  \
	       BR1['H_bb']*1.0  +  \
	       BR1['H_tautau']*1.0  +  \
	       BR1['H_mumu']*1.0  +  \
	       BR1['H_ssbar']*1.0  +  \
	       BR1['H_ccbar']*1.0  +  \
	       BR1['H_ttbar']*1.0





#########################################################################
# Some tests
#########################################################################


def test_sm_kGlu2_7TeV():
	import nose
	nose.tools.assert_almost_equal( kGlu2_7TeV(1,1), 1.0, places=6 )

def test_sm_kGlu2_8TeV():
	import nose
	nose.tools.assert_almost_equal( kGlu2_8TeV(1,1), 1.0, places=6 )

def test_sm_kHGluGlu2():
	import nose
	nose.tools.assert_almost_equal( kHGluGlu2(1,1), 1.0, places=6 )


def test_sm_kGamma2():
	import nose
	nose.tools.assert_almost_equal( kGamma2(1,1,1,1), 1.0, places=4 )

def test_sm_kHGluGlu2():
	import nose
	nose.tools.assert_almost_equal( kHGluGlu2(1,1), 1.0, places=6 )

def test_sm_kHZGamma2():
	import nose
	nose.tools.assert_almost_equal( kHZGamma2(1,1,1,1), 1.0, places=6 )

def test_sm_kH2():
	import nose
	nose.tools.assert_almost_equal( kH2(1,1,1,1), 1.0, places=3 )


