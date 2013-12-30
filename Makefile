# 9 Sept 2013
# Sven Kreiss, Kyle Cranmer


all:
	$(MAKE) models
	$(MAKE) decouple
	$(MAKE) recouple
	$(MAKE) plots
	$(MAKE) other
models:
	cd ModelGenerators; $(MAKE)
decouple: decoupleTwoBin decoupleAtlasCountingInterpCode0
decoupleAll: decouple decoupleAtlasCounting
recouple: recoupleTwoBinInterpCode0 recoupleAtlasCountingInterpCode0
recoupleAll: recouple recoupleTwoBin recoupleAtlasCounting
plots: plotTwoBin plotAtlasCounting

clean:
	rm -rf output/twoBin output/atlas_counting
	rm -rf plots/twoBin plots/atlas_counting plots/plots.pdf plots.zip plots/interpCodes

clean-decoupleTwoBin:
	rm -f output/twoBin/oneAlpha_catUniversal/table_etas.pickle
	rm -f output/twoBin/oneAlpha_catNonUniversal/table_etas.pickle
	rm -f output/twoBin/twoAlpha_catUniversal/table_etas.pickle
	rm -f output/twoBin/twoAlpha_catNonUniversal/table_etas.pickle

	rm -f output/twoBin/oneAlpha_catUniversal_interpCode0/table_etas.pickle
	rm -f output/twoBin/oneAlpha_catNonUniversal_interpCode0/table_etas.pickle
	rm -f output/twoBin/twoAlpha_catUniversal_interpCode0/table_etas.pickle
	rm -f output/twoBin/twoAlpha_catNonUniversal_interpCode0/table_etas.pickle

	rm -f output/twoBin/scenarioA/table_etas.pickle
	rm -f output/twoBin/scenarioA2/table_etas.pickle
	rm -f output/twoBin/scenarioB/table_etas.pickle
	rm -f output/twoBin/scenarioC/table_etas.pickle
	rm -f output/twoBin/scenarioC2/table_etas.pickle
	rm -f output/twoBin/scenarioD/table_etas.pickle

	rm -f output/twoBin/scenarioA_interpCode0/table_etas.pickle
	rm -f output/twoBin/scenarioA2_interpCode0/table_etas.pickle
	rm -f output/twoBin/scenarioB_interpCode0/table_etas.pickle
	rm -f output/twoBin/scenarioC_interpCode0/table_etas.pickle
	rm -f output/twoBin/scenarioC2_interpCode0/table_etas.pickle
	rm -f output/twoBin/scenarioD_interpCode0/table_etas.pickle

	rm -f output/twoBin/scenarioA_additiveMu_interpCode0/table_etas.pickle
	rm -f output/twoBin/scenarioA2_additiveMu_interpCode0/table_etas.pickle
	rm -f output/twoBin/scenarioB_additiveMu_interpCode0/table_etas.pickle
	rm -f output/twoBin/scenarioC_additiveMu_interpCode0/table_etas.pickle
	rm -f output/twoBin/scenarioC2_additiveMu_interpCode0/table_etas.pickle
	rm -f output/twoBin/scenarioD_additiveMu_interpCode0/table_etas.pickle

clean-decoupleAtlasCounting:
	rm -f output/atlas_counting/2ph/table_etas.pickle
	rm -f output/atlas_counting/4l/table_etas.pickle
	rm -f output/atlas_counting/lvlv/table_etas.pickle
	rm -f output/atlas_counting/2ph_interpCode0/table_etas.pickle
	rm -f output/atlas_counting/4l_interpCode0/table_etas.pickle
	rm -f output/atlas_counting/lvlv_interpCode0/table_etas.pickle

clean-decoupleAtlasCountingBox:
	rm -f output/atlas_counting/2ph_box/muTmuW.root
	rm -f output/atlas_counting/4l_box/muTmuW.root
	rm -f output/atlas_counting/lvlv_box/muTmuW.root
	rm -f output/atlas_counting/2ph_interpCode0_box/muTmuW.root
	rm -f output/atlas_counting/4l_interpCode0_box/muTmuW.root
	rm -f output/atlas_counting/lvlv_interpCode0_box/muTmuW.root

clean-decouple: clean-decoupleTwoBin clean-decoupleAtlasCounting clean-decoupleAtlasCountingBox

clean-recouple:
	rm -f output/twoBin/oneAlpha_catUniversal/muTmuW_profiledContour*.root
	rm -f output/twoBin/oneAlpha_catNonUniversal/muTmuW_profiledContour*.root
	rm -f output/twoBin/twoAlpha_catUniversal/muTmuW_profiledContour*.root
	rm -f output/twoBin/twoAlpha_catNonUniversal/muTmuW_profiledContour*.root

	rm -f output/twoBin/scenarioA/muTmuW_profiledContour*.root
	rm -f output/twoBin/scenarioA2/muTmuW_profiledContour*.root
	rm -f output/twoBin/scenarioB/muTmuW_profiledContour*.root
	rm -f output/twoBin/scenarioC/muTmuW_profiledContour*.root
	rm -f output/twoBin/scenarioC2/muTmuW_profiledContour*.root
	rm -f output/twoBin/scenarioD/muTmuW_profiledContour*.root

	rm -f output/atlas_counting/2ph/*_profiledContour*.root
	rm -f output/atlas_counting/4l/*_profiledContour*.root
	rm -f output/atlas_counting/lvlv/*_profiledContour*.root

other: studyInterpCodes




######################################################
# decouple (not just etas)

output/twoBin/%/table_etas.pickle: output/twoBin/%.root
	python Decouple/decouple.py -i $< -p alpha_sys,alpha_sys_GGF

decoupleTwoBin: \
		output/twoBin/oneAlpha_catUniversal/table_etas.pickle \
		output/twoBin/oneAlpha_catNonUniversal/table_etas.pickle \
		output/twoBin/twoAlpha_catUniversal/table_etas.pickle \
		output/twoBin/twoAlpha_catNonUniversal/table_etas.pickle \
		\
		output/twoBin/oneAlpha_catUniversal_interpCode0/table_etas.pickle \
		output/twoBin/oneAlpha_catNonUniversal_interpCode0/table_etas.pickle \
		output/twoBin/twoAlpha_catUniversal_interpCode0/table_etas.pickle \
		output/twoBin/twoAlpha_catNonUniversal_interpCode0/table_etas.pickle \
		\
		output/twoBin/scenarioA/table_etas.pickle \
		output/twoBin/scenarioA2/table_etas.pickle \
		output/twoBin/scenarioB/table_etas.pickle \
		output/twoBin/scenarioC/table_etas.pickle \
		output/twoBin/scenarioC2/table_etas.pickle \
		output/twoBin/scenarioD/table_etas.pickle \
		\
		output/twoBin/scenarioA_interpCode0/table_etas.pickle \
		output/twoBin/scenarioA2_interpCode0/table_etas.pickle \
		output/twoBin/scenarioB_interpCode0/table_etas.pickle \
		output/twoBin/scenarioC_interpCode0/table_etas.pickle \
		output/twoBin/scenarioC2_interpCode0/table_etas.pickle \
		output/twoBin/scenarioD_interpCode0/table_etas.pickle \
		\
		output/twoBin/scenarioA_additiveMu_interpCode0/table_etas.pickle \
		output/twoBin/scenarioA2_additiveMu_interpCode0/table_etas.pickle \
		output/twoBin/scenarioB_additiveMu_interpCode0/table_etas.pickle \
		output/twoBin/scenarioC_additiveMu_interpCode0/table_etas.pickle \
		output/twoBin/scenarioC2_additiveMu_interpCode0/table_etas.pickle \
		output/twoBin/scenarioD_additiveMu_interpCode0/table_etas.pickle

# box full scan reference
ATLASCOUNTINGPARAMETERS = alpha_QCDscale_Higgs_ggH2in,alpha_QCDscale_Higgs_ggH,alpha_ATLAS_LUMI_2012
output/atlas_counting/2p%_box/muTmuW.root: output/atlas_counting/2p%_box.root
	python Decouple/decouple.py -i $< --range=0.5,-0.1,3.0,4.0 --bins=250,250 -p $(ATLASCOUNTINGPARAMETERS) --skip_etas --skip_eff
output/atlas_counting/4%_box/muTmuW.root: output/atlas_counting/4%_box.root
	python Decouple/decouple.py -i $< --range=-0.3,-3.0,3.6,11.5 --bins=200,400 -p $(ATLASCOUNTINGPARAMETERS) --skip_etas --skip_eff
output/atlas_counting/lvl%_box/muTmuW.root: output/atlas_counting/lvl%_box.root
	python Decouple/decouple.py -i $< --range=-0.5,-1.2,2.5,5.2 --bins=250,250 -p $(ATLASCOUNTINGPARAMETERS) --skip_etas --skip_eff
# wideGauss full scan
output/atlas_counting/2p%_wideGauss/muTmuW.root: output/atlas_counting/2p%_wideGauss.root
	python Decouple/decouple.py -i $< --range=0.5,-0.1,3.0,4.0 --bins=250,250 -p $(ATLASCOUNTINGPARAMETERS) --skip_etas --skip_eff
output/atlas_counting/4%_wideGauss/muTmuW.root: output/atlas_counting/4%_wideGauss.root
	python Decouple/decouple.py -i $< --range=-0.3,-3.0,3.6,11.5 --bins=200,400 -p $(ATLASCOUNTINGPARAMETERS) --skip_etas --skip_eff
output/atlas_counting/lvl%_wideGauss/muTmuW.root: output/atlas_counting/lvl%_wideGauss.root
	python Decouple/decouple.py -i $< --range=-0.5,-1.2,2.5,5.2 --bins=250,250 -p $(ATLASCOUNTINGPARAMETERS) --skip_etas --skip_eff

# no box
output/atlas_counting/2p%/table_etas.pickle: output/atlas_counting/2p%.root
	python Decouple/decouple.py -i $< --range=0.5,-0.1,3.0,4.0 --bins=250,250 -p $(ATLASCOUNTINGPARAMETERS)

output/atlas_counting/4%/table_etas.pickle: output/atlas_counting/4%.root
	python Decouple/decouple.py -i $< --range=-0.3,-3.0,3.6,11.5 --bins=200,400 -p $(ATLASCOUNTINGPARAMETERS)

output/atlas_counting/lvl%/table_etas.pickle: output/atlas_counting/lvl%.root
	python Decouple/decouple.py -i $< --range=0.0,-0.8,1.7,4.5 --bins=250,250 -p $(ATLASCOUNTINGPARAMETERS)


decoupleAtlasCountingInterpCode0Box: \
		output/atlas_counting/2ph_interpCode0_box/muTmuW.root \
		output/atlas_counting/4l_interpCode0_box/muTmuW.root \
		output/atlas_counting/lvlv_interpCode0_box/muTmuW.root
decoupleAtlasCountingInterpCode0WideGauss: \
		output/atlas_counting/2ph_interpCode0_wideGauss/muTmuW.root \
		output/atlas_counting/4l_interpCode0_wideGauss/muTmuW.root \
		output/atlas_counting/lvlv_interpCode0_wideGauss/muTmuW.root

decoupleAtlasCountingInterpCode0Channels: \
		output/atlas_counting/2ph_interpCode0/table_etas.pickle \
		output/atlas_counting/4l_interpCode0/table_etas.pickle \
		output/atlas_counting/lvlv_interpCode0/table_etas.pickle

decoupleAtlasCountingInterpCode0: \
		decoupleAtlasCountingInterpCode0Channels \
		decoupleAtlasCountingInterpCode0Box


decoupleAtlasCounting: \
		output/atlas_counting/2ph/table_etas.pickle \
		output/atlas_counting/4l/table_etas.pickle \
		output/atlas_counting/lvlv/table_etas.pickle \
		\
		output/atlas_counting/2ph_box/muTmuW.root \
		output/atlas_counting/4l_box/muTmuW.root \
		output/atlas_counting/lvlv_box/muTmuW.root


######################################################
# recouple

output/twoBin/%/muTmuW_profiledContour.root: output/twoBin/%/muTmuW_eff.root
	python Decouple/recouple.py -i $<:profiledNLL:output/twoBin/$*/table_etas.pickle:2                    --skip_kVkF --skip_kGlukGamma

