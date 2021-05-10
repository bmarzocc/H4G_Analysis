import ROOT
from root_numpy import tree2array
from array import array
import numpy as np
import matplotlib.pyplot as plt
from pltStyleParams import *
plt.rcParams.update({'figure.max_open_warning': 0})
plt.style.use('physics.mplstyle')

import argparse
parser =  argparse.ArgumentParser(description='H4G Brazil Plot Maker')
parser.add_argument('-t','--type',dest='type',required=True,type=str)
parser.add_argument('-m','--mass',dest='mass',required=True,type=str)
parser.add_argument('-iD','--inDir',dest='inDir',required=True,type=str)
parser.add_argument('-oD','--oDir',dest='oDir',required=True,type=str)

opt = parser.parse_args()
type = opt.type ## Type of 2HDM+S model
mass = opt.mass ## mass of pseudoscalar
inDir = opt.inDir
oDir = opt.oDir


tanbeta = [0.5,0.6,0.7,0.8,0.9,1.0,1.5,2.0,2.5,3.0,3.5,4.0,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0]
br_val = []

## Read limit values

quantile = ["_0.16","_0.5","_0.84","_Observed"]
limit_arr = []
limit_over_brsquared_arr = []
for qi, q in enumerate(quantile):
    file_in_exp = ROOT.TFile(inDir+"/higgsCombine_M"+str(mass)+str(q)+".HybridNew.mH125.root","read")
    tree_in_exp = file_in_exp.Get("limit")
    limit_val = tree2array(tree_in_exp,branches="limit")
    limit_arr.append(limit_val[0])

## Read dat files to obtain BR values
for t in tanbeta:
    dat_file = "/afs/cern.ch/work/t/twamorka/H4G_Analysis/LimitPlots/BR/BR_"+str(type)+"_"+str(t)+".dat" ## Read dat file
    file_in = open(dat_file)

    lst = []
    m_a, br_arr = array( 'd' ), array( 'd' )

    for line in file_in:
        lst += [line.split()]
        # print line.split()
        m_a.append(float(line.split()[1]))
        br_arr.append(float(line.split()[-3]))


    num_points = len(lst)
    gr = ROOT.TGraph(num_points,m_a,br_arr)
    br_val.append(gr.Eval(float(mass)))

## Evaluate XS (pp->h) X BR (h->aa->4gamma)/ XS(SM)

for l in limit_arr:
    limit_over_brsquared_arr.append(np.ones(len(br_val))*l/(norm_factor))

## Evaluate XS (pp->h) X BR (h->aa)/ XS(SM) by dividing XS (pp->h) X BR (h->aa->4gamma)/ XS(SM) by BR(a->gamma gamma) X BR (a->gamma gamma)

exp_down01sigma =  np.divide(limit_over_brsquared_arr[0],np.multiply(br_val,br_val)) ## Down 01 sigma expected
exp_median = np.divide(limit_over_brsquared_arr[1],np.multiply(br_val,br_val)) ##Median expected
exp_up01sigma =  np.divide(limit_over_brsquared_arr[2],np.multiply(br_val,br_val)) ## Up 01 sigma expected
obs =  np.divide(limit_over_brsquared_arr[3],np.multiply(br_val,br_val)) ## Observed


## Make limit plots

plt.ylim(0.01,1.5*max(obs))
plt.yscale("log")
plt.xlim(0.49,10.01)
plt.xticks([0.5,1,2,3,4,5,6,7,8,9,10])
plt.xlabel(r'tan $\beta$',x=1, ha='right',fontsize=14)

plt.plot(tanbeta, exp_down01sigma,lineStyle='')#,color='#67001f') ## Down 01 sigma expected
plt.plot(tanbeta, exp_median,lineStyle='--',color='#67001f') ## Median expected
plt.plot(tanbeta, exp_up01sigma,lineStyle='')#,color='#67001f') ## Up 01 sigma expected

plt.plot(tanbeta, obs, lineStyle='',color='#67001f',alpha=0.3) ## Observed
plt.fill_between(tanbeta,exp_down01sigma,exp_up01sigma,lineStyle='--',facecolor="none",hatch='////',edgecolor='#67001f',lw=0,label=r'Expected exclusion 95% CL $\pm 1\sigma$')
plt.fill_between(tanbeta,obs,1.5*np.max(obs),color='#67001f',alpha=0.3,lw=0,label='Observed exclusion 95% CL')

plt.axhline(1, ls="--", color="red")
plt.legend(loc='lower left',framealpha=0,fontsize=12)

model_type_text = r"2 HDM+S Type-"+str(type)
plt.text(
        0.5, 0.5, model_type_text,
        fontsize=14, horizontalalignment='left',
        verticalalignment='bottom',
        transform=ax.transAxes
    )

mass_a_text = r"m$_{a}$ = "+str(mass)+".0 GeV"
plt.text(
        0.5, 0.42, mass_a_text,
        fontsize=14, horizontalalignment='left',
        verticalalignment='bottom',
        transform=ax.transAxes
    )

plt.savefig(oDir+'2HDMPlusS_Type'+str(type)+'_ma_'+str(mass)+'_TanBetaScan'+'.pdf')
plt.savefig(oDir+'2HDMPlusS_Type'+str(type)+'_ma_'+str(mass)+'_TanBetaScan'+'.png')
