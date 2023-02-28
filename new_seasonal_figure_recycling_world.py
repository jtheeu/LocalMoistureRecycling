#########################################################################
# Date: 28-02-2023 Written by: J. Theeuwen                              #
#########################################################################
# This script creates a figure with 4 plots that show local moisture    #
# recycling ratio as defined by Theeuwen et al. (2022) at a resolution  #
# of 0.5 degrees for each season.                                       #
# Theeuwen, J., Staal, A., Tuinenburg, O., Hamelers, B., and Dekker, S. #
# Local moisture recycling across the globe, EGUsphere [preprint],      #
# https://doi.org/10.5194/egusphere-2022-612, 2022.                     #
#########################################################################
# Input: Sesonally averaged local moisture recycling ratio at a         #
# resolution of 0.5 degrees. available at:
#########################################################################
#########################################################################

################################
#####Import python packages#####
################################
from netCDF4 import Dataset
from numpy import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
from scipy.interpolate import RegularGridInterpolator
import cartopy.crs as ccrs
import cartopy.feature as cfeature

##############################
###Import land surface mask###
##############################
f_lsm = Dataset('lsm_nan.nc')
lsm = f_lsm.variables['lsm'][:,:]
lsm[lsm==0.0] = np.nan
plotlsm=np.zeros(lsm.shape)
plotlsm[:,:360]=lsm[:,360:]
plotlsm[:,360:]=lsm[:,:360]

###########################
###Import recycling data###
###########################
f=Dataset('weighted_yearly_average_moisture_recycling_r9.nc')
rec = f.variables['recycling'][:,:,:]
plotrec=zeros(rec.shape)
plotrec[:,:,:360]=rec[:,:,360:]
plotrec[:,:,360:]=rec[:,:,:360]


##############################
#####Plot local recycling#####
##############################
mpl.rcParams['figure.figsize'] = [20.0, 8.0]
mpl.rcParams['figure.dpi'] = 80
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['font.size'] = 20
mpl.rcParams['legend.fontsize'] = 'large'
mpl.rcParams['figure.titlesize'] = 'large'

lats=arange(90,-90,-0.5)
lons=arange(-180,180,0.5)
title = 'Evaporation recycling in 9 grid cells'
cm=mpl.cm.get_cmap('YlGnBu')
cols=[]
ticks = arange(0,0.09,0.009)

for i in arange(0,1,1.0/(len(ticks)+1)):
    cols.append(cm(i))
cols.append(cm(0.95))


def plot_subplots(seasonal_rec_plot):
    lats=arange(90,-90,-0.5)
    lons=arange(-180,180,0.5)
    fig1 = plt.figure(figsize=(15,8))
    ax1 = fig1.add_subplot(2,2,1, projection=ccrs.PlateCarree())
    #ax1.gridlines()
    ax1.add_feature(cfeature.OCEAN, color='lightgray')
    ax1.coastlines(resolution='50m')
    cs1 = ax1.contourf(lons,lats,rec_plot[0,:,:],ticks,colors=cols,transform=ccrs.PlateCarree(),extend='max')
    ax1.set_title('DJF', size=16);
    print('meanLMR')
    print(np.nanmean(rec_plot[0,:,:]))
    #plt.show()
    #plt.close()
    ax2 = fig1.add_subplot(2,2,2, projection=ccrs.PlateCarree())
    #ax2.background_patch.set_fill(False)
    ax2.add_feature(cfeature.OCEAN, color='lightgray')
    #ax2.gridlines()
    ax2.coastlines(resolution='50m')
    cs2 = ax2.contourf(lons,lats,rec_plot[1,:,:],ticks,colors=cols,transform=ccrs.PlateCarree(),extend='max')
    ax2.set_title('MAM', size=16);

    ax3 = fig1.add_subplot(2,2,3,projection=ccrs.PlateCarree())
    #ax3.gridlines()
    ax3.coastlines(resolution='50m')
    ax3.add_feature(cfeature.OCEAN, color='lightgray')
    cs3 = ax3.contourf(lons,lats,rec_plot[2,:,:],ticks,colors=cols,transform=ccrs.PlateCarree(),extend='max')
    ax3.set_title('JJA', size=16);

    ax4 = fig1.add_subplot(2,2,4,projection=ccrs.PlateCarree())
    #ax4.gridlines()
    ax4.coastlines(resolution='50m')
    ax4.add_feature(cfeature.OCEAN, color='lightgray')
    cs4 = ax4.contourf(lons,lats,rec_plot[3,:,:],ticks,colors=cols,transform=ccrs.PlateCarree(),extend='max')
    ax4.set_title('SON', size=16);

    # fig1.subplots_adjust(right=0.80)
    # cbar_ax = fig1.add_axes([0.83, 0.25, 0.02, 0.5])
    # out = fig1.colorbar(cs4, cax=cbar_ax,extend='max')#,fontsize=18)
    # out.set_ticklabels(["0", "", "0.018", "","0.036","","0.054","","0.072"])
    # cbar_ax.tick_params(labelsize=16)
    # out.set_label('Local moisture recycling ratio (-)',size=16)
    #out.set_ticks(ticks, fontsize=18)

    plt.tight_layout()
    plt.savefig('seasonal_weighted_gray_background.png')
    #plt.savefig('C:/Users/jthe/Documents/Python/project_ob_1/figs_worldwide/YlGnBu_cbar_seasonal_only_land_world_mrec9_plot.png')
    #plt.savefig('seasonal_test_font16_nobar.png')
    #plt.show()
    plt.close()

