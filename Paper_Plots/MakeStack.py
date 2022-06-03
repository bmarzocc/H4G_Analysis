from pullClass import *
from ROOT import *
import json, os
import shutil
from configs import *
import resource

gROOT.SetBatch()

gStyle.SetOptStat(0)
TGaxis.SetMaxDigits(3)


dummyTFile = TFile("dummy.root", "RECREATE")

NiceBlue = '#51A7F9'
NiceBlueDark = '#2175E0'
NiceGreen = '#6FBF41'
NiceGreen2 = '#35DC3D'
NiceYellow = '#FBE12A'
NiceYellow2 = '#FEEA01'
NiceOrange = '#F0951A'
NiceRed = '#FA4912'
NicePurple = '#885BB2'
NicePaleYellow = '#FFFF66'
NiceMidnight = '#000080'
NiceTangerine = '#FF8000'
cNiceBlue = TColor.GetColor('#51A7F9')
cNiceBlueDark = TColor.GetColor('#2175E0')
cNiceGreen = TColor.GetColor('#6FBF41')
#cNiceGreen2 = TColor.GetColor(NiceGreen2)
cNiceGreen2 = 415
cNiceGreenDark = TColor.GetColor('#008040')
cNiceYellow = TColor.GetColor('#FBE12A')
cNiceYellow2 = TColor.GetColor(NiceYellow2)
cNiceOrange = TColor.GetColor('#F0951A')
cNiceRed = TColor.GetColor('#FA4912')
cNicePurple = TColor.GetColor('#885BB2')
cNicePaleYellow = TColor.GetColor('#FFFF66')
cNiceMidnight = TColor.GetColor('#000080')
cNiceTangerine = TColor.GetColor('#FF8000')

myCols = [cNiceMidnight, cNiceRed,  cNiceOrange, cNiceGreen2, cNiceTangerine, cNicePaleYellow, cNiceOrange, cNiceRed, cNicePurple, cNiceGreen, cNiceGreen2]

if not os.path.exists(dirName):
        print dirName, "doesn't exist, creating it..."
        os.makedirs(dirName)
        if os.path.exists(dirName):
                print dirName, "now exists!"

datasets = json.load(data_file)

Trees = {}

if doKinCut == True:
    Cut += " pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1"
    Cut_Signal += "&& pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 115 && tp_mass < 135 "
    Cut_Bkg += " pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1"

#
if doHiggsWindow ==  True:
   # Cut += " && tp_mass > 100 && tp_mass < 180"
   # Cut_Signal += "&& tp_mass > 100 && tp_mass < 180"
   # Cut_Bkg += "&& tp_mass > 100 && tp_mass < 180"
   Cut += " && tp_mass > 110 && tp_mass < 180"
   Cut_Signal += "&& tp_mass > 110 && tp_mass < 180"
   Cut_Bkg += "&& tp_mass > 110 && tp_mass < 180"

if doBlind == True:
    if doSignalRegion:
        Cut += "&& !(tp_mass > 115 && tp_mass < 135)"
        Cut_Signal += "&& (tp_mass > 115 && tp_mass < 135)"
    else:
	    Cut += " && !(tp_mass > 115 && tp_mass < 135) "

#print "Cut_signal ", Cut_Signal
#Cut_DataDriven = "pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass < 180 &&  !((tp_mass > 115 && tp_mass < 135))"
weightedcut = "weight"

weightedCut = TCut(weightedcut)