output/twoBin/%/muTmuW_profiledContour_template0.root: output/twoBin/%/muTmuW_eff.root
	python Decouple/recouple.py -i $<:profiledNLL:output/twoBin/$*/table_etas.pickle:2 --template=0       --skip_kVkF --skip_kGlukGamma

output/twoBin/%/muTmuW_profiledContour_templateM1.root: output/twoBin/%/muTmuW_eff.root
	python Decouple/recouple.py -i $<:profiledNLL:output/twoBin/$*/table_etas.pickle:2 --template=-1      --skip_kVkF --skip_kGlukGamma

output/twoBin/%/muTmuW_profiledContour_template14_etasgeneric_M4.root: output/twoBin/%/muTmuW_eff.root
	python Decouple/recouple.py -i $<:profiledNLL:output/twoBin/$*/table_etas.pickle:generic_M4:2         --template=14 --skip_kVkF --skip_kGlukGamma

output/twoBin/%/muTmuW_profiledContour_template10_etasgeneric_M5.root: output/twoBin/%/muTmuW_eff.root
	python Decouple/recouple.py -i $<:profiledNLL:output/twoBin/$*/table_etas.pickle:generic_M5:2         --template=10 --skip_kVkF --skip_kGlukGamma

output/twoBin/%/muTmuW_profiledContour_template14_etasgeneric_M5.root: output/twoBin/%/muTmuW_eff.root
	python Decouple/recouple.py -i $<:profiledNLL:output/twoBin/$*/table_etas.pickle:generic_M5:2         --template=14 --skip_kVkF --skip_kGlukGamma

output/twoBin/%/muTmuW_profiledContour_template14_etasgeneric_fisherInfo.root: output/twoBin/%/muTmuW_eff.root
	python Decouple/recouple.py -i $<:profiledNLL:output/twoBin/$*/table_etas.pickle:generic_fisherInfo:2 --template=14 --skip_kVkF --skip_kGlukGamma


output/twoBin/%/muTmuW_profiledContour_template10_etasgeneric10_learning.root: output/twoBin/%/muTmuW_eff.root
	python Decouple/recouple.py -i $<:profiledNLL:output/twoBin/$*/table_etas.pickle:generic10_learning:2   --template=10 --skip_kVkF --skip_kGlukGamma

output/twoBin/%/muTmuW_profiledContour_template14_etasgeneric14_learning.root: output/twoBin/%/muTmuW_eff.root
	python Decouple/recouple.py -i $<:profiledNLL:output/twoBin/$*/table_etas.pickle:generic14_learning:2   --template=14 --skip_kVkF --skip_kGlukGamma

output/twoBin/%/muTmuW_profiledContour_template20_etasgeneric20_learning.root: output/twoBin/%/muTmuW_eff.root
	python Decouple/recouple.py -i $<:profiledNLL:output/twoBin/$*/table_etas.pickle:generic20_learning:2   --template=20 --skip_kVkF --skip_kGlukGamma

output/twoBin/%/muTmuW_profiledContour_template24_etasgeneric24_learning.root: output/twoBin/%/muTmuW_eff.root
	python Decouple/recouple.py -i $<:profiledNLL:output/twoBin/$*/table_etas.pickle:generic24_learning:2   --template=24 --skip_kVkF --skip_kGlukGamma




# box full scan reference
TWOBINPARAMETERS = alpha_sys,alpha_sys_GGF
output/twoBin/%_box/muTmuW.root: output/twoBin/%_box.root
	python Decouple/decouple.py -i $< -p $(TWOBINPARAMETERS) --skip_etas --skip_eff

output/twoBin/%/muTmuW_profiledContour_template0_etasfisherInfo_box1.0.root: output/twoBin/%/muTmuW_eff.root
	python Decouple/recouple.py -i $<:profiledNLL:output/twoBin/$*/table_etas.pickle:fisherInfo:2   --template=0 --skip_kVkF --skip_kGlukGamma --box=1

output/twoBin/%/muTmuW_profiledContour_template10_etasgeneric_M5_box1.0.root: output/twoBin/%/muTmuW_eff.root
	python Decouple/recouple.py -i $<:profiledNLL:output/twoBin/$*/table_etas.pickle:generic_M5:2   --template=10 --skip_kVkF --skip_kGlukGamma --box=1

output/twoBin/%/muTmuW_profiledContour_template20_etasgeneric20_learning_box1.0.root: output/twoBin/%/muTmuW_eff.root
	python Decouple/recouple.py -i $<:profiledNLL:output/twoBin/$*/table_etas.pickle:generic20_learning:2   --template=20 --skip_kVkF --skip_kGlukGamma --box=1



#Old recoupleTwoBin
# output/twoBin/scenarioA/muTmuW_profiledContour_template14_etasgeneric_M4.root \
# output/twoBin/scenarioA2/muTmuW_profiledContour_template14_etasgeneric_M4.root \
# output/twoBin/scenarioB/muTmuW_profiledContour_template14_etasgeneric_M4.root \
# output/twoBin/scenarioC/muTmuW_profiledContour_template14_etasgeneric_M4.root \
# output/twoBin/scenarioC2/muTmuW_profiledContour_template14_etasgeneric_M4.root \
# output/twoBin/scenarioD/muTmuW_profiledContour_template14_etasgeneric_M4.root \
# \

