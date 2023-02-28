#########################################################################
# Date: 28-02-2023 Written by: J. Theeuwen                              #
#########################################################################
# This script creates a figure with 3 plots that show local moisture    #
# recycling ratio as defined by Theeuwen et al. (2022) at a resolution  #
# of 0.5 degrees for each season. Each plot shows a different definition#
# recycling over 1, 9 or 25 grid cells                                  #
# Theeuwen, J., Staal, A., Tuinenburg, O., Hamelers, B., and Dekker, S. #
# Local moisture recycling across the globe, EGUsphere [preprint],      #
# https://doi.org/10.5194/egusphere-2022-612, 2022.                     #
#########################################################################
# Input: Yearly averaged local moisture recycling ratio at a resolution #
# of 0.5 degrees. available at:
#########################################################################
#########################################################################

############################
###Import Python packages###
############################
from netCDF4 import Dataset
from numpy import *
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import sys
from scipy.interpolate import RegularGridInterpolator
import cartopy.crs as ccrs


###########################
###Import recycling data###
###########################
filepath = 'filepath'
filename = 'weighted_yearly_average_moisture_recycling_r'
grids = ['1','9','25']
grid_name = ['1grid', '9grids', '25grids']

def obtain_rec(grids,grid_name):
    f=Dataset(filepath+filename+str(grids)+'.nc')
    rec = f.variables[grid_name][:,:]
    # plotrec=np.zeros(rec.shape)
    # plotrec[:,:360]=rec[:,360:]
    # plotrec[:,360:]=rec[:,:360]
    return rec

rec_plot = np.zeros((3,360,720))
for i in np.arange(3):
    rec_plot[i,:,:] = obtain_rec(grids[i],grid_name[i])

##############################
#####Plot local recycling#####
##############################
def plot_subplots(rec_plot, ticks1,ticks9,ticks25):
    cm=mpl.cm.get_cmap('YlGnBu')
    cols=[]
    for i in arange(0,1,1.0/(len(ticks1)+1)):
        cols.append(cm(i))
    cols.append(cm(0.95))

    ##set range
    lats=arange(90,-90,-0.5)
    lons=arange(-180,180,0.5)

    ##create figure
    fig1 = plt.figure(figsize=(5,7))

    ##Create subplots
    ax1 = fig1.add_subplot(3,1,1, projection=ccrs.PlateCarree())
    ax1.coastlines(resolution='50m')
    cs1 = ax1.contourf(lons,lats,rec_plot[0,:,:],ticks1,colors=cols,transform=ccrs.PlateCarree(),extend='max')#,angles='xy')    #ax.quiver(lons[pointsx], lats[pointsy],plotarrx[pointsx], plotarry[pointsy],transform=ccrs.PlateCarree())
    ax1.set_title('1 grid cell', size=12);
    cbar1 = plt.colorbar(cs1, ax=ax1, shrink=0.9)#, location='bottom')
    cbar1.set_ticklabels(["0", "", "0.002", "","0.004","","0.006","","0.008"])
    cbar1.set_label('Local recycling ratio [-]', size=12)

    ax2 = fig1.add_subplot(3,1,2, projection=ccrs.PlateCarree())
    ax2.coastlines(resolution='50m')
    cs2 = ax2.contourf(lons,lats,rec_plot[1,:,:],ticks9,colors=cols,transform=ccrs.PlateCarree(),extend='max')#,angles='xy')    #ax.quiver(lons[pointsx], lats[pointsy],plotarrx[pointsx], plotarry[pointsy],transform=ccrs.PlateCarree())
    ax2.set_title('9 grid cells', size=12);
    cbar2 = plt.colorbar(cs2, ax=ax2, shrink=0.9)
    cbar2.set_ticklabels(["0", "", "0.018", "","0.036","","0.054","","0.072"])
    cbar2.set_label('Local recycling ratio [-]', size=12)

    ax3 = fig1.add_subplot(3,1,3, projection=ccrs.PlateCarree())
    ax3.coastlines(resolution='50m')
    cs3 = ax3.contourf(lons,lats,rec_plot[2,:,:],ticks25,colors=cols,transform=ccrs.PlateCarree(),extend='max')#,angles='xy')    #ax.quiver(lons[pointsx], lats[pointsy],plotarrx[pointsx], plotarry[pointsy],transform=ccrs.PlateCarree())
    ax3.set_title('25 grid cells', size=12);
    cbar3 = plt.colorbar(cs3, ax=ax3, shrink=0.9)
    cbar3.set_ticklabels(["0", "", "0.05", "","0.10","","0.15","","0.20"])
    cbar3.set_label('Local recycling ratio [-]', size=12)

    plt.tight_layout()
    plt.savefig('yearly_average_per_grid_type_2.png')
    plt.show()
    plt.close()

ticks1 = arange(0,0.01,0.001)
ticks9 = arange(0,0.09,0.009)
ticks25 = arange(0,0.25,0.025)

plot_subplots(rec_plot, ticks1,ticks9,ticks25)
