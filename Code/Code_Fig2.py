import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import ticker as mticker
import matplotlib as mpl 
from matplotlib.colors import ListedColormap
import seaborn as sns
mpl.use('Agg')

## Read Data
file_path = "../SourceData/SourceData_Fig2.xlsx"  
df1 = pd.read_excel(file_path, sheet_name='Fig2a_Normal Day Backscatter',header=0,index_col=0) 
df2 = pd.read_excel(file_path, sheet_name='Fig2a_Heatwave Day Backscatter',header=0,index_col=0) 
df3 = pd.read_excel(file_path, sheet_name='Fig2a_PBLH',header=0,index_col=None) 
df4 = pd.read_excel(file_path, sheet_name='Fig2b',header=0,index_col=None) 
df5 = pd.read_excel(file_path, sheet_name='Fig2c_EKMA Max O3',header=0,index_col=0) 
df6 = pd.read_excel(file_path, sheet_name='Fig2c_point',header=0,index_col=0) 

BS_nm=df1.iloc[:,:].values
BS_hw=df2.iloc[:,:].values
PBLHh=df3['Heatwave Day PBLH (m)']
PBLHn=df3['Normal Day PBLH (m)']
Height=np.arange(10,4510,10)
Timer=pd.date_range("2023-05-01 00:00:00","2023-05-01 23:50:00",freq='10T')  #any date is ok, just use for x axis

O3_max=df5.iloc[:,:].values
Rvocs=np.arange(1,30)*0.266
Cnox=np.arange(1,40)*0.5615
X_vocs,Y_nox, = np.meshgrid( Rvocs,Cnox,) 

NOx_surfacen, NOx_surfaceh, NOx_aloftn, NOx_alofth,=df6.iloc[0,:]
VOC_surfacen, VOC_surfaceh, VOC_aloftn, VOC_alofth,=df6.iloc[1,:]
VOC_xerror=df6.iloc[2,2]

hh=df4['Altitude (m)']
o3_nm_m=df4['ΔO3_NM']
o3_hw_m=df4['ΔO3_HW']
o3_nm_sd=df4['O3_sd_NM']
o3_hw_sd=df4['O3_sd_HW']
nox_nm_m=df4['ΔNOx_NM']
nox_hw_m=df4['ΔNOx_HW']
nox_nm_sd=df4['NOx_sd_NM']
nox_hw_sd=df4['NOx_sd_HW']

# Define Colorbar
newcolors=[[1.        , 1.        , 1.        , 0.8       ],
       [0.58039216, 0.80352941, 0.94901961, 0.8       ],
       [0.49019608, 0.74117647, 0.90196078, 0.8       ],
       [0.4       , 0.6627451 , 0.85490196, 0.8       ],
       [0.30980392, 0.58039216, 0.77784314, 0.8       ],
       [0.28235294, 0.58823529, 0.60843137, 0.8       ],
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
       [0.92941176, 0.34509804, 0.16078431, 0.8       ]]
mycmap1=ListedColormap(newcolors[::1],name='mycmap1')  
cmap2 = sns.diverging_palette( 250, 25, s=85, l=70, n=15, as_cmap=True)

## Plot 
fig = plt.figure(num="figure1", figsize=(6.3, 5.4), facecolor='w', dpi=180)
# Fig2a

ax5 = fig.add_axes([0.56, 0.6,0.405, 0.22,],)
ax6 = fig.add_axes([1.027, 0.6,0.405, 0.22,],)

ax6.plot(Timer,PBLHh,'k',lw=1,ls='--',label='PBLH')
ax5.plot(Timer,PBLHn,'k',lw=1,ls='--',label='PBLH')
ax5.legend(frameon=False,fontsize=9)
c10=ax5.pcolormesh(Timer, Height, np.transpose(BS_nm),vmin=375,vmax=1200,
                    cmap=mycmap1,  shading='nearest', alpha=0.85)
ax6.pcolormesh(Timer, Height, np.transpose(BS_hw), vmin=375,vmax=1200,
                    cmap=mycmap1, shading='nearest', alpha=0.85)