recoupleTwoBinLearningInterpCode0Multiplicative: \
		output/twoBin/scenarioA_interpCode0/muTmuW_profiledContour_template14_etasgeneric14_learning.root \
		output/twoBin/scenarioA2_interpCode0/muTmuW_profiledContour_template14_etasgeneric14_learning.root \
		output/twoBin/scenarioB_interpCode0/muTmuW_profiledContour_template14_etasgeneric14_learning.root \
		output/twoBin/scenarioC_interpCode0/muTmuW_profiledContour_template14_etasgeneric14_learning.root \
		output/twoBin/scenarioC2_interpCode0/muTmuW_profiledContour_template14_etasgeneric14_learning.root \
		output/twoBin/scenarioD_interpCode0/muTmuW_profiledContour_template14_etasgeneric14_learning.root \
		\
		output/twoBin/scenarioA_interpCode0/muTmuW_profiledContour_template24_etasgeneric24_learning.root \
		output/twoBin/scenarioA2_interpCode0/muTmuW_profiledContour_template24_etasgeneric24_learning.root \
		output/twoBin/scenarioB_interpCode0/muTmuW_profiledContour_template24_etasgeneric24_learning.root \
		output/twoBin/scenarioC_interpCode0/muTmuW_profiledContour_template24_etasgeneric24_learning.root \
		output/twoBin/scenarioC2_interpCode0/muTmuW_profiledContour_template24_etasgeneric24_learning.root \
		output/twoBin/scenarioD_interpCode0/muTmuW_profiledContour_template24_etasgeneric24_learning.root

recoupleTwoBinLearningInterpCode0: \
		output/twoBin/scenarioA_interpCode0/muTmuW_profiledContour_template10_etasgeneric10_learning.root \
		output/twoBin/scenarioA2_interpCode0/muTmuW_profiledContour_template10_etasgeneric10_learning.root \
		output/twoBin/scenarioB_interpCode0/muTmuW_profiledContour_template10_etasgeneric10_learning.root \
		output/twoBin/scenarioC_interpCode0/muTmuW_profiledContour_template10_etasgeneric10_learning.root \
		output/twoBin/scenarioC2_interpCode0/muTmuW_profiledContour_template10_etasgeneric10_learning.root \
		output/twoBin/scenarioD_interpCode0/muTmuW_profiledContour_template10_etasgeneric10_learning.root \
		\
		output/twoBin/scenarioA_interpCode0/muTmuW_profiledContour_template20_etasgeneric20_learning.root \
		output/twoBin/scenarioA2_interpCode0/muTmuW_profiledContour_template20_etasgeneric20_learning.root \
		output/twoBin/scenarioB_interpCode0/muTmuW_profiledContour_template20_etasgeneric20_learning.root \
		output/twoBin/scenarioC_interpCode0/muTmuW_profiledContour_template20_etasgeneric20_learning.root \
		output/twoBin/scenarioC2_interpCode0/muTmuW_profiledContour_template20_etasgeneric20_learning.root \
		output/twoBin/scenarioD_interpCode0/muTmuW_profiledContour_template20_etasgeneric20_learning.root \
		\
		output/twoBin/scenarioA_interpCode0_box/muTmuW.root \
		output/twoBin/scenarioA2_interpCode0_box/muTmuW.root \
		output/twoBin/scenarioB_interpCode0_box/muTmuW.root \
		output/twoBin/scenarioC_interpCode0_box/muTmuW.root \
		output/twoBin/scenarioC2_interpCode0_box/muTmuW.root \
		output/twoBin/scenarioD_interpCode0_box/muTmuW.root \
		\
		output/twoBin/scenarioA_interpCode0/muTmuW_profiledContour_template20_etasgeneric20_learning_box1.0.root \
		output/twoBin/scenarioA2_interpCode0/muTmuW_profiledContour_template20_etasgeneric20_learning_box1.0.root \
		output/twoBin/scenarioB_interpCode0/muTmuW_profiledContour_template20_etasgeneric20_learning_box1.0.root \
		output/twoBin/scenarioC_interpCode0/muTmuW_profiledContour_template20_etasgeneric20_learning_box1.0.root \
		output/twoBin/scenarioC2_interpCode0/muTmuW_profiledContour_template20_etasgeneric20_learning_box1.0.root \
		output/twoBin/scenarioD_interpCode0/muTmuW_profiledContour_template20_etasgeneric20_learning_box1.0.root

recoupleTwoBinLearning: \
		output/twoBin/scenarioA/muTmuW_profiledContour_template10_etasgeneric10_learning.root \
		output/twoBin/scenarioA2/muTmuW_profiledContour_template10_etasgeneric10_learning.root \
		output/twoBin/scenarioB/muTmuW_profiledContour_template10_etasgeneric10_learning.root \
		output/twoBin/scenarioC/muTmuW_profiledContour_template10_etasgeneric10_learning.root \
		output/twoBin/scenarioC2/muTmuW_profiledContour_template10_etasgeneric10_learning.root \
		output/twoBin/scenarioD/muTmuW_profiledContour_template10_etasgeneric10_learning.root \
		\
		output/twoBin/scenarioA/muTmuW_profiledContour_template14_etasgeneric14_learning.root \
		output/twoBin/scenarioA2/muTmuW_profiledContour_template14_etasgeneric14_learning.root \
		output/twoBin/scenarioB/muTmuW_profiledContour_template14_etasgeneric14_learning.root \
		output/twoBin/scenarioC/muTmuW_profiledContour_template14_etasgeneric14_learning.root \
		output/twoBin/scenarioC2/muTmuW_profiledContour_template14_etasgeneric14_learning.root \
		output/twoBin/scenarioD/muTmuW_profiledContour_template14_etasgeneric14_learning.root \
		\
		output/twoBin/scenarioA/muTmuW_profiledContour_template20_etasgeneric20_learning.root \
		output/twoBin/scenarioA2/muTmuW_profiledContour_template20_etasgeneric20_learning.root \
		output/twoBin/scenarioB/muTmuW_profiledContour_template20_etasgeneric20_learning.root \
		output/twoBin/scenarioC/muTmuW_profiledContour_template20_etasgeneric20_learning.root \
		output/twoBin/scenarioC2/muTmuW_profiledContour_template20_etasgeneric20_learning.root \
		output/twoBin/scenarioD/muTmuW_profiledContour_template20_etasgeneric20_learning.root \
		\
		output/twoBin/scenarioA/muTmuW_profiledContour_template24_etasgeneric24_learning.root \
		output/twoBin/scenarioA2/muTmuW_profiledContour_template24_etasgeneric24_learning.root \
		output/twoBin/scenarioB/muTmuW_profiledContour_template24_etasgeneric24_learning.root \
		output/twoBin/scenarioC/muTmuW_profiledContour_template24_etasgeneric24_learning.root \
		output/twoBin/scenarioC2/muTmuW_profiledContour_template24_etasgeneric24_learning.root \
		output/twoBin/scenarioD/muTmuW_profiledContour_template24_etasgeneric24_learning.root \
		\
		\
		output/twoBin/twoAlpha_catNonUniversal/muTmuW_profiledContour_template10_etasgeneric10_learning.root \
		output/twoBin/twoAlpha_catNonUniversal/muTmuW_profiledContour_template14_etasgeneric14_learning.root \
		output/twoBin/twoAlpha_catNonUniversal/muTmuW_profiledContour_template20_etasgeneric20_learning.root \
		output/twoBin/twoAlpha_catNonUniversal/muTmuW_profiledContour_template24_etasgeneric24_learning.root \
		\
		output/twoBin/twoAlpha_catNonUniversal_interpCode0/muTmuW_profiledContour_template10_etasgeneric10_learning.root \
		output/twoBin/twoAlpha_catNonUniversal_interpCode0/muTmuW_profiledContour_template14_etasgeneric14_learning.root \
		output/twoBin/twoAlpha_catNonUniversal_interpCode0/muTmuW_profiledContour_template20_etasgeneric20_learning.root \
		output/twoBin/twoAlpha_catNonUniversal_interpCode0/muTmuW_profiledContour_template24_etasgeneric24_learning.root \
		\
		output/twoBin/scenarioA_box/muTmuW.root \
		output/twoBin/scenarioA2_box/muTmuW.root \
		output/twoBin/scenarioB_box/muTmuW.root \
		output/twoBin/scenarioC_box/muTmuW.root \
		output/twoBin/scenarioC2_box/muTmuW.root \
		output/twoBin/scenarioD_box/muTmuW.root \
		\
		output/twoBin/scenarioA/muTmuW_profiledContour_template20_etasgeneric20_learning_box1.0.root \
		output/twoBin/scenarioA2/muTmuW_profiledContour_template20_etasgeneric20_learning_box1.0.root \
		output/twoBin/scenarioB/muTmuW_profiledContour_template20_etasgeneric20_learning_box1.0.root \
		output/twoBin/scenarioC/muTmuW_profiledContour_template20_etasgeneric20_learning_box1.0.root \
		output/twoBin/scenarioC2/muTmuW_profiledContour_template20_etasgeneric20_learning_box1.0.root \
		output/twoBin/scenarioD/muTmuW_profiledContour_template20_etasgeneric20_learning_box1.0.root

