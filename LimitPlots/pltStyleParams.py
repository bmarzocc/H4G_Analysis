import matplotlib.pyplot as plt

norm_factor = 50*1000 ## Theoretical higgs production XS value in pb

plt.figure()
ax = plt.gca()

cms = plt.text(
        0.0, 1.0, u"CMS $\it{Preliminary}$" ,
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


plt.ylabel(r'95% CL on $\sigma (pp\rightarrow h)\times BR (h \rightarrow aa) / \sigma_{SM}$',y=1, ha='right',fontsize=14)
