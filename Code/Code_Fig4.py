import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cartopy.crs as ccrs
from matplotlib.colors import ListedColormap
from cartopy.io.shapereader import Reader
import os
mpl.use('Agg')
## Read Data
file_path = "../SourceData/SourceData_Fig4.xlsx" 
df1 = pd.read_excel(file_path, sheet_name='Fig4a',header=0,index_col=None) 
df2 = pd.read_excel(file_path, sheet_name='Fig4b',header=[0,1],index_col=0) 
df3=  pd.read_excel(file_path, sheet_name='Fig4c_Regions',header=[0,1],index_col=0) 
df4=  pd.read_excel(file_path, sheet_name='Fig4c_Co-occurrence Frequency',header=None,index_col=None) 
df5=  pd.read_excel(file_path, sheet_name='Fig4c_Grid Longitude',header=None,index_col=None) 
df6=  pd.read_excel(file_path, sheet_name='Fig4c_Grid Latitude',header=None,index_col=None) 


Emis_NOx_Base=df1['NOx Baseline'][0:9]
Emis_NOx_Cut=df1['NOx on-time peak-net zero-clean air'][0:9]
Tas_avg=df1['Tmax relative to 2020 (℃)'][:]
Tas_std=df1['Tmax standard deviation (℃)'][:]
Ur_Areas=df1['urban expension relative to 2020 (×10⁴ km²)'][0:5]

Areas=['NCP','YRD','SCB','PRD']
Species=['NO2','MDA8O3']
createVar = locals()
for i in range(0,4):
    for j in range(0,2):
            da = df2.loc[Areas[i]]
            createVar[Species[j]+'_Base_'+Areas[i]+'_mean']=da[j*8]
            createVar[Species[j]+'_Cut_'+Areas[i]+'_mean']=da[j*8+4]
            createVar[Species[j]+'_Base_'+Areas[i]+'_median']=da[j*8+1]
            createVar[Species[j]+'_Cut_'+Areas[i]+'_median']=da[j*8+4+1]
            createVar[Species[j]+'_Base_'+Areas[i]+'_10']=da[j*8+2]
            createVar[Species[j]+'_Cut_'+Areas[i]+'_10']=da[j*8+4+2]
            createVar[Species[j]+'_Base_'+Areas[i]+'_90']=da[j*8+3]
            createVar[Species[j]+'_Cut_'+Areas[i]+'_90']=da[j*8+4+3]

couped_days_Base=df4.iloc[:,:].values
lon=df5.iloc[:,:].values
lat=df6.iloc[:,:].values

CO_Freq=df3.iloc[:,:].values

# Define Colorbar
newcolors=[[1.        , 1.        , 1.        , 0.8       ],
       [0.58039216, 0.82352941, 0.94901961, 0.8       ],
       [0.49019608, 0.74117647, 0.90196078, 0.8       ],
       [0.4       , 0.6627451 , 0.85490196, 0.8       ],
       [0.30980392, 0.58039216, 0.80784314, 0.8       ],
       [0.28235294, 0.58823529, 0.67843137, 0.8       ],
       [0.28235294, 0.63137255, 0.54117647, 0.8       ],
       [0.28627451, 0.6745098 , 0.4       , 0.8       ],
       [0.3254902 , 0.72156863, 0.27843137, 0.8       ],
       [0.50980392, 0.77647059, 0.30196078, 0.8       ],
       [0.69803922, 0.82745098, 0.3254902 , 0.8       ],
       [0.88627451, 0.88235294, 0.34901961, 0.8       ],
       [0.97647059, 0.84313725, 0.33333333, 0.8       ],
       [0.97254902, 0.70980392, 0.27843137, 0.8       ],
       [0.96862745, 0.57647059, 0.22745098, 0.8       ],
       [0.96078431, 0.44313725, 0.17254902, 0.8       ],
       [0.92941176, 0.34509804, 0.16078431, 0.8       ],
       [0.90980392, 0.30588235, 0.16078431, 0.8       ],
       [0.85490196, 0.18431373, 0.15686275, 0.8       ],
       [0.78039216, 0.11372549, 0.14509804, 0.8       ],
       [0.6745098 , 0.09803922, 0.12156863, 0.8       ],
       [0.57254902, 0.08235294, 0.09803922, 0.8       ]]
mycmap1=ListedColormap(newcolors[::1],name='mycmap1')  

