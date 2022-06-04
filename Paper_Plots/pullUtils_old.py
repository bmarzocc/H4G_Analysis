from ROOT import *
from copy import deepcopy
from math import *
from array import array
from MyCMSStyle import *

# c1 = TCanvas('c1', 'c1', 800, 700)

# def test():
	# return 1
def getSig(hist_B, hist_S):

	c1 = TCanvas('c1', 'c1', 700, 700)
	graph = TGraph(hist_B)
	npoint = 0
	for i in xrange(0, hist_B.GetNbinsX()):
		Bin = i+1
		b1 = hist_B.GetBinContent(Bin)
		b2 = hist_S.GetBinContent(Bin)

		if b1 == 0 or b2 == 0:
			continue

		ratio = b2/sqrt(b1)
		#print ratio
		graph.SetPoint(npoint, hist_B.GetBinCenter(Bin), ratio)
		npoint += 1
	graph.Set(npoint)
	# graph.Draw()

        return graph
def getRatio(hist1, hist2):
	c1 = TCanvas('c1', 'c1', 700, 700)
        ratio_list = []
	graph = TGraphAsymmErrors(hist1)
	npoint = 0
        chi2_hist = 0
        chi2_ratio = 0
	for i in xrange(0, hist1.GetNbinsX()):
		Bin = i+1
		b1 = hist1.GetBinContent(Bin)
		b2 = hist2.GetBinContent(Bin)

		if b1 == 0 or b2 == 0:
			continue

		ratio = b1/b2
                #print "b1: ", b1, " b2: ", b2
		chi2_hist += ((b1-b2)*(b1-b2))/b2
		chi2_ratio += (ratio - 1)*(ratio-1)
                #print ((b1-b2)*(b1-b2))/b2, "  " , (ratio - 1)*(ratio-1)
		b1sq = b1*b1
		b2sq = b2*b2

		e1sq_up = hist1.GetBinErrorUp(Bin)*hist1.GetBinErrorUp(Bin)
		#e2sq_up = hist2.GetBinErrorUp(Bin)*hist2.GetBinErrorUp(Bin)
                e2sq_up = 0.

		e1sq_low = hist1.GetBinErrorLow(Bin)*hist1.GetBinErrorLow(Bin)
		#e2sq_low = hist2.GetBinErrorLow(Bin)*hist2.GetBinErrorLow(Bin)
                e2sq_low = 0.

		#error_up = sqrt((e1sq_up * b2sq + e2sq_up * b1sq) / (b2sq * b2sq))
		#error_low = sqrt((e1sq_low * b2sq + e2sq_low * b1sq) / (b2sq * b2sq))
                error_up = 0.
		error_low = 0.

		graph.SetPoint(npoint, hist1.GetBinCenter(Bin), ratio)
		graph.SetPointError(npoint, 0, 0, error_low, error_up)
		npoint += 1
	graph.Set(npoint)
	graph.Draw()
        ratio_list.append(graph)
        ratio_list.append(chi2_hist)
        ratio_list.append(chi2_ratio)
	#print "chi2_hist: ", chi2_hist
	#print "chi2_ratio: ", chi2_ratio
	# c1.SaveAs("ratio.pdf")
	#return graph
        return ratio_list

# The following function was copied (with permission) from the Latino's GitHub:
# https://github.com/latinos/LatinoAnalysis/blob/master/ShapeAnalysis/scripts/mkPlot.py#L437
# Thanks Andrea!
#

# _____________________________________________________________________________
# --- poissonian error bayesian 1sigma band
#                                     1/0   1/0
def GetPoissError(numberEvents, down, up):
	alpha = (1-0.6827)
	L = 0
	if numberEvents!=0 :
		L = Math.gamma_quantile (alpha/2,numberEvents,1.)
	U = 0
	if numberEvents==0 :
		U = Math.gamma_quantile_c (alpha/2,numberEvents+1,1.)
	else :
		U = Math.gamma_quantile_c (alpha/2,numberEvents+1,1.)

       # the error
	L = numberEvents - L
	if numberEvents > 0 :
		U = U - numberEvents
       #else :
         #U = 1.14 # --> bayesian interval Poisson with 0 events observed
         #1.14790758039 from 10 lines above

	if up and not down :
		return U
	if down and not up :
		return L
	if up and down :
		return [L,U]

