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




  inputDir = os.getcwd()
  if not os.path.isdir('error'): os.mkdir('error')
  if not os.path.isdir('output'): os.mkdir('output')
  if not os.path.isdir('log'): os.mkdir('log')

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

  #year = [2018]
  year = [2016, 2017, 2018]
  #mass = [60,50,55]
  # mass_training = 55
  #mass = [60, 55, 50, 45, 40, 30, 25, 20, 15]
  #mass = [60,55,50]
  #mass = [15,25,45]
  #genMass = [30]
  # mass = [20,30,40,50,60]
  mass = {'17.5':[15,20],'22.5':[20,25]}
  doSystematics = 1

  ## parametrized training
  #weightFile = '/eos/user/b/bmarzocc/H4G/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_newSignalWeights_parametrized'
  #outDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/FullRun2_Parametrized/UsingM55/'

  ## modified parametrized training
  weightFile = '/eos/user/b/bmarzocc/H4G/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_newSignalWeights_parametrized_v2'
  outDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgOdd_newSignalWeights_parametrized_v2/'
  inputfile_signal = '/eos/user/t/twamorka/H4G_Signal_Campaign_18Jan2021/'
  inputfile_data = '/eos/user/t/twamorka/h4g_fullRun2/withSystematics/'
  inputfile_bkg = '/eos/user/t/twamorka/h4g_fullRun2/withSystematics/DataMix_HighStat/hadd/'
  files = ['even']
  for m in mass:
      if (m == 20):genMass = [17.5,22.5]
      elif (m == 30): genMass = [27.5]
      elif (m == 40): genMass = [37.5, 42.5]
      elif (m == 50): genMass = [47.5,52.5]
      elif (m == 60): genMass = [57.5]
      #elif (m == 60): genMass = [30,58,59]
      #genMass = [17.5, 22.5, 27.5, 42.5, 47.5, 52.5, 57.5]
      for y in year:
          for g in genMass:
              arguments.append("{} {} {} {} {} {} {} {}".format(inputDir, inputfile_signal+str(y)+'/hadd/signal_m_'+str(m)+'_even.root',m,g,doSystematics,y,weightFile+'/weights/TMVAClassification_BDTG.weights.xml',outDir+'Training_M'+str(m)+'/signal_m_'+str(g)+'_'+str(y)+'_even.root'))
              #arguments.append("{} {} {} {} {} {} {} {}".format(inputDir, inputfile_signal+str(y)+'/hadd/signal_m_'+str(m)+'_even.root',m,g,doSystematics,y,weightFile+'/weights/TMVAClassification_BDTG.weights.xml',outDir+str(g)+'/signal_m_'+str(g)+'_'+str(y)+'_even.root'))
              #arguments.append("{} {} {} {} {} {} {} {}".format(inputDir, inputfile_data+str(y)+'/hadd/data_'+str(y)+'.root',m,g,doSystematics,y,weightFile+'/weights/TMVAClassification_BDTG.weights.xml',outDir+str(g)+'/data_'+str(y)+'.root'))
              #arguments.append("{} {} {} {} {} {} {} {}".format(inputDir, inputfile_bkg+'data_mix_'+str(y)+'_kinWeight_even.root',m,g,doSystematics,y,weightFile+'/weights/TMVAClassification_BDTG.weights.xml',outDir+str(g)+'/data_mix_'+str(y)+'_even.root'))
              #arguments.append("{} {} {} {} {} {} {} {}".format(inputDir, inputfile_data+str(y)+'/hadd/data_'+str(y)+'.root',m,g,doSystematics,y,weightFile+str(m)+'/weights/TMVAClassification_BDTG.weights.xml',outDir+str(g)+'/data_'+str(y)+'.root'))
  #for m in mass:
      #for y in year:
          #for f in files:
              #arguments.append("{} {} {} {} {} {} {} {}".format(inputDir, inputfile_signal+str(y)+'/hadd/signal_m_'+str(m)+'_'+f+'.root',m,m,doSystematics,y,weightFile+'/weights/TMVAClassification_BDTG.weights.xml',outDir+str(m)+'/signal_m_'+str(m)+'_'+str(y)+'_'+f+'.root'))

              # arguments.append("{} {} {} {} {} {} {}".format(inputDir, inputfile_signal+str(y)+'/hadd/signal_m_'+str(m)+'_'+f+'.root',m,doSystematics,y,weightFile+str(m)+'/weights/TMVAClassification_BDTG.weights.xml',outDir+str(m)+'/signal_m_'+str(m)+'_'+str(y)+'_'+f+'.root'))
  #for m in mass:
      #for y in year:
          #arguments.append("{} {} {} {} {} {} {} {}".format(inputDir, inputfile_data+str(y)+'/hadd/data_'+str(y)+'.root',60,m,doSystematics,y,weightFile+str(m)+'/weights/TMVAClassification_BDTG.weights.xml',outDir+str(m)+'/data_'+str(y)+'.root'))
  #for m in mass:
      #for y in year:
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
