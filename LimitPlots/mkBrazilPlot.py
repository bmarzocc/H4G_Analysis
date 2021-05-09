import ROOT
from root_numpy import tree2array
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

plt.style.use('physics.mplstyle')

import argparse
parser =  argparse.ArgumentParser(description='H4G Brazil Plot Maker')
parser.add_argument('-s','--style',dest='style',required=True,type=str)
parser.add_argument('-b','--blind',dest='blind',required=True,type=int)
parser.add_argument('-norm','--norm',dest='norm',required=True,type=int)
parser.add_argument('-ymin','--ymin',dest='ymin',required=False,default=0,type=float)
parser.add_argument('-ymax','--ymax',dest='ymax',required=False,default=4,type=float)
parser.add_argument('-iD','--inDir',dest='inDir',required=True,type=str)
parser.add_argument('-oD','--oDir',dest='oDir',required=True,type=str)
parser.add_argument('-n','--name',dest='name',required=True,type=str)

opt = parser.parse_args()
style = opt.style
blind = opt.blind
norm = opt.norm
ymin = opt.ymin
ymax = opt.ymax
inDir = opt.inDir
oDir = opt.oDir
name = opt.name

label_left = "Preliminary" ## set the label to be displayed after "CMS"
label_right = "132 $fb^{-1}$  (13 TeV)"

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
    # print ("mass: ", m)
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


## Make Brazil Plot
plt.figure()
plt.ylim(ymin,ymax)
if (norm==1):
    plt.ticklabel_format(axis='y',style='sci',scilimits=(0,4))
    plt.title(r'$\bf{CMS}$'+' $\it{'+str(label_left)+'}$',position=(0.15, 0.93)) ## Put CMS Preliminary inside the canvas; position=(0,0) is the bottom left and position=(1,1) is the top right
    # plt.ylabel(r'$\dfrac {\sigma (pp\rightarrow h)} {\sigma (SM)}\times BR (h \rightarrow aa \rightarrow \gamma\gamma\gamma\gamma) $',labelpad=0.1) ## labelpad determines the distance between label axis and label values; a higher value will increase the distance
    plt.ylabel(r'$\sigma (pp\rightarrow h)\times BR (h \rightarrow aa \rightarrow \gamma\gamma\gamma\gamma) / \sigma_{SM}$',labelpad=0.1) ## labelpad determines the distance between label axis and label values; a higher value will increase the distance
else:
    plt.title(r'$\bf{CMS}$'+' $\it{'+str(label_left)+'}$',loc='left')    ## Put CMS Preliminary outside the canvas
    plt.ylabel(r'$\sigma (pp\rightarrow h)\times BR (h \rightarrow aa \rightarrow \gamma\gamma\gamma\gamma) \quad[fb] $',labelpad=2)

# plt.ylabel(labelpad=10)
# plt.ticklabel_format(axis='y',style='sci',scilimits=(0,4))
# plt.ylim(style="sci")
plt.xlim(14.9,60.1)
plt.xticks([15,20,25,30,35,40,45,50,55,60])

# plt.grid(True)

plt.plot(mass, exp_median,lineStyle='--', marker='',color='black',label='Median expected')
if (blind==0): plt.plot(mass, obs,lineStyle='-', marker='',color='black',label='Observed')

plt.fill_between(mass,exp_down01sigma , exp_median,facecolor='#00CC00',lw=0,label="68% expected")
plt.fill_between(mass,exp_down02sigma , exp_down01sigma,facecolor='#FFCC01',lw=0, label="95% expected")

plt.fill_between(mass,exp_median , exp_up01sigma,facecolor='#00CC00',lw=0)
plt.fill_between(mass,exp_up01sigma , exp_up02sigma,facecolor='#FFCC01',lw=0)


plt.xlabel('m(a) [GeV]')
plt.legend(loc='upper right',framealpha=0)
# plt.tight_layout()


# plt.title('Run 2 (13 TeV)',loc='right')
plt.title(str(label_right),loc='right')

plt.savefig(oDir+name+'.pdf')
plt.savefig(oDir+name+'.png')

plt.yscale("log")

if (norm==0): plt.ylim(0,10)
else:
    plt.ylim(1e-6,1e-3)

plt.savefig(oDir+name+'_log.pdf')
plt.savefig(oDir+name+'_log.png')