def doPull(bkg, data, stack):
	data_nbins = data.GetNbinsX()
	bkg_nbins = bkg.GetNbinsX()
	if data_nbins != bkg_nbins:
		print "Your data and background histograms don't match!"
		return 0
	px = []
	pxh = []
	pxl = []
	pyh = []
	pyl = []
	py = []
	pe = []
	pex = []
	pey = []
	largest = 0
	UpEdge = 0
	LowEdge = 0
	bWidth = 0
	thisStack = stack.Clone("thisStackClone")
	for x in xrange(0, data_nbins):
		LowEdge = data.GetXaxis().GetBinLowEdge(data_nbins - x)
		UpEdge = data.GetXaxis().GetBinUpEdge(x+1)
		n_data = data.GetBinContent(x+1)
		n_bkg = bkg.GetBinContent(x+1)
		bin_center = data.GetBinCenter(x+1)
		bWidth = data.GetBinWidth(x+1)*0.5
#		bWidth = data.GetBinWidth(x+1)*1
		px.append(bin_center)
		pey.append(1)
		pex.append(bWidth)
		pxh.append(0)
		pxl.append(0)
		yErrors = GetPoissError(n_data, 1, 1)
		pyl.append(yErrors[0])
		pyh.append(yErrors[1])
		if n_bkg == 0 :
			if n_data == 0:
				py.append(1)
				pe.append(0)
			else:
				py.append(5)
				pe.append(5)
		else:
			sigma = (float(n_data))/float((n_bkg))
#			erro = sigma*sqrt(1./float(n_data) + 1./float(n_bkg))
#			erro = sqrt( float(n_bkg) )
#			erro = (bkg.GetBinContent(x+1)+bkg.GetBinError(x+1))/bkg.GetBinContent(x+1)
			erro = bkg.GetBinError(x+1)
			err = thisStack.GetStack().Last().GetBinError(x+1)
			cont = thisStack.GetStack().Last().GetBinContent(x+1)
			erro = (cont+err)/cont - 1
#			erro = stack.GetStack().Last().GetBinError(x+1)
                        d = data.GetBinContent(x+1)
                        b = bkg.GetBinContent(x+1)
                        sd = sqrt(data.GetBinContent(x+1))
                        sb = sqrt(bkg.GetBinContent(x+1))
                        erro = sqrt(sb*sb/(d*d) + sd*sd*b*b/(d*d*d*d))
			py.append(sigma)
			pe.append(erro)
			#print "bin center:", bin_center, "bin width",bWidth, "n data:",n_data, "nbkg:",n_bkg, "sigma:",sigma, "erro:",erro
			if abs(sigma) > largest:
				largest = abs(sigma)
			if abs(erro) > largest:
				largest = abs(erro)
	pX = array('d', px)
	pXH = array('d', pxh)
	pXL = array('d', pxl)
	pY = array('d', py)
	pYH = array('d', pyh)
	pYL = array('d', pyl)
	pE = array('d', pe)
	pEY = array('d', pey)
	pEX = array('d', pex)
