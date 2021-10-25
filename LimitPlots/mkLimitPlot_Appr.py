import ROOT
from root_numpy import tree2array

ROOT.gROOT.SetBatch(ROOT.kTRUE)

import argparse
parser =  argparse.ArgumentParser(description='H4G Brazil Plot Maker')
parser.add_argument('-iD','--inDir',dest='inDir',required=True,type=str)

opt = parser.parse_args()
inDir = opt.inDir


outputLoc = '/eos/user/t/twamorka/www/H4G_forApproval/'

## Obtain values of expected and observed limits for each mass point
# quantile = ["_0.025","_0.16","_0.5","_0.84","_0.975","_Observed"]
# higgXS = 52*1000
higgXS = 1
quantile = [0.025, 0.16, 0.5, 0.84, 0.975]
mass = []
exp_median = []
exp_up01sigma = []
exp_up02sigma = []
exp_down01sigma = []
exp_down02sigma = []
obs = []


## Obtain values of expected and observed limits for each mass point
# for m in range (15,61): ## m(a) ranges from 15 to 60 GeV
#     mass.append(m)
for m in range(15,63,1):
    mass.append(m)
    if (m < 40):
       mass.append(m+0.5)
    #if (m+0.5!=45.5 and m+0.5!=60.5):
       #mass.append(m+0.5)
print len(mass)
print mass
for m in mass:
    print "mass: ", m
    for q in quantile:
        file_in = ROOT.TFile(inDir+"/higgsCombine_M"+str(m)+"_"+str(q)+".HybridNew.mH125.root","read")
        #print "infile: ", inDir+"/higgsCombine_M"+str(m)+"_"+str(q)+".HybridNew.mH125.root"
        tree_in = file_in.Get("limit")
        limit = tree2array(tree_in,branches="limit")
        # print limit
        if (q==0.025):
            exp_down02sigma.append(limit[0]/higgXS)
            # exp_twoSigma.SetPoint(i, masses[i][1], limit[4])
        elif (q==0.16):
            exp_down01sigma.append(limit[0]/higgXS)
        elif (q==0.5):
            exp_median.append(limit[0]/higgXS)
        elif (q==0.84):
            exp_up01sigma.append(limit[0]/higgXS)
        elif (q==0.975):
            exp_up02sigma.append(limit[0]/higgXS)

    file_in_obs = ROOT.TFile(inDir+"/higgsCombine_M"+str(m)+"_Observed.HybridNew.mH125.root","read")
    #print "infile obs: ", inDir+"/higgsCombine_M"+str(m)+"_Observed.HybridNew.mH125.root"
    tree_in_obs = file_in_obs.Get("limit")
    limit_obs = tree2array(tree_in_obs,branches="limit")
    obs.append(limit_obs[0]/higgXS)

print (obs)


median_gr = ROOT.TGraph(len(mass))
oneSigma_gr = ROOT.TGraph(2*len(mass))
twoSigma_gr = ROOT.TGraph(2*len(mass))
obs_gr = ROOT.TGraph(len(mass))
for i in range(len(mass)):
    #print i, " ", mass[i]," ", exp_up02sigma[i], " ", 2*(len(mass))-1-i
    twoSigma_gr.SetPoint(i, mass[i],exp_up02sigma[i] ) ## +2 sigma
    oneSigma_gr.SetPoint(i, mass[i],exp_up01sigma[i] ) ## +1 sigma
    median_gr.SetPoint(i, mass[i],exp_median[i] )
    oneSigma_gr.SetPoint(2*(len(mass))-1-i, mass[i],exp_down01sigma[i] ) ## -1 sigma
    twoSigma_gr.SetPoint(2*(len(mass))-1-i, mass[i], exp_down02sigma[i]) ## -2 sigma
    obs_gr.SetPoint(i,mass[i],obs[i])
    median_gr.SetLineColor(ROOT.kBlack)
    median_gr.SetLineWidth(2)
    median_gr.SetLineStyle(2)
    twoSigma_gr.SetFillColor(ROOT.kOrange)
    twoSigma_gr.SetLineColor(ROOT.kOrange)
    oneSigma_gr.SetFillColor(ROOT.kGreen+1)
    oneSigma_gr.SetLineColor(ROOT.kGreen+1)
    obs_gr.SetLineColor(ROOT.kBlack)
    obs_gr.SetLineWidth(2)
    obs_gr.SetMarkerStyle(20)
    obs_gr.SetMarkerSize(0.8)
    obs_gr.SetMarkerColor(ROOT.kBlack)
