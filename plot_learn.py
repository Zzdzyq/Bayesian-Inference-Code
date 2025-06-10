import numpy as np
import matplotlib.pyplot as plt
from graph_tool.all import *
import cartopy.crs as ccrs
from cartopy.feature import LAND, OCEAN

plt.rcParams.update({'font.size': 15})

# load the graph and the weights saved earlier
g = load_graph("/home/zzdzyqzzd/inferred_graph/inferred_100.gt.gz")
u = GraphView(g)
weights = np.loadtxt("/home/zzdzyqzzd/inferred_graph/weights_100.txt", delimiter=",")
weights = weights[weights != 0]
uni_weights = np.unique(weights)
degree = [u.degree_property_map("total")[v] for v in u.vertices()]

# plot the learned model on a world map
print("generating map")
adj_mat = np.zeros((u.num_vertices(), u.num_vertices()), dtype=np.double)
for i, edge in enumerate(u.edges()):
    src = int(edge.source())
    tgt = int(edge.target())
    adj_mat[src, tgt] = weights[i]
    adj_mat[tgt, src] = weights[i]

# scales of the map
latrange = np.arange(25, 55, 2)
lonrange = np.arange(75, 125, 2)
lo = lonrange.shape[0]

# generate the figure
fig = plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.add_feature(LAND, edgecolor='black')
ax.add_feature(OCEAN)
ax.set_extent([70, 130, 20, 60], crs=ccrs.PlateCarree())

# add in grid lines and labels
gl = ax.gridlines(
    draw_labels=True,
    linewidth=1, 
    color='gray', 
    alpha=0.3,
    linestyle='--'
)
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 10}
gl.ylabel_style = {'size': 10}

# add in the points
for i, lat in enumerate(latrange):
    for j, lon in enumerate(lonrange):
        ax.plot(lon, lat, marker='o', color='red', markersize=degree[i*lo+j]//2, transform=ccrs.PlateCarree())

# add in the edges
for i, row in enumerate(adj_mat):
    for j, connected in enumerate(row):
        if connected:
            # Get coordinates of connected nodes
            lat1, lon1 = latrange[i//lo], lonrange[i%lo]
            lat2, lon2 = latrange[j//lo], lonrange[j%lo]
            if adj_mat[i, j] == uni_weights[0]:
                ax.plot(
                    [lon1, lon2], [lat1, lat2],
                    color='blue', linewidth=0.25, transform=ccrs.PlateCarree()
                )
            elif adj_mat[i, j] == uni_weights[1]:
                ax.plot(
                    [lon1, lon2], [lat1, lat2],
                    color='red', linewidth=0.5, transform=ccrs.PlateCarree()
                )
            else:
                ax.plot(
                    [lon1, lon2], [lat1, lat2],
                    color='yellow', linewidth=0.5, transform=ccrs.PlateCarree()
                )
plt.title('Graph Overlay on Satellite Map')
plt.savefig("/home/zzdzyqzzd/inferred_graph/infer_80.png", dpi=300)
plt.close()

# create the map for the cities we chose
sel_loc = [51, 195, 218, 226]
for loc in sel_loc:
    # generate the figure
    fig = plt.figure(figsize=(10, 5))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(LAND, edgecolor='black')
    ax.add_feature(OCEAN)
    ax.set_extent([70, 130, 20, 60], crs=ccrs.PlateCarree())

    # add in grid lines and labels
    gl = ax.gridlines(
        draw_labels=True,
        linewidth=1, 
        color='gray', 
        alpha=0.3,
        linestyle='--'
    )
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 10}
    gl.ylabel_style = {'size': 10}

    # add in the points
    for i, lat in enumerate(latrange):
        for j, lon in enumerate(lonrange):
            ax.plot(lon, lat, marker='o', color='red', markersize=degree[i*lo+j]//2, transform=ccrs.PlateCarree())

    # add in the edges
    for j, connected in enumerate(adj_mat[loc]):
        if connected:
            # Get coordinates of connected nodes
            lat1, lon1 = latrange[loc//lo], lonrange[loc%lo]
            lat2, lon2 = latrange[j//lo], lonrange[j%lo]
            if adj_mat[loc, j] == uni_weights[0]:
                ax.plot(
                    [lon1, lon2], [lat1, lat2],
                    color='blue', linewidth=1, transform=ccrs.PlateCarree()
                )
            elif adj_mat[loc, j] == uni_weights[1]:
                ax.plot(
                    [lon1, lon2], [lat1, lat2],
                    color='red', linewidth=1, transform=ccrs.PlateCarree()
                )
            else:
                ax.plot(
                    [lon1, lon2], [lat1, lat2],
                    color='yellow', linewidth=1, transform=ccrs.PlateCarree()
                )
    plt.savefig(f"/home/zzdzyqzzd/inferred_graph/infer_loc_{loc}.png", dpi=300)
    plt.close()