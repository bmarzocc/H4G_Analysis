#!/bin/bash
#
#########################################################################################
# The purpose of this script is to produce root files that are used for bias studies    #
## Before doing anything, you must first go to a CMSSW release where you have Higgs Combine setup and do a cmsenv. This is essential to do so that you can use scripts that are needed in the subsequent steps.

# Step 1: It is suggested to make a separate datacard for each category separately. This is because the background modeling is independent in each category. To make a datacard with only one category from the combined datacard:
#combineCards.py --ic=catA Datacard.txt > Datacard_catA.txt (where Datacard.txt is your datacard with multiple categories, and catA is the category for which you want to create a separate datacard.) This step is not part of the scripts below since H4G datacards only have category to begin with. If your datacards have multiple categories, then you should do this step for each category.
#
#########################################################################################

step=$1
mass='60 55 50 45 40 30 25 20 15'
year='2016 2017 2018'
pdfindex='0 1 2 3 4 5'
expectSignal='1'
nToys='2000'
#rmin='2'
# year='2017'

if [ $step == "biasstudies" ]; then
    cd Datacard
    for m in ${mass};
    do
      mkdir BiasStudies_M${m}_${nToys}Toys_23Jan2021
      biasstudies_input=BiasStudies_M${m}_${nToys}Toys_23Jan2021
      # inputDatacard=Datacard_NoVtxSplit_M${m}_wTheorySyst_noQCDSyst.txt
      inputDatacard=Datacard_23Jan2021_M${m}_noQCD.txt
      echo text2workspace.py ${inputDatacard} -o ${biasstudies_input}/M${m}.root
      text2workspace.py ${inputDatacard} -o ${biasstudies_input}/M${m}.root
      if [[ $m == "60" ]]; then
      expectSignal=0.3
      elif [[ $m == "55" ]]; then
      expectSignal=0.41
      elif [[ $m == "50" ]]; then
      expectSignal=0.53
      elif [[ $m == "45" ]]; then
      expectSignal=0.70
      elif [[ $m == "40" ]]; then
      expectSignal=0.73
      elif [[ $m == "30" ]]; then
      expectSignal=0.87
      elif [[ $m == "25" ]]; then
      expectSignal=0.88
      elif [[ $m == "20" ]]; then
      expectSignal=0.74
      elif [[ $m == "15" ]]; then
      expectSignal=0.99
      fi
      for p in ${pdfindex};
      do
         for e in ${expectSignal};
         do
            echo combine ${biasstudies_input}/M${m}.root -M GenerateOnly  -t ${nToys} --setParameters pdfindex_H4GTag_Cat0_13TeV=${p},r=${e} --saveToys --name _M${m}_Cat0_13TeV_pdfindex${p}_signal${e} -m 125 --toysNoSystematics
            combine ${biasstudies_input}/M${m}.root -M GenerateOnly  -t ${nToys} --setParameters pdfindex_H4GTag_Cat0_13TeV=${p},r=${e} --saveToys --name _M${m}_Cat0_13TeV_pdfindex${p}_signal${e} -m 125 --toysNoSystematics
            mv higgsCombine_M${m}_Cat0_13TeV_pdfindex${p}_signal${e}.GenerateOnly.mH125.123456.root ${biasstudies_input}/
         done
      done
    done
    cd ..
fi
