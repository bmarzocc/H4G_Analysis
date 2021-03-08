#!/usr/bin/python
import numpy as n
from ROOT import *
import sys, getopt
from array import array
import itertools
from optparse import OptionParser
import operator
import os



if __name__ == '__main__':


  # parser = OptionParser()
  # # parser.add_option(   "-i", "--input",     dest="input",     default="",   type="string", help="input root file" )
  # parser.add_option(   "-m", "--max",     dest="max",     default="",   type="string", help="max" )
  # # parser.add_option(   "-y", "--year",     dest="year",     default="",   type="string", help="year" )
  # # parser.add_opction(   "-o", "--output",     dest="output",     default="",   type="string", help="output" )
  #
  #
  # (options, args) = parser.parse_args()
  #
  # # input     = options.input
  # max     = options.max
  # # year      = options.year
  # # output    = options.output
  #
  # # print "input    =",input
  # print "max      =",max
  # # print "year     =",year
  # # print "output    =",output


  inputDir = os.getcwd()
  if not os.path.isdir('error'): os.mkdir('error')
  if not os.path.isdir('output'): os.mkdir('output')
  if not os.path.isdir('log'): os.mkdir('log')

  # print max
  # for i in range(1,int(max)+1):
  #     print i

#   subset_len = len(list(itertools.combinations(range(nSteps), len(maxs))))
#   step = float(subset_len)/float(nBunch)
#   subset_min = []
#   subset_max = []
#   for i in range(nBunch):
#      subset_min.append(int(i*step))
#      subset_max.append(int((i+1)*step))
#
#   print "Number combinatorics: ", subset_len
#   print "Step: ", step
#
#   iSubset = 0
#   final_selection = ['']*nBunch
#   for subset in itertools.combinations(range(nSteps), len(maxs)):
#      selection_tmp = "1>0"
#      for ivar in range(len(subset)):
#         selection_tmp = selection_tmp +" && "+selections_perVar[ivar][int(subset[ivar])]
#      final_selection[int(iSubset/step)] = final_selection[int(iSubset/step)] + " / " + selection_tmp
#      #print iSubset,int(iSubset/step),final_selection[int(iSubset/step)]
#      iSubset=iSubset+1
#
  # Prepare condor jobs
  condor = '''executable              = run_script.sh
output                  = output/strips.$(ClusterId).$(ProcId).out
error                   = error/strips.$(ClusterId).$(ProcId).err
log                     = log/strips.$(ClusterId).log
transfer_input_files    = run_script.sh
on_exit_remove          = (ExitBySignal == False) && (ExitCode == 0)
periodic_release        = (NumJobStarts < 3) && ((CurrentTime - EnteredCurrentStatus) > (60*60))
+JobFlavour             = "workday"
+AccountingGroup        = "group_u_CMS.CAF.ALCA"
queue arguments from arguments.txt
'''

  with open("condor_job.txt", "w") as cnd_out:
     cnd_out.write(condor)

  outputDir = os.getcwd()

  script = '''#!/bin/sh -e
LOCAL=$1;
INPUTFILE=$2;
MASS=$3;
GENMASS=$4;
SYSTEMATICS=$5;
YEAR=$6;
WEIGHT=$7;
OUTPUT=$8;
python ${LOCAL}/ApplyCatBDT.py ${INPUTFILE} ${MASS} ${GENMASS} ${SYSTEMATICS} ${YEAR} ${WEIGHT} ${OUTPUT}
echo -e "DONE";
'''
  arguments=[]

  year = [2018]
  #year = [2016, 2017, 2018]
  #mass = [60]
  # mass_training = 55
  #mass = [60, 55, 50, 45, 40, 35,30, 25, 20, 15]
  mass = [25]
  doSystematics = 1
  # weightFile = '/eos/user/b/bmarzocc/H4G/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_m'
  # weightFile = '/eos/user/b/bmarzocc/H4G/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_m'
  #weightFile = '/eos/user/b/bmarzocc/H4G/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataDriven_crA_MGPodd_m'

  # outDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_newSignalWeights_noTails/'

  # outDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd/SignalInterpol_M55/'
  #outDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataDriven_crA_MGPodd/'

  # ## per-mass point training without m_a variables
  #weightFile = '/afs/cern.ch/work/t/twamorka/H4G_Analysis/BDTTraining/PerformTraining/PerMassPoint_WithoutMa_M55'
  #outDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/FullRun2_PerMassPoint_WithoutMa/M55_Cat/'

  ## all masses training without m_a variables
  # weightFile = '/afs/cern.ch/work/t/twamorka/H4G_Analysis/BDTTraining/PerformTraining/AllMasses/AllMassPoints_WithoutMa'
  # outDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/FullRun2_AllMasses_WithoutMa/'

  ## all masses training with m_a variables
  # weightFile = '/afs/cern.ch/work/t/twamorka/H4G_Analysis/BDTTraining/PerformTraining/AllMasses/AllMassPoints_WithMa'
  # outDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/FullRun2_AllMasses_WithMa/'

  ## parametrized training
  #weightFile = '/eos/user/b/bmarzocc/H4G/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_newSignalWeights_parametrized'
  #outDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/FullRun2_Parametrized/M55_Cat/'
  
  ## modified parametrized training
  #weightFile = '/eos/user/b/bmarzocc/H4G/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_newSignalWeights_parametrized_v2'
  #outDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_newSignalWeights_parametrized_v2/'
  #weightFile = '/eos/user/b/bmarzocc/H4G/H4G_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_m'
  #outDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/H4G_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_noCorrel/'
  #weightFile = '/eos/user/b/bmarzocc/H4G/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_newSignalWeights_parametrized_v2_noCorrel/'
  #outDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_newSignalWeights_parametrized_v2_noCorrel/'
  #weightFile = '/afs/cern.ch/work/t/twamorka/H4G_Analysis/BDTTraining/PerformTraining/Parametrized_v3/'
  #outDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/Parametrized_v3/'
  #weightFile = '/afs/cern.ch/work/t/twamorka/H4G_Analysis/BDTTraining/PerformTraining/Training_v2_DiffMassRange_60/'
  #outDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/H4G_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_noCorrel_DiffMassRange/'
  #weightFile = '/eos/user/b/bmarzocc/H4G/H4G_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_m'
  #outDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/H4G_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_noCorrel_v2/'
  weightFile = '/afs/cern.ch/work/t/twamorka/H4G_Analysis/BDTTraining/PerformTraining/Parametrized_v2_noCorrel_fullMassPoint/'
  outDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/Parametrized_NoCorrel_FullMassRange/'
  inputfile_signal = '/eos/user/t/twamorka/H4G_Signal_Campaign_18Jan2021/'
  inputfile_data = '/eos/user/t/twamorka/h4g_fullRun2/withSystematics/'
  inputfile_bkg = '/eos/user/t/twamorka/h4g_fullRun2/withSystematics/DataMix_HighStat/hadd/'
  # inputfile_bkg = '/eos/user/t/twamorka/H4G_BkgMC/'
  files = ['even']
  for m in mass:
      for y in year:
          for f in files:
              arguments.append("{} {} {} {} {} {} {} {}".format(inputDir, inputfile_signal+str(y)+'/hadd/signal_m_'+str(m)+'_'+f+'.root',m,m,doSystematics,y,weightFile+'/weights/TMVAClassification_BDTG.weights.xml',outDir+str(m)+'/signal_m_'+str(m)+'_'+str(y)+'_'+f+'.root'))
              arguments.append("{} {} {} {} {} {} {} {}".format(inputDir, inputfile_data+str(y)+'/hadd/data_'+str(y)+'.root',m,m,doSystematics,y,weightFile+'/weights/TMVAClassification_BDTG.weights.xml',outDir+str(m)+'/data_'+str(y)+'.root'))
              arguments.append("{} {} {} {} {} {} {} {}".format(inputDir, inputfile_bkg+'data_mix_'+str(y)+'_kinWeight_even.root',m,m,doSystematics,y,weightFile+'/weights/TMVAClassification_BDTG.weights.xml',outDir+str(m)+'/data_mix_'+str(y)+'_even.root'))

              # arguments.append("{} {} {} {} {} {} {}".format(inputDir, inputfile_signal+str(y)+'/hadd/signal_m_'+str(m)+'_'+f+'.root',m,doSystematics,y,weightFile+str(m)+'/weights/TMVAClassification_BDTG.weights.xml',outDir+str(m)+'/signal_m_'+str(m)+'_'+str(y)+'_'+f+'.root'))
  #for m in mass:
      #for y in year:
          #arguments.append("{} {} {} {} {} {} {} {}".format(inputDir, inputfile_data+str(y)+'/hadd/data_'+str(y)+'.root',60,m,doSystematics,y,weightFile+str(m)+'/weights/TMVAClassification_BDTG.weights.xml',outDir+str(m)+'/data_'+str(y)+'.root'))
  #for m in mass:
      #or y in year:
             #arguments.append("{} {} {} {} {} {} {} {}".format(inputDir, inputfile_data+str(y)+'/hadd/data_'+str(y)+'.root',m,m,doSystematics,y,weightFile+'/weights/TMVAClassification_BDTG.weights.xml',outDir+str(m)+'/data_'+str(y)+'.root'))
             #arguments.append("{} {} {} {} {} {} {} {}".format(inputDir, inputfile_bkg+'data_mix_'+str(y)+'_kinWeight_even.root',m,m,doSystematics,y,weightFile+'/weights/TMVAClassification_BDTG.weights.xml',outDir+str(m)+'/data_mix_'+str(y)+'_even.root'))

      # for y in year:
  #         #arguments.append("{} {} {} {} {} {} {}".format(inputDir, inputfile_bkg+'DiPho_40to80_'+str(y)+'.root',60,doSystematics,y,weightFile+str(m)+'_newSignalWeights/weights/TMVAClassification_BDTG.weights.xml',outDir+str(m)+'/DiPho_40to80_'+str(y)+'_skim_CR_D.root'))
  #         #arguments.append("{} {} {} {} {} {} {}".format(inputDir, inputfile_bkg+'DiPho_80toInf_'+str(y)+'.root',60,doSystematics,y,weightFile+str(m)+'_newSignalWeights/weights/TMVAClassification_BDTG.weights.xml',outDir+str(m)+'/DiPho_80toInf_'+str(y)+'_skim_CR_D.root'))
  #         #arguments.append("{} {} {} {} {} {} {}".format(inputDir, inputfile_bkg+'DataDriven_'+str(y)+'_CR_A.root',60,doSystematics,y,weightFile+str(m)+'_newSignalWeights/weights/TMVAClassification_BDTG.weights.xml',outDir+str(m)+'/DataDriven_'+str(y)+'_CR_A.root'))
  #
          # for f in files:
          #     arguments.append("{} {} {} {} {} {} {}".format(inputDir, inputfile_bkg+'data_mix_'+str(y)+'_kinWeight_'+f+'.root',60,doSystematics,y,weightFile+str(m)+'/weights/TMVAClassification_BDTG.weights.xml',outDir+str(m)+'/data_mix_'+str(y)+'_'+f+'.root'))
  # for y in year:
  #        arguments.append("{} {} {} {} {} {} {}".format(inputDir, inputfile_data+str(y)+'/hadd/data_'+str(y)+'.root',60,doSystematics,y,weightFile+'/weights/TMVAClassification_BDTG.weights.xml',outDir+'data_'+str(y)+'.root'))
  #        arguments.append("{} {} {} {} {} {} {}".format(inputDir, inputfile_bkg+'data_mix_'+str(y)+'_kinWeight_even.root',60,doSystematics,y,weightFile+'/weights/TMVAClassification_BDTG.weights.xml',outDir+'data_mix_'+str(y)+'_even.root'))

  # for y in year:
  #     for f in files:
  #         arguments.append("{} {} {} {} {} {} {}".format(inputDir, inputfile_bkg+'data_mix_'+str(y)+'_kinWeight_'+f+'.root',60,doSystematics,y,weightFile+'/weights/TMVAClassification_BDTG.weights.xml',outDir+'data_mix_'+str(y)+'_'+f+'.root'))

  with open("arguments.txt", "w") as args:
     args.write("\n".join(arguments))
  with open("run_script.sh", "w") as rs:
     rs.write(script)
