from graph_tool.all import *
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 15})

# load the graph and block we saved early to recover the graphview
g = load_graph("/home/zzdzyqzzd/inferred_graph/inferred_100.gt.gz")
blocks = np.load("/home/zzdzyqzzd/inferred_graph/inferred_state_100.npy")
bstate = BlockState(g, b=blocks)
u = GraphView(g)

# plot the number of edges according to the learning cycles
num_edges = [0]
for i in range(10, 101, 10):
    weights = np.loadtxt(f"/home/zzdzyqzzd/inferred_graph/weights_{i}.txt", delimiter=",")
    weights = weights[weights != 0]
    num_edges.append(len(weights))
plt.plot(np.arange(0, 101, 10), num_edges, "-")
plt.xlabel("Learning Cycles")
plt.ylabel("Number of Edges")
plt.tight_layout()
plt.savefig("/home/zzdzyqzzd/inferred_graph/edge_learn.png")
plt.close()

# create graph for degree distributions
print("printing degree distribution")
degree = [u.degree_property_map("total")[v] for v in u.vertices()]
values, counts = np.unique(degree, return_counts=True)
value_range = np.arange(max(values)+1)
full_counts = np.zeros_like(value_range)
print(value_range, values)
full_counts[np.isin(value_range, values)] = counts
plt.plot(value_range, full_counts, ".", lw="1")
plt.grid(axis='y', linestyle='--')
plt.xlabel("Node Degree")
plt.ylabel("Counts")
plt.tight_layout()
plt.savefig("/home/zzdzyqzzd/inferred_graph/degree_dist.png")
plt.close()

# the in-build structured graph drawing method
pos = sfdp_layout(u, bstate.get_blocks())
graph_draw(u, pos, edge_color=weights,
    ecmap=matplotlib.cm.coolwarm_r, output=f"/home/zzdzyqzzd/inferred_graph/infer_EA_80.png")

# generate the block relations graph
print("generating blocks")
b = contiguous_map(bstate.get_blocks())
bstate = bstate.copy(b=b)
e = bstate.get_matrix()
B = bstate.get_nonempty_B()
fig, ax = plt.subplots()
plt.matshow(e.todense()[:B, :B])
print(e.todense())
plt.ylabel("Block Numbers")
plt.savefig("/home/zzdzyqzzd/inferred_graph/block_relas.png")
plt.close()

def distance(origin, destination):
    # algorithm to compute distance based on latitude and longitude
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

# the ranges of our selected region
latrange = np.arange(25, 55, 2)
lonrange = np.arange(75, 125, 2)
lo = lonrange.shape[0]
lengths = []

# compute and plot the lengths of the edges
for edge in u.get_edges():
    ori = (latrange[edge[0]//lo], lonrange[edge[0]%lo])
    des = (latrange[edge[1]//lo], lonrange[edge[1]%lo])
    lengths.append(round(distance(ori, des)))
plt.hist(lengths, bins=100, density=True)
plt.yscale("log")
plt.ylabel("Density")
plt.xlabel("Distance(km)")
plt.tight_layout()
plt.savefig("/home/zzdzyqzzd/inferred_graph/dist_distr.png")
plt.close()