recoupleTwoBinInterpCode0: \
		output/twoBin/scenarioA_interpCode0/muTmuW_profiledContour.root \
		output/twoBin/scenarioA2_interpCode0/muTmuW_profiledContour.root \
		output/twoBin/scenarioB_interpCode0/muTmuW_profiledContour.root \
		output/twoBin/scenarioC_interpCode0/muTmuW_profiledContour.root \
		output/twoBin/scenarioC2_interpCode0/muTmuW_profiledContour.root \
		output/twoBin/scenarioD_interpCode0/muTmuW_profiledContour.root \
		\
		output/twoBin/scenarioA_interpCode0/muTmuW_profiledContour_template0.root \
		output/twoBin/scenarioA2_interpCode0/muTmuW_profiledContour_template0.root \
		output/twoBin/scenarioB_interpCode0/muTmuW_profiledContour_template0.root \
		output/twoBin/scenarioC_interpCode0/muTmuW_profiledContour_template0.root \
		output/twoBin/scenarioC2_interpCode0/muTmuW_profiledContour_template0.root \
		output/twoBin/scenarioD_interpCode0/muTmuW_profiledContour_template0.root \
		\
		output/twoBin/scenarioA_interpCode0/muTmuW_profiledContour_templateM1.root \
		output/twoBin/scenarioA2_interpCode0/muTmuW_profiledContour_templateM1.root \
		output/twoBin/scenarioB_interpCode0/muTmuW_profiledContour_templateM1.root \
		output/twoBin/scenarioC_interpCode0/muTmuW_profiledContour_templateM1.root \
		output/twoBin/scenarioC2_interpCode0/muTmuW_profiledContour_templateM1.root \
		output/twoBin/scenarioD_interpCode0/muTmuW_profiledContour_templateM1.root \
		\
		output/twoBin/scenarioA_interpCode0/muTmuW_profiledContour_template10_etasgeneric_M5.root \
		output/twoBin/scenarioA2_interpCode0/muTmuW_profiledContour_template10_etasgeneric_M5.root \
		output/twoBin/scenarioB_interpCode0/muTmuW_profiledContour_template10_etasgeneric_M5.root \
		output/twoBin/scenarioC_interpCode0/muTmuW_profiledContour_template10_etasgeneric_M5.root \
		output/twoBin/scenarioC2_interpCode0/muTmuW_profiledContour_template10_etasgeneric_M5.root \
		output/twoBin/scenarioD_interpCode0/muTmuW_profiledContour_template10_etasgeneric_M5.root \
		\
		output/twoBin/scenarioA_interpCode0/muTmuW_profiledContour_template10_etasgeneric_M5_box1.0.root \
		output/twoBin/scenarioA2_interpCode0/muTmuW_profiledContour_template10_etasgeneric_M5_box1.0.root \
		output/twoBin/scenarioB_interpCode0/muTmuW_profiledContour_template10_etasgeneric_M5_box1.0.root \
		output/twoBin/scenarioC_interpCode0/muTmuW_profiledContour_template10_etasgeneric_M5_box1.0.root \
		output/twoBin/scenarioC2_interpCode0/muTmuW_profiledContour_template10_etasgeneric_M5_box1.0.root \
		output/twoBin/scenarioD_interpCode0/muTmuW_profiledContour_template10_etasgeneric_M5_box1.0.root \
		\
		output/twoBin/scenarioA_interpCode0/muTmuW_profiledContour_template14_etasgeneric_M5.root \
		output/twoBin/scenarioA2_interpCode0/muTmuW_profiledContour_template14_etasgeneric_M5.root \
		output/twoBin/scenarioB_interpCode0/muTmuW_profiledContour_template14_etasgeneric_M5.root \
		output/twoBin/scenarioC_interpCode0/muTmuW_profiledContour_template14_etasgeneric_M5.root \
		output/twoBin/scenarioC2_interpCode0/muTmuW_profiledContour_template14_etasgeneric_M5.root \
		output/twoBin/scenarioD_interpCode0/muTmuW_profiledContour_template14_etasgeneric_M5.root \
		\
		output/twoBin/scenarioA_interpCode0/muTmuW_profiledContour_template14_etasgeneric_fisherInfo.root \
		output/twoBin/scenarioA2_interpCode0/muTmuW_profiledContour_template14_etasgeneric_fisherInfo.root \
		output/twoBin/scenarioB_interpCode0/muTmuW_profiledContour_template14_etasgeneric_fisherInfo.root \
		output/twoBin/scenarioC_interpCode0/muTmuW_profiledContour_template14_etasgeneric_fisherInfo.root \
		output/twoBin/scenarioC2_interpCode0/muTmuW_profiledContour_template14_etasgeneric_fisherInfo.root \
		output/twoBin/scenarioD_interpCode0/muTmuW_profiledContour_template14_etasgeneric_fisherInfo.root \
		\
		output/twoBin/scenarioA_interpCode0/muTmuW_profiledContour_template0_etasfisherInfo_box1.0.root \
		output/twoBin/scenarioA2_interpCode0/muTmuW_profiledContour_template0_etasfisherInfo_box1.0.root \
		output/twoBin/scenarioB_interpCode0/muTmuW_profiledContour_template0_etasfisherInfo_box1.0.root \
		output/twoBin/scenarioC_interpCode0/muTmuW_profiledContour_template0_etasfisherInfo_box1.0.root \
		output/twoBin/scenarioC2_interpCode0/muTmuW_profiledContour_template0_etasfisherInfo_box1.0.root \
		output/twoBin/scenarioD_interpCode0/muTmuW_profiledContour_template0_etasfisherInfo_box1.0.root \
		\
		recoupleTwoBinLearningInterpCode0

recoupleTwoBin: \
		output/twoBin/oneAlpha_catUniversal/muTmuW_profiledContour.root \
		output/twoBin/oneAlpha_catNonUniversal/muTmuW_profiledContour.root \
		output/twoBin/twoAlpha_catUniversal/muTmuW_profiledContour.root \
		output/twoBin/twoAlpha_catNonUniversal/muTmuW_profiledContour.root \
		\
		output/twoBin/oneAlpha_catUniversal/muTmuW_profiledContour_template0.root \
		output/twoBin/oneAlpha_catNonUniversal/muTmuW_profiledContour_template0.root \
		output/twoBin/twoAlpha_catUniversal/muTmuW_profiledContour_template0.root \
		output/twoBin/twoAlpha_catNonUniversal/muTmuW_profiledContour_template0.root \
		\
		output/twoBin/scenarioA/muTmuW_profiledContour.root \
		output/twoBin/scenarioA2/muTmuW_profiledContour.root \
		output/twoBin/scenarioB/muTmuW_profiledContour.root \
		output/twoBin/scenarioC/muTmuW_profiledContour.root \
		output/twoBin/scenarioC2/muTmuW_profiledContour.root \
		output/twoBin/scenarioD/muTmuW_profiledContour.root \
		\
		output/twoBin/scenarioA/muTmuW_profiledContour_template0.root \
		output/twoBin/scenarioA2/muTmuW_profiledContour_template0.root \
		output/twoBin/scenarioB/muTmuW_profiledContour_template0.root \
		output/twoBin/scenarioC/muTmuW_profiledContour_template0.root \
		output/twoBin/scenarioC2/muTmuW_profiledContour_template0.root \
		output/twoBin/scenarioD/muTmuW_profiledContour_template0.root \
		\
		output/twoBin/scenarioA/muTmuW_profiledContour_templateM1.root \
		output/twoBin/scenarioA2/muTmuW_profiledContour_templateM1.root \
		output/twoBin/scenarioB/muTmuW_profiledContour_templateM1.root \
		output/twoBin/scenarioC/muTmuW_profiledContour_templateM1.root \
		output/twoBin/scenarioC2/muTmuW_profiledContour_templateM1.root \
		output/twoBin/scenarioD/muTmuW_profiledContour_templateM1.root \
		\
		output/twoBin/scenarioA/muTmuW_profiledContour_template10_etasgeneric_M5.root \
		output/twoBin/scenarioA2/muTmuW_profiledContour_template10_etasgeneric_M5.root \
		output/twoBin/scenarioB/muTmuW_profiledContour_template10_etasgeneric_M5.root \
		output/twoBin/scenarioC/muTmuW_profiledContour_template10_etasgeneric_M5.root \
		output/twoBin/scenarioC2/muTmuW_profiledContour_template10_etasgeneric_M5.root \
		output/twoBin/scenarioD/muTmuW_profiledContour_template10_etasgeneric_M5.root \
		\
		output/twoBin/scenarioA/muTmuW_profiledContour_template10_etasgeneric_M5_box1.0.root \
		output/twoBin/scenarioA2/muTmuW_profiledContour_template10_etasgeneric_M5_box1.0.root \
		output/twoBin/scenarioB/muTmuW_profiledContour_template10_etasgeneric_M5_box1.0.root \
		output/twoBin/scenarioC/muTmuW_profiledContour_template10_etasgeneric_M5_box1.0.root \
		output/twoBin/scenarioC2/muTmuW_profiledContour_template10_etasgeneric_M5_box1.0.root \
		output/twoBin/scenarioD/muTmuW_profiledContour_template10_etasgeneric_M5_box1.0.root \
		\
		output/twoBin/scenarioA/muTmuW_profiledContour_template14_etasgeneric_M5.root \
		output/twoBin/scenarioA2/muTmuW_profiledContour_template14_etasgeneric_M5.root \
		output/twoBin/scenarioB/muTmuW_profiledContour_template14_etasgeneric_M5.root \
		output/twoBin/scenarioC/muTmuW_profiledContour_template14_etasgeneric_M5.root \
		output/twoBin/scenarioC2/muTmuW_profiledContour_template14_etasgeneric_M5.root \
		output/twoBin/scenarioD/muTmuW_profiledContour_template14_etasgeneric_M5.root \
		\
		output/twoBin/scenarioA/muTmuW_profiledContour_template14_etasgeneric_fisherInfo.root \
		output/twoBin/scenarioA2/muTmuW_profiledContour_template14_etasgeneric_fisherInfo.root \
		output/twoBin/scenarioB/muTmuW_profiledContour_template14_etasgeneric_fisherInfo.root \
		output/twoBin/scenarioC/muTmuW_profiledContour_template14_etasgeneric_fisherInfo.root \
		output/twoBin/scenarioC2/muTmuW_profiledContour_template14_etasgeneric_fisherInfo.root \
		output/twoBin/scenarioD/muTmuW_profiledContour_template14_etasgeneric_fisherInfo.root \
		\
		output/twoBin/scenarioA/muTmuW_profiledContour_template0_etasfisherInfo_box1.0.root \
		output/twoBin/scenarioA2/muTmuW_profiledContour_template0_etasfisherInfo_box1.0.root \
		output/twoBin/scenarioB/muTmuW_profiledContour_template0_etasfisherInfo_box1.0.root \
		output/twoBin/scenarioC/muTmuW_profiledContour_template0_etasfisherInfo_box1.0.root \
		output/twoBin/scenarioC2/muTmuW_profiledContour_template0_etasfisherInfo_box1.0.root \
		output/twoBin/scenarioD/muTmuW_profiledContour_template0_etasfisherInfo_box1.0.root \
		\
		recoupleTwoBinLearning