SHP = r'./Needed_Data'
def make_map(ax,box):
    ax.add_geometries(Reader(os.path.join(SHP, 'china.shp')).geometries(),
                      ccrs.PlateCarree(),facecolor='none',edgecolor='k', linewidth=0.4) 

    ax.set_extent([box[0],box[1],box[2],box[3]])
    return ax


#Plot Fig
fig = plt.figure(num="figure1", figsize=(8,6),facecolor='w',dpi=200)
colorss=['#454552','tab:blue','#8a0004']
## Figa
ax = fig.add_axes([0.0, 0.5, 0.35*0.923, 0.33*0.9])
ax1=ax.twinx()
ax.plot(np.arange(2020,2065,5),Emis_NOx_Base,color=colorss[0],ls='-',lw=0.8,label='Baseline')
ax.plot(np.arange(2020,2065,5),Emis_NOx_Cut,color=colorss[0],ls='--',lw=0.8,label='On-time peak-net zero-clean air')
ax.fill_between(np.arange(2020,2065,5), Emis_NOx_Base,Emis_NOx_Cut, color='#d4d4d1', alpha=0.2,lw=0)
ax1.plot(np.arange(2020,2061,1),Tas_avg,color=colorss[2],lw=1)
ax1.fill_between(np.arange(2020,2061,1), Tas_avg- Tas_std/2, Tas_avg+ Tas_std/2,color='#AD2330', alpha=0.2,lw=0)
axu = ax.twinx()
axu.plot(np.arange(2020,2061,10),Ur_Areas,color=colorss[1],lw=1.2)


ax.spines['right'].set_linewidth(0)
axu.spines['right'].set_position(("outward", 32))
for spine in ['left', 'top']:
    axu.spines[spine].set_linewidth(0)
    ax1.spines[spine].set_linewidth(0)
axu.spines['right'].set(color=colorss[1], linewidth=1, linestyle='-')
axu.tick_params(axis='both', which='both', direction='in',labelcolor=colorss[1], color=colorss[1],labelsize=8.5, length=2.5, width=1)
axu.set_ylim(0, 1.7)
axu.set_yticks([0, 0.5, 1, 1.5])
ax1.spines['right'].set(color=colorss[2], linewidth=1, linestyle='-')
ax.legend(frameon=False, fontsize=7, loc='right', bbox_to_anchor=(0.75, 0.9))
ax.plot([2030, 2030], [-0.50, 1.4], color='grey', lw=0.6, ls='dotted')
ax.tick_params(axis='both', which='both', direction='in',labelsize=8.5, length=2.5, width=1)
ax.set_ylim(-0.01, 1.5)
ax.set_yticks([0, 0.5, 1, 1.5])
ax.set_xlim(2020, 2060)
for x, label in zip([2030, 2060], ["Carbon peak", "Carbon neutrality"]):
    ax.text(x, -0.25, label, size=8, ha="center", va="center",
            bbox=dict(boxstyle="round", ec='w', fc='#ffda8e'))
ax1.set_yticks([0,0.5,1,1.5,2])
ax1.tick_params(axis='both',which='both',direction='in',labelcolor=colorss[2],color=colorss[2],labelsize=8.5,length=2.5,width=0.5)
ax1.set_ylabel("Tmax relative to 2020 ($^o$C)",color=colorss[2],fontsize=8)
ax.set_ylabel("NO$_x$ Emission level relative to 2020 ",color='k',fontsize=8)
axu.set_ylabel("Urban expansion relative to 2020 (×10$^4$ km$^2$)",color=colorss[1],fontsize=7.5)

## Figb
ax21 = fig.add_axes([0.505, 0.5, 0.35*0.94, 0.17*0.9])
ax22 = fig.add_axes([0.505, 0.68*0.95, 0.35*0.94, 0.17*0.9])
var1=["NO2_Base","NO2_Cut","MDA8O3_Base","MDA8O3_Cut"]
colors=['#3566AB','#F1FAEE','#3566AB','#F1FAEE','dimgrey','#7B68EE','#957DAD','#E0BBE4','k']
def draw_bar_with_error(ax, x, vmean, vmedian,err_low, err_high, color, edgecolor, label=None):
    ax.bar(x, vmean, width=0.3, lw=0.5, alpha=0.85, edgecolor=edgecolor, color=color, label=label)
    ax.errorbar(x, vmedian, xerr=0., yerr=np.array([err_low, err_high]).reshape(2, 1),
                color=colors[8], marker='o', markersize=2, markeredgecolor=colors[8], 
                markerfacecolor='w', mew=0.6, capsize=1, ecolor=colors[8],
                elinewidth=0.6, capthick=0.45)
    ax.set_xlim(-0.6, 4.2)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.tick_params(axis='y', which='both', direction='in', labelsize=8, length=2.5, width=0.45)
