
from pullClass import *
from ROOT import *
import json, os
import shutil
from configs import *
import resource

gROOT.SetBatch(1)
gROOT.ForceStyle()
gStyle.SetOptStat(0)

#mass = [60,55,50,45,40,35,20,25,20,15]
#mass = [50]
mass = [15]
inDir = "/eos/user/t/twamorka/h4g_fullRun2/TrainingApplied_22Jan2021/19Feb2021/Parametrized_NoCorrel_FullMassRange/"
#outDir = "/eos/user/t/twamorka/www/H4G_forApproval/BDTPlot/"
outDir = "/afs/cern.ch/work/b/bmarzocc/FlasHGG_Hto4G/CMSSW_8_0_26/src/H4G_Analysis/Paper_Plots/PLOTS/"
#cut_SB =  "(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass < 180 && !(tp_mass > 115 && tp_mass < 135) && bdt>-0.9 )"

cut_SR =  "(pho1_pt > 30 && pho2_pt > 18 && pho3_pt > 15 && pho4_pt > 15 && abs(pho1_eta) < 2.5 && abs(pho2_eta) < 2.5 && abs(pho3_eta) < 2.5 && abs(pho4_eta) < 2.5 && (abs(pho1_eta) < 1.4442 || abs(pho1_eta) > 1.566) && (abs(pho2_eta) < 1.4442 || abs(pho2_eta) > 1.566) && (abs(pho3_eta) < 1.4442 || abs(pho3_eta) > 1.566) && (abs(pho4_eta) < 1.4442 || abs(pho4_eta) > 1.566) && pho1_electronveto==1 && pho2_electronveto==1 && pho3_electronveto==1 && pho4_electronveto==1 && tp_mass > 110 && tp_mass < 180 && bdt>-0.9 )"

nBins=30