#	pullData = TGraphAsymmErrors(len(pX), pX, pY, pXL, pXH, pYL, pYH) #points
	# pullData = getRatio(data, bkg) #TGraphAsymmErrors(len(pX), pX, pY, pXL, pXH, pYL, pYH) #points
	#pullData = getRatio(bkg,data)
        pullData = getRatio(bkg,data)[0]
        chi2_hist =  getRatio(bkg,data)[1]
        chi2_ratio =  getRatio(bkg,data)[2]
	# getRatio_pull(datas,bkg)
	pullError = TGraphErrors(len(pX), pX, pEY, pEX, pE) #bars
	Largest = ceil(largest*1.2)
	pullError.SetMaximum(1.99)
	pullError.SetMinimum(0.01)
	pullData.SetMaximum(1.99)
	pullData.SetMinimum(0.01)
	#pullError.SetMaximum(5)
	#pullError.SetMinimum(0.001)
	#pullData.SetMaximum(5)
	#pullData.SetMinimum(0.001)
	pullError.SetTitle("")
	pullData.SetTitle("")
	pullData.SetMarkerColor(kBlack)
	pullError.SetMarkerColor(kBlack)
	pullError.SetMarkerStyle(20)
	pullError.SetFillColorAlpha(kGray+2, 0.5)
	# pullError.SetFillColorAlpha(kGray+2, 0.5)
	pullError.SetFillStyle(1001)
#	pullError.SetLineWidth(0)
	pullError.SetLineColor(kBlack)
	pullData.SetMarkerStyle(20)
	pullData.SetLineColor(kBlack)

	# pullData.SetMarkerColorAlpha(0,0)
	pullAll = [pullData, pullError, LowEdge - bWidth*0.18, UpEdge+bWidth*0.18, chi2_hist, chi2_ratio]
	#print LowEdge, UpEdge
	return pullAll

# def SaveNoPull(data, bkg, fileName):
# 	c0 = TCanvas("c0", "c0", 1000, 800)
# 	c0.cd()
# 	data.Draw()
# 	bkg.Draw('histsame')
# 	c0.SaveAs("sample.png")



def SaveWithPull(data, bkg, legend, pullH, pullE, fileName, varName, dirName, lumi, signals, SUM, hideData, year, chi2_hist, chi2_ratio):
	gStyle.SetHatchesLineWidth(5)
	data.SetStats(0)
	Font = 43
	labelSize = 20
	titleSize = 27
        #bkg.Sumw2()
	bkg.Draw('hist')
	bkg.SetTitle("")
	bkg.SetMinimum(0.01)
	print "number of background histograms ",bkg.GetNhists()
#	bkg.GetYaxis().SetTitle("Events")
#	if "GeV" in varName:
	nbins = bkg.GetXaxis().GetNbins()
	binslow = bkg.GetXaxis().GetBinLowEdge(1)
	binsup = bkg.GetXaxis().GetBinUpEdge(nbins)
	perbin = round((float(binsup) - float(binslow))/float(nbins),3)
	#thisLabel = "Events/("+str(perbin)+")"
        thisLabel = "Events"
	bkg.GetYaxis().SetTitle(thisLabel)

	#if "GeV" in varName:
	#	thisLabel = "Events/("+str(perbin)+"GeV)"


	bkg.GetYaxis().SetTitleOffset(1.75)

	#### Configure thstack
	bkg.GetHistogram().GetXaxis().SetNdivisions(515)

	#cs = TCanvas("cs", "cs", 800, 600)
        cs = TCanvas("cs", "cs", 700, 700)
        #bkg.Sumw2()
	bkg.Draw('hist')
	bkg.GetHistogram().GetXaxis().SetTitle(varName)
	bkg.GetHistogram().GetYaxis().SetTitleOffset(1.25)
	GenMax = max(data.GetMaximum(), bkg.GetMaximum())*1.65
	# GenMax = max(data.GetMaximum(), bkg.GetMaximum())
	#bkg.SetMaximum(GenMax)
	bkg.SetTitle("")
	bkg.SetMinimum(0.001)
	SUM.Draw("E2 same")
	if(hideData == False):
		data.Draw('E same')
	tlatex = TLatex()
	baseSize = 25
	tlatex.SetNDC()
	tlatex.SetTextAngle(0)
	tlatex.SetTextColor(kBlack)
	tlatex.SetTextFont(63)
	tlatex.SetTextAlign(11)
	tlatex.SetTextSize(25)
        #print "I am here" , chi2_hist
        #tlatex.DrawLatex(0.11, 0.91, str(chi2_hist))
	# tlatex.DrawLatex(0.11, 0.91, "CMS")
	# tlatex.SetTextFont(53)
	# # tlatex.DrawLatex(0.18, 0.91, "Work in progress")
	# tlatex.DrawLatex(0.18, 0.91, "Preliminary")
	# tlatex.SetTextFont(43)
	# tlatex.SetTextSize(23)
        tlatex.DrawLatex(0.12,0.91,"#bf{CMS}")
	#tlatex.DrawLatex(0.12,0.91,"#bf{CMS} #it{Preliminary}")
    #lat0.DrawLatex(0.12,0.92,"#bf{CMS}")
        tlatex.DrawLatex(0.6,0.91,"132 fb^{-1} (13 TeV)")
