#########################################################################
# Date: 28-02-2023 Written by: J. Theeuwen                              #
#########################################################################
# This script creates figures that show recycling of evaporated moisture#
# within their source grid cell computed from two models: UTrack and    #
# WAM2-Layers. It also plots the difference between the two models.     #
# Theeuwen, J., Staal, A., Tuinenburg, O., Hamelers, B., and Dekker, S. #
# Local moisture recycling across the globe, EGUsphere [preprint],      #
# https://doi.org/10.5194/egusphere-2022-612, 2022.                     #
#########################################################################
# Input: Yearly averaged local moisture recycling ratio at a resolution #
# of 1.5 degrees. available at:
#########################################################################
#########################################################################

############################
###Import Python packages###
############################
import numpy as np
import os
import time
from netCDF4 import Dataset
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

mpl.rcParams['figure.figsize'] = [20.0, 8.0]
mpl.rcParams['figure.dpi'] = 80
mpl.rcParams['savefig.dpi'] = 300

f_link = Dataset('link_1.5degrees_weighted_yearly_average_moisture_recycling_seasonal.nc')
f_utrack = Dataset('1.5degrees_weighted_yearly_average_moisture_recycling_seasonal.nc')#UTrack data

rec_link = f_link.variables['recycling'][:,:]
rec_utrack = f_utrack.variables['recycling'][:,:]
plot_rec_link = np.zeros(rec_link.shape)
plot_rec_utrack = np.zeros(rec_utrack.shape)
plot_rec_link[:,:120]=rec_link[:,120:]
plot_rec_link[:,120:]=rec_link[:,:120]
plot_rec_utrack[:,:120]=rec_utrack[:,120:]
plot_rec_utrack[:,120:]=rec_utrack[:,:120]

# plot_rec_link[plot_rec_link==0]=np.nan
# plot_rec_utrack[plot_rec_utrack==0]=np.nan

###################################
###Calculate absolute difference###
###################################
difference = np.subtract(plot_rec_utrack,plot_rec_link)
mer_average = np.nanmean(abs(difference),axis=1)#meridional average of absolute differnce
#Change to zonal average by changing the axis.
mer_stdev = np.nanstd(abs(difference),axis=1)#st.dev. of meridional average of the absolute difference

###################################
###Calculate relative difference###
###################################
r_difference = np.divide(np.subtract(plot_rec_utrack,plot_rec_link),plot_rec_utrack)
r_mer_average = np.nanmean(r_difference,axis=1)
r_mer_stdev = np.nanstd(r_difference,axis=1)
r_average = np.nanmean(abs(r_difference))
r_average_stdev = np.nanstd(abs(r_difference))
#print(r_average)
#print(r_average_stdev)

##############################
###Plot absolute difference###
##############################
ticks = np.array(np.arange(-0.06,0.065,0.01))

lats=np.arange(79.5,-80,-1.5)
lons=np.arange(-180,180,1.5)

fig = plt.figure(figsize=(10,8))
plt.plot(lats,mer_average)

plt.fill_between(lats, mer_average-mer_stdev, mer_average+mer_stdev,
    alpha=0.2, edgecolor='#1B2ACC', facecolor='#089FFF')
plt.xlabel('Latitude [degrees]',size=16)
plt.ylabel('Difference in recycling [-]',size=16)
plt.title('abs(UTrack - WAM2-Layers)', size=14)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.xlim(-60,80)
#plt.show()
#plt.savefig('meridional_average_recycling_difference_absolute.png')
plt.close()

cm=mpl.cm.get_cmap('bwr')
cols=[]
for i in np.arange(0,1,1.0/len(ticks)):
    cols.append(cm(i))
cols.append(cm(0.95))


fig = plt.figure(figsize=(10,6))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines(resolution='50m')
cs = ax.contourf(lons,lats,difference,ticks,colors=cols,transform=ccrs.PlateCarree(),extend='both')
cax,kw = mpl.colorbar.make_axes(ax,location='right',pad=0.05,shrink=0.5)
out=fig.colorbar(cs,cax=cax,extend='both',**kw,drawedges='none')
out.set_label('difference [-]',size=14)
out.ax.tick_params(labelsize=12)
#ax.set_title(title, size=12);
#plt.savefig('LMR_difference.png')
#plt.show()
plt.close()

