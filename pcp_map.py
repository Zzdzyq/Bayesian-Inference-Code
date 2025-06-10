import os # package for getting filenames from directory
import netCDF4 as nc
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# directory for data files
dir = "/home/zzdzyqzzd/data_files"

def get_nc4_files(directory):
    """Get a sorted list of HDF5 files in the specified directory."""
    files = [fi for fi in os.listdir(directory)]
    files.sort()
    return files

# the sizes of the resaved data(before classification)
la = 600
lo = 1500
n = la * lo

# load the precipitation at the locations
pcp = np.zeros((0, lo, la))
count = 0
for filename in get_nc4_files(dir):
    file_path = os.path.join(dir, filename)
    f = nc.Dataset(file_path)
    pcp = np.concatenate((pcp, f.variables['precipitation'][:]), axis=0)
    count += f.variables['precipitation'][:].shape[0]
    f.close()
print("file recorded")

# no need for increasing the step as we are just going to plot the data
step = 1

def ec_wd(ts, perc):
    # function accommodated to reture only the threshold
    th = st.scoreatpercentile(ts[ts > 1/6.25], perc)
    return th

# the percentile may be changed for the plot we wish to see
for perc in [80]:
    th = np.zeros((lo, la))
    for l in range(0, la, step):
        precip = pcp[:, :, l]
        if np.ma.is_masked(precip) is True:
            rain = pcp[:, :, l].filled(0)
        else:
            rain = pcp[:, :, l]
        for k in range(0, lo, step):
            th[k, l] = ec_wd(rain[:,k], perc)

# plot the figure of the percentile values on the map
fig = plt.figure()
ax_map = fig.add_subplot(projection=ccrs.PlateCarree())
ax_map.set_extent([-150, 150, -60, 60], crs=ccrs.PlateCarree())
ax_map.coastlines(linewidth=0.5)

# add in the grid of the region we chose earlier
lon_grid, lat_grid = np.meshgrid(np.linspace(-150, 150, lo), np.linspace(-60, 60, la))
mesh = ax_map.pcolormesh(lon_grid, lat_grid, th.T, cmap="viridis_r")
cbar = plt.colorbar(mesh, ax=ax_map, orientation='horizontal', pad=0.05, aspect=50)
cbar.set_label('80th Percentile Rainfall (mm·day$^{-1}$)', fontsize=12)

# add in the grid lines and labels
gl = ax_map.gridlines(
    draw_labels=True,
    linewidth=1, 
    color='gray', 
    alpha=0.5,
    linestyle='--'
)
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 10}
gl.ylabel_style = {'size': 10}

plt.tight_layout()
plt.savefig("/home/zzdzyqzzd/inferred_graph/pcp_map.png")
plt.close()