# print twoSigma_gr

canv = ROOT.TCanvas("canv","canv",700,700)
canv.SetLeftMargin(0.175)
canv.SetTickx(0)
canv.SetTicky(0)
frame = canv.DrawFrame(1.4,0.001, 4.1, 10)
#frame = canv.DrawFrame(20,0.001, 4.1, 50)
frame.GetYaxis().CenterTitle()
frame.GetYaxis().SetTitleSize(0.05)
frame.GetXaxis().SetTitleSize(0.05)
frame.GetXaxis().SetLabelSize(0.04)
frame.GetYaxis().SetLabelSize(0.04)
frame.GetYaxis().SetTitleOffset(0.9)
frame.GetXaxis().SetNdivisions(508)
frame.GetYaxis().CenterTitle(True)
frame.GetXaxis().SetTitle("m_{a} (GeV)")
frame.GetYaxis().SetTitle("#sigma(pp#rightarrowH) #times BR(H#rightarrowaa#rightarrow#gamma#gamma#gamma#gamma) (fb)")
#frame.GetYaxis().SetTitle("#frac{#sigma(pp#rightarrowH)}{#sigma_{SM}} #times BR(H#rightarrowaa#rightarrow#gamma#gamma#gamma#gamma)")
frame.GetXaxis().SetTitleSize(0.045)
frame.GetYaxis().SetTitleOffset(1.25)
#frame.GetYaxis().SetTitleOffset(1.75)
frame.GetYaxis().SetTitleSize(0.045)
frame.GetXaxis().SetLimits(15,62)
#frame.GetXaxis().SetNdivisions(10)
frame.SetMinimum(0.1)
#frame.GetYaxis().SetDecimals()
frame.SetMaximum(10)
#frame.SetMaximum(0)

#leg = ROOT.TLegend(0.6,0.68,0.85,0.91)

x1 = 0.55
x2 = x1 + 0.24
y2 = 0.76
y1 = 0.60
#leg = ROOT.TLegend(x1,y1,x2,y2)
leg = ROOT.TLegend(0.54,0.63,0.78,0.79)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetLineColor(0)
leg.SetTextSize(0.030)
#leg.SetTextFont(42)
#leg.SetEntrySeparation(0.4)

pad = canv.cd()
frame.SetLineWidth(3)
leg.AddEntry(obs_gr,'Observed','lp')
leg.AddEntry(median_gr,'Median expected','lp')
leg.AddEntry(oneSigma_gr,'68% CL expected','f')
leg.AddEntry(twoSigma_gr,'95% CL expected','f')
#canv.SetTickx()
#canv.SetTicky()
leg.Draw('same')
#median_gr.Draw('LP same')
#oneSigma_gr.Draw('F same')
twoSigma_gr.Draw('F same')
oneSigma_gr.Draw('F same')
median_gr.Draw('LP same')
obs_gr.Draw('LP same')
lat0 = ROOT.TLatex()
lat0.SetTextFont(42)
lat0.SetTextAlign(11)
lat0.SetNDC()
lat0.SetTextSize(0.045)

#lat0.DrawLatex(0.18,0.92,"#bf{CMS} #it{Preliminary}")
#lat0.DrawLatex(0.23,0.827,"#bf{CMS} #it{Preliminary}")
#lat0.DrawLatex(0.25,0.92,"#bf{CMS} #it{Preliminary}")
lat0.DrawLatex(0.18,0.92,"#bf{CMS}")
lat0.DrawLatex(0.6,0.92,"132 fb^{-1} (13 TeV)")

lat1 = ROOT.TLatex()
lat1.SetTextFont(42)
lat1.SetTextAlign(11)
lat1.SetNDC()
lat1.SetTextSize(0.035)

lat1.DrawLatex(0.56,0.82,"95% CL upper limits")

# canv.Update()
# canv.Draw()
ROOT.gPad.SetTicks(1,1)
frame.Draw('sameaxis')
canv.SetLogy()
canv.SaveAs(outputLoc+"Limit_FineDebug_ForCWR_LogY.pdf")
canv.SaveAs(outputLoc+"Limit_FineDebug_ForCWR_LogY.png")
canv.SaveAs(outputLoc+"Limit_FineDebug_ForCWR_LogY.root")
#canv.SaveAs(outputLoc+"Limit_FineDebug_ForCWR.pdf")
#canv.SaveAs(outputLoc+"Limit_FineDebug_ForCWR.png")
#canv.SaveAs(outputLoc+"Limit_FineDebug_ForCWR.root")