for i, area in enumerate(Areas):    
    for j, (var22, var21,color, edge, label) in enumerate(zip(var1[:2],var1[2:], colors[:2], ['#1a1f4a', '#8c8c8c'], ['Baseline', 'On-time peak-net zero-clean air'])):
        x = i - 0.15 if j == 0 else i + 0.15
        label = label if i == 0 else None
        draw_bar_with_error(ax22, x, createVar[var22+'_'+area+'_mean'], createVar[var22+'_'+area+'_median'], 
                            createVar[var22+'_'+area+'_median'] - createVar[var22+'_'+area+'_10'], createVar[var22+'_'+area+'_90']- createVar[var22+'_'+area+'_median'], color, edge, label)    
        draw_bar_with_error(ax21, x, createVar[var21+'_'+area+'_mean'], createVar[var21+'_'+area+'_median'], 
                            createVar[var21+'_'+area+'_median'] - createVar[var21+'_'+area+'_10'], createVar[var21+'_'+area+'_90']- createVar[var21+'_'+area+'_median'], color, edge, label)   

ax22.set_ylim(0, 75)
ax22.set_yticks(np.arange(0, 70, 20))
ax22.set_ylabel("NO$_2$ ($\mu$g/m$^3$)", color='k', fontsize=8)
ax22.set_xticks([])
ax21.set_ylim(0, 200)
ax21.set_yticks(np.arange(0, 160, 50))
ax21.set_xticks(np.arange(0, 4))
ax21.set_xticklabels(Areas, size=8)

ax21.spines['left'].set_bounds(0, 180)
ax21.tick_params(axis='x', which='both', direction='in', labelsize=8, length=0.5, width=0.45)
ax21.set_ylabel("MDA8 O$_3$ ($\mu$g/m$^3$)", color='k', fontsize=8)

for ax, y_vals in zip([ax21, ax21, ax22], [[100], [60], [10]]):
    for y in y_vals:
        ax.plot([-2, 5], [y, y], ls='--', lw=0.45, color=colors[4])

ax21.text(3.05, 64, "WHO-AQG (60$\mu$g/m$^3$)", color=colors[4], fontsize=6)
ax21.text(3., 104, "WHO Interim Target 1\n       (100$\mu$g/m$^3$)", color=colors[4], fontsize=6)
ax22.text(3.05, 11.2, "WHO-AQG (10$\mu$g/m$^3$)", color=colors[4], fontsize=6)

## plot for legend
ax22.errorbar(3.33, 63.5, yerr=10, color=colors[8], marker='o', markersize=3,
              markeredgecolor=colors[8], markerfacecolor='w', mew=0.6, capsize=2,
              ecolor=colors[8], elinewidth=0.6, capthick=0.45)
rect1 = patches.Rectangle((3.2, 48), 0.24, 11, lw=0.5, alpha=1, edgecolor=colors[8], facecolor='w')
ax22.add_patch(rect1)
ax22.legend(frameon=False, fontsize=6, loc='upper right', handlelength=1,
            columnspacing=0.8, handletextpad=0.5, ncol=2, bbox_to_anchor=(0.8, 1.15))
annotations = [
    ("Median", (3.45, 63.5), (4, 63.5)),
    ("Mean", (3.45, 58.5), (3.95, 58.5)),
    ("10th percentile", (3.45, 53.5), (4.2, 53.5)),
    ("90th percentile", (3.45, 73.5), (4.2, 73.5)),
]
for text, xy, xytext in annotations:
    ax22.annotate(text, xy=xy, xytext=xytext,
                  arrowprops=dict(arrowstyle="-|>", color="black", lw=0.5,
                                  shrinkA=0, shrinkB=2, mutation_scale=5),
                  fontsize=5, ha="center", va="center")

proj0=ccrs.LambertConformal(
    central_longitude=105, standard_parallels=(25, 47))
ax3 = fig.add_axes([-0.055, -0.12, 1, 0.55],projection = proj0)
box=[70, 145 ,12, 50]
make_map(ax3,box)
ax_nanhai = fig.add_axes([0.161, -0.045, 0.2, 0.09],projection = ccrs.PlateCarree())
make_map(ax_nanhai,[103,125,0,28])