##############################
###Plot relative difference###
##############################
ticks = np.array(np.arange(-3,3.5,0.5))
lats=np.arange(79.5,-80,-1.5)
lons=np.arange(-180,180,1.5)
fig = plt.figure(figsize=(10,8))
plt.plot(lats,mer_average)

plt.fill_between(lats, r_mer_average-r_mer_stdev, r_mer_average+r_mer_stdev,
    alpha=0.2, edgecolor='#1B2ACC', facecolor='#089FFF')
plt.xlabel('Latitude [degrees]',size=16)
plt.ylabel('Difference in recycling [-]',size=16)
plt.title('(UTrack - WAM2-Layers)/UTrack', size=14)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.xlim(-60,80)
#plt.show()
#plt.savefig('meridional_average_recycling_difference_relative.png')
plt.close()

cm=mpl.cm.get_cmap('bwr')
cols=[]
for i in np.arange(0,1,1.0/len(ticks)):
    cols.append(cm(i))
cols.append(cm(0.95))

fig = plt.figure(figsize=(10,6))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines(resolution='50m')
cs = ax.contourf(lons,lats,r_difference,ticks,colors=cols,transform=ccrs.PlateCarree(),extend='both')
plt.title('(UTrack - WAM2-Layers)/UTrack', size=14)
cax,kw = mpl.colorbar.make_axes(ax,location='right',pad=0.05,shrink=0.5)
out=fig.colorbar(cs,cax=cax,extend='both',**kw,drawedges='none')
out.set_label('Relative difference [-]',size=14)
out.ax.tick_params(labelsize=12)
#plt.savefig('LMR_relative_difference.png')
#plt.show()
plt.close()

###########################
###Plot recycling UTrack###
###########################
#ticks = np.array(np.arange(0,0.1,0.01))
ticks = np.arange(0,0.09,0.009)

lats=np.arange(79.5,-80,-1.5)
lons=np.arange(-180,180,1.5)
cm=mpl.cm.get_cmap('YlGnBu')
cols=[]
for i in np.arange(0,1,1.0/len(ticks)):
    cols.append(cm(i))
cols.append(cm(0.95))

fig = plt.figure(figsize=(10,6))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines(resolution='50m')
cs = ax.contourf(lons,lats,plot_rec_utrack,ticks,colors=cols,transform=ccrs.PlateCarree(),extend='max')
cax,kw = mpl.colorbar.make_axes(ax,location='right',pad=0.05,shrink=0.5)
out=fig.colorbar(cs,cax=cax,extend='max',**kw,drawedges='none')
out.set_label('Recycling UTrack [-]',size=14)
out.ax.tick_params(labelsize=12)
#plt.savefig('LMR_utrack.png')
#plt.show()
plt.close()

################################
###Plot recycling WAM2-Layers###
################################
lats=np.arange(79.5,-80,-1.5)
lons=np.arange(-180,180,1.5)
cm=mpl.cm.get_cmap('YlGnBu')
cols=[]
for i in np.arange(0,1,1.0/len(ticks)):
    cols.append(cm(i))
cols.append(cm(0.95))

fig = plt.figure(figsize=(10,6))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines(resolution='50m')
cs = ax.contourf(lons,lats,plot_rec_link,ticks,colors=cols,transform=ccrs.PlateCarree(),extend='max')
cax,kw = mpl.colorbar.make_axes(ax,location='right',pad=0.05,shrink=0.5)
out=fig.colorbar(cs,cax=cax,extend='max',**kw,drawedges='none')
out.set_label('Recycling WAM2-layers [-]',size=14)
out.ax.tick_params(labelsize=12)
#plt.savefig('LMR_link.png')
#plt.show()
plt.close()