OPTIONS_2PH = --options_muTmuW='--range=0.6,0.5,2.6,3.6 --bins=250,250' --skip_kVkF --skip_kGlukGamma
output/atlas_counting/2ph/muTmuW_profiledContour.root: output/atlas_counting/2ph/muTmuW_eff.root
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:2 $(OPTIONS_2PH)
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:2 $(OPTIONS_2PH) --template=0
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:2 $(OPTIONS_2PH) --template=-1
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:generic_M4:2 $(OPTIONS_2PH) --template=14
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:generic_M4:2 $(OPTIONS_2PH) --template=14 --box=1
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:generic_M5:2 $(OPTIONS_2PH) --template=14
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:generic_M5:2 $(OPTIONS_2PH) --template=14 --box=1
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:generic_M5:2 $(OPTIONS_2PH) --template=10
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:generic_M5:2 $(OPTIONS_2PH) --template=10 --box=1

	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:generic10_learning:2 $(OPTIONS_2PH) --template=10
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:generic10_learning:2 $(OPTIONS_2PH) --template=10 --box=1
	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:generic14_learning:2 $(OPTIONS_2PH) --template=14
	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:generic14_learning:2 $(OPTIONS_2PH) --template=14 --box=1
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:generic20_learning:2 $(OPTIONS_2PH) --template=20
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:generic20_learning:2 $(OPTIONS_2PH) --template=20 --box=1
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:generic24_learning:2 $(OPTIONS_2PH) --template=24
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:generic24_learning:2 $(OPTIONS_2PH) --template=24 --box=1

OPTIONS_4L = --options_muTmuW='--range=0.4,-2.0,3.0,6.2 --bins=100,200' --skip_kVkF --skip_kGlukGamma
output/atlas_counting/4l/muTmuW_profiledContour.root: output/atlas_counting/4l/muTmuW_eff.root
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l/table_etas.pickle:2 $(OPTIONS_4L)
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l/table_etas.pickle:2 $(OPTIONS_4L) --template=0
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l/table_etas.pickle:2 $(OPTIONS_4L) --template=-1
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l/table_etas.pickle:generic_M4:2 $(OPTIONS_4L) --template=14
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l/table_etas.pickle:generic_M4:2 $(OPTIONS_4L) --template=14 --box=1.0
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l/table_etas.pickle:generic_M5:2 $(OPTIONS_4L) --template=14
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l/table_etas.pickle:generic_M5:2 $(OPTIONS_4L) --template=14 --box=1.0
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l/table_etas.pickle:generic_M5:2 $(OPTIONS_4L) --template=10
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l/table_etas.pickle:generic_M5:2 $(OPTIONS_4L) --template=10 --box=1.0

	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l/table_etas.pickle:generic10_learning:2 $(OPTIONS_4L) --template=10
	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l/table_etas.pickle:generic10_learning:2 $(OPTIONS_4L) --template=10 --box=1.0
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l/table_etas.pickle:generic14_learning:2 $(OPTIONS_4L) --template=14
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l/table_etas.pickle:generic14_learning:2 $(OPTIONS_4L) --template=14 --box=1.0
	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l/table_etas.pickle:generic20_learning:2 $(OPTIONS_4L) --template=20
	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l/table_etas.pickle:generic20_learning:2 $(OPTIONS_4L) --template=20 --box=1.0
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l/table_etas.pickle:generic24_learning:2 $(OPTIONS_4L) --template=24
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l/table_etas.pickle:generic24_learning:2 $(OPTIONS_4L) --template=24 --box=1.0

OPTIONS_LVLV = --options_muTmuW='--range=0.0,0.0,1.9,3.8 --bins=160,160' --skip_kVkF --skip_kGlukGamma
output/atlas_counting/lvlv/muTmuW_profiledContour.root: output/atlas_counting/lvlv/muTmuW_eff.root
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:2 $(OPTIONS_LVLV)
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:2 $(OPTIONS_LVLV) --template=0
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:2 $(OPTIONS_LVLV) --template=-1
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:generic_M4:2 $(OPTIONS_LVLV) --template=14
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:generic_M4:2 $(OPTIONS_LVLV) --template=14 --box=1.0
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:generic_M5:2 $(OPTIONS_LVLV) --template=14
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:generic_M5:2 $(OPTIONS_LVLV) --template=14 --box=1.0
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:generic_M5:2 $(OPTIONS_LVLV) --template=10
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:generic_M5:2 $(OPTIONS_LVLV) --template=10 --box=1.0

	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:generic10_learning:2 $(OPTIONS_LVLV) --template=10
	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:generic10_learning:2 $(OPTIONS_LVLV) --template=10 --box=1.0
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:generic14_learning:2 $(OPTIONS_LVLV) --template=14
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:generic14_learning:2 $(OPTIONS_LVLV) --template=14 --box=1.0
	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:generic20_learning:2 $(OPTIONS_LVLV) --template=20
	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:generic20_learning:2 $(OPTIONS_LVLV) --template=20 --box=1.0
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:generic24_learning:2 $(OPTIONS_LVLV) --template=24
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:generic24_learning:2 $(OPTIONS_LVLV) --template=24 --box=1.0


output/atlas_counting/2ph_interpCode0/muTmuW_profiledContour.root: output/atlas_counting/2ph_interpCode0/muTmuW_eff.root
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph_interpCode0/table_etas.pickle:fisherInfo:2 $(OPTIONS_2PH) --template=0
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph_interpCode0/table_etas.pickle:generic_M5:2 $(OPTIONS_2PH) --template=10
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph_interpCode0/table_etas.pickle:generic_M5:2 $(OPTIONS_2PH) --template=10 --box=1
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph_interpCode0/table_etas.pickle:generic_M5:2 $(OPTIONS_2PH) --template=10 --wideGauss=1.3

	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph_interpCode0/table_etas.pickle:generic10_learning:2 $(OPTIONS_2PH) --template=10
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph_interpCode0/table_etas.pickle:generic10_learning:2 $(OPTIONS_2PH) --template=10 --box=1
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph_interpCode0/table_etas.pickle:generic20_learning:2 $(OPTIONS_2PH) --template=20
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph_interpCode0/table_etas.pickle:generic20_learning:2 $(OPTIONS_2PH) --template=20 --box=1

	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph_interpCode0/table_etas.pickle:generic10_learningFull:2 $(OPTIONS_2PH) --template=10
	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph_interpCode0/table_etas.pickle:generic10_learningFull:2 $(OPTIONS_2PH) --template=10 --box=1
	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph_interpCode0/table_etas.pickle:generic20_learningFull:2 $(OPTIONS_2PH) --template=20
	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/2ph_interpCode0/table_etas.pickle:generic20_learningFull:2 $(OPTIONS_2PH) --template=20 --box=1

