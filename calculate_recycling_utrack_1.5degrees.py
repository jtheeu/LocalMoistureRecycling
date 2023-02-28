#########################################################################
# Date: 28-02-2023 Written by: J. Theeuwen                              #
#########################################################################
# This script is used to calculate the moisutre recycling within one    #
# grid cell of 1.5 degrees.                                             #
# Theeuwen, J., Staal, A., Tuinenburg, O., Hamelers, B., and Dekker, S. #
# Local moisture recycling across the globe, EGUsphere [preprint],      #
# https://doi.org/10.5194/egusphere-2022-612, 2022.                     #
#########################################################################
# Input: atmospehric moisutre connections with a resolution of 0.5      #
# degrees from Tuinenburg et al. (2020)                                 #
#########################################################################
#########################################################################
import numpy as np
from netCDF4 import Dataset
import time
import sys

start_time = time.time()
print(start_time)

evap_f = Dataset('evap_precip_monthly_average.nc')#monthly averaged total evaporation and total precipitation from ERA5 for years 2008-2017

for month_i in np.arange(12):
    month = month_i + 1
    recyclingfile=Dataset('utrack_climatology_0.5_'+str(month).zfill(2)+'.nc')#atmospheric moisutre connections from Tuinenburg et al (2020)
    E = evap_f.variables['evap'][month_i,:,:]

    local_recycling_frac = np.zeros((120,240))
    for k in np.arange(120):
        #start_idx_y = (k-1)*3+1
        start_idx_y = k*3
        for l in np.arange(240):
            #start_idx_x = (l-1)*3+1
            start_idx_x = l*3

            counter = 0
            flows_15_ij = np.zeros(9)
            for i in np.arange(3):
                for j in np.arange(3):
                    idx_i = start_idx_y + i
                    idx_j = start_idx_x + j
                    fp = recyclingfile.variables['moisture_flow'][idx_i,idx_j,:,:]
                    fp=np.exp(fp*-0.1)
                    fp[fp==1]=0
                    fp=fp/np.nansum(fp)#normaliseren
                    flows_mm = fp*E[idx_i,idx_j] #Tot hier gaat het goed
                    #print(start_idx_y, start_idx_x)
                    flows_temp = flows_mm[start_idx_y:start_idx_y+2,start_idx_x:start_idx_x+2]
                    flows_sum = np.sum(flows_temp)
                    flows_15_ij[counter] = flows_sum
                    # print(flows_15_ij)
                    counter = counter+1
            # print(flows_15_ij)
            local_recycling_mm = np.sum(flows_15_ij)
            # print('recycling in mm: ')
            # print(local_recycling_mm)
            verdamping = E[start_idx_y:start_idx_y+2,start_idx_x:start_idx_x+2]
            # print('verdamping')
            # print(verdamping)
            verdamping_sum = np.sum(verdamping)
            # print('Som verdamping:')
            # print(verdamping_sum)
            local_recycling_frac[k,l] = local_recycling_mm/verdamping_sum
            int_time = time.time()
            print_time = int_time - start_time
            # print('local recycling: fraction')
            # print(local_recycling_frac[k,l])
            print('time:')
            print(print_time)

    outf=Dataset('moisture_recycling_in_grid_1.5degrees_'+str(month).zfill(2)+'.nc','w')
    lats=arange(90,-90,-1.5)
    lons=arange(0,360,1.5)
    lon=outf.createDimension('lon',len(lons))
    lat=outf.createDimension('lat',len(lats))
    unc=outf.createVariable('recycling',float64,('lat','lon'))
    unc[:,:]=local_recycling_frac
    outf.close()