data_integral_2016 = 1
data_integral_2017 = 1
data_integral_2018 = 1
Cut_data = Cut
Cut_data = Cut_data + Cut_additional +")"
print "Cut_data: ", Cut_data
if (year==1):
    dataHist_PhoMVA_2016 = TH1F('dataHist_PhoMVA_2016','dataHist_PhoMVA_2016',100,-1.1,1)
    dataHist_PhoMVA_2017 = TH1F('dataHist_PhoMVA_2017','dataHist_PhoMVA_2017',100,-1.1,1)
    dataHist_PhoMVA_2018 = TH1F('dataHist_PhoMVA_2018','dataHist_PhoMVA_2018',100,-1.1,1)
    if datasets['data_2016'] not in Trees:
        Trees[datasets['data_2016']] = TChain("Data_13TeV_H4GTag_0")
        Trees[datasets['data_2016']].AddFile(DataLocation+datasets['data_2016'])
        SetOwnership( Trees[datasets['data_2016']], True )
    if datasets['data_2017'] not in Trees:
        Trees[datasets['data_2017']] = TChain("Data_13TeV_H4GTag_0")
        Trees[datasets['data_2017']].AddFile(DataLocation+datasets['data_2017'])
        SetOwnership( Trees[datasets['data_2017']], True )
    if datasets['data_2018'] not in Trees:
        Trees[datasets['data_2018']] = TChain("Data_13TeV_H4GTag_0")
        Trees[datasets['data_2018']].AddFile(DataLocation+datasets['data_2018'])
        SetOwnership( Trees[datasets['data_2018']], True )


    Trees[datasets['data_2016']].Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>dataHist_PhoMVA_2016", TCut(Cut_data ))
    Trees[datasets['data_2017']].Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>dataHist_PhoMVA_2017", TCut(Cut_data ))
    Trees[datasets['data_2018']].Draw("pho1_MVA<-1.?-1.1:pho1_MVA>>dataHist_PhoMVA_2018", TCut(Cut_data ))
    data_integral_2016 = dataHist_PhoMVA_2016.Integral()
    data_integral_2017 = dataHist_PhoMVA_2017.Integral()
    data_integral_2018 = dataHist_PhoMVA_2018.Integral()

