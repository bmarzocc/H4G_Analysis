#!/bin/bash

inDir='/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_newSignalWeights_noTails/'
outDir='/eos/user/t/twamorka/www/H4G_for_PreApp/PreApp_Checks/Training_without_tails/SmoothingPlots/'
for m in 60 55 50 45 40 30 25 20 15;
do
    echo python smooth_BDT.py -d ${inDir}${m}/ -g ${m} -n 190 --min -0.9 --max 1. --oP ${outDir}${m}/
    python smooth_BDT.py -d ${inDir}${m}/ -g ${m} -n 190 --min -0.9 --max 1. --oP ${outDir}${m}/
done
