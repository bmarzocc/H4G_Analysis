from ROOT import *
from array import array
import sys, getopt

# import argparse
if __name__ == '__main__':
    File = sys.argv[1]
    mass = sys.argv[2]
    doSystematics = sys.argv[3]
    year = sys.argv[4]
    Weight = sys.argv[5]
    Out = sys.argv[6]

    reader = TMVA.Reader()

    diffdM = array('f',[0])
    ct1 = array('f',[0])
    a1pt = array('f',[0])
    a2pt = array('f',[0])
    p1mva = array('f',[0])
    p2mva = array('f',[0])
    p3mva = array('f',[0])
    p4mva = array('f',[0])
    a1_a2_dR = array('f',[0])
    a1_pt_Over_tp_mass = array('f',[0])
    a2_pt_Over_tp_mass = array('f',[0])
    a1mass = array('f',[0])
    a2mass = array('f',[0])

    reader.AddVariable('pho1_MVA<-1.? -1.1: pho1_MVA',p1mva)
    reader.AddVariable('pho2_MVA<-1.? -1.1: pho2_MVA',p2mva)
    reader.AddVariable('pho3_MVA<-1.? -1.1: pho3_MVA',p3mva)
    reader.AddVariable('pho4_MVA<-1.? -1.1: pho4_MVA',p4mva)
    reader.AddVariable('a1_mass_dM-a2_mass_dM',diffdM)
    reader.AddVariable('a1_mass_dM',a1mass)
    reader.AddVariable('a2_mass_dM',a2mass)
    reader.AddVariable('cosTheta_a1_dM',ct1)
    reader.AddVariable('a1_pt_dM',a1pt)
    reader.AddVariable('a2_pt_dM',a2pt)
    reader.AddVariable('a1_a2_dR_dM',a1_a2_dR)
    reader.AddVariable('a1_pt_dM/tp_mass',a1_pt_Over_tp_mass)
    reader.AddVariable('a2_pt_dM/tp_mass',a2_pt_Over_tp_mass)

    reader.BookMVA("BDT",Weight)


    systLabels = [""]
    if (doSystematics and 'signal' in File):
        for direction in ["Up","Down"]:
               systLabels.append("MvaShift%s01sigma"%direction)
               systLabels.append("SigmaEOverEShift%s01sigma"%direction)
               systLabels.append("MaterialCentralBarrel%s01sigma"%direction)
               systLabels.append("MaterialOuterBarrel%s01sigma"%direction)
               systLabels.append("MaterialForward%s01sigma"%direction)
               systLabels.append("FNUFEB%s01sigma"%direction)
               systLabels.append("FNUFEE%s01sigma"%direction)
               systLabels.append("MCScaleGain6EB%s01sigma"%direction)
               systLabels.append("MCScaleGain1EB%s01sigma"%direction)
               systLabels.append("MCScaleHighR9EB%s01sigma" % direction)
               systLabels.append("MCScaleHighR9EE%s01sigma" % direction)
               systLabels.append("MCScaleLowR9EB%s01sigma" % direction)
               systLabels.append("MCScaleLowR9EE%s01sigma" % direction)
               systLabels.append("MCSmearHighR9EBPhi%s01sigma" % direction)
               systLabels.append("MCSmearHighR9EBRho%s01sigma" % direction)
               systLabels.append("MCSmearHighR9EEPhi%s01sigma" % direction)
               systLabels.append("MCSmearHighR9EERho%s01sigma" % direction)
               systLabels.append("MCSmearLowR9EBPhi%s01sigma" % direction)
               systLabels.append("MCSmearLowR9EBRho%s01sigma" % direction)
               systLabels.append("MCSmearLowR9EEPhi%s01sigma" % direction)
               systLabels.append("MCSmearLowR9EERho%s01sigma" % direction)
               systLabels.append("ShowerShapeHighR9EB%s01sigma" % direction)
               systLabels.append("ShowerShapeHighR9EE%s01sigma" % direction)
               systLabels.append("ShowerShapeLowR9EB%s01sigma" % direction)
               systLabels.append("ShowerShapeLowR9EE%s01sigma" % direction)
               systLabels.append("SigmaEOverEShift%s01sigma" % direction)

    FilesToRedo = File.split(',')
    treelist = []
    for f in FilesToRedo:
        # print f
        infilename =  f
        infile = TFile(infilename)
        # print "file: ", infile
        tree = ''
        outfile = TFile(Out, "RECREATE")
        if ('signal' in f):
            for sys_i,syst in enumerate(systLabels):
                # print('on systematic',sys_i,'/',len(systLabels),':',syst)
                systLabel = ""
                # print (syst)
                if syst != "":
                   systLabel += '_' + syst
                if (year == "2016"):
                     tree = infile.Get("HAHMHToAA_AToGG_MA_"+str(mass)+"GeV_TuneCUETP8M1_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_0" + systLabel)
                     treelist.append(tree)
                     # print "tree name: ", "HAHMHToAA_AToGG_MA_"+str(mass)+"GeV_TuneCUETP8M1_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_0" + systLabel
                elif (year == "2017" or year == "2018"):
                     tree = infile.Get("HAHMHToAA_AToGG_MA_"+str(mass)+"GeV_TuneCP5_PSweights_13TeV_madgraph_pythia8_13TeV_H4GTag_0" + systLabel)
                     treelist.append(tree)
        elif ('mix' in f):
             tree = infile.Get("Data_13TeV_H4GTag_0")
             treelist.append(tree)
        else:
            tree = infile.Get("tagsDumper/trees/Data_13TeV_H4GTag_0")
            treelist.append(tree)
        for tree in treelist:
            nentries = tree.GetEntries()
            # print "Number of entries ", nentries
            outtree = tree.CloneTree(0)
            bdt = array('f', [0])
            _bdt = outtree.Branch('bdt', bdt, 'bdt/F')
            for i in range(0, nentries):
                if i%1000 == 0: print i
                tree.GetEntry(i)

                diffdM[0] = float((tree.a1_mass_dM-tree.a2_mass_dM))
                ct1[0] = float(tree.cosTheta_a1_dM)
                a1pt[0] = float(tree.a1_pt_dM)
                a2pt[0] = float(tree.a2_pt_dM)
                if (tree.pho1_MVA<-1.):
                    p1mva[0] = -1.1
                else: p1mva[0] =float(tree.pho1_MVA)
                if (tree.pho2_MVA<-1.):
                    p2mva[0] = -1.1
                else: p2mva[0] =float(tree.pho2_MVA)
                if (tree.pho3_MVA<-1.):
                    p3mva[0] = -1.1
                else: p3mva[0] =float(tree.pho3_MVA)
                if (tree.pho4_MVA<-1.):
                    p4mva[0] = -1.1
                else: p4mva[0] =float(tree.pho4_MVA)

                a1_a2_dR[0] = float(tree.a1_a2_dR_dM)
                a1_pt_Over_tp_mass[0] = float(float(tree.a1_pt_dM)/float(tree.tp_mass))
                a2_pt_Over_tp_mass[0] = float(float(tree.a2_pt_dM)/float(tree.tp_mass))
                a1mass[0] = float(tree.a1_mass_dM)
                a2mass[0] = float(tree.a2_mass_dM)

                bdt[0] = reader.EvaluateMVA("BDT")

                outtree.Fill()
            outfile.cd()
            outtree.Write()


    outfile.Write()