for m in mass:

    infile_2016_data = inDir+str(m)+"/data_2016.root"
    infile_2017_data = inDir+str(m)+"/data_2017.root"
    infile_2018_data = inDir+str(m)+"/data_2018.root"

    ch_2016_data = TChain()
    ch_2017_data = TChain()
    ch_2018_data = TChain()

    ch_2016_data.Add(infile_2016_data+"/Data_13TeV_H4GTag_0")
    ch_2017_data.Add(infile_2017_data+"/Data_13TeV_H4GTag_0")
    ch_2018_data.Add(infile_2018_data+"/Data_13TeV_H4GTag_0")

    h_2016_data = TH1F('h_2016_data','h_2016_data',nBins,-0.9,1)
    h_2017_data = TH1F('h_2017_data','h_2017_data',nBins,-0.9,1)
    h_2018_data = TH1F('h_2018_data','h_2018_data',nBins,-0.9,1)
    h_data_SR = TH1F('h_data_SR','h_data_SR',nBins,-0.9,1)

    ch_2016_data.Draw("bdt >> h_data_SR",cut_SR)
    ch_2017_data.Draw("bdt >> h_data_SR",cut_SR)
    ch_2018_data.Draw("bdt >> h_data_SR",cut_SR)


    # infile_2016_mix = inDir+str(m)+"/data_mix_2016_even.root"
    # infile_2017_mix = inDir+str(m)+"/data_mix_2017_even.root"
    # infile_2018_mix = inDir+str(m)+"/data_mix_2018_even.root"
    #
    # ch_2016_mix = TChain()
    # ch_2017_mix = TChain()
    # ch_2018_mix = TChain()
    #
    # ch_2016_mix.Add(infile_2016_mix+"/Data_13TeV_H4GTag_0")
    # ch_2017_mix.Add(infile_2017_mix+"/Data_13TeV_H4GTag_0")
    # ch_2018_mix.Add(infile_2018_mix+"/Data_13TeV_H4GTag_0")
    #
    # h_2016_mix = TH1F('h_2016_mix','h_2016_mix',30,-0.9,1)
    # h_2017_mix = TH1F('h_2017_mix','h_2017_mix',30,-0.9,1)
    # h_2018_mix = TH1F('h_2018_mix','h_2018_mix',30,-0.9,1)
    #
    # ch_2016_mix.Draw("bdt >> h_2016_mix",cut_SB+"*weight")
    # ch_2017_mix.Draw("bdt >> h_2017_mix",cut_SB+"*weight")
    # ch_2018_mix.Draw("bdt >> h_2018_mix",cut_SB+"*weight")
    #
    # h_2016_mix.Scale(h_2016_data.Integral()/h_2016_mix.Integral())
    # h_2017_mix.Scale(h_2017_data.Integral()/h_2017_mix.Integral())
    # h_2018_mix.Scale(h_2018_data.Integral()/h_2018_mix.Integral())
    #
    # h_2016_mix.Add(h_2017_mix)
    # h_2016_mix.Add(h_2018_mix)


    in_file = TFile(inDir+str(m)+"/BDT_Histos_smoothing_SmoothSuper_bins"+str(nBins)+"_massMin115.0_massMax135.0.root","read")
    #h_data_SB = in_file.Get("h_bdt_data_SB")
    h_datamix_weighted = in_file.Get("h_bdt_datamix_SR_weighted_smooth")
    h_datamix_weighted_SB = in_file.Get("h_bdt_datamix_SB_weighted_smooth")
    h_datamix_weighted.Add(h_datamix_weighted_SB)
    h_datamix_weighted.Sumw2()
    h_datamix_weighted.Scale(h_data_SR.Integral()/h_datamix_weighted.Integral())
    for bin in range(1,h_datamix_weighted.GetNbinsX()+1 ):
        h_datamix_weighted.SetBinError(bin,sqrt(h_datamix_weighted.GetBinContent(bin))) 

    h_datamix_weighted_err = h_datamix_weighted.Clone()
    h_datamix_weighted_err.SetFillStyle(3001)
    h_datamix_weighted_err.SetFillColor(kGray+2)
    h_datamix_weighted_err.SetLineColor(kWhite)
    h_bdt_signal_SR = in_file.Get("h_bdt_signal_SR")
    h_bdt_signal_SR.Scale(h_bdt_signal_SR.Integral()*2)

    # c = TCanvas()
    h_data_SR.SetLineColor(1)
    h_data_SR.SetMarkerStyle(20)
    h_data_SR.SetMarkerColor(1)

    h_datamix_weighted.SetLineColor(868)
    h_datamix_weighted.SetFillColor(868)
    # #
    # h_2016_mix.SetLineColor(kRed)
    # h_2016_mix.SetMarkerColor(kRed)
    # h_2016_mix.SetLineWidth(2)

    h_bdt_signal_SR.SetLineColor(kRed)
    h_bdt_signal_SR.SetLineWidth(2)

    # h_datamix_weighted.SetTitle("")
    # h_datamix_weighted.GetYaxis().SetTitle("Events")
    # h_datamix_weighted.GetXaxis().SetTitle("BDT")
    #
    # # h_datamix_weighted.GetYaxis().SetLabelSize(0.0)
    # axis = TGaxis(-5, 20, -5, 220, 20, 220, 510, "")
    # axis.SetLabelFont(43)
    # axis.SetLabelSize(15)
    # axis.Draw()

    # h_datamix_weighted.SetMaximum(10e6)
    # h_datamix_weighted.SetMinimum(0.001)





    # c0 = TCanvas('a', 'a', 800, 900)

    # tlatex = TLatex()
    # tlatex.SetNDC()
    # tlatex.SetTextAngle(0)
    # tlatex.SetTextColor(kBlack)
    # tlatex.SetTextFont(63)
    # tlatex.SetTextAlign(11)
    # tlatex.SetTextSize(25)
    # tlatex.DrawLatex(0.11, 0.91, "CMS")
    # tlatex.SetTextFont(53)
    # tlatex.DrawLatex(0.18, 0.91, " Work in progress")
    # tlatex.SetTextFont(43)
    # tlatex.SetTextSize(23)
    # Lumi = "L = 131.78 fb^{-1} (13 TeV)"#, "+year+")"
    # tlatex.SetTextAlign(31)
    # tlatex.DrawLatex(0.9, 0.91, Lumi)

    # pad1 = TPad('pad1','pad1',0,0.3,1,1)
    # pad1.SetBottomMargin(0)
    # pad1.Draw()
    canv = TCanvas("canv","canv",700,700)
    pad1 = TPad("pad1","pad1",0,0.25,1,1)
    pad1.SetTickx()
    pad1.SetTicky()
    pad1.SetBottomMargin(0.18)
    pad1.SetLeftMargin(0.12)
    pad1.Draw()
    pad2 = TPad("pad2","pad2",0,0,1,0.35)
    pad2.SetTickx()
    pad2.SetTicky()
    pad2.SetTopMargin(0.03)
    pad2.SetBottomMargin(0.25)
    pad2.SetLeftMargin(0.12)
    pad2.Draw()
    padSizeRatio = 0.75/0.35

    # Axis options
    TGaxis.SetMaxDigits(4)
    TGaxis.SetExponentOffset(-0.05,0.00,"y")


    # Add TLatex to plot
    lat0 = TLatex()
    lat0.SetTextFont(42)
    lat0.SetTextAlign(11)
    lat0.SetNDC()
    lat0.SetTextSize(0.045)
    #lat0.DrawLatex(0.12,0.94,"#bf{CMS} #it{Preliminary}")
    lat0.DrawLatex(0.12,0.94,"#bf{CMS}")
    lat0.DrawLatex(0.6,0.94,"132 fb^{-1} (13 TeV)")

    pad1.cd()
    pad1.SetLogy()

    # leg.Draw("same")


    # print h_datamix_weighted.GetMaximum()
    h_datamix_weighted.SetMaximum((h_datamix_weighted.GetMaximum()+h_datamix_weighted.GetBinError(h_datamix_weighted.GetMaximumBin()))*10)
    h_datamix_weighted.SetMinimum(0.01)
    h_datamix_weighted.SetTitle("")
    h_datamix_weighted.GetXaxis().SetTitle("")
    h_datamix_weighted.GetXaxis().SetLabelSize(0)
    h_datamix_weighted.GetYaxis().SetTitleSize(0.05)
    h_datamix_weighted.GetYaxis().SetTitle("Events")
    h_datamix_weighted.GetYaxis().SetTitleOffset(1.1)
    h_datamix_weighted.GetYaxis().SetLabelSize(0.035)
    h_datamix_weighted.GetYaxis().SetLabelOffset(0.007)

    lline = TLine(0.987,0,pad1.GetUxmax(),0)
    lline.SetLineStyle(1)
    #lline.Draw('same')
    h_datamix_weighted.Draw("hist same")
    h_datamix_weighted_err.Draw("E2 same")

    h_data_SR.Draw("PE same")
    h_bdt_signal_SR.Draw("hist same")

    leg = TLegend(0.6, 0.68, 0.89, 0.87)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.040)


    leg.AddEntry(h_data_SR,'Data','pe')
    leg.AddEntry(h_datamix_weighted,'Event mixing','lf')
    leg.AddEntry(h_datamix_weighted_err,'Stat. uncertainty','lf')
    leg.AddEntry(h_bdt_signal_SR,'m_{a} = '+str(mass)+' GeV','l')

    leg.Draw("same")


    lline.Draw("same")
    print h_datamix_weighted.GetXaxis().FindBin(0.987)
    pad2.cd()
    pad2.SetGridy()

    h_ratio_weighted = h_datamix_weighted.Clone("h_ratio_weighted")
    h_ratio_pullE = h_datamix_weighted.Clone("h_ratio_pullE")
    
    hist1 = h_datamix_weighted.Clone("hist1")
    hist2 = h_data_SR.Clone("hist2")
    for i in xrange(0, hist1.GetNbinsX()):
		Bin = i+1
		b1 = hist1.GetBinContent(Bin)
		b2 = hist2.GetBinContent(Bin)

		if b1 == 0 or b2 == 0:
			continue

		ratio = b1/b2
                
		b1sq = b1*b1
		b2sq = b2*b2

		e1sq_up = hist1.GetBinErrorUp(Bin)*hist1.GetBinErrorUp(Bin)
		e2sq_up = hist2.GetBinErrorUp(Bin)*hist2.GetBinErrorUp(Bin)
                #e2sq_up = 0.

		e1sq_low = hist1.GetBinErrorLow(Bin)*hist1.GetBinErrorLow(Bin)
		e2sq_low = hist2.GetBinErrorLow(Bin)*hist2.GetBinErrorLow(Bin)
                #e2sq_low = 0.

		error_up = sqrt((e1sq_up * b2sq + e2sq_up * b1sq) / (b2sq * b2sq))
		error_low = sqrt((e1sq_low * b2sq + e2sq_low * b1sq) / (b2sq * b2sq))

                h_ratio_weighted.SetBinContent(Bin,ratio)
                h_ratio_weighted.SetBinError(Bin,0.)
                #h_ratio_weighted.SetBinError(Bin,error_up)

                h_ratio_pullE.SetBinContent(Bin,1.)
                h_ratio_pullE.SetBinError(Bin,error_up)
                #h_ratio_pullE.SetBinError(Bin,error_low)

    h_ratio_pullE.SetMarkerColor(kGray+2)
    h_ratio_pullE.SetMarkerStyle(6)
    h_ratio_pullE.SetFillColorAlpha(kGray+2, 0.5)
    h_ratio_pullE.SetFillStyle(1001)
    h_ratio_pullE.SetLineColor(kGray+2)

    h_ratio_weighted.SetMaximum(1.99)
    h_ratio_weighted.SetMinimum(0.01)
    h_ratio_weighted.SetTitle("")
    h_ratio_weighted.GetYaxis().SetTitleSize(0.095)
    h_ratio_weighted.GetYaxis().SetTitleOffset(0.5)
    h_ratio_weighted.GetYaxis().SetTitle("Bkg./Data")
    h_ratio_weighted.GetYaxis().SetNdivisions(505)
    h_ratio_weighted.GetXaxis().SetTitle("BDT Output")

    h_ratio_weighted.GetXaxis().SetTitleSize(0.05*padSizeRatio)
    h_ratio_weighted.GetXaxis().SetLabelSize(0.035*padSizeRatio)
    h_ratio_weighted.GetXaxis().SetLabelOffset(0.007)
    h_ratio_weighted.GetXaxis().SetTickLength(0.03*padSizeRatio)
    h_ratio_weighted.GetYaxis().SetLabelSize(0.035*padSizeRatio)
    h_ratio_weighted.GetYaxis().SetLabelOffset(0.007)
    # h_ratio_weighted.GetYaxis().SetTitle("")
    h_ratio_weighted.SetMarkerStyle(20)
    h_ratio_weighted.SetMarkerColor(1)
    h_ratio_weighted.SetLineColor(1)
    h_ratio_weighted.Draw("P")
    h_ratio_pullE.Draw("E2,same")
    h_ratio_weighted.Draw("P,same")
    # h_ratio_weighted.Draw("EP")

    # lline = TLine(pad2.GetUxmin(),1,pad2.GetUxmax(),1)
    # lline.SetLineStyle(1)
    # lline.Draw('same')
    pad2.Update()

    canv.Draw()
    canv.SaveAs(outDir+"BDT_M"+str(m)+"_nBins_"+str(nBins)+".pdf")
    canv.SaveAs(outDir+"BDT_M"+str(m)+"_nBins_"+str(nBins)+".png")
    canv.SaveAs(outDir+"BDT_M"+str(m)+"_nBins_"+str(nBins)+".root")
    canv.SaveAs(outDir+"BDT_M"+str(m)+"_nBins_"+str(nBins)+".C")
    # leg.Draw("same")

    # axis = TGaxis(0, 0, 0, 220, 0.001,220,510,"")
    # axis.SetLabelFont(43)
    # axis.SetLabelSize(15)
    # axis.Draw("same")

    #
    # c0.cd()
    #
    # pad2 = TPad("pad2", "pad2", 0, 0.09, 1, 0.3)
    # pad2.SetTopMargin(0)
    # pad2.SetBottomMargin(0.2)
    # pad2.Draw()
    # pad2.cd()
    #
    #
    # h_ratio_weighted.SetMarkerColor(TColor.GetColor('#2B74BA'))
    # h_ratio_weighted.SetMinimum(0.5)
    # h_ratio_weighted.SetMaximum(3.0)
    # h_ratio_weighted.Sumw2()
    # h_ratio_weighted.SetStats(0)
    # h_ratio_weighted.Divide(h_data_SR)
    # h_ratio_weighted.SetMarkerStyle(20)
    # h_ratio_weighted.Draw("EP")
    # pad2.Update()
    # lline = TLine(pad2.GetUxmin(),1,pad2.GetUxmax(),1)
    # lline.SetLineStyle(1)
    # lline.Draw('same')
    # h_ratio_weighted.GetYaxis().SetTitle("Bkg/Data")
    # h_ratio_weighted.GetYaxis().SetNdivisions(505)
    # h_ratio_weighted.GetYaxis().SetTitleSize(20)
    # h_ratio_weighted.GetYaxis().SetTitleFont(43)
    # h_ratio_weighted.GetYaxis().SetTitleOffset(1.55)
    # h_ratio_weighted.GetYaxis().SetLabelFont(43) #Absolute font size in pixel (precision 3)
    # h_ratio_weighted.GetYaxis().SetLabelSize(15)
    # h_ratio_weighted.GetXaxis().SetNdivisions(100)
    # h_ratio_weighted.GetXaxis().SetTitleSize(20)
    # h_ratio_weighted.GetXaxis().SetTitleFont(43)
    # h_ratio_weighted.GetXaxis().SetTitleOffset(4.)
    # h_ratio_weighted.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
    # h_ratio_weighted.GetXaxis().SetLabelSize(15)
    # h_ratio_weighted.GetXaxis().SetNdivisions(515)
    # h_ratio_weighted.GetXaxis().SetTickLength(0.15)
    #
    # h_ratio_unweighted = h_2016_mix.Clone("h_ratio_unweighted")
    # h_ratio_unweighted.SetLineColor(kRed)
    # h_ratio_unweighted.SetMarkerColor(kRed)
    # h_ratio_unweighted.SetMinimum(0.5)
    # h_ratio_unweighted.SetMaximum(3.0)
    # h_ratio_unweighted.Sumw2()
    # h_ratio_unweighted.SetStats(0)
    # h_ratio_unweighted.Divide(h_data_SR)
    # h_ratio_unweighted.SetMarkerStyle(20)
    # h_ratio_unweighted.Draw("EP same")
    # pad2.Update()
    #
    # h_ratio_unweighted.GetYaxis().SetTitle("Bkg/Data")
    # h_ratio_unweighted.GetYaxis().SetNdivisions(505)
    # h_ratio_unweighted.GetYaxis().SetTitleSize(20)
    # h_ratio_unweighted.GetYaxis().SetTitleFont(43)
    # h_ratio_unweighted.GetYaxis().SetTitleOffset(1.55)
    # h_ratio_unweighted.GetYaxis().SetLabelFont(43) #Absolute font size in pixel (precision 3)
    # h_ratio_unweighted.GetYaxis().SetLabelSize(15)
    # h_ratio_unweighted.GetXaxis().SetNdivisions(100)
    # h_ratio_unweighted.GetXaxis().SetTitleSize(20)
    # h_ratio_unweighted.GetXaxis().SetTitleFont(43)
    # h_ratio_unweighted.GetXaxis().SetTitleOffset(4.)
    # h_ratio_unweighted.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
    # h_ratio_unweighted.GetXaxis().SetLabelSize(15)
    # h_ratio_unweighted.GetXaxis().SetNdivisions(515)
    # h_ratio_unweighted.GetXaxis().SetTickLength(0.15)
    #
    # c0.Update()
    # c0.Draw()
    # c0.SaveAs("/eos/user/t/twamorka/www/H4G_Review/BDT_Distributions/LOG_bdt_M"+str(m)+".pdf")
    # c0.SaveAs("/eos/user/t/twamorka/www/H4G_Review/BDT_Distributions/LOG_bdt_M"+str(m)+".png")
    # c0.SaveAs("/eos/user/t/twamorka/www/H4G_Review/BDT_Distributions/LOG_bdt_M"+str(m)+".C")
    # c0.SaveAs("/eos/user/t/twamorka/www/H4G_Review/BDT_Distributions/LOG_bdt_M"+str(m)+".root")
