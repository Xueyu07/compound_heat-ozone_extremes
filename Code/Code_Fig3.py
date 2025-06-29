import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib as mpl
mpl.use('Agg')

# Read Data
file_path = "../SourceData/SourceData_Fig3.xlsx"  
df1 = pd.read_excel(file_path, sheet_name='Fig3a',header=1,index_col=0) 
df2 = pd.read_excel(file_path, sheet_name='Fig3b',header=0,index_col=None) 


Chemways = np.transpose(df1.iloc[:,:].values)
def get_cumulated_array(data, **kwargs):
    cum = data.clip(**kwargs)
    cum = np.cumsum(cum, axis=0)
    d = np.zeros(np.shape(data))
    d[1:] = cum[:-1]
    return d  
data_shape = np.shape(Chemways)
cumulated_data = get_cumulated_array(Chemways, min=0)
cumulated_data_neg = get_cumulated_array(Chemways, max=0)
row_mask = (Chemways<0)
cumulated_data[row_mask] = cumulated_data_neg[row_mask]
data_stack = cumulated_data

O3_nm = df2['O3_NM']
O3_hw = df2['O3_HW']
Chem_O3_nm = df2['ChemO3_NM']
Chem_O3_hw = df2['ChemO3_HW']

## Plot Fig
# Figure setup
fig = plt.figure(figsize=(6.6, 3.52), dpi=180, facecolor='w', constrained_layout=True)

plt.rcParams['axes.labelsize'] = 8
ax_left = fig.add_axes([0.03, 0., 0.26, 0.7])
ax_left.grid(axis='both', lw=0.4, color='#bbbbbb', ls='--')
labels=['PhotChem_Rate','Emis_BVOC','Met_NO$_x$Vmix','Met_O$_3$Vmix',]

category_colors=['tab:orange','tab:green','tab:red','tab:blue']
for i in range(Chemways.shape[0]):
    ax_left.barh(np.arange(0.1, 2.3, 0.1), Chemways[i,:], left=data_stack[i,:],
            height=0.07, alpha=0.7, color=category_colors[i],
            edgecolor='k', lw=0., label=labels[i])


ax_left.set(xlim=(-40, 42), ylim=(0.058, 2.2),xlabel="Heatwave-contributed O$_3$ (ppb)", ylabel="Altitude (km)")
ax_left.set_yticks([0.5, 1.0, 1.5, 2.0])
ax_left.set_yticklabels(['500', '1000', '1500', '2000'])
ax_left.xaxis.set_major_locator(ticker.MultipleLocator(20))


ax_left.tick_params(axis='both', which='major', direction='in', 
                   labelsize=8.8, length=3.5, width=0.35)

handles, labels = ax_left.get_legend_handles_labels()
ax_left.legend(handles, labels, frameon=False, fontsize=5.8, ncol=1,
              loc='upper right', bbox_to_anchor=(0.5, 1.), handletextpad=0.5,
              handlelength=1, handleheight=1, labelspacing=0.3)

ax_top = fig.add_axes([0.45, 0.31, 0.45, 0.39])
ax_bottom = fig.add_axes([0.45, 0., 0.45, 0.31])
ax_right = ax_top.twinx()
colors = {
    'normal': '#3566AB',
    'heatwave': '#AD2330',
    'gray': '#A3A3A3',
    'dark_gray': '#4F4E48',
    'grid': 'lightgrey',
    'dimgrey': 'dimgrey'
}

for ax in [ax_top, ax_bottom, ax_right]:
    ax.set_axisbelow(True)
    ax.grid(axis='both', lw=0.5, color=colors['grid'], ls='--')
    ax.tick_params(axis='both', which='major', direction='in',
                  labelsize=8.2, length=3.5, width=0.3)

ax_top.plot(np.arange(0., 1, 0.1)*100, O3_nm,
          color=colors['normal'], ls='-', lw=0.8, label='Normal Day')
ax_top.plot(np.arange(0., 1, 0.1)*100, O3_hw,
          color=colors['heatwave'], ls="-", lw=0.8, label='Heatwave day')
ax_right.plot(np.arange(0., 1., 0.1)*100, Chem_O3_nm,
             color=colors['normal'], ls='--', lw=0.7)
ax_right.plot(np.arange(0., 1., 0.1)*100, Chem_O3_hw,
             color=colors['heatwave'], ls="--", lw=0.7)
##for legend---
line1=ax_bottom.plot(np.arange(0.,1,0.1)*100,O3_nm[::-1]*1000+10000,color='k',ls='-',lw=0.8,marker='o',ms=0,label='O$_3$')
line2=ax_bottom.plot(np.arange(0.,1,0.1)*100,O3_hw[::-1]*1000+10000,color='k',ls="--",lw=0.8,marker='o',ms=0,label='Chem_O$_3$')
#-----

