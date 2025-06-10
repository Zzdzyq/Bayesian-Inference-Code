from graph_tool.all import *
import os
import numpy as np
import matplotlib.pyplot as plt
import time

# directory for data files
dir = "/home/zzdzyqzzd/saved_pcp"

plt.rcParams.update({'font.size': 15})

# function for getting files within a given directory
def get_nc4_files(directory):
    """Get a sorted list of files in the specified directory."""
    files = [fi for fi in os.listdir(directory)]
    files.sort()
    return files

# read in all the data files
for filename in get_nc4_files(dir):
    file_path = os.path.join(dir, filename)
    ext = np.loadtxt(file_path, delimiter=",")

    # create the model we are going to learn with
    state = IsingGlauberBlockState(ext, directed=False, self_loops=False)
    times = time.time()
    delta = np.inf
    tol = 10e-6
    res = np.array([])
    count = 0

    # learn the model with given iterations and tolerance
    while np.abs(delta) > tol and count < 100:
        delta, *_ = state.mcmc_sweep(beta=np.inf, niter=10)
        count += 1
        res = np.append(res, delta)

        if not count % 10:
            # print and plot the results every 10 cycles
            print(res)

            plt.plot(state.get_xvals(), state.get_xhist(), ".", lw = 2)
            plt.grid(axis='y', linestyle='--')
            plt.ylabel("Counts")
            plt.xlabel("Edge Weight")
            plt.tight_layout()
            plt.savefig(f"/home/zzdzyqzzd/inferred_graph/edge_weight_counts_{count}.png")
            plt.close()
            
            bstate = state.get_block_state().levels[0]
            u = state.get_graph()

            print(f"there are {u.num_edges()} edges")
            print(f"there are {u.num_vertices()} vertices")
            u.base.save(f"/home/zzdzyqzzd/learned_models/inferred_{count}.gt.gz")
            np.save(f"/home/zzdzyqzzd/learned_models/inferred_state_{count}.npy", bstate.get_blocks().a)
            np.savetxt(f"/home/zzdzyqzzd/learned_models/weights_{count}.txt", state.get_x().get_array(), delimiter=",")

    # generate the residual plot
    np.savetxt(f"/home/zzdzyqzzd/inferred_graph/res.txt", res, delimiter=",")
    print("plotting residuals")
    plt.plot(np.arange(count)+1, np.abs(res), "b")
    plt.plot(np.arange(count)+1, np.abs([np.mean(res[80:])]*100), "r--")
    plt.ylabel("Residuals")
    plt.xlabel("Learning Cycles")
    plt.yscale("symlog", linthresh=1)
    plt.savefig(f"/home/zzdzyqzzd/inferred_graph/residuals.png")
    plt.close()

    # get the time used to run the process
    timee = time.time()
    print(f'learn time: {timee - times}')