#	tlatex.DrawLatex(0.65, 0.91,"L = 2.70 fb^{-1} (13 TeV)")
	# Lumi = "" + str(lumi) + " pb^{-1} (13 TeV)"#, "+ year + ")"
	# if lumi > 1000:
		# llumi = float(lumi)/1000.
	Lumi = "" + str(lumi) + " fb^{-1} (13 TeV)"#, "+year+")"
	# tlatex.DrawLatex(0.14, 0.82, Lumi)
	tlatex.SetTextAlign(31)
	# tlatex.DrawLatex(0.9, 0.91, Lumi)
	# tlatex.SetTextAlign(11)


	for leg in legend:
		leg.Draw('same')

	for h in signals:
		h[0].Draw("same hist")
	cs.SaveAs(dirName+"/NP_" + fileName + ".pdf")
	cs.SaveAs(dirName+"/NP_" + fileName + ".png")
        cs.SaveAs(dirName+"/NP_" + fileName + ".C")
        cs.SaveAs(dirName+"/NP_" + fileName + ".root")

	if hideData:
		cs.SetLogy()
		bkg.SetMinimum(0.01)
		bkg.SetMaximum(bkg.GetMaximum()*1000)
		print "maximum background" , bkg.GetMaximum()
	        cs.SaveAs(dirName+"/LOG_" + fileName + ".pdf")
	        cs.SaveAs(dirName+"/LOG_" + fileName + ".png")
		return


	ratio = 0.2
	epsilon = 0.0
	# Significance = TGraph()

	# for h in signals:
		# h[0].Draw("same hist")
		# print "[SIGNAL INTEGRAL]: ", h[0].Integral()
	# for s in signals:
		# print s[0]
	#Significance = getSig(SUM, signals[0][0])
	#Significance.GetXaxis().SetLabelFont(Font)
	#Significance.GetXaxis().SetLabelSize(labelSize)
	#Significance.GetXaxis().SetLabelOffset(0.01)

	#Significance.GetXaxis().SetTitle(varName)
	#Significance.GetXaxis().SetTitleFont(Font)
	#Significance.GetXaxis().SetTitleSize(titleSize)
	#Significance.GetXaxis().SetTitleOffset(5)
	#Significance.GetXaxis().SetLabelOffset(0.05)
	#Significance.GetXaxis().SetNdivisions(515)
	#Significance.GetXaxis().SetTickLength(0.15)

		# pullE.GetYaxis().SetTitle("Data/MC")
	#Significance.GetYaxis().SetTitle("S/sqrt(B)")
	#Significance.SetMarkerStyle(20)
	#Significance.SetMarkerColor(kBlack)
	#Significance.GetYaxis().SetTitleFont(Font)
	#Significance.GetYaxis().SetTitleSize(18)
	#Significance.GetYaxis().SetTitleOffset(1.5)
	#Significance.GetYaxis().CenterTitle()
	#Significance.GetYaxis().SetLabelFont(Font)
	#Significance.GetYaxis().SetLabelSize(15)

	#Significance.GetYaxis().SetNdivisions(504)
	#Significance.GetXaxis().SetRangeUser(bkg.GetHistogram().GetXaxis().GetXmin(), bkg.GetHistogram().GetXaxis().GetXmax())
	x = Double(0.)
        y = Double(0.)
        #for i in range(1, Significance.GetN()):
            #Significance.GetPoint(i, x, y)
            #print "================="
	    #print x, y
	c1 = TCanvas("c2", "c2", 700, 700)
	SetOwnership(c1,False) #If I don't put this, I get memory leak problems...
	#p1 = TPad("pad1","pad1", 0, float(ratio - epsilon), 1, 1)
        p1 = TPad("pad1","pad1",0,0.25,1,1)
        p1.SetTickx()
        p1.SetTicky()
        p1.SetBottomMargin(0)
        p1.SetLeftMargin(0.12)
	SetOwnership(p1,False)
	# p1.SetBottomMargin(epsilon)
	#p2 = TPad("pad2","pad2",0,0,1,float(ratio*(1-epsilon)) )
	#print "float(ratio*(1-epsilon))" , float(ratio*(1-epsilon))
        p2 = TPad("pad2","pad2",0,0,1,0.35)
	SetOwnership(p2,False)
	p2.SetFillColor(0)
	p2.SetFillStyle(0)
        p2.SetTickx()
        p2.SetTicky()
	p2.SetTopMargin(0.35)
	p2.SetBottomMargin(0.35)
        p2.SetLeftMargin(0.12)
	p2.SetGridy()
	#p3 = TPad("pad3","pad3",0,0.05,1,0.1 )
	#SetOwnership(p3,False)
	#p3.SetFillColor(0)
	#p3.SetFillStyle(0)
	#p3.SetTopMargin(0.0)
	#p3.SetBottomMargin(0.35)
	#p3.SetGridy()

	p1.cd()
	bkg.Draw('hist')
	bkg.SetTitle("")
	bkg.SetMinimum(0.001)
	# print "number of background", bkg.GetNhists()

	#### Configure thstack
	bkg.GetHistogram().GetXaxis().SetNdivisions(515)
	if(hideData == False):
		bkg.GetHistogram().GetXaxis().SetTitleFont(Font)
		bkg.GetHistogram().GetXaxis().SetTitleSize(0)
		bkg.GetHistogram().GetXaxis().SetLabelFont(Font)
		bkg.GetHistogram().GetXaxis().SetLabelSize(0)
	if(hideData):
		bkg.GetHistogram().GetXaxis().SetTitleFont(Font)
		bkg.GetHistogram().GetXaxis().SetTitleSize(titleSize)
		bkg.GetHistogram().GetXaxis().SetLabelFont(Font)
		bkg.GetHistogram().GetXaxis().SetLabelSize(labelSize)
		bkg.GetHistogram().GetXaxis().SetTitle(varName)


	bkg.GetYaxis().SetTitleFont(Font)
	bkg.GetYaxis().SetTitleSize(titleSize)
	bkg.GetYaxis().SetLabelFont(Font)
	bkg.GetYaxis().SetLabelSize(labelSize)

	pullE.GetXaxis().SetLabelFont(Font)
	pullE.GetXaxis().SetLabelSize(labelSize)
	pullE.GetXaxis().SetLabelOffset(0.01)

	pullE.GetXaxis().SetTitle(varName)
	pullE.GetXaxis().SetTitleFont(Font)
	pullE.GetXaxis().SetTitleSize(titleSize)
	pullE.GetXaxis().SetTitleOffset(4)
	pullE.GetXaxis().SetLabelOffset(0.05)
	pullE.GetXaxis().SetNdivisions(515)
	pullE.GetXaxis().SetTickLength(0.03*0.75/0.35)
	# pullE.GetXaxis().SetTickLength(0.15)

	# pullE.GetYaxis().SetTitle("Data/MC")
	pullE.GetYaxis().SetTitle("Bkg./Data")
	pullE.SetMarkerStyle(20)
	pullE.SetMarkerColor(kBlack)
	pullE.GetYaxis().SetTitleFont(Font)
	# pullE.GetYaxis().SetTitleSize(0.095)
	# pullE.GetYaxis().SetTitleOffset(0.5)
	pullE.GetYaxis().SetTitleSize(20)
	pullE.GetYaxis().SetTitleOffset(1.5)
	pullE.GetYaxis().CenterTitle()
	pullE.GetYaxis().SetLabelFont(Font)
	pullE.GetYaxis().SetLabelSize(15)

	pullE.GetYaxis().SetNdivisions(504)
	pullE.GetXaxis().SetRangeUser(bkg.GetHistogram().GetXaxis().GetXmin(), bkg.GetHistogram().GetXaxis().GetXmax())

	# for h in signals:
	# 	# h[0].Draw("same hist")
	# 	# print "[SIGNAL INTEGRAL]: ", h[0].Integral()
	# 	Significance = getSig(SUM, h[0])
		# print Significance
		# Significance.GetXaxis().SetLabelFont(Font)
		# Significance.GetXaxis().SetLabelSize(labelSize)
		# Significance.GetXaxis().SetLabelOffset(0.01)
		#
		# Significance.GetXaxis().SetTitle(varName)
		# Significance.GetXaxis().SetTitleFont(Font)
		# Significance.GetXaxis().SetTitleSize(titleSize)
		# Significance.GetXaxis().SetTitleOffset(5)
		# Significance.GetXaxis().SetLabelOffset(0.05)
		# Significance.GetXaxis().SetNdivisions(515)
		# Significance.GetXaxis().SetTickLength(0.15)
		#
		# # pullE.GetYaxis().SetTitle("Data/MC")
		# Significance.GetYaxis().SetTitle("MC/Data")
		# Significance.SetMarkerStyle(20)
		# Significance.SetMarkerColor(kBlack)
		# Significance.GetYaxis().SetTitleFont(Font)
		# Significance.GetYaxis().SetTitleSize(18)
		# Significance.GetYaxis().SetTitleOffset(1.5)
		# Significance.GetYaxis().CenterTitle()
		# Significance.GetYaxis().SetLabelFont(Font)
		# Significance.GetYaxis().SetLabelSize(15)
		#
		# Significance.GetYaxis().SetNdivisions(504)
		# Significance.GetXaxis().SetRangeUser(bkg.GetHistogram().GetXaxis().GetXmin(), bkg.GetHistogram().GetXaxis().GetXmax())
		#
		# print Significance

	### Fin

	p1.Update()
	gStyle.SetHatchesLineWidth(15)
	SUM.SetFillStyle(3001)
	SUM.Draw("E2 same")
	# SUM.Draw("a3 same")
	#print "Data integral  = ",data.Integral()
	#print "Background integral = ",SUM.Integral()
	scale = data.Integral()/SUM.Integral()
	# SUM.Scale(scale)
	# SUM.Draw("E1 same")

	if(hideData == False):
		data.Draw('E same')
	tlatex = TLatex()
	baseSize = 25
	tlatex.SetNDC()
	tlatex.SetTextAngle(0)
	tlatex.SetTextColor(kBlack)
	tlatex.SetTextFont(42)
	tlatex.SetTextAlign(11)
	tlatex.SetTextSize(0.045)
	#tlatex.DrawLatex(0.11, 0.91, "CMS")
	#tlatex.SetTextFont(53)
	#tlatex.DrawLatex(0.18, 0.91, "Work in Progress")
       	#tlatex.SetTextFont(43)
	#tlatex.SetTextSize(23)
        tlatex.DrawLatex(0.12,0.91,"#bf{CMS}")
        #tlatex.DrawLatex(0.12,0.91,"#bf{CMS} #it{Preliminary}")
        #tlatex.DrawLatex(0.13, 0.78, "#chi^{2}(Ratio) = " +str(round(chi2_ratio,3)))
        #tlatex.DrawLatex(0.13, 0.73, "#chi^{2}(Hist) = " +str(round(chi2_hist,3)))