xticks=np.arange(40,141,10)
yticks=np.arange(10,61,10)
c1=ax3.contourf(lon,lat,couped_days_Base,levels=np.arange(0,42,2),transform=ccrs.PlateCarree(),
               cmap=mycmap1,alpha=0.8,extend='both')
ax3.axis('off')
position1 = fig.add_axes([0.2, -0.1, 0.25, 0.015]) 
cb1 = plt.colorbar(c1,cax=position1,extendrect='both',orientation='horizontal',ticks=np.arange(0,45,5))  
cb1.outline.set_linewidth(0.)
cb1.ax.tick_params(axis='both',which='major',labelsize=7.5*0.875,length=2,width=0.2)
cb1.ax.set_title("Co-occurrence Frequency (days year$^{-1}$)",fontsize=8*0.875)

ax4c=fig.add_axes([0.01+0.005, -0.07-0.02, 0.15, 0.17])
ax4a=fig.add_axes([0.01+0.005, 0.17-0.02, 0.15, 0.17])
ax4d=fig.add_axes([0.665+0.005, -0.07-0.02, 0.15, 0.17])
ax4b=fig.add_axes([0.665+0.005, 0.17-0.02, 0.15, 0.17])
cols=['#008B8B','dimgrey','#9B59B6','#808080','#9C5250','#D1A45E','#5B605F',]
i=0
for ax4 in (ax4a,ax4b,ax4c,ax4d):
    ax4.bar(0,CO_Freq[i,0],width=0.3,color=cols[0],lw=0.47,edgecolor='k')
    ax4.bar(0.30,CO_Freq[i,1]-CO_Freq[i,0],bottom=CO_Freq[i,0],width=0.3,color=cols[1],lw=0.47,edgecolor='k')
    ax4.bar(0.6,CO_Freq[i,1]-CO_Freq[i,2],bottom=CO_Freq[i,2],width=0.3,color=cols[2],lw=0.4,edgecolor='k')
    ax4.plot([-2,6],[0,0],'k-',lw=1)

    ax4.text(0,CO_Freq[i,0]+0.2,str(round(CO_Freq[i,0],1)),color=cols[0],horizontalalignment='center',fontsize=8.5*0.875)
    ax4.text(0.3,CO_Freq[i,1]+0.2,str(round(CO_Freq[i,1],1)),color=cols[1],horizontalalignment='center',fontsize=8.5*0.875)
  
    ax4a.set_ylabel("Co-occurrence Frequency \n(days year$^{-1}$)",fontsize=8*0.875)
    ax4.text(0.6,CO_Freq[i,1]*0.5,"-"+str(round(CO_Freq[i,1]-CO_Freq[i,2],1)),color='w',horizontalalignment='center',
             verticalalignment='top',fontsize=7.5*0.875)
    if i !=3:
            ax4.text(0.3,CO_Freq[i,1]*0.8,"+"+str(round(CO_Freq[i,1]-CO_Freq[i,0],1)),color='w',horizontalalignment='center',
             verticalalignment='top',fontsize=7.5*0.875)
    else:
            ax4.text(0.3,CO_Freq[i,1]*1,"+"+str(round(CO_Freq[i,1]-CO_Freq[i,0],1)),color='w',horizontalalignment='center',
             verticalalignment='top',fontsize=7.5*0.875)
    ax4.set_xlim(-0.2,1.)
    ax4.set_ylim(-0.1,15)
    ax4.spines['top'].set_linewidth(0)
    ax4.spines['bottom'].set_linewidth(0.)
    ax4.spines['right'].set_linewidth(0.)
    ax4.text(0.8,14,Areas[i],fontsize=9)
    ax4.set_xticks([])
    ax4.set_yticks([0,5,10,15])
    ax4.tick_params(axis='y',which='both',direction='out',labelsize=8*0.875,length=3,width=0.35)
    i=i+1
ax3.text(95,49,"2060 Baseline",fontsize=10*0.89,color='k',transform=ccrs.PlateCarree(),)
ax4a.text(-0.15,20,"2014-2023 Observation",color=cols[0],fontsize=8*0.875)
ax4a.text(-0.15,18,"2060 Baseline",color=cols[1],fontsize=8*0.875)
ax4a.text(-0.15,16,"2060 On-time peak-net zero-clean air",color=cols[2],fontsize=8*0.875)
plt.savefig("Fig4.png",dpi=500,bbox_inches = 'tight')