output/atlas_counting/4l_interpCode0/muTmuW_profiledContour.root: output/atlas_counting/4l_interpCode0/muTmuW_eff.root
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l_interpCode0/table_etas.pickle:fisherInfo:2 $(OPTIONS_4L) --template=0
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l_interpCode0/table_etas.pickle:generic_M5:2 $(OPTIONS_4L) --template=10
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l_interpCode0/table_etas.pickle:generic_M5:2 $(OPTIONS_4L) --template=10 --box=1
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l_interpCode0/table_etas.pickle:generic_M5:2 $(OPTIONS_4L) --template=10 --wideGauss=1.3

	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l_interpCode0/table_etas.pickle:generic10_learning:2 $(OPTIONS_4L) --template=10
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l_interpCode0/table_etas.pickle:generic10_learning:2 $(OPTIONS_4L) --template=10 --box=1.0
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l_interpCode0/table_etas.pickle:generic20_learning:2 $(OPTIONS_4L) --template=20
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l_interpCode0/table_etas.pickle:generic20_learning:2 $(OPTIONS_4L) --template=20 --box=1.0

	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l_interpCode0/table_etas.pickle:generic10_learningFull:2 $(OPTIONS_4L) --template=10
	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l_interpCode0/table_etas.pickle:generic10_learningFull:2 $(OPTIONS_4L) --template=10 --box=1.0
	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l_interpCode0/table_etas.pickle:generic20_learningFull:2 $(OPTIONS_4L) --template=20
	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/4l_interpCode0/table_etas.pickle:generic20_learningFull:2 $(OPTIONS_4L) --template=20 --box=1.0

output/atlas_counting/lvlv_interpCode0/muTmuW_profiledContour.root: output/atlas_counting/lvlv_interpCode0/muTmuW_eff.root
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv_interpCode0/table_etas.pickle:fisherInfo:2 $(OPTIONS_LVLV) --template=0
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv_interpCode0/table_etas.pickle:generic_M5:2 $(OPTIONS_LVLV) --template=10
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv_interpCode0/table_etas.pickle:generic_M5:2 $(OPTIONS_LVLV) --template=10 --box=1
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv_interpCode0/table_etas.pickle:generic_M5:2 $(OPTIONS_LVLV) --template=10 --wideGauss=1.3

	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv_interpCode0/table_etas.pickle:generic10_learning:2 $(OPTIONS_LVLV) --template=10
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv_interpCode0/table_etas.pickle:generic10_learning:2 $(OPTIONS_LVLV) --template=10 --box=1.0
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv_interpCode0/table_etas.pickle:generic20_learning:2 $(OPTIONS_LVLV) --template=20
	# python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv_interpCode0/table_etas.pickle:generic20_learning:2 $(OPTIONS_LVLV) --template=20 --box=1.0

	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv_interpCode0/table_etas.pickle:generic10_learningFull:2 $(OPTIONS_LVLV) --template=10
	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv_interpCode0/table_etas.pickle:generic10_learningFull:2 $(OPTIONS_LVLV) --template=10 --box=1.0
	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv_interpCode0/table_etas.pickle:generic20_learningFull:2 $(OPTIONS_LVLV) --template=20
	python Decouple/recouple.py -i $<:profiledNLL:output/atlas_counting/lvlv_interpCode0/table_etas.pickle:generic20_learningFull:2 $(OPTIONS_LVLV) --template=20 --box=1.0


# shifted contour: place holder is variable
shiftedAtlasCounting: output/atlas_counting/2ph/muTmuW_eff.root output/atlas_counting/4l/muTmuW_eff.root output/atlas_counting/lvlv/muTmuW_eff.root
	python Decouple/src/muTmuW.py -i output/atlas_counting/2ph/muTmuW_eff.root:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:fisherInfo:2 -o output/atlas_counting/2ph/muTmuW_eff.root --template=0 --range=0.6,0.5,2.6,3.6 --bins=250,250 --setParameter=alpha_QCDscale_Higgs_ggH=0.0
	python Decouple/src/muTmuW.py -i output/atlas_counting/2ph/muTmuW_eff.root:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:fisherInfo:2 -o output/atlas_counting/2ph/muTmuW_eff.root --template=0 --range=0.6,0.5,2.6,3.6 --bins=250,250 --setParameter=alpha_QCDscale_Higgs_ggH=1.0

	python Decouple/src/muTmuW.py -i output/atlas_counting/4l/muTmuW_eff.root:profiledNLL:output/atlas_counting/4l/table_etas.pickle:fisherInfo:2 -o output/atlas_counting/4l/muTmuW_eff.root --template=0 --range=0.4,-2.0,3.0,6.2 --bins=100,200 --setParameter=alpha_QCDscale_Higgs_ggH=0.0
	python Decouple/src/muTmuW.py -i output/atlas_counting/4l/muTmuW_eff.root:profiledNLL:output/atlas_counting/4l/table_etas.pickle:fisherInfo:2 -o output/atlas_counting/4l/muTmuW_eff.root --template=0 --range=0.4,-2.0,3.0,6.2 --bins=100,200 --setParameter=alpha_QCDscale_Higgs_ggH=1.0

	python Decouple/src/muTmuW.py -i output/atlas_counting/lvlv/muTmuW_eff.root:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:fisherInfo:2 -o output/atlas_counting/lvlv/muTmuW_eff.root --template=0 --range=0.0,0.0,1.9,3.8 --bins=160,160 --setParameter=alpha_QCDscale_Higgs_ggH=0.0
	python Decouple/src/muTmuW.py -i output/atlas_counting/lvlv/muTmuW_eff.root:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:fisherInfo:2 -o output/atlas_counting/lvlv/muTmuW_eff.root --template=0 --range=0.0,0.0,1.9,3.8 --bins=160,160 --setParameter=alpha_QCDscale_Higgs_ggH=1.0

shiftedAtlasCountingInterpCode0: output/atlas_counting/2ph_interpCode0/muTmuW_eff.root output/atlas_counting/4l_interpCode0/muTmuW_eff.root output/atlas_counting/lvlv_interpCode0/muTmuW_eff.root
	python Decouple/src/muTmuW.py -i output/atlas_counting/2ph_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/2ph_interpCode0/table_etas.pickle:fisherInfo:2 -o output/atlas_counting/2ph_interpCode0/muTmuW_eff.root --template=0 --range=0.6,0.5,2.6,3.6 --bins=250,250 --setParameter=alpha_QCDscale_Higgs_ggH=0.0
	python Decouple/src/muTmuW.py -i output/atlas_counting/2ph_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/2ph_interpCode0/table_etas.pickle:fisherInfo:2 -o output/atlas_counting/2ph_interpCode0/muTmuW_eff.root --template=0 --range=0.6,0.5,2.6,3.6 --bins=250,250 --setParameter=alpha_QCDscale_Higgs_ggH=1.0

	python Decouple/src/muTmuW.py -i output/atlas_counting/4l_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/4l_interpCode0/table_etas.pickle:fisherInfo:2 -o output/atlas_counting/4l_interpCode0/muTmuW_eff.root --template=0 --range=0.4,-2.0,3.0,6.2 --bins=200,400 --setParameter=alpha_QCDscale_Higgs_ggH=0.0
	python Decouple/src/muTmuW.py -i output/atlas_counting/4l_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/4l_interpCode0/table_etas.pickle:fisherInfo:2 -o output/atlas_counting/4l_interpCode0/muTmuW_eff.root --template=0 --range=0.4,-2.0,3.0,6.2 --bins=200,400 --setParameter=alpha_QCDscale_Higgs_ggH=1.0

	python Decouple/src/muTmuW.py -i output/atlas_counting/lvlv_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/lvlv_interpCode0/table_etas.pickle:fisherInfo:2 -o output/atlas_counting/lvlv_interpCode0/muTmuW_eff.root --template=0 --range=0.0,0.0,1.9,3.8 --bins=250,250 --setParameter=alpha_QCDscale_Higgs_ggH=0.0
	python Decouple/src/muTmuW.py -i output/atlas_counting/lvlv_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/lvlv_interpCode0/table_etas.pickle:fisherInfo:2 -o output/atlas_counting/lvlv_interpCode0/muTmuW_eff.root --template=0 --range=0.0,0.0,1.9,3.8 --bins=250,250 --setParameter=alpha_QCDscale_Higgs_ggH=1.0


COMBINPUT  = output/atlas_counting/2ph/muTmuW_eff.root:profiledNLL:output/atlas_counting/2ph/table_etas.pickle:generic20_learning:2
COMBINPUT += output/atlas_counting/4l/muTmuW_eff.root:profiledNLL:output/atlas_counting/4l/table_etas.pickle:generic20_learning:2
COMBINPUT += output/atlas_counting/lvlv/muTmuW_eff.root:profiledNLL:output/atlas_counting/lvlv/table_etas.pickle:generic20_learning:2
OPTIONS_COMB = --skip_muTmuW --options_kVkF='--range=0.65,-1.7,1.5,2.0 --bins=200,200' --options_kGlukGamma='--range=0.6,0.4,1.8,1.6 --bins=200,200'
output/atlas_counting/2ph_4l_lvlv/kVkF_profiledContour.root: output/atlas_counting/2ph/muTmuW_eff.root output/atlas_counting/4l/muTmuW_eff.root output/atlas_counting/lvlv/muTmuW_eff.root
	@echo "For combination, using as input: "+$(COMBINPUT)
	python Decouple/recouple.py -i "$(COMBINPUT)" -o output/atlas_counting/2ph_4l_lvlv/ $(OPTIONS_COMB) --template=20
	python Decouple/recouple.py -i "$(COMBINPUT)" -o output/atlas_counting/2ph_4l_lvlv/ $(OPTIONS_COMB) --template=20 --box=1.0

