from graph_tool.all import *
import os # package for getting filenames from directory
import netCDF4 as nc
import numpy as np

# directory for data files
dir = "/home/zzdzyqzzd/data_files"

def get_nc4_files(directory):
    """Get a sorted list of HDF5 files in the specified directory."""
    files = [fi for fi in os.listdir(directory)]
    files.sort()
    return files

# initial file to get the latitude and longitude without needing to
# put them into the loop
file_path0 = os.path.join(dir, get_nc4_files(dir)[0])
f = nc.Dataset(file_path0)
lat = f.variables['lat'][300:1500:2]
lon = f.variables['lon'][300:3300:2]
la = lat.shape[0]
lo = lon.shape[0]
f.close()

# initialize arrays based the number of days in the month
time = np.zeros(30)
pcp = np.zeros((30, lo, la))

count = 0
for filename in get_nc4_files(dir):
    # read in all files in the directory together into arrays
    file_path = os.path.join(dir, filename)
    f = nc.Dataset(file_path)
    time[count] = f.variables['time'][:].item()
    pcp_tmp = f.variables['precipitation'][:]*24
    pcp[count] = pcp_tmp[:, 300:3300:2, 300:1500:2]
    f.close()
    count += 1
    print(count)
print(np.unique(pcp))

# create a new file storing new dataset containing the information read above
new_file = '/home/zzdzyqzzd/data_files/merged_2016_11.nc4'
new_dataset = nc.Dataset(new_file, 'w', format='NETCDF4')

new_dataset.createDimension('time', 30)
new_dataset.createDimension('lat', la)
new_dataset.createDimension('lon', lo)

time_var = new_dataset.createVariable('time', 'i4', ('time',))
lat_var = new_dataset.createVariable('lat', 'f4', ('lat',))
lon_var = new_dataset.createVariable('lon', 'f4', ('lon',))
pcp_var = new_dataset.createVariable('precipitation', 'f4', ('time', 'lon', 'lat'))

time_var[:] = time
lat_var[:] = lat
lon_var[:] = lon
pcp_var[:] = pcp

new_dataset.close()