#	tlatex.DrawLatex(0.65, 0.91,"L = 2.70 fb^{-1} (13 TeV)")
	# Lumi = "L = " + str(lumi) + " pb^{-1} (13 TeV)"#, "+ year + ")"
	# if lumi > 1000:
		# llumi = float(lumi)/1000.
	#Lumi = "L = " + str(lumi) + " fb^{-1} (13 TeV)" #+ "(" + str(year) +")"
	# tlatex.DrawLatex(0.14, 0.82, Lumi)

	#tlatex.SetTextAlign(31)
	#tlatex.DrawLatex(0.9, 0.91, Lumi)
	#tlatex.SetTextAlign(11)
        tlatex.DrawLatex(0.67,0.91,"132 fb^{-1} (13 TeV)")

	for leg in legend:
		leg.Draw('same')

	for h in signals:
		h[0].Draw("same hist")




	p2.cd()
#	pullE.GetYaxis().SetNdivisions(4, False)

	if(hideData==False):
		pullE.Draw("AF2")
		# print Significance
		# Significance.Draw("E2 same")
		# p2.Update()
		# pullE.Draw("E2")
	if(hideData):
		pullE.Draw("E2")


		# pullE.Draw("A")
	Line = TLine(bkg.GetHistogram().GetXaxis().GetXmin(), 1., bkg.GetHistogram().GetXaxis().GetXmax(), 1.)
	Line.SetLineColor(kRed)
	if(hideData==False):
		# Line.Draw()
		pullH.Draw("PE0same")
		# print Significance
		#Significance.Draw("E2 same")
		# p2.Update()
	c1.cd()
	p2.Draw()
        c1.cd()
	#p3.cd()
	#Significance.Draw("E2")
	#p3.Draw()
        #c1.SaveAs(dirName+"/test.pdf")
        c1.cd()
	p1.Draw()
        c1.cd()
	c1.Update()
	c1.SaveAs(dirName+"/" + fileName + ".pdf")
	c1.SaveAs(dirName+"/" + fileName + ".png")
        c1.SaveAs(dirName+"/" + fileName + ".C")
        c1.SaveAs(dirName+"/" + fileName + ".root")

	p1.cd()
	p1.SetLogy()
	GeneralMaximus = max(bkg.GetMaximum(), data.GetMaximum())
	if(hideData):
		GeneralMaximus = bkg.GetMaximum()*10
	GeneralMaximus = max(GeneralMaximus, 1E-5)
	#print GeneralMaximus, log10(abs(GeneralMaximus))
	GenMax = pow(10, log10(abs(GeneralMaximus))*2.5)
	bkg.SetMaximum(GenMax)
	GenMin = bkg.GetMinimum()
	if GenMin == 0:
		GenMin = 1
	bkg.SetMinimum(0.01)
	if(hideData):
		bkg.SetMinimum(0.001)
	p1.Update()
	c1.cd()
	c1.Update()
	c1.SaveAs(dirName+"/LOG_" + fileName + ".pdf")
	c1.SaveAs(dirName+"/LOG_" + fileName + ".png")
        c1.SaveAs(dirName+"/LOG_" + fileName + ".C")
        c1.SaveAs(dirName+"/LOG_" + fileName + ".root")
