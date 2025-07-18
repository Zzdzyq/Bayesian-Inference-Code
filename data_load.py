from graph_tool.all import *
import os # package for getting filenames from directory
import netCDF4 as nc
import numpy as np
import scipy.stats as st

# directory for data files
dir = "/home/zzdzyqzzd/data_files"

def get_nc4_files(directory):
    """Get a sorted list of HDF5 files in the specified directory."""
    files = [fi for fi in os.listdir(directory)]
    files.sort()
    return files

# Selected range for longitude and latitude
la = 300//2
lo = 500//2
n = la * lo

pcp = np.zeros((0, lo, la))
count = 0
for filename in get_nc4_files(dir):
    file_path = os.path.join(dir, filename)
    f = nc.Dataset(file_path) # read files as 'r', 'w' changes the file itself
    # choose the subset of precipitation at given locations
    pcp = np.concatenate((pcp, f.variables['precipitation'][:][:, 2250//2:2750//2, 850//2:1150//2]), axis=0)
    count += f.variables['precipitation'][:].shape[0]
    f.close()
print("file recorded")

# possible to loop over step sizes to get different coarsity of grid
for step in [10]:
    def ec_wd(ts, perc):
        # function for classification of given input array
        th = st.scoreatpercentile(ts[ts > 1/6.25], perc)
        ext = [1 if t > th else -1 for t in ts]
        return ext

    for perc in [80]: # possible to choose different percentiles for classification
        ext = np.zeros((n//step**2, count), dtype = 'int')
        for l in range(0, la, step):
            precip = pcp[:, :, l]
            if np.ma.is_masked(precip) is True:
                rain = pcp[:, :, l].filled(0)
            else:
                rain = pcp[:, :, l]
            for k in range(0, lo, step):
                # store the classified extreme days into respective locations in the array ext
                ext[(l//step) * (lo//step) + k//step, :] = ec_wd(rain[:,k], perc)
                print(f"ext being updated {(l//step) * (lo//step) + k//step} time")
        print(np.unique(np.sum(ext, 1), return_counts=True))
        print(ext.shape)

        # save the classified data as txt files for later use
        np.savetxt(f"/home/zzdzyqzzd/saved_pcp/pcp_75-125E_25-55N_{step*2}_{perc}_1yr.txt", ext, delimiter=",")