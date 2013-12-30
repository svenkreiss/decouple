
# 26 Nov 2013
# Sven Kreiss, Kyle Cranmer

all: twoBin atlas_counting



twoBin:
	@echo "\n=== Making two bin counting models. ==="
	python twoBinCountingModel.py --scenario=-1 --name=oneAlpha_catUniversal
	python twoBinCountingModel.py --scenario=-2 --name=oneAlpha_catNonUniversal
	python twoBinCountingModel.py --scenario=-3 --name=twoAlpha_catUniversal
	python twoBinCountingModel.py --scenario=-4 --name=twoAlpha_catNonUniversal

	python twoBinCountingModel.py --scenario=1 --name=scenarioA
	python twoBinCountingModel.py --scenario=1.1 --name=scenarioA2
	python twoBinCountingModel.py --scenario=2 --name=scenarioB
	python twoBinCountingModel.py --scenario=3 --name=scenarioC
	python twoBinCountingModel.py --scenario=3.1 --name=scenarioC2
	python twoBinCountingModel.py --scenario=4 --name=scenarioD

	python twoBinCountingModel.py --scenario=1 --additiveMu --name=scenarioA_additiveMu
	python twoBinCountingModel.py --scenario=1.1 --additiveMu --name=scenarioA2_additiveMu
	python twoBinCountingModel.py --scenario=2 --additiveMu --name=scenarioB_additiveMu
	python twoBinCountingModel.py --scenario=3 --additiveMu --name=scenarioC_additiveMu
	python twoBinCountingModel.py --scenario=3.1 --additiveMu --name=scenarioC2_additiveMu
	python twoBinCountingModel.py --scenario=4 --additiveMu --name=scenarioD_additiveMu

	$(MAKE) twoBin_interpCode0_workpsaces
	$(MAKE) twoBin_box_workspaces
	$(MAKE) twoBin_wideGauss_workspaces

atlas_counting:
	@echo "\n=== Making atlas counting model. ==="
	python atlasCountingModel.py

	$(MAKE) atlas_interpCode0_workspaces
	$(MAKE) atlas_box_workspaces
	$(MAKE) atlas_wideGauss_workspaces




###################################
# interpcode=0 workspaces

%_interpCode0.root: %.root
	python switchInterpCode.py --interpCode=0 \
		-i $< \
		-o $@

twoBin_interpCode0_workpsaces: \
		../output/twoBin/oneAlpha_catUniversal_interpCode0.root \
		../output/twoBin/oneAlpha_catNonUniversal_interpCode0.root \
		../output/twoBin/twoAlpha_catUniversal_interpCode0.root \
		../output/twoBin/twoAlpha_catNonUniversal_interpCode0.root \
		\
		../output/twoBin/scenarioA_interpCode0.root \
		../output/twoBin/scenarioA2_interpCode0.root \
		../output/twoBin/scenarioB_interpCode0.root \
		../output/twoBin/scenarioC_interpCode0.root \
		../output/twoBin/scenarioC2_interpCode0.root \
		../output/twoBin/scenarioD_interpCode0.root \
		\
		../output/twoBin/scenarioA_additiveMu_interpCode0.root \
		../output/twoBin/scenarioA2_additiveMu_interpCode0.root \
		../output/twoBin/scenarioB_additiveMu_interpCode0.root \
		../output/twoBin/scenarioC_additiveMu_interpCode0.root \
		../output/twoBin/scenarioC2_additiveMu_interpCode0.root \
		../output/twoBin/scenarioD_additiveMu_interpCode0.root
	@echo "done creating interpCode0 workspaces."

atlas_interpCode0_workspaces: \
		../output/atlas_counting/comb_interpCode0.root \
		../output/atlas_counting/2ph_interpCode0.root \
		../output/atlas_counting/4l_interpCode0.root \
		../output/atlas_counting/lvlv_interpCode0.root
	@echo "done creating interpCode0 workspaces."





###################################
# box constraint workspaces

%_box.root: %.root
	python toBoxConstraint.py -i $< --centeredAtMLE

twoBin_box_workspaces: \
		../output/twoBin/scenarioA_box.root \
		../output/twoBin/scenarioA2_box.root \
		../output/twoBin/scenarioB_box.root \
		../output/twoBin/scenarioC_box.root \
		../output/twoBin/scenarioC2_box.root \
		../output/twoBin/scenarioD_box.root \
		\
		../output/twoBin/scenarioA_interpCode0_box.root \
		../output/twoBin/scenarioA2_interpCode0_box.root \
		../output/twoBin/scenarioB_interpCode0_box.root \
		../output/twoBin/scenarioC_interpCode0_box.root \
		../output/twoBin/scenarioC2_interpCode0_box.root \
		../output/twoBin/scenarioD_interpCode0_box.root
	@echo "done creating twoBin box workspaces."

atlas_box_workspaces: \
		../output/atlas_counting/comb_box.root \
		../output/atlas_counting/2ph_box.root \
		../output/atlas_counting/4l_box.root \
		../output/atlas_counting/lvlv_box.root \
		../output/atlas_counting/comb_interpCode0_box.root \
		../output/atlas_counting/2ph_interpCode0_box.root \
		../output/atlas_counting/4l_interpCode0_box.root \
		../output/atlas_counting/lvlv_interpCode0_box.root
	@echo "done creating atlas counting box workspaces."



###################################
# wideGauss constraint workspaces

%_wideGauss.root: %.root
	python toBoxConstraint.py -i $< --wideGauss

twoBin_wideGauss_workspaces: \
		../output/twoBin/scenarioA_wideGauss.root \
		../output/twoBin/scenarioA2_wideGauss.root \
		../output/twoBin/scenarioB_wideGauss.root \
		../output/twoBin/scenarioC_wideGauss.root \
		../output/twoBin/scenarioC2_wideGauss.root \
		../output/twoBin/scenarioD_wideGauss.root \
		\
		../output/twoBin/scenarioA_interpCode0_wideGauss.root \
		../output/twoBin/scenarioA2_interpCode0_wideGauss.root \
		../output/twoBin/scenarioB_interpCode0_wideGauss.root \
		../output/twoBin/scenarioC_interpCode0_wideGauss.root \
		../output/twoBin/scenarioC2_interpCode0_wideGauss.root \
		../output/twoBin/scenarioD_interpCode0_wideGauss.root
	@echo "done creating twoBin box workspaces."

atlas_wideGauss_workspaces: \
		../output/atlas_counting/comb_wideGauss.root \
		../output/atlas_counting/2ph_wideGauss.root \
		../output/atlas_counting/4l_wideGauss.root \
		../output/atlas_counting/lvlv_wideGauss.root \
		../output/atlas_counting/comb_interpCode0_wideGauss.root \
		../output/atlas_counting/2ph_interpCode0_wideGauss.root \
		../output/atlas_counting/4l_interpCode0_wideGauss.root \
		../output/atlas_counting/lvlv_interpCode0_wideGauss.root
	@echo "done creating atlas counting box workspaces."
















makeAtlasInputFile:
	@echo "\n=== Making the input file for ATLAS. ==="
	python makeAtlasInputFile.py

makeCountingInputFile:
	@echo "\n=== Making the counting model file. ==="
	python makeCountingInputFile.py

makeTwoBinInputFile:
	@echo "\n=== Making the two bin model file. ==="
	python makeTwoBinInputFile.py