ax_bottom.bar(np.arange(0., 1, 0.1)*100+2, O3_hw-O3_nm,
             color=colors['gray'], edgecolor='k', lw=0., alpha=0.85, width=3.8,label="O$_3$$_{Heatwave}$ - O$_3$$_{Normal}$",)
for ax, points in [(ax_top, [(20, O3_hw[2], colors['heatwave']),
                              (30, O3_nm[3], colors['normal'])])]:
   for x, y, c in points:
        ax.scatter(x, y, s=54, color=c,lw=0.,ls='-', alpha=1, edgecolor='w', zorder=4.5)
for ax, points in [(ax_right, [(40, Chem_O3_hw[4], colors['heatwave']),
                              (50, Chem_O3_nm[5], colors['normal'])])]:
   for x, y, c in points:
        ax.scatter(x, y, s=40, lw=1.5,ls='-',  color='w', alpha=1, edgecolor=c, zorder=4)
ax_top.set(xlim=(-0.25, 94), ylim=(40, 95), xticklabels=[],ylabel="Surface O$_3$  (ppb)")
ax_top.set_yticks([40, 55, 70, 85])
ax_right.set(ylim=(70, 175), yticks=[70, 100, 130, 160])
ax_bottom.set(xlim=(-0.25, 94), ylim=(-20, 20), 
             xlabel="Anthropogenic NO$_x$ reduction (%)",ylabel='$\Delta$ Surface O$_3$ (ppb)')
ax_bottom.set_yticks([-20, -10, 0, 10, 20])
ax_bottom.set_yticklabels([-20, -10, 0, 10, ""])
ax_bottom.set_xticks(range(0, 91, 10))
ax_bottom.set_xticklabels(["0", "", "-20", "", "-40", "", "-60", "", "-80", ""])
ax_top.plot([30, 30], [-100, 1000], color=colors['dimgrey'], lw=0.52, ls='--')
ax_bottom.plot([30, 30], [-100, 1000], color=colors['dimgrey'], lw=0.52, ls='--')

ax_bottom.plot([-5, 95], [0, 0], colors['dimgrey'], lw=0.45)
# legend
ax_top.scatter(45+3-2,42.3,
              s=50, color='#4F4E48', alpha=0.9, edgecolor='none', zorder=5) 
ax_top.scatter(45+10-2,42.5,ls='-',lw=1.5,
             s=35, color='w', alpha=1, edgecolor='#4F4E48', zorder=4)

ax_top.text(61, 47, 'Normal Day', color=colors['normal'], fontsize=7.5)
ax_top.text(35, 47, 'Heatwave Day', color=colors['heatwave'], fontsize=7.5)
ax_top.text(57, 41, "Tipping point", fontsize=7.5)
ax_bottom.text(15, -12.8, "Penalty", fontsize=8)
ax_bottom.text(31, -12.8, "Reward", fontsize=8)

handles, labelss = ax_bottom.get_legend_handles_labels()

legend1=ax_bottom.legend(handles[:2], labelss[:2],frameon=False,fontsize=7.5,ncol=2,loc='upper right',bbox_to_anchor=(0.95-0.05,1.03),columnspacing=0.5)
ax_bottom.add_artist(legend1)
ax_bottom.legend(handles[2:], labelss[2:],frameon=False,fontsize=7.5,ncol=1,loc='upper right',bbox_to_anchor=(0.91,0.85))
arrow_props = dict(arrowstyle="-|>", color="black", lw=1, 
                  shrinkA=0, shrinkB=2, mutation_scale=10)
ax_bottom.annotate("", xy=(46, -15), xytext=(32, -15), arrowprops=arrow_props)
ax_bottom.annotate("", xy=(14, -15), xytext=(28, -15), arrowprops=arrow_props)

ax_right.yaxis.tick_left()
ax_right.tick_params(axis='x',which='both',direction='in',labelsize=8.2,length=0,width=0.)
ax_right.spines['left'].set_position(('outward', 35))
ax_right.spines['right'].set_linewidth(0)
ax_right.spines['top'].set_linewidth(0)
ax_right.spines['bottom'].set_linewidth(0)
ax_bottom.spines['top'].set_linewidth(0)
ax_top.spines['bottom'].set_linewidth(0)
ax_right.set_ylabel("Surface Chem_O$_3$ (ppb)  ",fontsize=8,labelpad=-277)
plt.savefig("Fig3.png",dpi=500,bbox_inches = 'tight')