#	c1.Delete()

	#print "Expected number of events (MC):", SUM.Integral()
	#print "Observed number of events (DATA):", data.Integral()

def SavePull(pullH, pullE, LowEdge, UpEdge, dirName):
	ca = TCanvas("ca", "ca", 700, 700)
	ca.cd()
	pullE.Draw("A2")
	pullE.GetXaxis().SetLimits(LowEdge,UpEdge)
	pullE.GetXaxis().SetTitle
	ca.Update()
	pullH.Draw("Psame")
	# 	pullH.Draw("A*")
	# 	pullH.GetXaxis().SetRangeUser(LowEdge,UpEdge)
	# 	pullE.Draw("same2")
	# ca.SaveAs(dirName + "/pull.pdf")
	# ca.SaveAs(dirName + "/pull.png")
	# ca.Delete()

def MakeLegend(HistList, DataHist, lumi, Signals, SUM):
	newList = []
	newLegs = []
	for h in HistList:
		if h[1] in newLegs:
			continue
		else:
			newList.append(h)
			newLegs.append(h[1])

	nMaxPerBox = (len(newList)+len(Signals)+2)/3
#	nMaxPerBox = (len(newList)+1)/3
	# print "**************************************", len(newList), "   ", nMaxPerBox

#	if (3*nMaxPerBox < len(newList)+len(Signals)+2):
	if (3*nMaxPerBox < len(newList)+1):
		nMaxPerBox += 1
	lenPerHist = 0.04

	legends = []
	#leg1 = TLegend(0.65, 0.65, 0.71, 0.65+lenPerHist*float(nMaxPerBox))
	leg1 = TLegend(0.15, 0.85-lenPerHist*float(len(Signals)), 0.49, 0.87)
	leg2 = TLegend(0.44, 0.85-lenPerHist*3, 0.68, 0.87)
	# leg2.SetNColumns(2)
	# leg2.SetColumnSeparation(0.001)
	leg3 = TLegend(0.70, 0.85-lenPerHist, 0.85, 0.87)
        #leg1 = TLegend(0.6, 0.7, 0.89, 0.89)
	#leg2 = TLegend(0.6, 0.7, 0.89, 0.89)
	#leg3 = TLegend(0.6, 0.7, 0.89, 0.89)
        #leg1.SetNColumns(2)
	legends.append(leg1)
	legends.append(leg2)
	legends.append(leg3)

	data_lumi = " Data (" + str(lumi) + " pb^{-1})"
	if lumi > 1000:
		llumi = float(lumi)/1000.
		data_lumi = " Data (" + str(llumi) + " fb^{-1})"
