#!/usr/bin/env python
#  Created on: Dec 6, 2013

__author__ = "Sven Kreiss, Kyle Cranmer"
__version__ = "0.1"

__description__ = """
Intended to be run from main directory (not plotsForPaper).
Specify list of plots (eps files) to copy here. Give a tuple of src and dest filename 
if you need to rename fiels.
The idea is to keep all plots dynamically updating in plots/ and have stable versions
in this directory that is updated manually. Also helps with version control of plots.
"""

import os


files = [
	# 'plots/twoBin/scenarioA_interpCode0_muTmuW_overlay.eps',
	# 'plots/twoBin/scenarioB_interpCode0_muTmuW_overlay.eps',
	# 'plots/twoBin/scenarioC_interpCode0_muTmuW_overlay.eps',
	# 'plots/twoBin/scenarioA_interpCode0_muTmuW_overlay_box.eps',
	# 'plots/twoBin/scenarioB_interpCode0_muTmuW_overlay_box.eps',
	# 'plots/twoBin/scenarioC_interpCode0_muTmuW_overlay_box.eps',

	# ('plots/twoBin/scenarioA_interpCode0_etas/fisherInfo.eps', 'scenarioA_interpCode0_etas_fisherInfo.eps'),
	# ('plots/twoBin/scenarioA_interpCode0_etas/table_etas.py',  'scenarioA_interpCode0_etas_table.py'),
	# ('plots/twoBin/scenarioB_interpCode0_etas/fisherInfo.eps', 'scenarioB_interpCode0_etas_fisherInfo.eps'),
	# ('plots/twoBin/scenarioB_interpCode0_etas/table_etas.py',  'scenarioB_interpCode0_etas_table.py'),
	# ('plots/twoBin/scenarioC_interpCode0_etas/fisherInfo.eps', 'scenarioC_interpCode0_etas_fisherInfo.eps'),
	# ('plots/twoBin/scenarioC_interpCode0_etas/table_etas.py',  'scenarioC_interpCode0_etas_table.py'),

	# 'plots/atlas_counting/interpCode0_muTmuW.eps',
	# 'plots/atlas_counting/interpCode0_muTmuW_shifted.eps',
	# 'plots/atlas_counting/interpCode0_muTmuW_shifted_etaArrows.eps',
	# 'plots/atlas_counting/interpCode0_muTmuW_template0_etasfisherInfo.eps',
	# 'plots/atlas_counting/interpCode0_muTmuW_template10_etasgeneric_M5.eps',
	# 'plots/atlas_counting/interpCode0_muTmuW_template20_etasgeneric20_learningFull.eps',

	('plots/atlas_counting/2ph_interpCode0_etas/fisherInfo.eps', '2ph_etas_fisherInfo.eps'),
	# ('plots/atlas_counting/2ph_interpCode0_etas/table_etas.py',  '2ph_etas_table.py'),
	('plots/atlas_counting/4l_interpCode0_etas/fisherInfo.eps', '4l_etas_fisherInfo.eps'),
	# ('plots/atlas_counting/4l_interpCode0_etas/table_etas.py',  '4l_etas_table.py'),
	('plots/atlas_counting/lvlv_interpCode0_etas/fisherInfo.eps', 'lvlv_etas_fisherInfo.eps'),
	# ('plots/atlas_counting/lvlv_interpCode0_etas/table_etas.py',  'lvlv_etas_table.py'),

	# 'plots/atlas_counting/interpCode0_kGlukGamma_combined_template10_etasgeneric_M5.eps',
	# 'plots/atlas_counting/interpCode0_kGlukGamma_combined_template10_etasgeneric_M5_box1.0.eps',
	# 'plots/atlas_counting/interpCode0_kGlukGamma_combined_template10_etasgeneric_M5_wideGauss1.3.eps',
	# 'plots/atlas_counting/interpCode0_kVkF_combined_template10_etasgeneric_M5.eps',
	# 'plots/atlas_counting/interpCode0_kVkF_combined_template10_etasgeneric_M5_box1.0.eps',
	# 'plots/atlas_counting/interpCode0_kVkF_combined_template10_etasgeneric_M5_wideGauss1.3.eps',

	# 'plots/atlas_counting/interpCode0_kGlukGamma_combined_template10_etasgeneric10_learningFull.eps',
	# 'plots/atlas_counting/interpCode0_kGlukGamma_combined_template10_etasgeneric10_learningFull_box1.0.eps',
	# 'plots/atlas_counting/interpCode0_kGlukGamma_combined_template10_etasgeneric10_learningFull_wideGauss1.3.eps',
	# 'plots/atlas_counting/interpCode0_kVkF_combined_template10_etasgeneric10_learningFull.eps',
	# 'plots/atlas_counting/interpCode0_kVkF_combined_template10_etasgeneric10_learningFull_box1.0.eps',
	# 'plots/atlas_counting/interpCode0_kVkF_combined_template10_etasgeneric10_learningFull_wideGauss1.3.eps',
	# 'plots/atlas_counting/interpCode0_kVkF_combined_template10_etasgeneric10_learningFull_overlay.eps',
	# 'plots/atlas_counting/interpCode0_kGlukGamma_combined_template10_etasgeneric10_learningFull_overlay.eps',

	('~/tex/papers/CouplingsFromProdModes/dotProduct/plots/2ph_robustness_normEtas_normTh2.eps', 'atlas_counting/robustness_2ph.eps'),
	('~/tex/papers/CouplingsFromProdModes/dotProduct/plots/ZZ_robustness_normEtas_normTh2.eps', 'atlas_counting/robustness_4l.eps'),
	('~/tex/papers/CouplingsFromProdModes/dotProduct/plots/WW_robustness_normEtas_normTh2.eps', 'atlas_counting/robustness_lvlv.eps'),
]


def main():
	for f in files:
		targetDir = 'plotsForPaper/'

		if isinstance(f,str):
			if 'twoBin/' in f: targetDir = 'plotsForPaper/twoBin/'
			if 'atlas_counting/' in f: targetDir = 'plotsForPaper/atlas_counting/'
			os.system( 'mkdir -p '+targetDir )

			os.system("cp "+f+" "+targetDir)
			print(f+' to '+targetDir)
		elif len(f) == 2:
			if 'twoBin/' in f[0]: targetDir = 'plotsForPaper/twoBin/'
			if 'atlas_counting/' in f[0]: targetDir = 'plotsForPaper/atlas_counting/'
			os.system( 'mkdir -p '+targetDir )

			os.system("cp "+f[0]+" "+targetDir+f[1])
			print(f[0]+' to '+targetDir+f[1])
		else:
			print("Don't know what to do with "+str(f))
	print("Done.")


if __name__ == "__main__":
	main()
