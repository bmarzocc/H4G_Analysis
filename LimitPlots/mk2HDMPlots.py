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
parser.add_argument('-iD','--inDir',dest='inDir',required=True,type=str)
parser.add_argument('-oD','--oDir',dest='oDir',required=True,type=str)
parser.add_argument('-b','--beta',dest='beta',required=False,type=float)


opt = parser.parse_args()
type = opt.type ## Type of 2HDM+S model
inDir = opt.inDir
oDir = opt.oDir

if (type != "I"): beta = opt.beta ## Tan Beta value
else: beta = ""

## Read dat file
dat_file = "BR/BR_"+str(type)+"_"+str(beta)+".dat"
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

mass = []
limit_arr = []
limit_over_brsquared_arr = []

## Obtain values of expected and observed limits for each mass point
quantile = ["_0.16","_0.5","_0.84","_Observed"]

for qi, q in enumerate(quantile):
    limit_quantile = []
    limit_over_brsquared_quantile = []
    for m in range (15,61): ## m(a) ranges from 15 to 60 GeV
        if (qi ==0 ): mass.append(m)
        file_in_exp = ROOT.TFile(inDir+"/higgsCombine_M"+str(m)+str(q)+".HybridNew.mH125.root","read")
        tree_in_exp = file_in_exp.Get("limit")
        limit_val = tree2array(tree_in_exp,branches="limit")
        limit_quantile.append(limit_val[0])
        br_val = gr.Eval(m)
        # print br_val
        limit_over_brsquared_quantile.append((limit_val[0])/(br_val*br_val*norm_factor))

    limit_arr.append(limit_quantile)
    limit_over_brsquared_arr.append(limit_over_brsquared_quantile)

# print ((limit_arr[3]))


plt.ylim(0.01,1.5*max(limit_over_brsquared_arr[3]))
plt.xlim(14.9,60.1)
plt.xticks([15,20,25,30,35,40,45,50,55,60])

plt.plot(mass, limit_over_brsquared_arr[0],lineStyle='')#,color='#67001f')
plt.plot(mass, limit_over_brsquared_arr[1],lineStyle='--',color='#67001f')
plt.plot(mass, limit_over_brsquared_arr[2],lineStyle='')#,color='#67001f')

plt.plot(mass, limit_over_brsquared_arr[3],lineStyle='',color='#67001f',alpha=0.3)
plt.fill_between(mass,limit_over_brsquared_arr[0],limit_over_brsquared_arr[2],lineStyle='--',facecolor="none",hatch='////',edgecolor='#67001f',lw=0,label=r'Expected exclusion 95% CL $\pm 1\sigma$')
plt.fill_between(mass,limit_over_brsquared_arr[3],1.5*np.max(limit_over_brsquared_arr[3]),color='#67001f',alpha=0.3,lw=0,label='Observed exclusion 95% CL')

plt.axhline(1, ls="--", color="red")

if (type!="I"):model_type_text = r"2 HDM+S Type-"+str(type)+",tan $\\beta = $"+str(beta)
else: model_type_text = r"2 HDM+S Type-"+str(type)
plt.text(
        0.02, 0.5, model_type_text,
        fontsize=14, horizontalalignment='left',
        verticalalignment='bottom',
        transform=ax.transAxes
    )

plt.xlabel('m(a) [GeV]',x=1, ha='right',fontsize=14)

plt.yscale("log")
plt.legend(loc='lower left',framealpha=0,fontsize=12)
plt.savefig(oDir+'2HDMPlusS_Type'+str(type)+'_TanBeta'+str(beta)+'.pdf')
plt.savefig(oDir+'2HDMPlusS_Type'+str(type)+'_TanBeta'+str(beta)+'.png')