#	leg1.AddEntry(DataHist, data_lumi, "lep")
	# leg1.AddEntry(SUM, " Stat. Uncertainty", "lf")

	allLegs = []
#	allLegs.append([DataHist, "Data (" + str(llumi) + " fb^{-1})"])
	allLegs.append([DataHist, "Data"])
#	allLegs.append([SUM,  "Stat. Uncert."])
	allLegs += newList

	nMaxPerBox = (len(newList)+len(Signals)+1)/3
	if (3*nMaxPerBox < len(newList)+len(Signals)+1):
		nMaxPerBox += 1

	for j,l in enumerate(Signals):
		Type = 'l'
		if 'Grav.' in l[1] or 'Rad.' in l[1]:
			legends[len(legends)-3].AddEntry(l[0], ' '+l[1], Type)
		else:
			legends[len(legends)-3].AddEntry(l[0], ' '+l[1], Type)


	for i,l in enumerate(allLegs):
		Type = 'f'
		if 'Data' in l[1]:
			Type = 'lep'
			legends[len(legends)-1].AddEntry(l[0], ' '+l[1], "PE")
		else:
			legends[len(legends)-2].AddEntry(l[0], ' '+l[1], "lf")
                        legends[len(legends)-2].AddEntry(SUM, 'Stat. Uncertainty', "lf")
	#leg1.AddEntry(SUM, " Stat. Uncertainty", "lf")


        textFont = 43
        textSize = 20
	for leg in legends:
		leg.SetFillStyle(0)
		leg.SetLineWidth(0)
		leg.SetBorderSize(0)
		leg.SetTextFont(textFont)
		leg.SetTextSize(textSize)

	return legends