for ax in (ax5, ax6):
    ax.spines[:].set_linewidth(0.4)
    ax.set_xlabel("Hour of Day", fontsize=10.5)
    ax.set_ylim(0, 2500)
    ax.set_yticks([500, 1000, 1500, 2000])
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:00"))
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 6, 12, 18, 24]))
    ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 25, 2)))
    ax.tick_params(axis='both', which='major', direction='in', 
                 labelsize=9, length=2.5, width=0.5)
    ax.tick_params(axis='both', which='minor', direction='in',
                 labelsize=9, length=1.5, width=0.5)
    ax.yaxis.set_minor_locator(mticker.MaxNLocator(6))
ax5.set_ylabel("Altitude (m)", fontsize=10)
ax10 = fig.add_axes([1.45, 0.6, 0.015, 0.18])
cb10 = fig.colorbar(c10, cax=ax10, shrink=0.5, extendrect=False, pad=0.03,
                   ticks=np.arange(400, 1600, 200))
cb10.outline.set_linewidth(0.1)
cb10.ax.tick_params(which='major', direction='in', labelsize=6.5, 
                   length=0.6, width=0.3)
cb10.ax.set_ylabel("Bscat. Coeff.\n(10$^{-9}$m$^{-1}$Sr$^{-1}$)", fontsize=8.5)
ax5.text(Timer[5], 2100, 'Normal Day', fontsize=9)
ax6.text(Timer[5], 2100, 'Heatwave Day', fontsize=9)

# Fig2b

colors=['#3566AB','#AD2330']

ax33 = fig.add_axes([0.560, 0.05, 0.18,0.41,],)
ax33.plot(o3_nm_m,hh,marker='o',markersize=0,mfc='w',mew=0.5,color=colors[0],lw=0.8)
ax33.plot(o3_hw_m,hh,marker='o',markersize=0,mfc='w',mew=0.5,color=colors[1],lw=0.8)
ax33.plot(np.arange(0,1100,100)*0,np.arange(0,1100,100),color='dimgrey',ls='--',lw=0.5)
ax33.fill_betweenx(hh,o3_nm_m-o3_nm_sd/2,o3_nm_m+o3_nm_sd/2,color=colors[0],alpha=0.07,lw=0,)
ax33.fill_betweenx(hh,o3_hw_m-o3_hw_sd/2,o3_hw_m+o3_hw_sd/2,color=colors[1],alpha=0.07,lw=0,)
ax66 = fig.add_axes([0.235+0.53, 0.05, 0.18,0.41,],)
ax66.plot(np.arange(0,1100,100)*0,np.arange(0,1100,100),color='dimgrey',ls='--',lw=0.5)
ax66.plot(nox_nm_m,hh,marker='o',markersize=0,mfc='w',mew=0.5,color=colors[0],lw=0.8)
ax66.plot(nox_hw_m,hh,marker='o',markersize=0,mfc='w',mew=0.5,color=colors[1],lw=0.8)
ax66.fill_betweenx(hh,nox_nm_m-nox_nm_sd/2,nox_nm_m+nox_nm_sd/2,color=colors[0],alpha=0.07,lw=0,)
ax66.fill_betweenx(hh,nox_hw_m-nox_hw_sd/2,nox_hw_m+nox_hw_sd/2,color=colors[1],alpha=0.07,lw=0,)
ax33.set_title(' ' * 35 + 'Daytime change', fontsize=9.5)
for ax in (ax33, ax66):
    ax.spines[:].set_linewidth(0.45)
    ax.tick_params(axis='both', which='both', direction='in')
    ax.set_ylim(20, 1000)
ax33.set(xlim=(0, 70), xlabel="$\Delta$O$_3$ (ppb)", xticks=[0,20,40,60],
        yticks=[100, 300, 500, 700, 900])
ax33.spines.right.set_visible(False)
ax66.set(xlim=(-15, 7.5), xlabel="$\Delta$NO$_x$ (ppb)", 
        xticks=[-10, -5, 0, 5], yticks=[])
ax66.spines.left.set_visible(False)
ax33.set_ylabel("Altitude (m)",fontsize=10.5)
ax66.text(-20,900,"Normal Day",color=colors[0],fontsize=9)
ax66.text(-20,820,"Heatwave Day",color=colors[1],fontsize=9)

## Fig3c
colors1=['tab:blue','tab:red']
ax22= fig.add_axes([0.555+0.5, 0.05, 0.345+0.035,0.379+0.03,],)
cs = ax22.contourf(X_vocs, Y_nox, O3_max, extend='both', 
                   levels=np.linspace(10, 115, 20), cmap=cmap2)
