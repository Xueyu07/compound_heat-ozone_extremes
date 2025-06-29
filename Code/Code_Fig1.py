import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap
from cartopy.io.shapereader import Reader
import os
mpl.use('Agg')

## Read Data

file_path = "../SourceData/SourceData_Fig1.xlsx"  
df1 = pd.read_excel(file_path, sheet_name='Fig1a_O3 anomaly',header=0,index_col=None) 
df2 = pd.read_excel(file_path, sheet_name='Fig1b_NO2 anomaly',header=0,index_col=None) 
df3 = pd.read_excel(file_path, sheet_name='Fig1b NO2 column anomaly',index_col=0)

NO2_Col = df3.iloc[1:, 1:].values
extent1=[70,130,15,60]
## Load shp

SHP = r'./Needed_Data'
def make_map(ax,box):
    ax.add_geometries(Reader(os.path.join(SHP, 'china.shp')).geometries(),
                      ccrs.PlateCarree(),facecolor='none',edgecolor='k', linewidth=0.4) 

    ax.set_extent([box[0],box[1],box[2],box[3]])
    return ax
    
### Define Colorbar
mycmap1 = ListedColormap([
    [0.99987698, 0.99820099, 0.99748599, 1.0],
    [0.99987698, 0.95820099, 0.93748599, 1.0],
    [0.99692398, 0.89619398, 0.84890401, 1.0],
    [0.991373, 0.79137301, 0.70823503, 1.0],
    [0.988235, 0.66649801, 0.55475599, 1.0],
    [0.982099, 0.407013, 0.28466001, 1.0],
    [0.88033399, 0.20686701, 0.13633201, 1.0],
    [0.7699, 0.044291, 0.1074602, 1.0]
], name='mycmap1')


mycmap4 = ListedColormap([
       [0.14117647, 0.14117647, 0.14117647, 1.        ],
       [0.18823529, 0.18823529, 0.18823529, 1.        ],
       [0.22745098, 0.22745098, 0.22745098, 1.        ],
       [0.2745098 , 0.2745098 , 0.2745098 , 1.        ],
       [0.3242599 , 0.3242599 , 0.3242599 , 1.        ],
       [0.37777778, 0.37777778, 0.37777778, 1.        ],
       [0.43129566, 0.43129566, 0.43129566, 1.        ],
       [0.48481353, 0.48481353, 0.48481353, 1.        ],
       [0.5372549 , 0.5372549 , 0.5372549 , 1.        ],
       [0.58431373, 0.58431373, 0.58431373, 1.        ],
       [0.63137255, 0.63137255, 0.63137255, 1.        ],
       [0.67843137, 0.67843137, 0.67843137, 1.        ],
       [0.71764706, 0.71764706, 0.71764706, 1.        ],
       [0.75570934, 0.75570934, 0.75570934, 1.        ],
       [0.79077278, 0.79077278, 0.79077278, 1.        ],
       [0.82583622, 0.82583622, 0.82583622, 1.        ],
       [0.86089965, 0.86089965, 0.86089965, 1.        ],
       [0.89273356, 0.89273356, 0.89273356, 1.        ],
       [0.92133795, 0.92133795, 0.92133795, 1.        ],
       [0.94994233, 0.94994233, 0.94994233, 1.        ],
       [0.97854671, 0.97854671, 0.97854671, 1.        ],
       [0.99953864, 0.9916955 , 0.98708189, 1.        ],
       [0.97347174, 0.9527105 , 0.92364475, 1.        ],
       [0.9799308 , 0.93148789, 0.86366782, 1.        ],
       [0.98638985, 0.91026528, 0.80369089, 1.        ],
       [0.9928489 , 0.88904268, 0.74371396, 1.        ],
       [0.99561707, 0.85997693, 0.67543253, 1.        ],
       [0.99469435, 0.82306805, 0.5988466 , 1.        ],
       [0.99377163, 0.78615917, 0.52226067, 1.        ],
       [0.9928489 , 0.74925029, 0.44567474, 1.        ],
       [0.98546713, 0.70911188, 0.37001153, 1.        ],
       [0.95870819, 0.65928489, 0.29711649, 1.        ],
       [0.93194925, 0.6094579 , 0.22422145, 1.        ],
       [0.90519031, 0.55963091, 0.15132641, 1.        ],
       [0.87843137, 0.50980392, 0.07843137, 1.        ],
       [0.83690888, 0.4710496 , 0.06551326, 1.        ],
       [0.79538639, 0.43229527, 0.05259516, 1.        ],
       [0.7538639 , 0.39354095, 0.03967705, 1.        ],
       [0.71234141, 0.35478662, 0.02675894, 1.        ],
       [0.66597463, 0.32502884, 0.02491349, 1.        ],
       [0.61799308, 0.2982699 , 0.02675894, 1.        ],
       [0.57001153, 0.27151096, 0.02860438, 1.        ],
       [0.52202999, 0.24475202, 0.03044983, 1.        ]]
                         , name='mycmap4')