COMBINPUT_INTERPCODE0  = output/atlas_counting/2ph_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/2ph_interpCode0/table_etas.pickle:generic20_learning:2
COMBINPUT_INTERPCODE0 += output/atlas_counting/4l_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/4l_interpCode0/table_etas.pickle:generic20_learning:2
COMBINPUT_INTERPCODE0 += output/atlas_counting/lvlv_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/lvlv_interpCode0/table_etas.pickle:generic20_learning:2
COMBINPUT_INTERPCODE0T10  = output/atlas_counting/2ph_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/2ph_interpCode0/table_etas.pickle:generic10_learning:2
COMBINPUT_INTERPCODE0T10 += output/atlas_counting/4l_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/4l_interpCode0/table_etas.pickle:generic10_learning:2
COMBINPUT_INTERPCODE0T10 += output/atlas_counting/lvlv_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/lvlv_interpCode0/table_etas.pickle:generic10_learning:2
COMBINPUT_INTERPCODE0FULL  = output/atlas_counting/2ph_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/2ph_interpCode0/table_etas.pickle:generic20_learningFull:2
COMBINPUT_INTERPCODE0FULL += output/atlas_counting/4l_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/4l_interpCode0/table_etas.pickle:generic20_learningFull:2
COMBINPUT_INTERPCODE0FULL += output/atlas_counting/lvlv_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/lvlv_interpCode0/table_etas.pickle:generic20_learningFull:2
COMBINPUT_INTERPCODE0T10FULL  = output/atlas_counting/2ph_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/2ph_interpCode0/table_etas.pickle:generic10_learningFull:2
COMBINPUT_INTERPCODE0T10FULL += output/atlas_counting/4l_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/4l_interpCode0/table_etas.pickle:generic10_learningFull:2
COMBINPUT_INTERPCODE0T10FULL += output/atlas_counting/lvlv_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/lvlv_interpCode0/table_etas.pickle:generic10_learningFull:2
COMBINPUT_INTERPCODE0M5  = output/atlas_counting/2ph_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/2ph_interpCode0/table_etas.pickle:generic_M5:2
COMBINPUT_INTERPCODE0M5 += output/atlas_counting/4l_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/4l_interpCode0/table_etas.pickle:generic_M5:2
COMBINPUT_INTERPCODE0M5 += output/atlas_counting/lvlv_interpCode0/muTmuW_eff.root:profiledNLL:output/atlas_counting/lvlv_interpCode0/table_etas.pickle:generic_M5:2
output/atlas_counting/2ph_4l_lvlv_interpCode0/kVkF_profiledContour.root: output/atlas_counting/2ph_interpCode0/muTmuW_eff.root output/atlas_counting/4l_interpCode0/muTmuW_eff.root output/atlas_counting/lvlv_interpCode0/muTmuW_eff.root
	# @echo "For combination, using as input: "+$(COMBINPUT_INTERPCODE0)
	# python Decouple/recouple.py -i "$(COMBINPUT_INTERPCODE0)" -o output/atlas_counting/2ph_4l_lvlv_interpCode0/ $(OPTIONS_COMB) --template=20
	# python Decouple/recouple.py -i "$(COMBINPUT_INTERPCODE0)" -o output/atlas_counting/2ph_4l_lvlv_interpCode0/ $(OPTIONS_COMB) --template=20 --box=1.0
	# @echo "For combination, using as input: "+$(COMBINPUT_INTERPCODE0T10)
	# python Decouple/recouple.py -i "$(COMBINPUT_INTERPCODE0T10)" -o output/atlas_counting/2ph_4l_lvlv_interpCode0/ $(OPTIONS_COMB) --template=10
	# python Decouple/recouple.py -i "$(COMBINPUT_INTERPCODE0T10)" -o output/atlas_counting/2ph_4l_lvlv_interpCode0/ $(OPTIONS_COMB) --template=10 --box=1.0
	@echo "For combination, using as input: "+$(COMBINPUT_INTERPCODE0FULL)
	python Decouple/recouple.py -i "$(COMBINPUT_INTERPCODE0FULL)" -o output/atlas_counting/2ph_4l_lvlv_interpCode0/ $(OPTIONS_COMB) --template=20
	python Decouple/recouple.py -i "$(COMBINPUT_INTERPCODE0FULL)" -o output/atlas_counting/2ph_4l_lvlv_interpCode0/ $(OPTIONS_COMB) --template=20 --box=1.0
	python Decouple/recouple.py -i "$(COMBINPUT_INTERPCODE0FULL)" -o output/atlas_counting/2ph_4l_lvlv_interpCode0/ $(OPTIONS_COMB) --template=20 --wideGauss=1.3
	@echo "For combination, using as input: "+$(COMBINPUT_INTERPCODE0T10FULL)
	python Decouple/recouple.py -i "$(COMBINPUT_INTERPCODE0T10FULL)" -o output/atlas_counting/2ph_4l_lvlv_interpCode0/ $(OPTIONS_COMB) --template=10
	python Decouple/recouple.py -i "$(COMBINPUT_INTERPCODE0T10FULL)" -o output/atlas_counting/2ph_4l_lvlv_interpCode0/ $(OPTIONS_COMB) --template=10 --box=1.0
	python Decouple/recouple.py -i "$(COMBINPUT_INTERPCODE0T10FULL)" -o output/atlas_counting/2ph_4l_lvlv_interpCode0/ $(OPTIONS_COMB) --template=10 --wideGauss=1.3
	# @echo "For combination, using as input: "+$(COMBINPUT_INTERPCODE0M5)
	# python Decouple/recouple.py -i "$(COMBINPUT_INTERPCODE0M5)" -o output/atlas_counting/2ph_4l_lvlv_interpCode0/ $(OPTIONS_COMB) --template=10
	# python Decouple/recouple.py -i "$(COMBINPUT_INTERPCODE0M5)" -o output/atlas_counting/2ph_4l_lvlv_interpCode0/ $(OPTIONS_COMB) --template=10 --box=1.0
	# python Decouple/recouple.py -i "$(COMBINPUT_INTERPCODE0M5)" -o output/atlas_counting/2ph_4l_lvlv_interpCode0/ $(OPTIONS_COMB) --template=10 --wideGauss=1.3


COMBINPUT_INTERPCODE0_NAIVE  = output/atlas_counting/2ph_interpCode0/muTmuW.root:profiledNLL:None:None:2
COMBINPUT_INTERPCODE0_NAIVE += output/atlas_counting/4l_interpCode0/muTmuW.root:profiledNLL:None:None:2
COMBINPUT_INTERPCODE0_NAIVE += output/atlas_counting/lvlv_interpCode0/muTmuW.root:profiledNLL:None:None:2
output/atlas_counting/2ph_4l_lvlv_interpCode0_naive/kVkF_profiledContour.root: output/atlas_counting/2ph_interpCode0/muTmuW_eff.root output/atlas_counting/4l_interpCode0/muTmuW_eff.root output/atlas_counting/lvlv_interpCode0/muTmuW_eff.root
	@echo "For combination, using as input: "+$(COMBINPUT_INTERPCODE0_NAIVE)
	python Decouple/recouple.py -i "$(COMBINPUT_INTERPCODE0_NAIVE)" -o output/atlas_counting/2ph_4l_lvlv_interpCode0/ $(OPTIONS_COMB) --template=20



output/atlas_counting/2ph_4l_lvlv%/kVkF.root: output/atlas_counting/comb%.root
	@echo "\n=== Doing a box constraint fullCountingModelScan for kVkF"
	mkdir -p output/atlas_counting/2ph_4l_lvlv$*/
	python Decouple/src/fullCountingModelScan_kVkF.py -i $< -o $@

output/atlas_counting/2ph_4l_lvlv%/kGlukGamma.root: output/atlas_counting/comb%.root
	@echo "\n=== Doing a box constraint fullCountingModelScan for kGlukGamma"
	mkdir -p output/atlas_counting/2ph_4l_lvlv$*/
	python Decouple/src/fullCountingModelScan_kGlukGamma.py -i $< -o $@

output/atlas_counting/2ph_4l_lvlv/kVkF.root: output/atlas_counting/comb.root
	@echo "\n=== Doing a fullCountingModelScan for kVkF"
	mkdir -p output/atlas_counting/2ph_4l_lvlv/
	python Decouple/src/fullCountingModelScan_kVkF.py -i $< -o $@

output/atlas_counting/2ph_4l_lvlv/kGlukGamma.root: output/atlas_counting/comb.root
	@echo "\n=== Doing a fullCountingModelScan for kGlukGamma"
	mkdir -p output/atlas_counting/2ph_4l_lvlv/
	python Decouple/src/fullCountingModelScan_kGlukGamma.py -i $< -o $@


recoupleAtlasCountingInterpCode0Channels: \
		output/atlas_counting/2ph_interpCode0/muTmuW_profiledContour.root \
		output/atlas_counting/4l_interpCode0/muTmuW_profiledContour.root \
		output/atlas_counting/lvlv_interpCode0/muTmuW_profiledContour.root