plot_subplots(plotrec)

    # fig = plt.figure(figsize=(10,10))
    # ax = plt.axes(projection=ccrs.PlateCarree())
    # #ax.set_extent(extent)
    # ax.gridlines()
    # ax.coastlines(resolution='50m')
    # #ticks=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    # cs = ax.contourf(lons,lats,plotrec,ticks,colors=cols,transform=ccrs.PlateCarree(),extend='max')
    # cax,kw = matplotlib.colorbar.make_axes(ax,location='right',pad=0.05,shrink=0.6)
    # out=fig.colorbar(cs,cax=cax,extend='both',**kw)
    # out.set_label('Recycling ratio (-)',size=12)
    # out.ax.tick_params(labelsize=12)
    # ax.set_title(title, size=12);
    #
    # #plt.savefig('mb_local_recycling_'+str(month).zfill(2)+'.png')
    # plt.show()
    # plt.close()

    # #South Africa
    # central_lon, central_lat = 24, -33
    # extent = [10, 38, -40, -26]
    # fig = plt.figure(figsize=(10,10))
    # ax = plt.axes(projection=ccrs.Orthographic(central_lon, central_lat))
    # ax.set_extent(extent)
    # ax.gridlines()
    # ax.coastlines(resolution='50m')
    #
    # #ticks=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    # cs = ax.contourf(lons,lats,plotrec,ticks,colors=cols,transform=ccrs.PlateCarree(),extend='max')
    # cax,kw = matplotlib.colorbar.make_axes(ax,location='right',pad=0.05,shrink=0.6)
    # out=fig.colorbar(cs,cax=cax,extend='both',**kw)
    # out.set_label('Recycling ratio (-)',size=12)
    # out.ax.tick_params(labelsize=12)
    # ax.set_title(title, size=12);
    # plt.savefig('sa_local_recycling_'+str(month).zfill(2)+'.png')
    # #plt.show()
    # plt.close()
    #
    # #Australia
    # central_lon, central_lat = 130, -31.5
    # extent = [106, 154, -48, -15]
    # fig = plt.figure(figsize=(10,10))
    # ax = plt.axes(projection=ccrs.Orthographic(central_lon, central_lat))
    # ax.set_extent(extent)
    # ax.gridlines()
    # ax.coastlines(resolution='50m')
    #
    # #ticks=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    # cs = ax.contourf(lons,lats,plotrec,ticks,colors=cols,transform=ccrs.PlateCarree(),extend='max')
    # cax,kw = matplotlib.colorbar.make_axes(ax,location='right',pad=0.05,shrink=0.6)
    # out=fig.colorbar(cs,cax=cax,extend='both',**kw)
    # out.set_label('Recycling ratio (-)',size=12)
    # out.ax.tick_params(labelsize=12)
    # ax.set_title(title, size=12);
    # plt.savefig('au_local_recycling_'+str(month).zfill(2)+'.png')
    # #plt.show()
    # plt.close()
    #
    # #Chile
    # central_lon, central_lat = -70, -32
    # extent = [-80, -60, -54, -10]
    # fig = plt.figure(figsize=(10,10))
    # ax = plt.axes(projection=ccrs.Orthographic(central_lon, central_lat))
    # ax.set_extent(extent)
    # ax.gridlines()
    # ax.coastlines(resolution='50m')
    #
    # #ticks=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    # cs = ax.contourf(lons,lats,plotrec,ticks,colors=cols,transform=ccrs.PlateCarree(),extend='max')
    # cax,kw = matplotlib.colorbar.make_axes(ax,location='right',pad=0.05,shrink=0.6)
    # out=fig.colorbar(cs,cax=cax,extend='both',**kw)
    # out.set_label('Recycling ratio (-)',size=12)
    # out.ax.tick_params(labelsize=12)
    # ax.set_title(title, size=12);
    # plt.savefig('ch_local_recycling_'+str(month).zfill(2)+'.png')
    # plt.close()
    #
    # #California
    # central_lon, central_lat = -118, 36
    # extent = [-131, -105, 20, 52]
    # fig = plt.figure(figsize=(10,10))
    # ax = plt.axes(projection=ccrs.Orthographic(central_lon, central_lat))
    # ax.set_extent(extent)
    # ax.gridlines()
    # ax.coastlines(resolution='50m')
    #
    # #ticks=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    # cs = ax.contourf(lons,lats,plotrec,ticks,colors=cols,transform=ccrs.PlateCarree(),extend='max')
    # cax,kw = matplotlib.colorbar.make_axes(ax,location='right',pad=0.05,shrink=0.6)
    # out=fig.colorbar(cs,cax=cax,extend='both',**kw)
    # out.set_label('Recycling ratio (-)',size=12)
    # out.ax.tick_params(labelsize=12)
    # ax.set_title(title, size=12);
    # plt.savefig('ca_local_recycling_'+str(month).zfill(2)+'.png')
    # plt.close()
