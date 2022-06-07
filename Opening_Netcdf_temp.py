# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 14:38:50 2022

@author: Saiful Haque Rahat
"""

#### Step-1 Loading Libraries ####

import netCDF4 as nc
import numpy as np
import datetime as dt

### In order to load 'basemap' library you need to create an environment like the following in your machine 

import os
os.environ['PROJ_LIB'] = r'C:\Users\Research Lab\anaconda3\Lib\site-packages\mpl_toolkits\basemap' ## please change the directory here
                                                                                                ## by going to your users folder
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

#### Step-2 Opening Files and Identifying Variables ####

### The sample file is a netcdf file from a CMIP6 projection model named 'CESM2-WACCM' for ssp245 conditions
### The file contains daily temperature information from year 2095 to 2100 at different pressure

sample_file = r'F:\Netcdf_Python\Input_file\ta_day_CESM2-WACCM_ssp245_r1i1p1f1_gn_20950101-21010101.nc'  ## please change the directory here
netcdf_data = nc.Dataset(sample_file)
dir(netcdf_data)
netcdf_data.variables
print(netcdf_data)
netcdf_data.dimensions.keys()  ## This command shows that what variables are included in the file
                                # In this specific file we have temperature, time, latitude, longitude and air pressure
                                    # Here ta means tempearture, time means date, lon means longitude
                                        #lat means latitude and plev means air pressure at specific height

pres_values=netcdf_data["plev"] 

pres_values[3] ## shows air pressure in 500hpa

temp_values = netcdf_data["ta"][:,3,:,:]-273 ## we are extracting tempearture information for 500hpa 
                                                # The unit is in K which we are converting in degree celcius (-273)
time_indices = netcdf_data["time"][:]
lat_indices = netcdf_data["lat"][:]
lon_indices = netcdf_data["lon"][:]

start_date_str = netcdf_data.variables['time'].units.split(maxsplit=2)[-1]
start_date = dt.datetime.fromisoformat(start_date_str)

date_indices = [start_date + dt.timedelta(days=days) for days in time_indices]
filtered_time_inc = list(filter(lambda t:t.year == 2095, date_indices)) ## We are extracting daily temperature
                                                                        # For year 2095 only

lon, lat = np.meshgrid(lon_indices, lat_indices)

max_temp = np.max(temp_values[:5,:,:]) ## defining levels for map scale bar
min_temp = np.min(temp_values[:5,:,:])

#### Step-3 Creating Images in loop from NetCDF #### 

for i, date in enumerate(filtered_time_inc):
    fig, ax = plt.subplots(constrained_layout=True)
    mp = Basemap(projection="merc",
                 llcrnrlon=-1,   ## lower longitude
                 llcrnrlat=-70,    ## lower latitude
                 urcrnrlon=350,   ## uppper longitude
                 urcrnrlat=70,   ## uppper latitude
                 resolution="c",
                 ax=ax)
    x, y = mp(lon, lat)
    mp.drawcoastlines()
    mp.drawcountries()
    mp.drawstates()
    c_scheme = mp.pcolor(x, y, np.squeeze(temp_values[i, :, :]),
                         cmap="jet", vmin=min_temp, vmax=max_temp)
    date_str = date.strftime("%Y-%m-%d")
    cbar = mp.colorbar(c_scheme, location="bottom", size="2%", ax=ax,label='Temperature')
    plt.title(f"Global Daily Temperature(℃) at 500hpa ({date_str})")
    plt.savefig(f"F:/Netcdf_Python/Images/plt_{i}.png",dpi=200)    ## please change the directory here
    plt.clf()
    print(f"{i}", end=".")
    

#### Step-4 Creating GIF from the saved images ####

import PIL

image_frames = [] ## creating a empty list to be appended later on
days = np.arange(1,len(filtered_time_inc))  ## this  will create a gif for 365 days

for k in days:
    new_fram = PIL.Image.open(r'F:\Netcdf_Python\Images\plt_'+ str(k) + '.png') ## please change the directory here
    image_frames.append(new_fram)

image_frames[0].save(r'F:\Netcdf_Python\GIF\Temp_timelapse.gif',format='GIF',
                    append_images = image_frames[1: ],
                    save_all = True, duration=10, 
                    loop = 0)

PIL.Image.open(r'F:\Netcdf_Python\Images\plt_'+ str(k) + '.png')


#### End ####



