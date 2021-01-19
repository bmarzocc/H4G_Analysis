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
  # # parser.add_option(   "-o", "--output",     dest="output",     default="",   type="string", help="output" )
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
INPUTFILE=$1;
MASS=$2;
SYSTEMATICS=$3;
YEAR=$4;
WEIGHT=$5;
OUTPUT=$6;
python /afs/cern.ch/work/t/twamorka/flashgg_16aug2020/CMSSW_10_6_8/src/flashgg/Scripts/ApplyTraining/ApplyCatBDT.py ${INPUTFILE} ${MASS} ${SYSTEMATICS} ${YEAR} ${WEIGHT} ${OUTPUT}
echo -e "DONE";
'''
  arguments=[]
  
  
  year = [2016, 2017, 2018]
  mass = [60, 55, 50, 45, 40, 30, 25, 20, 15]
  doSystematics = 1
  weightFile = '/eos/user/b/bmarzocc/H4G/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgData_m'
  outDir = '/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Dec2020/dataset_PhoMVA_manyKinVars_aMass_fullRun2_DataMix_HighStat_kinWeight_dataSBScaling_MGPodd_bkgData/'
  inputfile_signal = '/eos/user/t/twamorka/H4G_SignalSamples_MGP/'
  inputfile_data = '/eos/user/t/twamorka/h4g_fullRun2/withSystematics/' 
  inputfile_bkg = '/eos/user/t/twamorka/h4g_fullRun2/withSystematics/DataMix_HighStat/hadd/'
  files = ['even','odd']
  for m in mass:
      for y in year:
          for f in files:
              arguments.append("{} {} {} {} {} {}".format(inputfile_signal+str(y)+'/hadd/signal_m_'+str(m)+'_'+f+'.root',m,doSystematics,y,weightFile+str(m)+'/weights/TMVAClassification_BDTG.weights.xml',outDir+str(m)+'/signal_m_'+str(m)+'_'+str(y)+'_'+f+'.root'))
  for m in mass:
      for y in year:
          arguments.append("{} {} {} {} {} {}".format(inputfile_data+str(y)+'/hadd/data_'+str(y)+'.root',60,doSystematics,y,weightFile+str(m)+'/weights/TMVAClassification_BDTG.weights.xml',outDir+str(m)+'/data_'+str(y)+'.root'))
  for m in mass:
      for y in year:
          for f in files:
              arguments.append("{} {} {} {} {} {}".format(inputfile_bkg+'data_mix_'+str(y)+'_kinWeight_'+f+'.root',60,doSystematics,y,weightFile+str(m)+'/weights/TMVAClassification_BDTG.weights.xml',outDir+str(m)+'/data_mix_'+str(y)+'_'+f+'.root'))

  with open("arguments.txt", "w") as args:
     args.write("\n".join(arguments))
  with open("run_script.sh", "w") as rs:
     rs.write(script)
