#!/usr/bin/env python

#  Created on: October 8, 2013

__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"


import ROOT


def getNll( pdf, data, minStrategy=0, enableOffset=True, globObs=None ):
	""" Generic functions to use with minimize() from BatchProfileLikelihood. """

	# config minimizer
	ROOT.RooAbsReal.defaultIntegratorConfig().method1D().setLabel("RooAdaptiveGaussKronrodIntegrator1D")
	ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit2","Minimize")
	ROOT.Math.MinimizerOptions.SetDefaultStrategy(minStrategy)
	ROOT.Math.MinimizerOptions.SetDefaultPrintLevel(-1)

	# minimizer initialize
	params = pdf.getParameters(data)
	ROOT.RooStats.RemoveConstantParameters(params)
	if globObs:
		nll = pdf.createNLL(
			data, 
			ROOT.RooFit.CloneData(ROOT.kFALSE), 
			ROOT.RooFit.Constrain(params), 
			ROOT.RooFit.GlobalObservables(globObs),
			ROOT.RooFit.Offset(enableOffset),
		)
	else:
		nll = pdf.createNLL(
			data, 
			ROOT.RooFit.CloneData(ROOT.kFALSE), 
			ROOT.RooFit.Constrain(params), 
			ROOT.RooFit.Offset(enableOffset),
		)
	# nllNoOffset = pdf.createNLL(
	# 	data, 
	# 	ROOT.RooFit.CloneData(ROOT.kFALSE), 
	# 	ROOT.RooFit.Constrain(params), 
	# 	ROOT.RooFit.Offset(False),
	# )
	nll.setEvalErrorLoggingMode(ROOT.RooAbsReal.CountErrors)
	# nllNoOffset.setEvalErrorLoggingMode(ROOT.RooAbsReal.CountErrors)
	# if options.enableOffset:
	print( "Get NLL once. This first call sets the offset, so it is important that this happens when the parameters are at their initial values." )
	print( "nll = "+str( nll.getVal() ) )

	return nll



def minimize( nll ):
	
	strat = ROOT.Math.MinimizerOptions.DefaultStrategy()

	msglevel = ROOT.RooMsgService.instance().globalKillBelow()
	ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.FATAL)

	minim = ROOT.RooMinimizer( nll )
	minim.setPrintLevel( ROOT.Math.MinimizerOptions.DefaultPrintLevel() )
	minim.setStrategy(strat)
	minim.optimizeConst(0)
	#minim.optimizeConst(options.minOptimizeConst)

	# Got to be very careful with SCAN. We have to allow for negative mu,
	# so large part of the space that is scanned produces log-eval errors.
	# Therefore, this is usually not feasible.
	#minim.minimize(ROOT.Math.MinimizerOptions.DefaultMinimizerType(), "Scan")
	
	status = -1
	for i in range( 3 ):
		status = minim.minimize(ROOT.Math.MinimizerOptions.DefaultMinimizerType(), 
										ROOT.Math.MinimizerOptions.DefaultMinimizerAlgo())
		if status == 0: break

		if status != 0  and  status != 1  and  strat <= 1:
			strat += 1
			print( "Retrying with strat "+str(strat) )
			minim.setStrategy(strat)
			status = minim.minimize(ROOT.Math.MinimizerOptions.DefaultMinimizerType(), 
											ROOT.Math.MinimizerOptions.DefaultMinimizerAlgo())
		
		if status != 0  and  status != 1  and  strat <= 1:
			strat += 1
			print( "Retrying with strat "+str(strat) )
			minim.setStrategy(strat)
			status = minim.minimize(ROOT.Math.MinimizerOptions.DefaultMinimizerType(), 
											ROOT.Math.MinimizerOptions.DefaultMinimizerAlgo())
		
	if status != 0 and status != 1:
		print( "ERROR::Minimization failed!" )

	ROOT.RooMsgService.instance().setGlobalKillBelow(msglevel)
	return nll.getVal()


def minimize_fitResult( nll, hesse=True ):
	
	strat = ROOT.Math.MinimizerOptions.DefaultStrategy()

	msglevel = ROOT.RooMsgService.instance().globalKillBelow()
	ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.FATAL)

	minim = ROOT.RooMinimizer( nll )
	minim.setPrintLevel( ROOT.Math.MinimizerOptions.DefaultPrintLevel() )
	minim.setStrategy(strat)
	minim.optimizeConst(0)
	#minim.optimizeConst(options.minOptimizeConst)

	# Got to be very careful with SCAN. We have to allow for negative mu,
	# so large part of the space that is scanned produces log-eval errors.
	# Therefore, this is usually not feasible.
	#minim.minimize(ROOT.Math.MinimizerOptions.DefaultMinimizerType(), "Scan")
	
	status = -1
	for i in range( 3 ):
		status = minim.minimize(ROOT.Math.MinimizerOptions.DefaultMinimizerType(), 
										ROOT.Math.MinimizerOptions.DefaultMinimizerAlgo())
		if status == 0: break

		if status != 0  and  status != 1  and  strat <= 1:
			strat += 1
			print( "Retrying with strat "+str(strat) )
			minim.setStrategy(strat)
			status = minim.minimize(ROOT.Math.MinimizerOptions.DefaultMinimizerType(), 
											ROOT.Math.MinimizerOptions.DefaultMinimizerAlgo())
		
		if status != 0  and  status != 1  and  strat <= 1:
			strat += 1
			print( "Retrying with strat "+str(strat) )
			minim.setStrategy(strat)
			status = minim.minimize(ROOT.Math.MinimizerOptions.DefaultMinimizerType(), 
											ROOT.Math.MinimizerOptions.DefaultMinimizerAlgo())
		
	if status != 0 and status != 1:
		print( "ERROR::Minimization failed!" )

	# call Hesse
	if hesse:
		minim.hesse()

	ROOT.RooMsgService.instance().setGlobalKillBelow(msglevel)
	return minim.save()