plot_params = {
    'marker': {'surface': 'o', '1km': 's'},
    'color': {'normal': 'tab:blue', 'heatwave': 'tab:red'},
    'errorbar': {
        'surface': {'elinewidth':0.8, 'capsize':2, 'capthick':0.5},
        '1km': {'elinewidth':0.6, 'capsize':3, 'capthick':0.5, 'xerr':VOC_xerror}
    },
    'common': {'mec':'k', 'mew':0.8, 'alpha':0.9, 'ecolor':'k'}}

surface_color = {'normal': 'tab:blue', 'heatwave': 'tab:red'}
height_marker = {'surface': 'o', '1km': 's'}

l1=ax22.errorbar(VOC_surfacen, NOx_surfacen, 
              fmt=height_marker['surface'], markersize=8, mec='k',mew=0.8,color=surface_color['normal'], 
              alpha=0.9, elinewidth=0.8, capsize=2, capthick=0.5, label='Normal Surface')

l2=ax22.errorbar(VOC_surfaceh, NOx_surfaceh, 
              fmt=height_marker['surface'], markersize=8, mec='k',mew=0.8,color=surface_color['heatwave'], 
              alpha=0.9, elinewidth=0.8, capsize=2, capthick=0.5, label='Heatwave Surface')
l3=ax22.errorbar(VOC_aloftn, NOx_aloftn, xerr=VOC_xerror, 
              fmt=height_marker['1km'], markersize=7.,mec='k',mew=0.8,color=surface_color['normal'], 
               alpha=0.9, ecolor='k',elinewidth=0.6, capsize=3, capthick=0.5, label='Normal 1km')
l4=ax22.errorbar(VOC_alofth, NOx_alofth, xerr=VOC_xerror,
              fmt=height_marker['1km'], markersize=7., mec='k',mew=0.8,color=surface_color['heatwave'], 
               alpha=0.9,ecolor='k', elinewidth=0.6, capsize=3, capthick=0.5, label='Heatwave 1km')
ax22.plot([X_vocs[0,0],5],[3.5,6.5],color='dimgrey',ls='--',lw=0.4)
ax22.plot([X_vocs[0,0],5],[3.5,15.5],color='dimgrey',ls='--',lw=0.4)
ax22.annotate("", xy=(2.96,9.02+0.4),xytext=(2.74+0.02,12.0-0.42),
            arrowprops=dict(arrowstyle='->',lw=0.5,color='k'),)

ax22.annotate("", xy=(2.48+0.01,6.1-0.42),xytext=(2.44,3.9+0.4),
            arrowprops=dict(arrowstyle='->',lw=0.5,color='k'),)
contour_lines = ax22.contour(X_vocs, Y_nox, O3_max, levels=np.linspace(10, 115, 20), 
                             colors='grey', linewidths=0., alpha=0.6)
ax22.set_xlim(X_vocs[0,0],4.5)
ax22.set_ylim(Y_nox[0,0],16)
ax22.set_yticks([5,10,15])
ax22.set_xticks([1,2,3,4])
ax22.text(0.7,14.5,'VOC-limited',fontsize=8.8,color='k')
ax22.text(0.7,1.5,'NO$_x$-limited',fontsize=8.8,color='k')
ax22.text(3.15,7.6,'Transitional',fontsize=8.8,color='k')
ax22.set_xlabel("VOCs (s$^{-1}$)",fontsize=10.5)
ax22.set_ylabel("NO$_x$ (ppb)",fontsize=10.5)
ax1a = fig.add_axes([1.45,0.11, 0.015,0.3,],)
cb1a=fig.colorbar(cs,cax=ax1a,shrink=0.5,extendrect=False,pad=0.03,ticks= np.arange(20,120,20))  
cb1a.outline.set_linewidth(0.)
cb1a.ax.tick_params(axis='both',which='major',direction='out',labelsize=8,length=2,width=0.2)
cb1a.ax.set_ylabel("Max O$_3$ (ppb)",fontsize=9)

ax22.legend(handles=[l1,l2,l3,l4], ncol=4,labels=['', 'Surface      ','', '~ 1km'],
            columnspacing=-0.5,handletextpad=0,frameon=False,fontsize=8.5,bbox_to_anchor=(.85, 1.12))
plt.savefig("Fig2.png",dpi=500,bbox_inches = 'tight')
