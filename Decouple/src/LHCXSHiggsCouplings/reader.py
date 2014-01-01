#!/usr/bin/env python

#  Created on: August 2, 2013
__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"


import numpy
import os,csv


cache_YR3 = {}


def readFile( fileHandle ):
	""" Read text files that are formatted like the data files for YR3. """
	header = None
	values = []
	
	for line in fileHandle:
		line = line.replace('\t', ' ')
		while('  ' in line): line = line.replace('  ',' ')
		line = line.strip()
		if len(line) == 0: continue
		line = line.split(' ')

		if not header: header = line
		else: values.append( [ float(r) for r in line ] )

	return (header,values)

def readYR3( filename, mH, verbose=False ):
	""" Use YR3 data and interpolate numbers between Higgs masses. """
	if filename+"_"+str(mH) in cache_YR3.keys():
		return cache_YR3[filename+"_"+str(mH)]

	header,values = (None,[])
	try:
		currentPath = os.path.dirname(os.path.realpath(__file__))
		with open(currentPath+'/Higgs-coupling-data/'+filename, 'r') as f:
			header,values = readFile(f)
	except IOError:
		with open(os.environ['HIGGSCOUPLINGDATA']+'/'+filename, 'r') as f:
			header,values = readFile(f)

	values = numpy.array( values )
	interpValues = [ numpy.interp(mH,values[:,0],values[:,i+1]) for i in range(len(values[0])-1) ]

	result = dict( zip(header,[mH]+interpValues) )
	cache_YR3[filename+"_"+str(mH)] = result

	if verbose:
		print( "" )
		print( "Values for "+filename+" at mH = "+str(mH)+" GeV:" )
		print( result )
		print( "" )

	return result
