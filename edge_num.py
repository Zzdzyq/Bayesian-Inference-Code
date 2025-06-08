from graph_tool.all import *
import os
import numpy as np
import matplotlib.pyplot as plt

dir = "/home/zzdzyqzzd/saved_pcp"
plt.rcParams.update({'font.size': 15})

# function for getting files within a given directory
def get_nc4_files(directory):
    """Get a sorted list of files in the specified directory."""
    files = [fi for fi in os.listdir(directory)]
    files.sort()
    return files

names = get_nc4_files(dir)
col = ["r", "b", "y", "g"]
lege = ["10 years", "1 month", "1 year", "5 years"]
# read in all the data files
for i in range(4):
    file_path = os.path.join(dir, names[i])
    ext = np.loadtxt(file_path, delimiter=",")

    # create the model we are going to learn with
    state = IsingGlauberBlockState(ext, directed=False, self_loops=False)
    delta = np.inf
    edges = np.array([0])
    count = 0

    # learn the model with given iterations and tolerance
    while count < 10:
        delta, *_ = state.mcmc_sweep(beta=np.inf, niter=10)
        count += 1
        edges = np.append(edges, state.get_graph().num_edges())
    
    plt.plot(np.arange(11), edges, color = col[i], label = lege[i])

plt.legend()
plt.xlabel("Learning Cycles")
plt.ylabel("Number of Edges")
plt.savefig("/home/zzdzyqzzd/inferred_graph/edge_sample.png")
plt.close()