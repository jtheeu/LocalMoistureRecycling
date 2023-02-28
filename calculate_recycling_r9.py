#########################################################################
# Date: 28-02-2023 Written by: J. Theeuwen                              #
#########################################################################
# This script is used to calculate the Local moisutre recycling ratio   #
# at a spatial resolution of 0.5 degrees.This is the fraction of        #
# evaporated moisture that rains out within its source grid cell + its  #
# eight surrounding grid cells.                                         #
# Theeuwen, J., Staal, A., Tuinenburg, O., Hamelers, B., and Dekker, S. #
# Local moisture recycling across the globe, EGUsphere [preprint],      #
# https://doi.org/10.5194/egusphere-2022-612, 2022.                     #
#########################################################################
# Input: atmospehric moisutre connections with a resolution of 0.5      #
# degrees from Tuinenburg et al. (2020)                                 #
#########################################################################
#########################################################################

from numpy import *
import numpy as np
from netCDF4 import Dataset
import time
import sys

lons=arange(0,360,0.5)
lats=arange(90,-90,-0.5)

for month_i in np.arange(12):
    month = month_i+1
    print(month)
#Open files
    recyclingfile=Dataset('utrack_climatology_0.5_'+str(month).zfill(2)+'.nc')

# output arrays
    doffset=20
    recycling = np.zeros((360,720))
    for offset in arange(0,720,doffset):
        print(offset)
        rec = recyclingfile.variables['moisture_flow'][:,offset:offset+doffset,:,:]
        for i in range(360):
            for j in range(doffset):
                fp=exp(rec[i,j,:,:]*-0.1)
                fp[fp==1]=0
                fp=fp/nansum(fp)#normaliseren
                #fp = lsm*fp
                j_o = j+offset
                if i == 0:
                    if j_o == 0:
                        rec_i = (fp[i,j+offset+1]+fp[i+1,j+offset+1]+fp[i,j+offset]+fp[i+1,j+offset])/nansum(fp)
                    elif j_o ==719:
                        rec_i = (fp[i,j+offset]+fp[i+1,j+offset]+fp[i,j+offset-1]+fp[i+1,j+offset-1])/nansum(fp)
                    else:
                        rec_i = (fp[i,j+offset+1]+fp[i+1,j+offset+1]+fp[i,j+offset]+fp[i+1,j+offset]+fp[i,j+offset-1]+fp[i+1,j+offset-1])/nansum(fp)
                elif i == 359:
                    if j_o == 0:
                        rec_i = (fp[i-1,j+offset+1]+fp[i,j+offset+1]+fp[i-1,j+offset]+fp[i,j+offset])/nansum(fp)
                    elif j_o == 719:
                        rec_i = (fp[i-1,j+offset]+fp[i,j+offset]+fp[i-1,j+offset-1]+fp[i,j+offset-1])/nansum(fp)
                    else:
                        rec_i = (fp[i-1,j+offset+1]+fp[i,j+offset+1]+fp[i-1,j+offset]+fp[i,j+offset]+fp[i-1,j+offset-1]+fp[i,j+offset-1])/nansum(fp)
                elif 0 < i < 359:
                    if j_o == 0:
                        rec_i = (fp[i-1,j+offset+1]+fp[i,j+offset+1]+fp[i+1,j+offset+1]+fp[i-1,j+offset]+fp[i,j+offset]+fp[i+1,j+offset])/nansum(fp)
                    elif j_o == 719:
                        rec_i = (fp[i-1,j+offset]+fp[i,j+offset]+fp[i+1,j+offset]+fp[i-1,j+offset-1]+fp[i,j+offset-1]+fp[i+1,j+offset-1])/nansum(fp)
                    else:
                        rec_i = (fp[i-1,j+offset+1]+fp[i,j+offset+1]+fp[i+1,j+offset+1]+fp[i-1,j+offset]+fp[i,j+offset]+fp[i+1,j+offset]+fp[i-1,j+offset-1]+fp[i,j+offset-1]+fp[i+1,j+offset-1])/nansum(fp)
                else:
                    rec_i = (fp[i-1,j+offset+1]+fp[i,j+offset+1]+fp[i+1,j+offset+1]+fp[i-1,j+offset]+fp[i,j+offset]+fp[i+1,j+offset]+fp[i-1,j+offset-1]+fp[i,j+offset-1]+fp[i+1,j+offset-1])/nansum(fp)
                recycling[i,j+offset] = rec_i

        del rec

    outf=Dataset('moisture_recycling_r9_'+str(month).zfill(2)+'.nc','w')
    lats=arange(90,-90,-0.5)
    lons=arange(0,360,0.5)
    lon=outf.createDimension('lon',len(lons))
    lat=outf.createDimension('lat',len(lats))
    unc=outf.createVariable('recycling',float64,('lat','lon'))
    unc[:,:]=recycling
    outf.close()
    del recyclingfile
