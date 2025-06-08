from graph_tool.all import *
import os # package for getting filenames from directory
import netCDF4 as nc
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt

dir = "/home/zzdzyqzzd/data_files"

def get_nc4_files(directory):
    """Get a sorted list of HDF5 files in the specified directory."""
    files = [fi for fi in os.listdir(directory)]
    files.sort()  # Sort files in a certain order (e.g., alphabetical)
    return files

la = 300//2
lo = 500//2
n = la * lo

pcp = np.zeros((0, lo, la))

count = 0
for filename in get_nc4_files(dir):
    file_path = os.path.join(dir, filename)
    f = nc.Dataset(file_path) # read files as 'r', 'w' changes the file itself
    pcp = np.concatenate((pcp, f.variables['precipitation'][:][:, 2250//2:2750//2, 850//2:1150//2]), axis=0)
    count += f.variables['precipitation'][:].shape[0]
    f.close()
print("file recorded")

sel_loc = [51, 195, 218, 226]
step = 10

def ec_wd(ts, perc):
    th = st.scoreatpercentile(ts[ts > 1/6.25], perc)
    ext = [1 if t > th else -1 for t in ts]
    return th, ext

perc = 80
ths = []
num_ext = []
yr_avg = []
for l in sel_loc:
    th, ext = ec_wd(pcp[:, l%(lo//step), l//(lo//step)], perc)
    ths.append(th)
    num_ext.append(np.unique(ext, return_counts=True)[1][1])
    cur_date = 0
    avg = []
    for d_yr in [365, 366, 365, 365, 365, 366, 365, 365, 365, 305]:
        avg.append(np.mean(pcp[cur_date:cur_date+d_yr, l%(lo//step), l//(lo//step)]))
        cur_date += d_yr
    yr_avg.append(avg)
print(ths)
print(num_ext)
yrs = np.arange(2015, 2025, 1)
col = ["r", "b", "y", "g"]
lege = ["Delhi", "Beijing", "Hohhot", "Almaty"]
for i in range(4):
    plt.plot(yrs, yr_avg[i], color = col[i], label = lege[i])
plt.xlabel("Year", fontsize=15)
plt.ylabel("Average Precipitation(mm/day)", fontsize=15)
plt.legend()
plt.tight_layout()
plt.savefig("/home/zzdzyqzzd/inferred_graph/city_avg.png")
plt.close()