for plot in plots:
    Histos = []
    variable = plot[1]
    varName = plot[2]
    thisStack = 0
    thisHist = 0
    thisStack = myStack('test'+plot[0], varName, varName, dirName, lumi)
    dataintegral = 0
    if hideData == True:
        thisStack.hideData()

    modelHist = TH1F(plot[0]+"_hist", "", plot[3], plot[4], plot[5])

    backgroundHists = []
    background_sum = 0

    for isi, signal in enumerate(datasets["signal"]):
        thisName = plot[0]+"_Signal_"+"_"+signal['name']
        thisHist = modelHist.Clone(thisName)
        thisHist.SetLineColor(signal["color"])
        thisHist.SetLineColor(myCols[isi])
        thisHist.SetLineWidth(3)
        thisHist.SetLineStyle(signal["style"])
        weightedCut = "weight* (" + str(Cut_Signal)
        #print "Additional Cut " , Cut_additional
        weightedCut = weightedCut+Cut_additional+")"
        print "Signal cut: ", weightedCut
        # print "Signal weightedCut ", weightedCut
        if (year==2016):
           thisTreeLoc_2016 = signal["file_2016"]
           if thisTreeLoc_2016 not in Trees:
               Trees[thisTreeLoc_2016] = TChain(str(signal["treeName_2016"]))
               Trees[thisTreeLoc_2016].AddFile(SignalLocation+thisTreeLoc_2016)
               SetOwnership( Trees[thisTreeLoc_2016], True )
           locName_2016 = thisName+str(isi)+'_2016'
           locHist_2016 = thisHist.Clone(locName_2016)
           Trees[thisTreeLoc_2016].Draw(plot[1]+">>"+locName_2016,weightedCut )
           locHist_2016.Scale(lumi)
           thisHist.Add(locHist_2016)
           Histos.append(locHist_2016)
        elif (year==2017):
             thisTreeLoc_2017 = signal["file_2017"]
             if thisTreeLoc_2017 not in Trees:
                 Trees[thisTreeLoc_2017] = TChain(str(signal["treeName_2017"]))
                 Trees[thisTreeLoc_2017].AddFile(SignalLocation+thisTreeLoc_2017)
                 SetOwnership( Trees[thisTreeLoc_2017], True )
             locName_2017 = thisName+str(isi)+'_2017'
             locHist_2017 = thisHist.Clone(locName_2017)
             Trees[thisTreeLoc_2017].Draw(plot[1]+">>"+locName_2017,weightedCut )
             locHist_2017.Scale(lumi)
             thisHist.Add(locHist_2017)
             Histos.append(locHist_2017)
        elif (year==2018):
             thisTreeLoc_2018 = signal["file_2018"]
             if thisTreeLoc_2018 not in Trees:
                 Trees[thisTreeLoc_2018] = TChain(str(signal["treeName_2018"]))
                 Trees[thisTreeLoc_2018].AddFile(SignalLocation+thisTreeLoc_2018)
                 SetOwnership( Trees[thisTreeLoc_2018], True )
             locName_2018 = thisName+str(isi)+'_2018'
             locHist_2018 = thisHist.Clone(locName_2018)
             Trees[thisTreeLoc_2018].Draw(plot[1]+">>"+locName_2018,weightedCut )
             locHist_2018.Scale(lumi)
             print "Signal integral: ", locHist_2018.Integral()
             thisHist.Add(locHist_2018)
             Histos.append(locHist_2018)
        elif (year==1):
             thisTreeLoc_2016 = signal["file_2016"]
             thisTreeLoc_2017 = signal["file_2017"]
             thisTreeLoc_2018 = signal["file_2018"]
             if thisTreeLoc_2016 not in Trees:
                 Trees[thisTreeLoc_2016] = TChain(str(signal["treeName_2016"]))
                 Trees[thisTreeLoc_2016].AddFile(SignalLocation+thisTreeLoc_2016)
                 SetOwnership( Trees[thisTreeLoc_2016], True )

             if thisTreeLoc_2017 not in Trees:
                 Trees[thisTreeLoc_2017] = TChain(str(signal["treeName_2017"]))
                 Trees[thisTreeLoc_2017].AddFile(SignalLocation+thisTreeLoc_2017)
                 SetOwnership( Trees[thisTreeLoc_2017], True )


             if thisTreeLoc_2018 not in Trees:
                 Trees[thisTreeLoc_2018] = TChain(str(signal["treeName_2018"]))
                 Trees[thisTreeLoc_2018].AddFile(SignalLocation+thisTreeLoc_2018)
                 SetOwnership( Trees[thisTreeLoc_2018], True )

             locName_2016 = thisName+str(isi)+'_2016'
             locHist_2016 = thisHist.Clone(locName_2016)

             locName_2017 = thisName+str(isi)+'_2017'
             locHist_2017 = thisHist.Clone(locName_2017)

             locName_2018 = thisName+str(isi)+'_2018'
             locHist_2018 = thisHist.Clone(locName_2018)

             Trees[thisTreeLoc_2016].Draw(plot[1]+">>"+locName_2016,weightedCut )
             Trees[thisTreeLoc_2017].Draw(plot[1]+">>"+locName_2017,weightedCut )
             Trees[thisTreeLoc_2018].Draw(plot[1]+">>"+locName_2018,weightedCut )
             locHist_2016.Scale(35.9)
             locHist_2017.Scale(41.5)
             locHist_2018.Scale(54.38)
             #print "2016 signal: ", locHist_2016.Integral()
             #print "2017 signal: ", locHist_2017.Integral()
             #print "2018 signal: ", locHist_2018.Integral()
             locHist_2016.Add(locHist_2017)
             locHist_2016.Add(locHist_2018)
             #print "Lumi: ", lumi
             # locHist_2016.Scale(lumi)
             #print "Run2 signal: ", locHist_2016.Integral()

             thisHist.Add(locHist_2016)
             Histos.append(locHist_2016)
             signal_hist = thisHist.Clone('h_bdt')
             #signal_hist.SaveAs(SignalLocation+"Hist_Signal_m0p9_"+str(nbin)+"Bins.root")

        thisStack.addSignal(thisHist, signal["legend"], lumi)   ##-- add all signals to "mySignals " in "thisStack"
        del thisHist

    dataName = plot[0]+"_hist"+"_data"
    dataName_2016 = plot[0]+"_hist"+"_data_2016"
    dataName_2017 = plot[0]+"_hist"+"_data_2017"
    dataName_2018 = plot[0]+"_hist"+"_data_2018"

    modelHist.Clear()
    dataHist = 0
    dataHist = modelHist.Clone(dataName)
    dataHist_2016 = modelHist.Clone(dataName_2016)
    dataHist_2017 = modelHist.Clone(dataName_2017)
    dataHist_2018 = modelHist.Clone(dataName_2018)
    # dataHist_PhoMVA_2016 = TH1F('dataHist_PhoMVA_2016','dataHist_PhoMVA_2016',100,-1.1,1)
    # dataHist_PhoMVA_2017 = TH1F('dataHist_PhoMVA_2017','dataHist_PhoMVA_2017',100,-1.1,1)
    # dataHist_PhoMVA_2018 = TH1F('dataHist_PhoMVA_2018','dataHist_PhoMVA_2018',100,-1.1,1)
