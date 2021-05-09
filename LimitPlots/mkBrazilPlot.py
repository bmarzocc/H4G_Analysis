import ROOT
from root_numpy import tree2array
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

import argparse
parser =  argparse.ArgumentParser(description='H4G Brazil Plot Maker')
parser.add_argument('-s','--style',dest='style',required=True,type=str)
parser.add_argument('-b','--blind',dest='blind',required=True,type=int)
parser.add_argument('-norm','--norm',dest='norm',required=True,type=int)
parser.add_argument('-iD','--inDir',dest='inDir',required=True,type=str)
parser.add_argument('-oD','--oDir',dest='oDir',required=True,type=str)
parser.add_argument('-n','--name',dest='name',required=True,type=str)

opt = parser.parse_args()
style = opt.style
blind = opt.blind
norm = opt.norm
inDir = opt.inDir
oDir = opt.oDir
name = opt.name

if (norm==0): ## if limits are to be presented in form of XS (pp->h) * BR (h->aa->gggg)
    norm_factor = 1
else: norm_factor = 50*1000  ## if limits are to be presented in form of XS (pp->h) * BR (h->aa->gggg) / XS (SM), then need to divide the limit values by SM XS value of Higgs i.e 50 pb or 50,000 fb

quantile = [0.025, 0.16, 0.5, 0.84, 0.975]
mass = []
exp_median = []
exp_up01sigma = []
exp_up02sigma = []
exp_down01sigma = []
exp_down02sigma = []
obs = []

## Obtain values of expected and observed limits for each mass point
for m in range (15,61): ## m(a) ranges from 15 to 60 GeV
    mass.append(m)
    if (style=="Asymptotic"):
        file_in = ROOT.TFile(inDir+"/higgsCombine_M"+str(m)+"_Asymptotic_FreezeMH.AsymptoticLimits.mH125.root","read")
        tree_in = file_in.Get("limit")
        limit = tree2array(tree_in,branches="limit")
        exp_down02sigma.append(limit[0]/norm_factor)
        exp_down01sigma.append(limit[1]/norm_factor)
        exp_median.append(limit[2]/norm_factor)
        exp_up01sigma.append(limit[3]/norm_factor)
        exp_up02sigma.append(limit[4]/norm_factor)
        if (blind==0): obs.append(limit[5]/norm_factor)

    elif (style=="HybridNew"):
        for q in quantile:
            file_in = ROOT.TFile(inDir+"/higgsCombine_M"+str(m)+"_"+str(q)+".HybridNew.mH125.root","read")
            tree_in = file_in.Get("limit")
            limit = tree2array(tree_in,branches="limit")
            # print limit
            if (q==0.025):
                exp_down02sigma.append(limit[0]/norm_factor)
            elif (q==0.16):
                exp_down01sigma.append(limit[0]/norm_factor)
            elif (q==0.5):
                exp_median.append(limit[0]/norm_factor)
            elif (q==0.84):
                exp_up01sigma.append(limit[0]/norm_factor)
            elif (q==0.975):
                exp_up02sigma.append(limit[0]/norm_factor)

        if (blind==0):
            file_in_obs = ROOT.TFile(inDir+"/higgsCombine_M"+str(m)+"_Observed.HybridNew.mH125.root","read")
            tree_in_obs = file_in_obs.Get("limit")
            limit_obs = tree2array(tree_in_obs,branches="limit")
            obs.append(limit_obs[0]/norm_factor)

# print mass
# print exp_median
# print obs

## Make Brazil Plot
# plt.ylim(0,4)
#plt.xlim(14.9,60.1)
plt.grid(True)

plt.plot(mass, exp_median,lineStyle='--', marker='',color='black',label='Median expected')
plt.plot(mass, exp_down01sigma,lineStyle='-', marker='',color='yellowgreen',label=r'$ \pm 1\sigma$ expected')
plt.plot(mass, exp_up01sigma,lineStyle='-', marker='',color='yellowgreen')
plt.plot(mass, exp_down02sigma,lineStyle='-', marker='',color='yellow',label=r'$ \pm 2\sigma$ expected')
plt.plot(mass, exp_up02sigma,lineStyle='-', marker='',color='yellow')

if (blind==0): plt.plot(mass, obs,lineStyle='-', marker='',color='black',label='Observed')

plt.fill_between(mass,exp_down02sigma , exp_up02sigma,facecolor='yellow')
plt.fill_between(mass,exp_down01sigma , exp_up01sigma,facecolor='yellowgreen')

if (norm==0): plt.ylabel(r'$\sigma (pp\rightarrow h)  \quad X \quad  BR (h \rightarrow aa \rightarrow \gamma\gamma\gamma\gamma) \quad [fb] $')
else:
    plt.ylabel(r'$\dfrac {\sigma (pp\rightarrow h)} {\sigma (SM)}  \quad X \quad  BR (h \rightarrow aa \rightarrow \gamma\gamma\gamma\gamma) $')
    plt.yscale("logit")
plt.xlabel('m(a) [GeV]')
plt.legend()
# plt.tight_layout()
plt.title(r'$\bf{CMS}$'+' $\it{Preliminary}$',loc='left')
plt.title('Run 2 (13 TeV)',loc='right')

plt.savefig(oDir+name+'.pdf')
plt.savefig(oDir+name+'.png')
