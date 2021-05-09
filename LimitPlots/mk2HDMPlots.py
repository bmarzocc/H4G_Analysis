import ROOT
from root_numpy import tree2array
from array import array
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
plt.style.use('physics.mplstyle')

import argparse
parser =  argparse.ArgumentParser(description='H4G Brazil Plot Maker')
parser.add_argument('-t','--type',dest='type',required=True,type=str)
parser.add_argument('-b','--beta',dest='beta',required=False,type=float)
parser.add_argument('-iD','--inDir',dest='inDir',required=True,type=str)
parser.add_argument('-oD','--oDir',dest='oDir',required=True,type=str)

opt = parser.parse_args()
type = opt.type ## Type of 2HDM+S model
if (type != "I"): beta = opt.beta ## Tan Beta value
else: beta = ""
inDir = opt.inDir
oDir = opt.oDir

norm_factor = 50*1000

## Create BR versus m(a) graph from dat file
dat_file = "/afs/cern.ch/work/t/twamorka/H4G_Analysis/LimitPlots/BR/BR_"+str(type)+"_"+str(beta)+".dat"
file_in = open(dat_file)

lst = []
m_a, br = array( 'd' ), array( 'd' )
for line in file_in:
    lst += [line.split()]
    # print line.split()
    m_a.append(float(line.split()[1]))
    br.append(float(line.split()[-3]))


num_points = len(lst)

gr = ROOT.TGraph(num_points,m_a,br)

mass = []
exp_median = []
obs = []

exp_median_over_brsquared = []
obs_over_brsquared = []

## Obtain values of expected and observed limits for each mass point
for m in range (15,61): ## m(a) ranges from 15 to 60 GeV
    mass.append(m)
    file_in_exp = ROOT.TFile(inDir+"/higgsCombine_M"+str(m)+"_0.5.HybridNew.mH125.root","read")
    tree_in_exp = file_in_exp.Get("limit")
    limit_exp = tree2array(tree_in_exp,branches="limit")
    exp_median.append(limit_exp[0])

    file_in_obs = ROOT.TFile(inDir+"/higgsCombine_M"+str(m)+"_Observed.HybridNew.mH125.root","read")
    tree_in_obs = file_in_obs.Get("limit")
    limit_obs = tree2array(tree_in_obs,branches="limit")
    obs.append(limit_obs[0])

    br = gr.Eval(m)
    exp_median_over_brsquared.append((limit_exp[0])/(br*br*norm_factor))
    obs_over_brsquared.append((limit_obs[0])/(br*br*norm_factor))


# print obs_over_brsquared
plt.figure()
ax = plt.gca()

cms = plt.text(
        0.05, 1, u"CMS $\it{Preliminary}$" ,
        fontsize=18, fontweight='bold',
        horizontalalignment='left',
        verticalalignment='bottom',
        transform=ax.transAxes
    )
lumi = plt.text(
        1., 1., r"%1.0f fb$^{-1}$ (13 TeV)" % 132.0,
        fontsize=14, horizontalalignment='right',
        verticalalignment='bottom',
        transform=ax.transAxes
    )


plt.ylabel(r'95% CL on $\sigma (pp\rightarrow h)\times BR (h \rightarrow aa) / \sigma_{SM}$',y=1, ha='right') ## labelpad determines the distance between label axis and label values; a higher value will increase the distance

plt.xlim(14.9,60.1)
# plt.ylim(bottom=0.01)
plt.ylim(0.01,1.5*max(obs_over_brsquared))
plt.xticks([15,20,25,30,35,40,45,50,55,60])
# print np.max(obs_over_brsquared)
plt.plot(mass, exp_median_over_brsquared,lineStyle='--',color='#67001f',label='Expected exclusion 95% CL')
plt.plot(mass, obs_over_brsquared,lineStyle='',color='#67001f',alpha=0.3)
plt.fill_between(mass,obs_over_brsquared,1.5*np.max(obs_over_brsquared),color='#67001f',alpha=0.3,lw=0,label='Observed exclusion 95% CL')
plt.axhline(1, ls="--", color="red")

if (type!="I"):model_type_text = r"2 HDM+S Type-"+str(type)+",tan $\\beta = $"+str(beta)
else: model_type_text = r"2 HDM+S Type-"+str(type)
plt.text(
        0.02, 0.5, model_type_text,
        fontsize=14, horizontalalignment='left',
        verticalalignment='bottom',
        transform=ax.transAxes
    )

plt.xlabel('m(a) [GeV]',x=1, ha='right')

plt.yscale("log")
plt.legend(loc='lower left',framealpha=0,fontsize=10)
plt.savefig(oDir+'2HDMPlusS_Type'+str(type)+'_TanBeta'+str(beta)+'.pdf')
plt.savefig(oDir+'2HDMPlusS_Type'+str(type)+'_TanBeta'+str(beta)+'.png')