# # #    dataHist.Sumw2()
    data_integral = 1
    # data_integral_2016 = 1
    # data_integral_2017 = 1
    # data_integral_2018 = 1

    #Cut_data = Cut
    #Cut_data = Cut_data + Cut_additional
    # print "Cut_data: ", Cut_data

    if (year==1):
        if datasets['data_2016'] not in Trees:
            Trees[datasets['data_2016']] = TChain("Data_13TeV_H4GTag_0")
            Trees[datasets['data_2016']].AddFile(DataLocation+datasets['data_2016'])
            SetOwnership( Trees[datasets['data_2016']], True )
        if datasets['data_2017'] not in Trees:
            Trees[datasets['data_2017']] = TChain("Data_13TeV_H4GTag_0")
            Trees[datasets['data_2017']].AddFile(DataLocation+datasets['data_2017'])
            SetOwnership( Trees[datasets['data_2017']], True )
        if datasets['data_2018'] not in Trees:
            Trees[datasets['data_2018']] = TChain("Data_13TeV_H4GTag_0")
            Trees[datasets['data_2018']].AddFile(DataLocation+datasets['data_2018'])
            SetOwnership( Trees[datasets['data_2018']], True )
        Trees[datasets['data_2016']].Draw(plot[1]+">>"+dataName_2016, TCut(Cut_data ))
        Trees[datasets['data_2017']].Draw(plot[1]+">>"+dataName_2017, TCut(Cut_data ))
        Trees[datasets['data_2018']].Draw(plot[1]+">>"+dataName_2018, TCut(Cut_data ))

        # print dataHist_2016.Integral()
        # print dataHist_2017.Integral()
        # print dataHist_2018.Integral()

        # Trees[datasets['data_2016']].Draw("pho1_MVA>>dataHist_PhoMVA_2016", TCut(Cut_data ))
        # Trees[datasets['data_2017']].Draw("pho1_MVA>>dataHist_PhoMVA_2017", TCut(Cut_data ))
        # Trees[datasets['data_2018']].Draw("pho1_MVA>>dataHist_PhoMVA_2018", TCut(Cut_data ))


    else:
         if datasets['data'] not in Trees:
             # Trees[datasets['data']] = TChain("tagsDumper/trees/Data_13TeV_H4GTag_0")
             Trees[datasets['data']] = TChain("Data_13TeV_H4GTag_0")
             Trees[datasets['data']].AddFile(DataLocation+datasets['data'])
             SetOwnership( Trees[datasets['data']], True )
         Trees[datasets['data']].Draw(plot[1]+">>"+dataName, TCut(Cut_data))
         h = TH1F('h','h',100,30,120)



    # Trees[datasets['data']].Draw(plot[1]+">>"+dataName, TCut(Cut_data))

    data_integral = dataHist.Integral()
    print data_integral

    if (year ==1 ):

       # data_integral_2016 = dataHist_PhoMVA_2016.Integral()
       # data_integral_2017 = dataHist_PhoMVA_2017.Integral()
       # data_integral_2018 = dataHist_PhoMVA_2018.Integral()
       data_integral_run2 = data_integral_2016 + data_integral_2017 + data_integral_2018
       dataHist_2016.Add(dataHist_2017)
       dataHist_2016.Add(dataHist_2018)


       dataHist = dataHist_2016.Clone('h_bdt')
       # print dataHist.Integral()
       # dataHist.SaveAs(SignalLocation+"Hist_Data.root")
       #dataHist.SaveAs(SignalLocation+"BDT_Data_SB.root")
    # print '[data_integral_2016]: ' , data_integral_2016
    # print '[data_integral_2017]: ' , data_integral_2017
    # print '[data_integral_2018]: ' , data_integral_2018
    #
    # print '[data_integral_Run2]: ', data_integral_run2

    dataHist.SetMarkerStyle(20)
    dataHist.SetMarkerSize(0.8)
    dataHist.SetMarkerColor(1)
    dataHist.SetLineColor(1)
    dataHist.SetLineWidth(2)
    print " dataHist.Integral() ", dataHist.Integral()

    # dataHist.Scale(lumi)
    dataHist.SetBinErrorOption(TH1.kPoisson)
    thisStack.addData(dataHist, "Data") ##--add data to "thisStack"
    # thisFile = TFile(plot[0]+"_data.root", "RECREATE")
    # thisFile.cd()
    # dataHist.Write()
    # thisFile.Close()
    dummyTFile.cd()

    for background in datasets["background"]:
        thisName = plot[0]+"_hist"+"_"+background
        thisName_2016 = plot[0]+"_hist"+"_"+background+"_2016"
        thisName_2017 = plot[0]+"_hist"+"_"+background+"_2017"
        thisName_2018 = plot[0]+"_hist"+"_"+background+"_2018"
        thisHist = modelHist.Clone(thisName)
        thisHist_2016 = modelHist.Clone(thisName_2016)
        thisHist_2017 = modelHist.Clone(thisName_2017)
        thisHist_2018 = modelHist.Clone(thisName_2018)
        #thisHist.SetLineColor(TColor.GetColor(datasets["background"][background]["color"]))
        #thisHist.SetFillColor(TColor.GetColor(datasets["background"][background]["color"]))
        thisHist.SetLineColor(866)
        thisHist.SetFillColor(866)
        if (year == 1):

            for i,fi in enumerate(datasets["background"][background]["files"]):
                thisTreeLoc_2016 = fi["file_2016"]
                thisTreeLoc_2017 = fi["file_2017"]
                thisTreeLoc_2018 = fi["file_2018"]
                if thisTreeLoc_2016 not in Trees:
                    Trees[thisTreeLoc_2016] = TChain(str(fi["treeName_2016"]))
                    Trees[thisTreeLoc_2016].AddFile(BkgLocation+thisTreeLoc_2016)
                    SetOwnership( Trees[thisTreeLoc_2016], True )
                if thisTreeLoc_2017 not in Trees:
                    Trees[thisTreeLoc_2017] = TChain(str(fi["treeName_2017"]))
                    Trees[thisTreeLoc_2017].AddFile(BkgLocation+thisTreeLoc_2017)
                    SetOwnership( Trees[thisTreeLoc_2017], True )
                if thisTreeLoc_2018 not in Trees:
                   Trees[thisTreeLoc_2018] = TChain(str(fi["treeName_2018"]))
                   Trees[thisTreeLoc_2018].AddFile(BkgLocation+thisTreeLoc_2018)
                   SetOwnership( Trees[thisTreeLoc_2018], True )
                locName_2016 = thisName_2016+str(i)
                locName_2017 = thisName_2017+str(i)
                locName_2018 = thisName_2018+str(i)

                locHist_2016 = thisHist_2016.Clone(locName_2016)
                locHist_2017 = thisHist_2017.Clone(locName_2017)
                locHist_2018 = thisHist_2018.Clone(locName_2018)

                thisWeightedCut = ""
                print "bkgtype: ", bkgtype
                if (bkgtype == 'mix'):
                    if (doreweight):
                        #thisWeightedCut = "(1)*(" +Cut_Bkg + "&& "+fi["cut"] + Cut_additional+")"
                        if doSignalRegion:
                            thisWeightedCut = "(weight)*(" +Cut_Bkg + "&& "+fi["cut"]  +Cut_additional+"))"
                        else:
                            thisWeightedCut = "(weight)*(" +Cut_Bkg + "&& "+fi["cut"]  +" && !(tp_mass > 115 && tp_mass < 135)) "+Cut_additional +")"
                            #thisWeightedCut = "(weight)*(" +Cut_Bkg + "&& "+fi["cut"]  +" && !(tp_mass > 115 && tp_mass < 135)) "+Cut_additional +")"
                    else:
                        if doSignalRegion: thisWeightedCut = "(1)*(" +Cut_Bkg + "&& "+fi["cut"]  +")) "+Cut_additional
                        else: thisWeightedCut = "(1)*(" +Cut_Bkg + "&& "+fi["cut"]  +" && !(tp_mass > 115 && tp_mass < 135))) "+Cut_additional
                elif (bkgtype == 'vbf'):
                    if ('DataDriven' in locName_2016 or 'DataDriven' in locName_2017 or 'DataDriven' in locName_2018)  :
                        # thisWeightedCut = "(weight_VBF)*( !(tp_mass > 115 && tp_mass < 135) && pho3_MVA > -0.75 && pho4_MVA > -0.75)"
                        thisWeightedCut = "(weight)"
                    else:
                        # thisWeightedCut =  "(0)"
                        # thisWeightedCut =  "(weight)*(" +Cut + "&& "+fi["cut"]  + "&& pho1_MVA > -0.9 && pho2_MVA > -0.9))"
                        # thisWeightedCut =  "(weight)*(" +Cut + "&& "+fi["cut"]  + "&& pho1_MVA > -0.9 && pho2_MVA > -0.9 && pho3_MVA > -0.75 && pho4_MVA > -0.75 ))"
                        thisWeightedCut =  "(weight)*(" +Cut + "&& "+fi["cut"]  + "&& pho1_MVA > -0.2 && pho2_MVA > -0.4 && pho3_MVA > -0.75 && pho4_MVA > -0.75 ))"
                print "Background Cut: ", thisWeightedCut
                Trees[thisTreeLoc_2016].Draw(plot[1]+">>"+locName_2016, thisWeightedCut)
                Trees[thisTreeLoc_2017].Draw(plot[1]+">>"+locName_2017, thisWeightedCut)
                Trees[thisTreeLoc_2018].Draw(plot[1]+">>"+locName_2018, thisWeightedCut)
                if (Norm == 'DataSB'):
                    print "2016 scale:", data_integral_2016/locHist_2016.Integral()
                    print "2017 scale:", data_integral_2017/locHist_2017.Integral()
                    print "2018 scale:", data_integral_2018/locHist_2018.Integral()
                    locHist_2016.Sumw2()
                    locHist_2017.Sumw2()
                    locHist_2018.Sumw2() 
                    locHist_2016.Scale(data_integral_2016/locHist_2016.Integral())
                    locHist_2017.Scale(data_integral_2017/locHist_2017.Integral())
                    locHist_2018.Scale(data_integral_2018/locHist_2018.Integral())
                    # print locHist_2016.Integral()
                    # print locHist_2017.Integral()
                    # print locHist_2018.Integral()
                    locHist_2016.Add(locHist_2017)
                    locHist_2016.Add(locHist_2018)
                    print locHist_2016.Integral()
                    for bin in range(1,locHist_2016.GetNbinsX()+1 ):
                        locHist_2016.SetBinError(bin,sqrt(locHist_2016.GetBinContent(bin))) 
                    #print "2016 scale:", data_integral_2016/locHist_2016.Integral()
                    #print "2017 scale:", data_integral_2017/locHist_2017.Integral()
                    #print "2018 scale:", data_integral_2018/locHist_2018.Integral()
                    # print locHist_2016.Integral()
                    locHist_DataMix = locHist_2016.Clone('h_bdt')
                    locHist_DataMix.Sumw2() 
                    #locHist_DataMix.SaveAs(SignalLocation+'BDT_DataMix_SB.root')

                    #locHist_DataMix.SaveAs(SignalLocation+'Hist_DataMix_m0p9_'+str(nbin)+'Bins.root')
                       
                elif (Norm == 'Lumi'):
                    # locHist_2016.Scale(35.9/locHist_2016.Integral())
                    # locHist_2017.Scale(41.5/locHist_2017.Integral())
                    # locHist_2018.Scale(54.38/locHist_2018.Integral())
                    locHist_2016.Sumw2()
                    locHist_2017.Sumw2()
                    locHist_2018.Sumw2() 
                    locHist_2016.Scale(35.9)
                    locHist_2017.Scale(41.5)
                    locHist_2018.Scale(54.38)
                    locHist_2016.Add(locHist_2017)
                    locHist_2016.Add(locHist_2018)
                    # locHist_2016.Scale(data_integral_run2/locHist_2016.Integral())

                elif (Norm == 'Total'):
                    locHist_2016.Sumw2()
                    locHist_2017.Sumw2()
                    locHist_2018.Sumw2() 
                    locHist_2016.Add(locHist_2017)
                    locHist_2016.Add(locHist_2018)
                    locHist_2016.Scale(data_integral_run2/locHist_2016.Integral())
                    # print locHist_2016.Integral()

                thisHist.Add(locHist_2016)
                Histos.append(locHist_2016)
                background_sum += thisHist_2016.Integral()




        else:
            for i,fi in enumerate(datasets["background"][background]["files"]):
                thisTreeLoc = fi["file"]
                print fi["file"]
                if thisTreeLoc not in Trees:
                    Trees[thisTreeLoc] = TChain(str(fi["treeName"]))

                    Trees[thisTreeLoc].AddFile(BkgLocation+thisTreeLoc)
                    SetOwnership( Trees[thisTreeLoc], True )

                locName = thisName+str(i)
                locHist = thisHist.Clone(locName)
                thisWeightedCut = ""
                if (bkgtype == 'mix'):
                   if (doreweight):

                       thisWeightedCut = "(weight)*(" +Cut_Bkg + "&& "+fi["cut"]  +" && !(tp_mass > 115 && tp_mass < 135)))"
                   else:
                       thisWeightedCut = "(1)*(" +Cut_Bkg + "&& "+fi["cut"]  +" && !(tp_mass > 115 && tp_mass < 135)))"
                elif (bkgtype == 'vbf'):
                    if 'DataDriven' in locName:
                        # thisWeightedCut = "(weight_VBF)*( !(tp_mass > 115 && tp_mass < 135) && pho3_MVA > -0.75 && pho4_MVA > -0.75)"
                        thisWeightedCut = "(weight)"
                    else:
                        # thisWeightedCut =  "(0)"
                        # thisWeightedCut =  "(weight)*(" +Cut + "&& "+fi["cut"]  + "&& pho1_MVA > -0.9 && pho2_MVA > -0.9))"
                        # thisWeightedCut =  "(weight)*(" +Cut + "&& "+fi["cut"]  + "&& pho1_MVA > -0.9 && pho2_MVA > -0.9 && pho3_MVA > -0.75 && pho4_MVA > -0.75 ))"
                        thisWeightedCut =  "(weight)*(" +Cut + "&& "+fi["cut"]  + "&& pho1_MVA > -0.2 && pho2_MVA > -0.4 && pho3_MVA > -0.75 && pho4_MVA > -0.75 ))"
                        # thisWeightedCut =  "(weight_VBF*weight)*(" +Cut + "&& "+fi["cut"] + "&&" + Cut_MVA  + ")"
                elif (bkgtype == 'MC'):
                    thisWeightedCut = "(weight) * (" + Cut + "&&" + fi["cut"] + "))"
                    # print "mc background"
                    # print thisWeightedCut

                print "Background Cut: ", thisWeightedCut
                Trees[thisTreeLoc].Draw(plot[1]+">>"+locName, thisWeightedCut)
                # print locHist.Integral()


                # print data_integral
                print "Bkg integral: " , locHist.Integral()
                if (bkgtype=="MC"):locHist.Scale(lumi)
                else:  locHist.Scale(data_integral/locHist.Integral())


                #print locHist.Integral()
                thisHist.Add(locHist)
                Histos.append(locHist)
                background_sum += thisHist.Integral()

        backgroundHists.append([thisHist, datasets["background"][background]["legend"], datasets["background"][background]["position"]])
        del thisHist
    OrderedBackgrounds = sorted(backgroundHists, key=lambda x: x[2], reverse=True)
    for background in OrderedBackgrounds:
        thisStack.addHist(background[0], background[1], background[2])  ##--add all background histograms to "myHistograms" in "thisStack"

    thisStack.drawStack(prefix + plot[0])

    del thisStack

dummyTFile.Close()
os.system("rm dummy.root")