## Plot Fig
fig = plt.figure( figsize=(8,5), facecolor='w', dpi=180)
proj = ccrs.PlateCarree()
# Plot ax1
ax1 = fig.add_axes([0.05, 0.1, 0.4, 0.8], projection=proj)
box = [99, 126.5, 17, 55]
make_map(ax1, box)
ax_nanhai = fig.add_axes([0.296, 0.1, 0.182, 0.17],projection = ccrs.PlateCarree())
make_map(ax_nanhai,[103,125,0,28])

# O3 anomaly
o3_cmap=mycmap1
o3_norm = mcolors.Normalize(vmin=10, vmax=46)
freq_bins = [(0, 1, 4), (1, 3, 8), (3, 6, 16), (6, np.inf, 30)]
for (low, high, size) in freq_bins:
    subset = df1[(df1['Co-occurrence Frequency'] >= low) & (df1['Co-occurrence Frequency'] < high)]
    sc1=ax1.scatter(subset['Longitude'], subset['Latitude'], s=size, c=subset['O3 anomaly'],
                cmap=o3_cmap, norm=o3_norm, transform=proj, edgecolors='k', linewidths=0.05)

for s, label in zip([5, 10, 15, 38], ["<1", "1–3", "3–6", ">6"]):
    ax1.scatter([], [], s=s, facecolor='lightgrey', edgecolor='k', lw=0.2,label=label)
ax1.legend(frameon=False, fontsize=7, title="Co-occurrence Frequency\n            (days/year)",
           loc='upper left', title_fontsize=8)
## Plot ax2
ax2 = fig.add_axes([0.55, 0.1, 0.4, 0.8], projection=proj)
make_map(ax2, box)
ax_nanhai2 = fig.add_axes([0.296+0.5, 0.1, 0.182, 0.17],projection =proj)
make_map(ax_nanhai2,[103,125,0,28])
## NO2 column 
im2 = ax2.imshow(NO2_Col, extent=extent1,  cmap=mycmap4, vmin=-0.18, vmax=0.18, 
                 origin='lower',  transform=ccrs.PlateCarree(), interpolation='none' )
## NO2 surface
no2_cmap = plt.get_cmap("bwr")
no2_norm = mcolors.Normalize(vmin=-10, vmax=10)
sc2 = ax2.scatter(df2['Longitude'], df2['Latitude'],
                 c=df2['NO2 anomaly'], s=22, cmap=no2_cmap,
                 norm=no2_norm, edgecolor='k', linewidth=0.1, transform=proj)
##  Plot legend
cbar_params = [{
        'im': im1,
        'pos': [0.46, 0.5, 0.012, 0.37],
        'ticks': pop_bounds,
        'label': "Population per km$^2$"},
    {
        'im': sc1,
        'pos': [0.46, 0.15, 0.01, 0.3],
        'ticks': np.arange(10, 50, 10),
        'label': "O$_3$ anomaly ($\mu$g/m$^3$)"},
    {
        'im': im2,
        'pos': [0.96, 0.55, 0.012, 0.3],
        'ticks': [-0.18, 0, 0.18],
        'label': "NO$_2$ column anomaly\n(10$^{16}$ mol cm$^{-2}$)"},
    {
        'im': sc2,
        'pos': [0.96, 0.15, 0.012, 0.3],
        'ticks': np.arange(-10, 11, 5),
        'label': "NO$_2$ anomaly ($\mu$g/m$^3$)"}]


cbar_list = []
for param in cbar_params:
    cbar_ax = fig.add_axes(param['pos'])
    cb = fig.colorbar(param['im'], cax=cbar_ax, ticks=param['ticks'])
    cb.ax.set_ylabel(param['label'], fontsize=8.5)
    cb.ax.tick_params(axis='both', which='major', 
                     labelsize=6.5, length=2.5, width=0.3)
    cbar_list.append(cb)
plt.savefig("Fig1.png",dpi=500,bbox_inches = 'tight')