recoupleAtlasCountingInterpCode0: \
		recoupleAtlasCountingInterpCode0Channels \
		\
		output/atlas_counting/2ph_4l_lvlv_interpCode0/kVkF.root \
		output/atlas_counting/2ph_4l_lvlv_interpCode0/kGlukGamma.root \
		output/atlas_counting/2ph_4l_lvlv_interpCode0_box/kVkF.root \
		output/atlas_counting/2ph_4l_lvlv_interpCode0_box/kGlukGamma.root \
		output/atlas_counting/2ph_4l_lvlv_interpCode0_wideGauss/kVkF.root \
		output/atlas_counting/2ph_4l_lvlv_interpCode0_wideGauss/kGlukGamma.root \
		\
		shiftedAtlasCountingInterpCode0 \
		output/atlas_counting/2ph_4l_lvlv_interpCode0/kVkF_profiledContour.root \
		output/atlas_counting/2ph_4l_lvlv_interpCode0_naive/kVkF_profiledContour.root

recoupleAtlasCountingChannels: \
		output/atlas_counting/2ph/muTmuW_profiledContour.root \
		output/atlas_counting/4l/muTmuW_profiledContour.root \
		output/atlas_counting/lvlv/muTmuW_profiledContour.root

recoupleAtlasCounting: \
		recoupleAtlasCountingChannels \
		\
		output/atlas_counting/2ph_4l_lvlv/kVkF.root \
		output/atlas_counting/2ph_4l_lvlv/kGlukGamma.root \
		output/atlas_counting/2ph_4l_lvlv_box/kVkF.root \
		output/atlas_counting/2ph_4l_lvlv_box/kGlukGamma.root \
		output/atlas_counting/2ph_4l_lvlv/kVkF_profiledContour.root \
		output/atlas_counting/2ph_4l_lvlv_naive/kVkF_profiledContour.root \
		\
		shiftedAtlasCounting





######################################################
# plots

plotTwoBin:
	@echo "\n=== Making all two bin plots. ==="
	python Plot/plotTwoBin.py

	python Plot/etas.py -i output/twoBin/scenarioA/table_etas.pickle -o plots/twoBin/scenarioA_etas/
	python Plot/etas.py -i output/twoBin/scenarioA2/table_etas.pickle -o plots/twoBin/scenarioA2_etas/
	python Plot/etas.py -i output/twoBin/scenarioB/table_etas.pickle -o plots/twoBin/scenarioB_etas/
	python Plot/etas.py -i output/twoBin/scenarioC/table_etas.pickle -o plots/twoBin/scenarioC_etas/
	python Plot/etas.py -i output/twoBin/scenarioC2/table_etas.pickle -o plots/twoBin/scenarioC2_etas/
	python Plot/etas.py -i output/twoBin/scenarioD/table_etas.pickle -o plots/twoBin/scenarioD_etas/

	python Plot/etas.py -i output/twoBin/scenarioA_interpCode0/table_etas.pickle -o plots/twoBin/scenarioA_interpCode0_etas/
	python Plot/etas.py -i output/twoBin/scenarioA2_interpCode0/table_etas.pickle -o plots/twoBin/scenarioA2_interpCode0_etas/
	python Plot/etas.py -i output/twoBin/scenarioB_interpCode0/table_etas.pickle -o plots/twoBin/scenarioB_interpCode0_etas/
	python Plot/etas.py -i output/twoBin/scenarioC_interpCode0/table_etas.pickle -o plots/twoBin/scenarioC_interpCode0_etas/
	python Plot/etas.py -i output/twoBin/scenarioC2_interpCode0/table_etas.pickle -o plots/twoBin/scenarioC2_interpCode0_etas/
	python Plot/etas.py -i output/twoBin/scenarioD_interpCode0/table_etas.pickle -o plots/twoBin/scenarioD_interpCode0_etas/


plotAtlasCounting:
	@echo "\n=== Making all ATLAS counting plots. ==="
	python Plot/plotAtlasCounting.py

	# python Plot/etas.py -i output/atlas_counting/2ph/table_etas.pickle -o plots/atlas_counting/2ph_etas/
	# python Plot/etas.py -i output/atlas_counting/4l/table_etas.pickle -o plots/atlas_counting/4l_etas/
	# python Plot/etas.py -i output/atlas_counting/lvlv/table_etas.pickle -o plots/atlas_counting/lvlv_etas/

	python Plot/etas.py -i output/atlas_counting/2ph_interpCode0/table_etas.pickle -o plots/atlas_counting/2ph_interpCode0_etas/
	python Plot/etas.py -i output/atlas_counting/4l_interpCode0/table_etas.pickle -o plots/atlas_counting/4l_interpCode0_etas/
	python Plot/etas.py -i output/atlas_counting/lvlv_interpCode0/table_etas.pickle -o plots/atlas_counting/lvlv_interpCode0_etas/

	# python Plot/npComparison.py -i output/atlas_counting/2ph/ -o plots/atlas_counting/2ph_npTemplate10/ -s _template10_etasgeneric10_learning
	# python Plot/npComparison.py -i output/atlas_counting/2ph/ -o plots/atlas_counting/2ph_npTemplate14/ -s _template14_etasgeneric14_learning
	# python Plot/npComparison.py -i output/atlas_counting/2ph/ -o plots/atlas_counting/2ph_npTemplate20/ -s _template20_etasgeneric20_learning
	# python Plot/npComparison.py -i output/atlas_counting/2ph/ -o plots/atlas_counting/2ph_npTemplate24/ -s _template24_etasgeneric24_learning

	# python Plot/npComparison.py -i output/atlas_counting/4l/ -o plots/atlas_counting/4l_npTemplate10/ -s _template10_etasgeneric10_learning
	# python Plot/npComparison.py -i output/atlas_counting/4l/ -o plots/atlas_counting/4l_npTemplate14/ -s _template14_etasgeneric14_learning
	# python Plot/npComparison.py -i output/atlas_counting/4l/ -o plots/atlas_counting/4l_npTemplate20/ -s _template20_etasgeneric20_learning
	# python Plot/npComparison.py -i output/atlas_counting/4l/ -o plots/atlas_counting/4l_npTemplate24/ -s _template24_etasgeneric24_learning

	# python Plot/npComparison.py -i output/atlas_counting/2ph/ -o plots/atlas_counting/2ph_npTemplate10/ -s _template10_etasgeneric10_learning
	# python Plot/npComparison.py -i output/atlas_counting/2ph/ -o plots/atlas_counting/2ph_npTemplate14/ -s _template14_etasgeneric14_learning
	# python Plot/npComparison.py -i output/atlas_counting/2ph/ -o plots/atlas_counting/2ph_npTemplate20/ -s _template20_etasgeneric20_learning
	# python Plot/npComparison.py -i output/atlas_counting/2ph/ -o plots/atlas_counting/2ph_npTemplate24/ -s _template24_etasgeneric24_learning

	python Plot/npComparison.py -i output/atlas_counting/2ph_interpCode0/ -o plots/atlas_counting/2ph_interpCode0_npM5/ -s _template10_etasgeneric_M5
	python Plot/npComparison.py -i output/atlas_counting/2ph_interpCode0/ -o plots/atlas_counting/2ph_interpCode0_npTemplate10/ -s _template10_etasgeneric10_learning
	python Plot/npComparison.py -i output/atlas_counting/2ph_interpCode0/ -o plots/atlas_counting/2ph_interpCode0_npTemplate20/ -s _template20_etasgeneric20_learning

	python Plot/npComparison.py -i output/atlas_counting/2ph_interpCode0/ -o plots/atlas_counting/2ph_interpCode0_box_npTemplate20/ -s _template20_etasgeneric20_learning_box1.0 -f output/atlas_counting/2ph_interpCode0_box/

	python Plot/npComparison.py -i output/atlas_counting/4l_interpCode0/ -o plots/atlas_counting/4l_interpCode0_npM5/ -s _template10_etasgeneric_M5
	python Plot/npComparison.py -i output/atlas_counting/4l_interpCode0/ -o plots/atlas_counting/4l_interpCode0_npTemplate10/ -s _template10_etasgeneric10_learning
	python Plot/npComparison.py -i output/atlas_counting/4l_interpCode0/ -o plots/atlas_counting/4l_interpCode0_npTemplate20/ -s _template20_etasgeneric20_learning

	python Plot/npComparison.py -i output/atlas_counting/lvlv_interpCode0/ -o plots/atlas_counting/lvlv_interpCode0_npM5/ -s _template10_etasgeneric_M5
	python Plot/npComparison.py -i output/atlas_counting/lvlv_interpCode0/ -o plots/atlas_counting/lvlv_interpCode0_npTemplate10/ -s _template10_etasgeneric10_learning
	python Plot/npComparison.py -i output/atlas_counting/lvlv_interpCode0/ -o plots/atlas_counting/lvlv_interpCode0_npTemplate20/ -s _template20_etasgeneric20_learning




######################################################
# other

plots/interpCodes/%.eps:
	mkdir -p plots/interpCodes
	python Plot/plotInterpCode.py -c $* -o $@

studyInterpCodes: \
	plots/interpCodes/0.eps \
	plots/interpCodes/1.eps \
	plots/interpCodes/2.eps \
	plots/interpCodes/3.eps \
	plots/interpCodes/4.eps


